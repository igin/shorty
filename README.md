![Shorty Overview](./overview.png)

# Shorty - Automatically fill the Swiss short time form from a time tracking sheet

The Swiss authorities want companies on short-time to submit a PDF form with details
on the amount of short-time accumulated in the company. In the form you need to specify
the hours worked on short-time per employee per day of the month. This quickly becomes
a very time consuming and error prone manual task. 

This tool tries to solve this issue by automatically filling the PDF form from the export
of a time tracking tool.

# Time Report File

The time report file is expected to be in CSV format and contain at least the following columns:

* Date - Isoformat date
* Hours - Number of hours spent in short time on this day (float)
* First Name
* Last Name

Here is an example file:

```
Date,Hours,First Name,Last Name
2021-08-02,3.5,Max,Mustermann
2021-08-03,1.2,Max,Mustermann
2021-08-06,3,Max,Mustermann
2021-08-09,7,Albert,Einstein
2021-08-10,9,Gitte,Gunter
```

Note: Multiple entries for the same day and same person will be accummulated. 

# Usage using docker

Assuming you have the report file in `./input-data/report.csv` and want the output to be written to `./output-data/`
use the following command to generate the pdfs. Pass the year and month you want to the pdfs to be generated for.

```
docker run -it --rm \
  -v$(pwd)/input-data:/input-data \
  -v$(pwd)/output-data:/output-data \
  igin/shorty \
  --report-file /input-data/report.csv \
  --output-dir /output-data \
  --year 2021 \
  --month 8
```

# Support

If you find this tool useful why not [!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/XgyU1H3)




