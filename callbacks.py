from dash import Dash, html, dcc, callback, Output, Input, State, dash_table, ctx
from dash.exceptions import PreventUpdate
import plotly.express as px
# These are our utility functions for executing queries on our database connections
import mysql_utils as sql_utils
import mongodb_utils as mongo_utils
import neo4j_utils as neo_utils
import pandas as pd

####################################################
#                     Widget 1                     #
####################################################
@callback(
    Output("widget-1-big-message", "children"),
    Output("widget-1-graph-container", "children"),
    Input("widget-1-dropdown", "value")
)
def update_widget_one(value):
    # ONE: Variables to store return values and intermediate values
    big_message = ""
    widget_data = html.Div(id="widget-1-data")
    trending_keywords = pd.DataFrame()
    
    # TWO: Database action logic
    if not value:
        big_message = "No data to show"
    else:
        trending_keywords = mongo_utils.get_trending_keywords(value)

    # THREE: Check if we have any data and set big message accordingly, then return
    if trending_keywords.empty:
        big_message = "No data to show"
    else:
        widget_data = dcc.Graph(figure=px.pie(trending_keywords, names="_id", values="count", hole=0.3), className="widget-1-data", id="widget-1-data")
    return big_message, widget_data

###################################################
#                  Widgets 2 & 3                  #
###################################################
@callback(
    Output("widgets-2-and-3-search-message", "children"),
    Output("widget-2-big-message", "children"),
    Output("widget-2-graph-container", "children"),
    Input("widgets-2-and-3-submit-button", "n_clicks"),
    State("widgets-2-and-3-input", "value")
)
def update_widget_two(n_clicks, value):
    # ONE: Variables to store return values and intermediate values
    search_message = ""
    big_message = ""
    widget_data = html.Div(id="widget-2-data")
    keyword_performance_over_time = pd.DataFrame()

    # TWO: Database action logic
    if n_clicks > 0:
        if not value:
            search_message = "Please enter a keyword"
        else:
            keyword_performance_over_time = sql_utils.get_keyword_performance_over_time(value)

    # THREE: Check if we have any data and set big message accordingly, then return
    if keyword_performance_over_time.empty:
        if n_clicks > 0 and value:
            big_message = f'No data for \"{value}\"'
        else:
            big_message = "No data to show"
    else:
        search_message = f'Results for \"{value}\"'
        widget_data = dcc.Graph(figure=px.line(keyword_performance_over_time, x="year", y="number_of_publications"), className="widget-2-data", id="widget-2-data")
    return search_message, big_message, widget_data

@callback(
    Output("widget-3-big-message", "children"),
    Output("widget-3-data", "data"),
    Input("widgets-2-and-3-submit-button", "n_clicks"),
    State("widgets-2-and-3-input", "value")
)
def update_widget_three(n_clicks, value):
    # ONE: Variables to store return values and intermediate values
    big_message = ""
    top_universities_by_keyword = []

    # TWO: Database action logic
    if n_clicks > 0:
        if value:
            top_universities_by_keyword = neo_utils.get_top_universities_by_keyword(value)

    # THREE: Check if we have any data and set big message accordingly, then return
    if not top_universities_by_keyword:
        if n_clicks > 0 and value:
            big_message = f'No data for \"{value}\"'
        else:
            big_message = "No data to show"
    return big_message, top_universities_by_keyword

####################################################
#                     Widget 4                     #
####################################################
@callback(
    Output("widget-4-search-message", "children"),
    Output("widget-4-big-message", "children"),
    Output("widget-4-data", "data"),
    Input("widget-4-submit-button", "n_clicks"),
    State("widget-4-input-university", "value"),
    State("widget-4-input-keyword", "value")
)
def update_widget_four(n_clicks, value_1, value_2):
    # ONE: Variables to store return values and intermediate values
    search_message = ""
    big_message = ""
    faculty_list_by_university = []

    # TWO: Database action logic
    if n_clicks > 0:
        if not value_1 or not value_2:
            search_message = "Please enter a university name and keyword"
        else:
            faculty_list_by_university = sql_utils.get_faculty_list_by_university(value_1, value_2)

    # THREE: Check if we have any data and set big message accordingly, then return
    if not faculty_list_by_university:
        if n_clicks > 0 and value_1 and value_2:
            big_message = f'No data for {value_1} and \"{value_2}\"'
        else:
            big_message = "No data to show"
    else:
        search_message = f'Results for {value_1} and \"{value_2}\"'
    return search_message, big_message, faculty_list_by_university

