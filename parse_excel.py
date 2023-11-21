import pandas as pd
import psycopg2
import openpyxl

db_params = {
    'host': 'localhost',
    'port': '5432',
    'database': 'postgres',
    'user': 'your_username',
    'password': 'your_password'
}

excel_file = 'path_to_your_excel_file.xlsx'
df = pd.read_excel(excel_file)
df = df.iloc[2:]
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()
num_columns = len(df.columns)
data_lists = []
for i in range(10):
    data_lists.append(df.iloc[:, i].tolist())
list_length = len(data_lists[0])
assert all(len(lst) == list_length for lst in data_lists), "Длины списков не совпадают"
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()
create_table_query = """
CREATE TABLE IF NOT EXISTS your_table_name (
    id SERIAL PRIMARY KEY,
    company VARCHAR,
    fact_qliq_data1 NUMERIC,
    fact_qliq_data2 NUMERIC,
    fact_qoil_data1 NUMERIC,
    fact_qoil_data2 NUMERIC,
    forecast_qliq_data1 NUMERIC,
    forecast_qliq_data2 NUMERIC,
    forecast_qoil_data1 NUMERIC,
    forecast_qoil_data2 NUMERIC
)
"""
cursor.execute(create_table_query)
conn.commit()

for row in range(list_length):
    insert_query = '''
    INSERT INTO your_table_name (
        id ,
    company,
    fact_qliq_data1,
    fact_qliq_data2,
    fact_qoil_data1,
    fact_qoil_data2,
    forecast_qliq_data1,
    forecast_qliq_data2,
    forecast_qoil_data1,
    forecast_qoil_data2
        
    )
    VALUES (
        %s, %s, %s, %s, %s, %s,%s, %s, %s, %s
    )
    '''
    values = tuple(data_lists[column][row] for column in range(len(data_lists)))
    cursor.execute(insert_query, values)
conn.commit()
cursor.close()
conn.close()