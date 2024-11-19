from sqlalchemy import create_engine
from pymongo import MongoClient
from neo4j import GraphDatabase
        
global _neo4j_connection

def get_mysql_connection():
    mysql_conn_str = 'mysql+pymysql://root:test_root@localhost/academicworld'
    _mysql_connection = create_engine(mysql_conn_str)
    return _mysql_connection

def get_mongodb_connection():
    conn = MongoClient()
    _mongodb_connection = conn.academicworld
    return _mongodb_connection

def get_neo4j_connection():
    _neo4j_connection = GraphDatabase.driver("neo4j://localhost:7474", auth=("root", "test_root"))
    return _neo4j_connection

def close_neo4j_connection():
    if _neo4j_connection:
        _neo4j_connection.close()

__all__ = [ 'get_mysql_connection', 'get_mongodb_connection', 'get_neo4j_connection' ]