####################################################
#                     Widget 5                     #
####################################################
@callback(
    [Output("widget-5-search-message", "children"),
    Output("widget-5-big-message", "children"),
    Output("widget-5-data-name", "children"),
    Output("widget-5-data-position", "children"),
    Output("widget-5-data-email", "children"),
    Output("widget-5-data-phone", "children"),
    Output("widget-5-data-photoUrl", "src"),
    Output("widget-5-data-photoUrl", "hidden"),
    Output("widget-5-data-university", "children"),
    Output("widget-5-data-keywords", "data")],
    Input("widget-5-submit-button", "n_clicks"),
    State("widget-5-input", "value")
)
def update_widget_five(n_clicks, value):
    # ONE: Variables to store return values and intermediate values
    result = [ "", "", "", "", "", "", "", True, "", [] ]
    professor_info = []

    # TWO: Database action logic
    if n_clicks > 0:
        if not value:
            result[0] = "Please enter a professor's name"
        else:
            professor_info = mongo_utils.get_professor_info(value)

    # THREE: Check if we have any data and set big message accordingly, then return
    if not professor_info:
        if n_clicks > 0 and value:
            result[1] = f'No data for {value}'
        else:
            result[1] = "No data to show"
    else:
        result[2] = f'Name: {professor_info[0]["name"]}'
        result[3] = f'Position: {professor_info[0]["position"]}'
        result[4] = f'Email: {professor_info[0]["email"]}'
        result[5] = f'Phone: {professor_info[0]["phone"]}'
        result[6] = f'{professor_info[0]["photoUrl"]}'
        result[7] = False
        result[8] = f'Affiliation: {professor_info[0]["university"]}',
        result[9] = mongo_utils.convert_array_json_to_table_data(professor_info[0]["keywords"])
    return result

####################################################
#                     Widget 6                     #
####################################################
@callback(
    Output("widget-6-search-message", "children"),
    Output("widget-6-big-message", "children"),
    Output("widget-6-data", "data"),
    [Input("widget-6-submit-button", "n_clicks"),
    State("widget-6-input", "value")],
    [Input("widget-6-data", "data_previous"),
    State("widget-6-data", "data")]
)
def update_widget_six(n_clicks, value, previous, current):
    # ONE: Variables to store return values and intermediate values
    search_message = ""
    big_message = ""

    # TWO: Database action logic
    # Handles insert
    if ctx.triggered_id == "widget-6-submit-button":
        if n_clicks > 0:
            if not value:
                search_message = "Please enter a university name"
            else:
                sql_utils.execute_insert_university_pick(value)
    # Handles delete & update
    elif ctx.triggered_id == "widget-6-data":
        if previous is None or current is None:
            raise PreventUpdate
        else:
            # Handles delete
            if len(previous) > len(current):
                deleted_row = [row for row in previous if row not in current]
                if not deleted_row:
                    raise PreventUpdate
                else:
                    sql_utils.execute_delete_university_pick(deleted_row[0]["id"], deleted_row[0]["ranking"])
            # Handles update
            elif len(current) == len(previous):
                new_row = [row for row in current if row not in previous]
                old_row = [row for row in previous if row not in current]
                if not new_row or not old_row:
                    raise PreventUpdate
                if new_row[0]["id"] != old_row[0]["id"]:
                    raise PreventUpdate
                if new_row[0]["ranking"] == old_row[0]["ranking"]:
                    raise PreventUpdate
                sql_utils.execute_update_ranking(new_row[0]["id"], new_row[0]["ranking"], old_row[0]["ranking"])
            else:
                raise PreventUpdate

    # THREE: Check if we have any data and set big message accordingly, then return
    # Always try to show user's followed universities
    university_picks = sql_utils.get_university_picks()
    if not university_picks:
        big_message = "Currently not following any universities"
    return search_message, big_message, university_picks
            
