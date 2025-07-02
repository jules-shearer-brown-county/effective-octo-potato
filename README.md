effective-octo-potato
=========

A simple dash app for analyzing the results of vulnerability scans within our environment. 

To install required packages run 

    'pip -r requirements.txt'

and then you can launch the dashboard with 

    'python monthly_report.py'

Requirements from Management

- [ ] Font size for section Headers: 36
- [ ] Font size for report title: 72
- [ ] Font size for sub section title: 72
- [ ] Sections: Waterfall Chart, Current State Open, Application Vulnerabilities Breakdown for May, All Open Vulnerabilities
- [ ] Subsections: 
    - [ ] "Scanning"
    - [ ] "Pie Charts"
    - [ ] "Upcomming Remediations"
    - [ ] "Acknowledged"
    - [ ] "Remediated"
- [ ] Footer containing "Page" of "Total Pages"
- Waterfall Chart
- [ ] Font size for Waterfall Chart title:32
- [ ] Font size for Waterfall Chart legend:28
- [ ] Font size for Waterfall Chart horizontal axis labels:24
- [ ] Font size for Waterfall Chart vertical axis labels:32
- [ ] Font size for Waterfall Chart data point labels:32
- [ ] Column colors: 
    - [ ] Found red
    - [ ] Acknowledged green 
    - [ ] Remediated green 
    - [ ] Total blue 
- Pie Charts
- [ ] Font size for pie Chart title:18
- [ ] Font size for pie Chart section labels:18
- [ ] Capitalize Remediated, Open, Found
- Tables
- [ ] Font size for Tables: 16
- [ ] Columns (ordered): Application, Name, Severity, Host, Link, Last Seen, Category
- [ ] Word wrap on column "Name"
- [ ] Shrink width column "Name" and "Link"
- Layout from top to bottom:
- [ ] Title
- [ ] Section: Waterfall chart 
    - [ ] Subsection: Scanning in upper right hand sie of waterfall chart space laid over top 
- [ ] Section: Current State Open
    - [ ] SubSection: Centered on the page across the width of the page
- [ ] Section: Application Vulnerabilities Breakdown for May 
    - [ ] Table "Remediated"
    - [ ] Table "Acknowledged"
    - [ ] Table "Upcomming Remediations"
    - [ ] Table "All Open Vulnerabilities"

        Suggestions from 6/27/2025
Insert "Page number" of "Total Page Numbers" into footer
Add section headers in a different color
Remove Tim's counts from the waterfall chart and the entire report
Rename "All Open Critical/High Vulnerabilities" to "All Open Application Critical/High Vulnerabilities"
Rename "Pending Vulnerabilities" to "All Open Application Critical/High Vulnerabilities"
Insert page break between "Application Vulnerabilities for May" and the Pie charts above
Compress YTD to just YTD, remove make blue

