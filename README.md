effective-octo-potato
=========
From UncommonX download the remediations and vulnerability reports

[Vulnerability Mapping](https://app.uncommonx.com/network-disc/vuln-host)
[Remediations](https://app.uncommonx.com/network-disc/vuln-remediation)

From Sharepoint download the deduplicated set 

[Sharepont deduplicated](https://bcwi.sharepoint.com/:x:/s/TS/Team/IQB7kkptHNU_S74RppbJkdHHAQsMbTvuAU7LqNIH_r3tH5g)

To install required packages run 

    'pip -r requirements.txt'

Then you can run prep.py

    './prep.py'

prep.py will prompt you for for the remedation, vulnerability, and deuplicated file paths. It will attempt to remove duplicated entries based on the HVM_ID and update deduplicated with the most up to date vulnerability information

After that upload deduplicated.xlsx to the sharepoint location and the uncommonX.xlsx report will need to be refreshed before it updates values
