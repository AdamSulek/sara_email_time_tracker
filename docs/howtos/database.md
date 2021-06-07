## Data insertion into Database

For data insertion into Database use Database class.  
The Database class takes dictionary list created on Message object with to_records method and database name.  
By default database_name = 'sqlite:///sqlalchemy.db'
Using of insert_bulk function on Database class instance insert the rows of data into Database.  


```python
from app.database import Database
msg_to_db = Database(timelogs=to_records_var, database_name=database_name)
msg_to_db.insert_bulk()
```
