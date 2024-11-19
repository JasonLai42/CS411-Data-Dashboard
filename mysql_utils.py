from sqlalchemy import text
import pandas as pd
# This sets up our database connections and the imported variables are the connections we can execute queries on
from db_connection_setup import mysql_engine

#########################################
#               Constants               #
#########################################
ORIENTATION_RECORDS = "records"

#########################################
#           Utility functions           #
#########################################
def execute_query(query_str, param_dict):
    # Using begin() in a Context Manager has the engine wrap our sql query in a transaction that rolls back the queries if an exception is thrown or commits 
    # the changes if no exception is thrown, which is redundant because I only use this function to execute stored procedures and all of them except one are 
    # already wrapped in a transaction that rolls back and commits based on exceptions as well
    with mysql_engine.begin() as db_conn:
        db_conn.execute(text(query_str), param_dict)

def get_mysql_dataframe(query_str, param_dict):
    df = pd.read_sql(query_str, con=mysql_engine, params=param_dict)
    return df

def get_mysql_dataframe_dict(dataframe, orientation):
    df_dict = dataframe.to_dict(orientation)
    return df_dict

##########################################
#       Specific SQL query strings       #
##########################################
# Non-updating query strings - executed through pandas's read_sql() so use PEP 249 paramstyle: %(param)s
def get_query_keyword_performance_over_time():
    query_str = "SELECT p.year AS year, COUNT(*) AS number_of_publications FROM publication AS p WHERE p.ID IN (SELECT pk.publication_id FROM publication_keyword AS pk WHERE pk.keyword_id = (SELECT k.id FROM keyword AS k WHERE k.name = %(keyword)s)) AND p.year IS NOT NULL GROUP BY p.year ORDER BY p.year ASC;"
    return query_str

def get_query_faculty_list_by_university():
    query_str = "SELECT f.name, fk_scores.score FROM faculty AS f, (SELECT fk.faculty_id, fk.score FROM faculty_keyword AS fk WHERE keyword_id = (SELECT k.id FROM keyword AS k WHERE k.name = %(keyword)s)) AS fk_scores WHERE f.id = fk_scores.faculty_id AND f.university_id = (SELECT u.id FROM university AS u WHERE u.name = %(university)s) ORDER BY fk_scores.score DESC;"
    return query_str

def get_query_university_picks():
    query_str = "CALL get_university_picks;"
    return query_str

def get_query_professors_for_university_pick():
    query_str = "CALL get_professors_for_university_pick(%(university_id)s);"
    return query_str

# Updating query strings - executed through sqlalchemy's execute() so use PEP 249 paramstyle: :param
def get_query_insert_university_pick():
    query_str = "CALL insert_university_pick(:university)"
    return query_str

def get_query_delete_university_pick():
    query_str = "CALL delete_university_pick(:university_id, :ranking)"
    return query_str

def get_query_drop_ranking():
    query_str = "CALL drop_ranking(:university_id, :new_ranking, :current_ranking)"
    return query_str

def get_query_raise_ranking():
    query_str = "CALL raise_ranking(:university_id, :new_ranking, :current_ranking)"
    return query_str

def get_query_insert_professor_for_university_pick():
    query_str = "CALL insert_professor_for_university_pick(:university_id, :professor, :keyword);"
    return query_str

def get_query_delete_professor_for_university_pick():
    query_str = "CALL delete_professor_for_university_pick(:university_id, :professor_id);"
    return query_str

def get_query_update_keyword_for_professor():
    query_str = "CALL update_uni_pick_research_interest_for_prof(:university_id, :professor_id, :keyword);"
    return query_str
    
############################################
# Specific widget data retrieval functions #
############################################
# Non-updating functions
def get_keyword_performance_over_time(keyword):
    p_dict = { "keyword": keyword }
    qs = get_query_keyword_performance_over_time()
    df = get_mysql_dataframe(qs, p_dict)
    return df

def get_faculty_list_by_university(university, keyword):
    p_dict = { "university": university, "keyword": keyword }
    qs = get_query_faculty_list_by_university()
    df = get_mysql_dataframe(qs, p_dict)
    df_dict = get_mysql_dataframe_dict(df, ORIENTATION_RECORDS)
    return df_dict

def get_university_picks():
    p_dict = {}
    qs = get_query_university_picks()
    df = get_mysql_dataframe(qs, p_dict)
    df_dict = get_mysql_dataframe_dict(df, ORIENTATION_RECORDS)
    return df_dict

def get_professors_for_university_pick(university_id):
    p_dict = { "university_id": university_id }
    qs = get_query_professors_for_university_pick()
    df = get_mysql_dataframe(qs, p_dict)
    df_dict = get_mysql_dataframe_dict(df, ORIENTATION_RECORDS)
    return df_dict

# Updating functions
def execute_insert_university_pick(university):
    p_dict = { "university": university }
    qs = get_query_insert_university_pick()
    execute_query(qs, p_dict)

def execute_delete_university_pick(university_id, ranking):
    p_dict = { "university_id": university_id, "ranking": ranking }
    qs = get_query_delete_university_pick()
    execute_query(qs, p_dict)

def execute_update_ranking(university_id, new_ranking, current_ranking):
    p_dict = { "university_id": university_id, "new_ranking": new_ranking, "current_ranking": current_ranking }
    qs = ""
    try:
        new_ranking_num = int(new_ranking)
        current_ranking_num = int(current_ranking)
        if new_ranking_num > current_ranking_num:
            qs = get_query_drop_ranking()
        else:
            qs = get_query_raise_ranking()
    except ValueError:
        return
    execute_query(qs, p_dict)

def execute_insert_professor_for_university_pick(university_id, professor, keyword):
    p_dict = { "university_id": university_id, "professor": professor, "keyword": keyword }
    qs = get_query_insert_professor_for_university_pick()
    execute_query(qs, p_dict)

def execute_delete_professor_for_university_pick(university_id, professor_id):
    p_dict = { "university_id": university_id, "professor_id": professor_id }
    qs = get_query_delete_professor_for_university_pick()
    execute_query(qs, p_dict)

def execute_update_keyword_for_professor(university_id, professor_id, keyword):
    p_dict = { "university_id": university_id, "professor_id": professor_id, "keyword": keyword }
    qs = get_query_update_keyword_for_professor()
    execute_query(qs, p_dict)