#  Script to query all the CSV files in a directory that might have different columns and merge into a single CSV file.
#  This does not take into account duplicate rows; they will still be processed.
#  By Brad Edgeworth
#
#  Version 2024-10-24
#     Fixed an issue where not all CSV files were returned
#
#  Version 2024-03-06
#      Fixed a bug with CSV format inserting an unneccessary space ' '
#
#  Version 2026-04-28
#      Fixed a bug where a blank column and a duplciate deviceID is present. 
#
#  Python dependencies:
#     pandas  (i.e. pip install pandas )
print('CSV consolidation tool.   Version: 2026-04-28')
print('---------------------------------------------')


from csv import DictReader
import glob
import re
import time
import pandas as pd
from datetime import datetime
finalcsv_column_names = ['']
mainData = []
regex = '!Consolidate*'
today = datetime.today()
d4 = datetime.now().strftime("%Y-%m-%d---%H-%M-%S")
 
# list all csv files only that do not start with Consolidate
all_csv_files = glob.glob("*.csv")

# Exclude files starting with 'ConsolidatedCSV'
csv_files = [f for f in all_csv_files if not f.startswith("ConsolidatedCSV")]
print('These are the CSV files that are being consolidated:')
print('------------------------------------------------------')
for f in csv_files:
    print(f)
    
currentcsv_column_names = set ()
for file in csv_files:
   df = pd.read_csv(file)
   currentcsv_column_names.update(df.columns)
   #print ('List of column names: ', currentcsv_column_names)
   #print (currentcsv_column_names)

# --------------------------------------------------------------------------------
#  Use for new ConfigurationGroups.   Remark if using the old Device Templates
#primary_headers = ['Device ID','Host Name']

# --------------------------------------------------------------------------------
# Unremark following line and use for old Device Templates
primary_headers = ['csv-deviceId', 'csv-deviceIP', 'csv-host-name']
  
for h in primary_headers:
    currentcsv_column_names.discard(h)
currentcsv_column_names.discard('')
  
finalcsv_column_names = primary_headers + sorted(list(currentcsv_column_names))



for file in csv_files:
  with open(file, 'r', encoding='utf-8') as read_obj:
        csv_dict_reader = DictReader(read_obj)
        for row in csv_dict_reader:
            companyRowData = []
            for headerName in finalcsv_column_names:
                try:
                    companyRowData.append(row[headerName])
                except:
                    companyRowData.append('')
            mainData.append(companyRowData)
        print(" Processed File : " + str(file))
print("------------------------------------------------------")
companyData = pd.DataFrame(mainData, columns=finalcsv_column_names)
newConsolidatedCSVfilename = 'ConsolidatedCSV-'+d4+'.csv'
companyData.to_csv(newConsolidatedCSVfilename, index=False)
print('Consolidated into this file:  ', newConsolidatedCSVfilename)
time.sleep(5)