####################################################
#                     Widget 7                     #
####################################################
@callback(
    Output("widget-7-label", "children"),
    Output("widget-7-search-message", "children"),
    Output("widget-7-big-message", "children"),
    Output("widget-7-data", "data"),
    Output("widget-7-store", "data"),
    [Input("widget-6-data", "selected_rows"),
    Input("widget-6-data", "data")],
    [Input("widget-7-submit-button", "n_clicks"),
    State("widget-7-input-professor", "value"),
    State("widget-7-input-keyword", "value")],
    [Input("widget-7-data", "data_previous"),
    State("widget-7-data", "data")],
    State("widget-7-store", "data")
)
def update_widget_seven(selected_row, uni_data, n_clicks, value_1, value_2, previous, current, stored_data):
    # ONE: Variables to store return values and intermediate values
    label = "Professors You're Interested in at Universities You're Following"
    search_message = ""
    big_message = ""
    professors_for_university_pick = []
    data = stored_data or { "uni_id": None, "uni_name": None }
    
    # TWO: Database action logic
    # Handles displaying the table
    if ctx.triggered_id == "widget-6-data":
        if not selected_row or not uni_data:
            big_message = "No data to show"
        else:
            if selected_row[0] > (len(uni_data) - 1) or selected_row[0] < 0:
                raise PreventUpdate
            data["uni_id"] = uni_data[selected_row[0]]["id"]
            data["uni_name"] = uni_data[selected_row[0]]["university_name"]
            professors_for_university_pick = sql_utils.get_professors_for_university_pick(data["uni_id"])
            label = f'Professors You\'re Interested in at {data["uni_name"]}'
    # This logic is all contingent on the fact we have selected a valid university which would set uni_id
    elif data["uni_id"] is not None:
        # Handles insert
        if ctx.triggered_id == "widget-7-submit-button":
            if n_clicks > 0:
                if not value_1 or not value_2:
                    search_message = "Please enter a professor's name and keyword"
                else:
                    sql_utils.execute_insert_professor_for_university_pick(data["uni_id"], value_1, value_2)
        # Handles delete & update
        elif ctx.triggered_id == "widget-7-data":
            if previous is None or current is None:
                raise PreventUpdate
            else:
                # Handles delete
                if len(previous) > len(current):
                    deleted_row = [row for row in previous if row not in current]
                    if not deleted_row:
                        raise PreventUpdate
                    else:
                        sql_utils.execute_delete_professor_for_university_pick(data["uni_id"], deleted_row[0]["professor_id"])
                # Handles update
                elif len(current) == len(previous):
                    new_row = [row for row in current if row not in previous]
                    old_row = [row for row in previous if row not in current]
                    if not new_row or not old_row:
                        raise PreventUpdate
                    if new_row[0]["professor_id"] != old_row[0]["professor_id"]:
                        raise PreventUpdate
                    sql_utils.execute_update_keyword_for_professor(new_row[0]["university_id"], new_row[0]["professor_id"], new_row[0]["research_interest"])
                else:
                    raise PreventUpdate
        professors_for_university_pick = sql_utils.get_professors_for_university_pick(data["uni_id"])
        label = f'Professors You\'re Interested in at {data["uni_name"]}'

    # THREE: Check if we have any data and set big message accordingly, then return
    if not professors_for_university_pick:
        if data["uni_id"] is not None:
            big_message = f'Currently not following any professors for {data["uni_name"]}'
        else:
            big_message = "No data to show"
    return label, search_message, big_message, professors_for_university_pick, data