import os
import sys
sys.path.append(os.getcwd())
from db.base import SessionLocal
from collections import defaultdict
from columnvalue import generate_fake_data
from db_params import tables

db = SessionLocal()

TOTAL_ENTRIES_MULTIPLIER = 1
ENTRIES_PER_FK = 2
# total entries proportional to ENTRIES_PER_FK * TOTAL_ENTRIES_MULTIPLIER

#Class to represent a graph
class Graph:
    def __init__(self,vertices):
        self.graph = defaultdict(list) #dictionary containing adjacency List
        self.V = vertices #No. of vertices
 
    # function to add an edge to graph
    def addEdge(self,u,v):
        if u not in self.graph[v] and u!=v:
            self.graph[u].append(v)
 
    # A recursive function used by topologicalSort
    def topologicalSortUtil(self,v,visited,stack):
 
        # Mark the current node as visited.
        visited[v] = True
 
        # Recurse for all the vertices adjacent to this vertex
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
 
        # Return contents of stack
        return (stack)
 

# Store "table_name": table_id
table_map={}

# Used to fill the maps
table_id=0

# Construct the map for tables to construct the graph
for table in tables:
    table_map[table.__tablename__] = table_id
    table_id+=1

g = Graph(table_id)

for table in tables:
    for column in table.__table__.c:

        # Add edge for every foreign key
        for fk in column.foreign_keys:

            # Reverse the fk for the edge; edge: fk -> column
            g.addEdge(
                table_map[str(fk.column).split(".")[0]],
                table_map[str(column).split(".")[0]]
            )

# Topsort the tables to fill
topo_tables = g.topologicalSort()

# Debug if need be 
# print(table_map)
# print(topo_tables)

def fill_data(one_many_fk=0,entry={}):
    # Run for every entry 
    for entry_number in range(ENTRIES_PER_FK-1):
        # Store the whole linked entry to refer foreign keys
        # Global data per ENTTY_PER_FK
        # key:value as "table_name.column_name" : "value"
        # entry = {}

        # Traverse in topological order
        for i in range(0,len(topo_tables)):
            table = topo_tables[i]

            # Make a dict for the db.add(**dict)
            # Will contain key:value as "column_name" : "value" 
            table_entry={}

            # List of all columns 
            columns = tables[table].__table__.c

            for column in columns:
                column_name = str(column).split(".")[1]
                
                # If a One-Many FK needs more values AND
                # If the current table is referenced by the FK, dont re generate row
                if one_many_fk!=0 and str(column).split(".")[0] == str(one_many_fk).split(".")[1]:
                    break

                # Case: The column has a FK
                if column.foreign_keys:
                    
                    # if a FK is nullable set it null
                    if column.nullable == True:
                        table_entry[column_name] = None
                    
                    else:
                        fk_column = list(column.foreign_keys)[0].column

                        # Refer global data as the fk reference is already generated
                        table_entry[column_name] = entry[str(fk_column)]

                # Case: a normal column with no FK
                else:
                        
                    # generate random data on the basis of the column
                    fake_data = generate_fake_data(column)

                    # Store the data for global access for FK later
                    entry[str(column)]= fake_data

                    # Store data for db.add()
                    table_entry[column_name] = fake_data
            
            try :
                # Ignore the empty dict because of the one-many FK reference
                if table_entry["id"]:
                    obj = tables[table](**table_entry)
                    db.add(obj)
                    db.commit()
            except Exception as e:
                pass
            
            # Get table of the one-many FK column
            if one_many_fk != 0:
                one_many_fk_table = table_map[str(one_many_fk).split(".")[0]]

            # Iterate for FK only if current table FK not recursed upon based on index of topo_tables
            if one_many_fk == 0 or topo_tables.index(table) > topo_tables.index(one_many_fk_table):
                for column in columns:
                    # One-many relation for FK which are not unique and not null
                    if column.foreign_keys and not column.unique and not column.nullable:
                        # Pass the one-many FK column
                        # Pass the values of all tables generated in this iteration,
                        # to re-reference the FK table entry.
                        fill_data(column,entry)

if __name__ == "__main__":
    for i in range(TOTAL_ENTRIES_MULTIPLIER):
        fill_data()