#!/bin/python3
#templated.py - take the data from prep an put the data into the templated .xlsx file

import prep
import pandas as pd

def tmeplated():
    #Get the data
    df = prep.prep()
# Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter("pandas_table.xlsx", engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object. Turn off the default
# header and index and skip one row to allow us to insert a user defined
# header.
    df.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False, index=False)

# Get the xlsxwriter workbook and worksheet objects.
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']

# Get the dimensions of the dataframe.
    (max_row, max_col) = df.shape

# Create a list of column headers, to use in add_table().
    column_settings = []
    for header in df.columns:
        column_settings.append({'header': header})

# Add the table.
    worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})

# Make the columns wider for clarity.
    worksheet.set_column(0, max_col - 1, 12)

# Close the Pandas Excel writer and output the Excel file.
    writer.close()

if __name__ ==  '__main__':
    tmeplated()
