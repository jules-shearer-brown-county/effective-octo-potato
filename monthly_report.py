from dash import Dash, dash_table, dcc, html, Input, Output, callback
import pandas as pd

import proccess_apps_team
import figures
import utility

app = Dash()

df = pd.concat([proccess_apps_team.proccess_apps_team(), proccess_apps_team.proccess_apps_team(utility.get_remediations()), proccess_apps_team.proccess_apps_team("/mnt/c/Users/jules.shearer/Downloads/brown_county_gov_vuln_rememdiation_365.xlsx")])
df.drop_duplicates(subset='hvm_id', keep='last', inplace=True)
#Filter out the rows where there is not application assigned
df=df[df['Application'].notna()]

columns_to_show=[
    'last_seen',
    #'first_seen',
    #'ack_dt',
    #'ack_by',
    #'closed_dt',
    #'closed_by',
    #''details.type',
    #''details.results',
    #'vuln_id.vuln_id',
    'vuln_id.name',
    'vuln_id.severity',
    #'vuln_id.unique_id',
    #'vuln_id.first_seen',
    #'vuln_id.last_seen',
    'vuln_id.cve',
    #'vuln_id.exploit',
    #'host_id.host_id',
    'host_id.hostname',
    #'host_id.ip_address',
    #'host_id.risk_score',
    #'host_id.criticality',
    #'ttr',
    'vuln_id.link',
    'host_id.link',
    'remediation_category.link',
    'Application'
]

app.layout = html.Div(
    className="row",
    children=[
        html.Div(
            html.H1("Uncommon X June",className="bg-secondary text-white p-2 mb-4")
        ),
        html.H3("Remedations, Acknowledgements, and Discovery year to date",className="bg-tertiary text-white p-2 mb-4"),
        html.Div(
            id='table-paging-with-graph-container-waterfall',
            className="waterfall columns"
        ),
        html.H3("Current State",className="bg-tertiary text-white p-2 mb-4"),
        html.Div([
            html.H3("Scanning"),
            html.P(
                [html.Img(src='assets/green_checkmarkwebp.webp',
                             style={'display': 'inline',
                                    'maxWidth':'15px'}),
                    "Servers",
                    ]
                   ),
            html.P([html.Img(src='assets/green_checkmarkwebp.webp',
                             style={'display': 'inline',
                                    'maxWidth':'15px'}),
                    "IT Workstations",
                    ]),
            html.P([
                    html.Img(src='assets/red_x.webp',
                             style={'display': 'inline',
                                    'maxWidth':'15px'}),
                "Other Workstations"
            ]),
        ]),
        html.Div(
            id='table-paging-with-graph-container-pie',
            className="five columns"
        ),
        html.H3("Pending Fixes and Acknowledgements",className="bg-tertiary text-white p-2 mb-4"),
        html.Div(
            dash_table.DataTable(
                id='table-paging-with-graph-scheduled',
                data=df[df.hvm_id == 2330].to_dict('records'),
                columns = [{"name": i, "id": i, 'presentation': 'markdown'} if ((i=='host_id.link') | (i=='vuln_id.link')) else ({"name": i, "id": i}) for i in columns_to_show],
                page_current=0,
                sort_action='custom',
                sort_by=[],
                style_table={
                    'height':'fill',
                    'width':'fill',
                },
                style_cell={
                    'overflow':'hidden',
                    'textOverflow':'ellipsis',
                    'maxWidth':0,
                },
            ),
            className="six columns"
        ),
        html.H3("Open",className="bg-tertiary text-white p-2 mb-4"),
        html.Div(
            dash_table.DataTable(
                id='table-paging-with-graph',
                columns = [{"name": i, "id": i, 'presentation': 'markdown'} if ((i=='host_id.link') | (i=='vuln_id.link')) else ({"name": i, "id": i}) for i in columns_to_show],
                page_current=0,
                page_size=10,
                page_action='custom',

                filter_action='custom',
                filter_query='',

                sort_action='custom',
                sort_by=[],
                sort_mode='multi',
                style_table={
                    'height':'fill',
                    'width':'fill',
                },
                style_cell={
                    'overflow':'hidden',
                    'textOverflow':'ellipsis',
                    'maxWidth':0,
                },
            ),

            className="six columns"
        ),
        html.H3("Applied Fixes and Acknowledgements",className="bg-tertiary text-white p-2 mb-4"),
        html.Div(
            dash_table.DataTable(
                id='table-paging-with-graph-fixes',
                data=df[df.remediation_category!='open'].to_dict('records'),
                columns = [{"name": i, "id": i, 'presentation': 'markdown'} if ((i=='host_id.link') | (i=='vuln_id.link')) else ({"name": i, "id": i}) for i in columns_to_show],
                page_current=0,
                sort_action='custom',
                sort_by=[],
                style_table={
                    'height':'fill',
                    'width':'fill',
                },
                style_cell={
                    'overflow':'hidden',
                    'textOverflow':'ellipsis',
                    'maxWidth':0,
                },
            ),

            className="six columns"
        ),
    ]
)

operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]


def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3

def update_data(sort_by, filter):
    filtering_expressions = filter.split(' && ')
    dff = df
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value, na=False)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value, na=False)]

    if len(sort_by):
        dff = dff.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )

    return dff

@callback(
    Output('table-paging-with-graph', "data"),
    Input('table-paging-with-graph', "page_current"),
    Input('table-paging-with-graph', "page_size"),
    Input('table-paging-with-graph', "sort_by"),
    Input('table-paging-with-graph', "filter_query"))

def update_table(page_current, page_size, sort_by, filter):
    dff=update_data(sort_by, filter)
    return dff.iloc[
        page_current*page_size: (page_current + 1)*page_size
    ].to_dict('records')


@callback(
    Output('table-paging-with-graph-container-pie', "children"),
    Input('table-paging-with-graph', "data"),
    Input('table-paging-with-graph', "sort_by"),
    Input('table-paging-with-graph', "filter_query"))

def update_pie_charts_graph(rows, sort_by, filter):
    dff=update_data(sort_by, filter)

    return html.Div(
        [
            dcc.Graph(
                figure=figures.app_and_severity(dff)
            )
        ]
    )

@callback(
    Output('table-paging-with-graph-container-waterfall', "children"),
    Input('table-paging-with-graph', "data"),
    Input('table-paging-with-graph', "sort_by"),
    Input('table-paging-with-graph', "filter_query"))

def update_waterfall_charts_graph(rows, sort_by, filter):
    dff=update_data(sort_by, filter)

    return html.Div(
        [
            dcc.Graph(
                figure=figures.waterfall(dff)
            )
        ]
    )


if __name__ == '__main__':
    app.run(debug=True)
