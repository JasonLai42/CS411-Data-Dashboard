from db_connection_manager import DatabaseConnectionManager

# Initialize our DatabaseConnectionManager object which stores all the info pertaining to our database connections
# Note: DatabaseConnectionManager is a singleton, so every call to DatabaseConnectionManager() will yield the same object instance 
# no matter what file the call is in
db_conn_manager = DatabaseConnectionManager()

# Set up which database connections we need; for this project we need all of them
# I'm commenting out all the mysql connection code here and in the class definition, because I'm using pandas's read_sql() and also following the sqlalchemy code 
# convention to use a Context Manager (with statement) with connect() or begin(), both of which use only the engine so I don't need a persistent connection
db_conn_manager.set_mysql_engine()
db_conn_manager.set_mongodb_client()
# db_conn_manager.set_mysql_connection()
db_conn_manager.set_mongodb_connection()
db_conn_manager.set_neo4j_connection()

# Get the database connections and set them to variables for other files to import that need them
mysql_engine = db_conn_manager.get_mysql_engine()
# mysql_conn = db_conn_manager.get_mysql_connection()
mongodb_conn = db_conn_manager.get_mongodb_connection()
neo4j_conn = db_conn_manager.get_neo4j_connection()