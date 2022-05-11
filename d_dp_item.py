import pandas as pd

df = pd.read_excel("C:\\Users\\arusahoo\\Desktop\\Model_Input_d_dp_item.xlsx", dtype=str, sheet_name="ConfigSheet")
df1 = pd.read_excel("C:\\Users\\arusahoo\\Desktop\\Model_Input_d_dp_item.xlsx", dtype=str, sheet_name="MappingSheet")
JSON_STRING = ""
for index, row in df.iterrows():
    merge_update = [x.strip() for x in row['merge_update_columns'].split(',')]
    merge_update_str = ''
    for s in merge_update:
        merge_update_str += "'" + s + "',"
    merge_update_str = "[" + merge_update_str[:-1] + "]"
    JSON_STRING += """
{{
        config( schema = '""" + row['schema'].strip() + """',
          tags = ['""" + row['tags'].strip() + """'],
          alias = '""" + row['alias'].strip() + """',
          materialized='""" + row['materialized'].strip() + """',
          unique_key='""" + row['unique_key'].strip() + """',
          merge_update_columns =""" + merge_update_str + """
        )                           
}}
SELECT
    """
DDL = ""
for index, row in df1.iterrows():
    if row['Mapping'] == "CONSTANT":
        DDL += (row['SourceColumn'] + " as " + row['TargetColumn'] + ",\n")
    elif row['Mapping'] == "DIRECT":
        DDL += (row['TargetColumn'] + ",\n")
    elif row['Mapping'] == "DERIVED":
        DDL += (row['SourceColumn'] + " as " + row['TargetColumn'] + ",\n")
DDL = DDL[:-2]
DDL += "\nFROM {{ref:" + row['SourceTable'] + "}}"
FILE_NAME = row['ModelName']
FILE_PATH = "C:\\Users\\arusahoo\Desktop\\"
FULL_NAME = FILE_PATH + FILE_NAME
# print(FULL_NAME)
f = open(FULL_NAME, 'a')
f.write(JSON_STRING)
f.write(DDL)
f.close()
