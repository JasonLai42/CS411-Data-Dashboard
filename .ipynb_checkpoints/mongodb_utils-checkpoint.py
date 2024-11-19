import pandas as pd
import pymongo
from pymongo.collation import Collation
# This sets up our database connections and the imported variables are the connections we can execute queries on
from db_connection_setup import mongodb_conn

#########################################
#               Constants               #
#########################################
COLLECTION_FACULTY = "faculty"
COLLECTION_PUBLICATIONS = "publications"
COLLATION_EN = "en"
ORIENTATION_RECORDS = "records"

#########################################
#           Utility functions           #
#########################################
def execute_aggregate(pipeline, collection_str):
    db_collection = mongodb_conn[collection_str]
    result = db_collection.aggregate(pipeline)
    return result

def execute_aggregate_with_collation(pipeline, collection_str, collation_locale):
    db_collection = mongodb_conn[collection_str]
    result = db_collection.aggregate(pipeline, collation=Collation(locale=collation_locale))
    return result

def get_mongodb_dataframe(mongodb_result):
    df = pd.DataFrame(list(mongodb_result))
    return df

def convert_dataframe_to_dict(dataframe, orientation):
    df_dict = dataframe.to_dict(orientation)
    return df_dict

def convert_array_json_to_table_data(arr):
    df = pd.json_normalize(arr)
    return convert_dataframe_to_dict(df, ORIENTATION_RECORDS)

######################################
# Specific aggregate query pipelines #
######################################
def get_pipeline_trending_keywords(year):
    pipeline = [
        {"$match": {"year": year}}, 
        {"$unwind": "$keywords"}, 
        {"$group": {"_id": "$keywords.name", "count": {"$sum": 1}}}, 
        {"$sort": {"count": pymongo.DESCENDING}}, 
        {"$limit": 10}
    ]
    return pipeline

def get_pipeline_year_dropdown():
    pipeline = [
        {"$project": {"year": 1}}, 
        {"$group": {"_id": "$year", "year": {"$first": "$year"}}}, 
        {"$sort": {"year": pymongo.DESCENDING}}
    ]
    return pipeline

def get_pipeline_professor_info(name):
    pipeline = [
        {"$match": {"name": name}}, 
        {"$project": {"name": 1, "position": 1, "email": 1, "phone": 1, "university": "$affiliation.name", "photoUrl": 1, "keywords.name": 1, "keywords.score": 1}}
    ]
    return pipeline

############################################
# Specific widget data retrieval functions #
############################################
def get_dropdown_years():
    pl = get_pipeline_year_dropdown()
    mongodb_res = execute_aggregate(pl, COLLECTION_PUBLICATIONS)
    df = get_mongodb_dataframe(mongodb_res)
    return df.year

def get_trending_keywords(year):
    pl = get_pipeline_trending_keywords(year)
    mongodb_res = execute_aggregate(pl, COLLECTION_PUBLICATIONS)
    df = get_mongodb_dataframe(mongodb_res)
    return df

def get_professor_info(name):
    pl = get_pipeline_professor_info(name)
    mongodb_res = execute_aggregate(pl, COLLECTION_FACULTY)
    df = get_mongodb_dataframe(mongodb_res)
    df_dict = convert_dataframe_to_dict(df, ORIENTATION_RECORDS)
    return df_dict