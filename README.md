effective-octo-potato
=========
From UncommonX download the remediations and vulnerability reports

[Vulnerability Mapping](https://app.uncommonx.com/network-disc/vuln-host)
[Remediations](https://app.uncommonx.com/network-disc/vuln-remediation)

From Sharepoint download the deduplicated set & the application by hostname list 

[Sharepont deduplicated](https://bcwi.sharepoint.com/:x:/s/TS/Team/IQB7kkptHNU_S74RppbJkdHHAQsMbTvuAU7LqNIH_r3tH5g)
[Sharepont names_and_tags](https://bcwi.sharepoint.com/:x:/s/TS/Team/IQCRanPxiK9gS4ToS97vf0C9AaCxtHTEM7UwMIJ0H9ZkaZE)

In a fresh folder start by cloning this repo if you haven't already.

    'git clone https://github.com/jules-shearer-brown-county/effective-octo-potato.git'

I am a fan of virtual environments to keep packages in the right version but you can skip this step if you want to.

    'python -m venv .'

And then Activate

    '.\Scripts\activate'

To install required packages on a fresh computer run 

    'pip install -r requirements.txt'

Then you can run prep.py to generate the output.xlsx file

    './prep.py 

prep.py will look for the 4 needed files and then do some light transformations to make the data pretty 

After that rename output.xlsx and replace deduplicated.xlsx in the sharepoint location and the uncommonX.xlsx report will need to be refreshed before it updates values, if the UncommonX report does not update values you can check that the PQ is pointing at the right source for the deduplicated


[UncommonX](https://bcwi.sharepoint.com/:x:/s/TS/Team/IQD8TPgPM6UlQ7rxA_jMfD9oAWiljqsxPMoygESAuZ_U4OI?e=OqWW94)
