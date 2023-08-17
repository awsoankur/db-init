import sys
import models
from colorama import Fore,Style
tables =[]
for model in dir(models):
    if model[0].isupper() and model not in ["Base","ForeignKey","Mapped"]:
        tables.append("\tmodels."+model+",\n")

with open("tables.py","w") as f:
    f.write("import models\n")
    f.write("tables= [\n")
    for table in tables:
        f.write(table)
    f.write("]\n")

try:
    from tables import tables as table_set
except Exception:
    print("Table generation failed, please check your models")
    exit(1)

try:
    from db_params import (
        table_id as old_table_id,
        column_faker as old_column_faker
    )
except Exception:
    print("Import Error: Some information is missing about previous db schema")
    print("ensure table_id and column_faker exist in db_params")
    exit(1)

# set id for table, use old values if found
number_new_tables_found = 0
new_table_id ={}
for table in table_set:
    if table.__tablename__ in old_table_id.keys():
        new_table_id[table.__tablename__] = old_table_id[table.__tablename__]
    else:
        new_table_id[table.__tablename__] = "set_a_table_id"
        number_new_tables_found+=1
        print(Fore.RED,"New table",table.__tablename__)
        

# set facker/0 for columns, use old values if found
number_new_columns_found = 0
new_column_faker={}
for table in table_set:
    for column in table.__table__.c:
        if str(column) in old_column_faker.keys():
            if old_column_faker[str(column)]:
                new_column_faker[str(column)] = str(old_column_faker[str(column)].name())+",\n"
            else:
                new_column_faker[str(column)] = "None,\n"
        else:
            new_column_faker[str(column)] = "set_faker,\n"
            number_new_columns_found +=1
            print(Fore.RED,"New column",str(column))


del sys.modules['db_params']

with open("db_params.py","w") as f:

    # for table list
    f.write("import models\n")
    f.write("from dbmap import *\n")
    f.write("tables= [\n")
    for table in tables:
        f.write(table)
    f.write("]\n")

    # for table id map
    f.write("table_id={\n")
    for table in table_set:
        f.write(f"\t\"{table.__tablename__}\" : \"{new_table_id[table.__tablename__]}\",\n")
    f.write("}\n")

    # for table.column -> faker map
    f.write("column_faker={\n")
    for column in new_column_faker.keys():
        f.write(f"\t\"{column}\" : {new_column_faker[column]}")
    f.write("}\n")

if number_new_columns_found + number_new_tables_found :
    print()
    print(f"Please set fakers for {number_new_columns_found} columns")
    print(f"and set Table IDs for {number_new_tables_found} tables")
    print(Style.RESET_ALL,end="")
    exit(1)
