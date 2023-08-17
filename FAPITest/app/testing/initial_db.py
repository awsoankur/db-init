import os
import sys
sys.path.append(os.getcwd())
from sqlalchemy import text
import faker
from app.database import SessionLocal
from app import models
from collections import defaultdict
from random import randint
from datetime import datetime
from faker.providers import BaseProvider

faker = faker.Faker("en_IN")
faker.add_provider(BaseProvider)
db = SessionLocal()
TOTAL_ENTRIES = 5

def value(column):
    # print(type(column.type))
    type = str(column.type)
    if type == "INTEGER":
        return faker.bothify(text="#######")
    elif type == "TIMESTAMP":
        return datetime.today()
    elif type == "VARCHAR":
        return faker.bothify(text="random-text: ????????????")
 
#Class to represent a graph
class Graph:
    def __init__(self,vertices):
        self.graph = defaultdict(list) #dictionary containing adjacency List
        self.V = vertices #No. of vertices
 
    # function to add an edge to graph
    def addEdge(self,u,v):
        if u not in self.graph[v]:
            self.graph[u].append(v)
 
    # A recursive function used by topologicalSort
    def topologicalSortUtil(self,v,visited,stack):
 
        # Mark the current node as visited.
        visited[v] = True
 
        # Recur for all the vertices adjacent to this vertex
        for i in self.graph[v]:
            if visited[i] == False:
                self.topologicalSortUtil(i,visited,stack)
 
        # Push current vertex to stack which stores result
        stack.insert(0,v)
 
    # The function to do Topological Sort. It uses recursive
    # topologicalSortUtil()
    def topologicalSort(self):
        # Mark all the vertices as not visited
        visited = [False]*self.V
        stack =[]
 
        # Call the recursive helper function to store Topological
        # Sort starting from all vertices one by one
        for i in range(self.V):
            if visited[i] == False:
                self.topologicalSortUtil(i,visited,stack)
 
        # Print contents of stack
        return (stack)
 

# store "table_name": table_id
table_map={}
inverse_map={}
table_id=0

tables = [models.User, models.Account, models.Post, models.Votes]
for table in tables:
    table_map[table.__tablename__] = table_id
    inverse_map[table_id]=table.__tablename__
    table_id+=1

g = Graph(table_id)

for table in tables:
    for column in table.__table__.c:

        for fk in column.foreign_keys:
            #add edge using the table as a hash map
            g.addEdge(
                table_map[str(fk.column).split(".")[0]],
                table_map[str(column).split(".")[0]]
            )

topo_tables = g.topologicalSort()
for entry_number in range(TOTAL_ENTRIES):
    # run for every entry 

    #store the whole linked entry to refer foreign keys
    #global data per TOTAL_ENTRY
    entry = {}

    # traverse in topological order
    for table in topo_tables:

        # make a dict for the db
        table_entry={}

        #list of all columns 
        columns = tables[table].__table__.c
        for column in columns:
            column_name = str(column).split(".")[1]
            # case the column has a fk
            if column.foreign_keys:
                fk_column = list(column.foreign_keys)[0].column

                # if fk then refer global data already made
                table_entry[column_name] = entry[str(fk_column)]
            else:
                # generate random data, modify for correctness
                data = value(column)

                # store data for db and global
                entry[str(column)]= data
                table_entry[column_name] = data
        
        obj = tables[table](**table_entry)
        db.add(obj)
        db.commit()