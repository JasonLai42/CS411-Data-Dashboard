from sqlalchemy import create_engine
from pymongo import MongoClient
from neo4j import GraphDatabase

class DatabaseConnectionManager(object):
    # Make this class a singleton
    def __new__(cls):
        if not hasattr(cls, 'instance'):
          cls.instance = super(DatabaseConnectionManager, cls).__new__(cls)
        return cls.instance

    # Set the user info needed for each of the three database connections: mysql, mongodb, neo4j
    def __init__(self):
        self._mysql_connection_str = "mysql+pymysql://root:test_root@localhost/academicworld"
        self._neo4j_uri = "bolt://localhost:7687"
        self._neo4j_username = "neo4j"
        self._neo4j_password = "test_root"
        
    # Call this when the database connections are no longer needed; closes any open connections
    def cleanup(self):
        # self._mysql_connection.close()
        self._neo4j_connection.close()

    ################################################
    #          Setup database connections          #
    ################################################
    def set_mysql_engine(self):
        self._mysql_engine = create_engine(self._mysql_connection_str)

    def set_mongodb_client(self):
        self._mongodb_client = MongoClient()
    
    def set_mysql_connection(self):
        self._mysql_connection = self._mysql_engine.connect()

    def set_mongodb_connection(self):
        self._mongodb_connection = self._mongodb_client.academicworld

    def set_neo4j_connection(self):
        self._neo4j_connection = GraphDatabase.driver(self._neo4j_uri, auth=(self._neo4j_username, self._neo4j_password))
        self._neo4j_connection.verify_connectivity()

    ###########################################################
    # Get database connections (if you're outside this class) #
    ###########################################################
    def get_mysql_engine(self):
        return self._mysql_engine

    def get_mongodb_client(self):
        return self._mongodb_client
    
    def get_mysql_connection(self):
        return self._mysql_connection
    
    def get_mongodb_connection(self):
        return self._mongodb_connection
    
    def get_neo4j_connection(self):
        return self._neo4j_connection