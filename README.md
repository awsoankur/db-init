# Database Initializer

## Requirements
Faker must be installed `pip install faker`.
You must also have the following files in the same directory

* `db_init.sh`
* `db_start_test.py`
* `db_fill.py`
* `db_map.py`
* `columnvalue.py`

Along with these, there must be alembic setup in the directory, a folder `models` with an init 
file importing all the required models.

## Usage
### Running the db initializer
Run the bashfile as follows :
```
./db_init.sh
```
### Modifications

In case of modificatio of models there are changes that need to be made in the project.

* In case one needs to **modify table ID** or the prefix of id for a table, modify the dictionary `table_id` in the file `db_params.py`
```
table_id={
    "table_name" : "tn", // add an entry like this
}
```
* In case of **modification/addition of a column** of table, update the name of the column in `column_faker` in file 
`db_params.py`.
```
column_faker ={
    "<table_name>.<column_name>" : <some_faker>,    // add/modify maintaining this format
}
```
* In case a **new model is created/modified**, add/modify the model in the list `tables` in file `db_fill.py` and add all columns with appropriate faker models and fill in table_id like done in previous steps.
```
tables =[
    models.NewModel, // add a model like this
]
```
* In case one needs a **new faker model**, create a new provider over `BaseProvider`. the provider must have a method `fake` which returns the required value.
```
class NewProvider(BaseProvider):    # Template for a Provider
    def fake(self,column):          # column can be used to
        return 0                    # subdivide types of random values

# Init faker
new_faker = faker.Faker("en_IN)
# Add Provider
new_faker.add_provider(NewProvider)
```