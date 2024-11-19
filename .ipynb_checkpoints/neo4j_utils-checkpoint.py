import pandas as pd
import neo4j
# This sets up our database connections and the imported variables are the connections we can execute queries on
from db_connection_setup import neo4j_conn

#########################################
#               Constants               #
#########################################
DB_ACADEMICWORLD = "academicworld"
ORIENTATION_RECORDS = "records"

#########################################
#           Utility functions           #
#########################################
def get_neo4j_dataframe(query_str, param_dict):
    df = neo4j_conn.execute_query(query_str, parameters_=param_dict, database_=DB_ACADEMICWORLD, result_transformer_=neo4j.Result.to_df)
    return df

def get_neo4j_dataframe_dict(dataframe, orientation):
    df_dict = dataframe.to_dict(orientation)
    return df_dict

###########################################
#      Specific Cypher query strings      #
###########################################
# Neo4j parameterized queries use PEP 249 paramstyle: $param
def get_cypher_top_universities_by_keyword(keyword):
    query_str = "MATCH (u:INSTITUTE)<-[:AFFILIATION_WITH]-(fm:FACULTY)-[research:INTERESTED_IN]->(k:KEYWORD) WHERE k.name = $keyword RETURN u.name AS uni_name, sum(research.score) / count(*) AS avg_score, count(*) AS num_faculty ORDER BY avg_score DESC LIMIT 5"
    return query_str

############################################
# Specific widget data retrieval functions #
############################################
def get_top_universities_by_keyword(keyword):
    p_dict = { "keyword": keyword }
    qs = get_cypher_top_universities_by_keyword(keyword)
    df = get_neo4j_dataframe(qs, p_dict)
    df_dict = get_neo4j_dataframe_dict(df, ORIENTATION_RECORDS)
    return df_dict