from dash import Dash, html, dcc, callback, Output, Input, dash_table
# This sets up our database connections and the imported variables are the connections we can execute queries on
from db_connection_setup import db_conn_manager
# These are our utility functions for executing queries on our database connections
import mongodb_utils as mongo_utils
# This has the callbacks for our dash plotly widgets
import callbacks

######################################
#     Column Renaming for Tables     #
######################################
widget_three_columns = [
    {"name": "Name", "id": "uni_name"},
    {"name": "Average Score", "id": "avg_score"},
    {"name": "Number of Faculty for Keyword", "id": "num_faculty"}
]

widget_four_columns = [
    {"name": "Name", "id": "name"},
    {"name": "Score", "id": "score"}
]

widget_five_columns = [
    {"name": "Keyword", "id": "name"},
    {"name": "Score", "id": "score"}
]

widget_six_columns = [
    {"name": "University Name", "id": "university_name"},
    {"name": "Rank (double click to edit)", "id": "ranking", "editable": True}
]
widget_six_hidden_columns = ["id"]

widget_seven_columns = [
    {"name": "Name", "id": "professor_name"},
    {"name": "Research Interest (double click to edit)", "id": "research_interest", "editable": True}
]
widget_seven_hidden_columns = ["university_id", "professor_id"]

#####################################
#        Persistent app data        #
#####################################
# This is data that we need for our app at all times
# Here, dropdown_years is used to populate the dropdown for widget 1, so we always have valid years our database contains, thereby reducing user error
dropdown_years = mongo_utils.get_dropdown_years()

####################################
#        Initialize the app        #
####################################
app = Dash()

####################################
#            App layout            #
####################################
app.layout = [
    html.Div(children=[
        html.H1(children="Hot Topic", className="data-dashboard-title", id="data-dashboard-title"),
        html.Div(children=[
            # Widget 1
            html.Div(children=[
                html.Label(children="Top 10 Trending Keywords", className="widget-1-label", id="widget-1-label"),
                html.Div(children=[
                    dcc.Dropdown(dropdown_years, dropdown_years[0], className="widget-1-dropdown", id="widget-1-dropdown"),
                    html.Div(className="widget-1-big-message", id="widget-1-big-message"),
                    html.Div(id="widget-1-graph-container")
                ], className="widget-1-container", id="widget-1-container")
            ], className="widget-1", id="widget-1"),
            # Widgets 2 & 3
            html.Div(children=[
                html.Label(children="Keyword Performance over Time", className="widget-2-label", id="widget-2-label"),
                html.Div(children=[
                    html.Div(children=[
                        html.Div(children=[
                            html.Div(children=[
                                dcc.Input(type="text", placeholder="Enter keyword", debounce=True, className="widgets-2-and-3-input", 
                                        id="widgets-2-and-3-input"),
                                html.Button(children="Show Results", n_clicks=0, className="widgets-2-and-3-submit-button", id="widgets-2-and-3-submit-button"),
                            ], className="widgets-2-and-3-input-flex-box", id="widgets-2-and-3-input-flex-box"),
                            html.Div(id="widgets-2-and-3-search-message")
                        ], className="widgets-2-and-3-input-container", id="widgets-2-and-3-input-container"),
                        html.Div(className="widget-2-big-message", id="widget-2-big-message"),
                        html.Div(id="widget-2-graph-container")
                    ], className="widget-2-container", id="widget-2-container"),
                    html.Label(children="Top 5 Universities for Keyword", className="widget-3-label", id="widget-3-label"),
                    html.Div(children=[
                        html.Div(className="widget-3-big-message", id="widget-3-big-message"),
                        html.Div(dash_table.DataTable(columns=widget_three_columns, style_table={ "width": "49.25rem", "margin-top": "-3rem" }, 
                                style_cell={ "textAlign": "left", "font-family": "Arial" }, page_size=5, id="widget-3-data"), 
                                className="widget-3-hide-table-container", id="widget-3-hide-table-container")
                    ], className="widget-3-container", id="widget-3-container")
                ], className="widgets-2-and-3-container", id="widgets-2-and-3-container")
            ], className="widgets-2-and-3", id="widgets-2-and-3"),
            # Widget 4
            html.Div(children=[
                html.Label(children="Faculty Member List at University for Keyword", className="widget-4-label", id="widget-4-label"),
                html.Div(children=[
                    html.Div(children=[
                        html.Div(children=[
                            dcc.Input(type="text", placeholder="Enter name of university", debounce=True, className="widget-4-input", 
                                    id="widget-4-input-university"),
                            dcc.Input(type="text", placeholder="Enter name of keyword", debounce=True, className="widget-4-input", 
                                    id="widget-4-input-keyword"),
                        ], className="widget-4-input-flex-box", id="widget-4-input-flex-box"),
                        html.Button(children="View Faculty", n_clicks=0, className="widget-4-submit-button", id="widget-4-submit-button"),
                        html.Div(id="widget-4-search-message")
                    ], className="widget-4-input-container", id="widget-4-input-container"),
                    html.Div(className="widget-4-big-message", id="widget-4-big-message"),
                    html.Div(dash_table.DataTable(columns=widget_four_columns, style_table={ "margin-top": "-6.5rem" }, 
                            style_cell={ "textAlign": "left", "font-family": "Arial" }, page_size=10, id="widget-4-data"), 
                            className="widget-4-hide-table-container", id="widget-4-hide-table-container")
                ], className="widget-4-container", id="widget-4-container")
            ], className="widget-4", id="widget-4"),
            # Widget 5
            html.Div(children=[
                html.Label(children="Search Professor", className="widget-5-label", id="widget-5-label"),
                html.Div(children=[
                    html.Div(children=[
                        html.Div(children=[
                            dcc.Input(type="text", placeholder="Enter name of professor", debounce=True, className="widget-5-input", id="widget-5-input"),
                            html.Button(children="View Professor", n_clicks=0, className="widget-5-submit-button", id="widget-5-submit-button")
                        ], className="widget-5-input-flex-box", id="widget-5-input-flex-box"),
                        html.Div(id="widget-5-search-message")
                    ], className="widget-5-input-container", id="widget-5-input-container"),
                    html.Div(className="widget-5-big-message", id="widget-5-big-message"),
                    html.Div(children=[
                        html.Img(className="widget-5-data-photoUrl", id="widget-5-data-photoUrl"),
                        html.Div(children=[
                            html.Div(id="widget-5-data-name"),
                            html.Div(id="widget-5-data-position"),
                            html.Div(id="widget-5-data-email"),
                            html.Div(id="widget-5-data-phone"),
                            html.Div(id="widget-5-data-university")
                        ], className="widget-5-prof-info", id="widget-5-prof-info"),
                        html.Div(dash_table.DataTable(columns=widget_five_columns, style_table={ "width": "300px" }, 
                                style_cell={ "textAlign": "left", "font-family": "Arial", "overflow": "hidden", "textOverflow": "ellipsis", "maxWidth": 0 }, 
                                style_cell_conditional=[
                                        { "if": { "column_id": "name" },
                                         "minWidth": "80px", "width": "80px", "maxWidth": "80px" },
                                        { "if": { "column_id": "score" },
                                         "minWidth": "25px", "width": "25px", "maxWidth": "25px" },
                                ], page_size=5, id="widget-5-data-keywords"), className="widget-5-hide-table-container", id="widget-5-hide-table-container")
                    ], className="widget-5-flex-box", id="widget-5-flex-box")
                ], className="widget-5-container", id="widget-5-container")
            ], className="widget-5", id="widget-5"),
            # Widget 6
            html.Div([
                html.Label(children="Universities You're Interested in", className="widget-6-label", id="widget-6-label"),
                html.Div(children=[
                    html.Div(children=[
                        html.Div(children=[
                            dcc.Input(type="text", placeholder="Enter name of university", debounce=True, className="widget-6-input", id="widget-6-input"),
                            html.Button(children="Add University", n_clicks=0, className="widget-6-submit-button", id="widget-6-submit-button")
                        ], className="widget-6-input-flex-box", id="widget-6-input-flex-box"),
                        html.Div(id="widget-6-search-message")
                    ], className="widget-6-input-container", id="widget-6-input-container"),
                    html.Div(className="widget-6-big-message", id="widget-6-big-message"),
                    html.Div(dash_table.DataTable(columns=widget_six_columns, hidden_columns=widget_six_hidden_columns, row_selectable="single", selected_rows=[], row_deletable=True, css=[{"selector": ".show-hide", "rule": "display: none"}], style_table={ "margin-top": "-6.9rem" }, style_cell={ "textAlign": "left", "font-family": "Arial" }, page_size=10, id="widget-6-data"), className="widget-6-hide-table-container", id="widget-6-hide-table-container")
                ], className="widget-6-container", id="widget-6-container")
            ], className="widget-6", id="widget-6"),
            # Widget 7
            html.Div(children=[
                html.Label(className="widget-7-label", id="widget-7-label"),
                html.Div(children=[
                    html.Div(children=[
                        html.Div(children=[
                            dcc.Input(type="text", placeholder="Enter name of professor", debounce=True, className="widget-7-input", id="widget-7-input-professor"),
                            dcc.Input(type="text", placeholder="Enter name of keyword", debounce=True, className="widget-7-input", id="widget-7-input-keyword")
                        ], className="widget-7-input-flex-box", id="widget-7-input-flex-box"),
                        html.Button(children="Add Professor", n_clicks=0, className="widget-7-submit-button", id="widget-7-submit-button"),
                        html.Div(id="widget-7-search-message")
                    ], className="widget-7-input-container", id="widget-7-input-container"),
                    html.Div(className="widget-7-big-message", id="widget-7-big-message"),
                    html.Div(dash_table.DataTable(columns=widget_seven_columns, hidden_columns=widget_seven_hidden_columns, row_deletable=True, css=[{"selector": ".show-hide", "rule": "display: none"}], style_table={ "margin-top": "-6.9rem" }, style_cell={ "textAlign": "left", "font-family": "Arial" }, page_size=10, id="widget-7-data"), className="widget-7-hide-table-container", id="widget-7-hide-table-container"),
                    dcc.Store(id="widget-7-store", storage_type="memory")
                ], className="widget-7-container", id="widget-7-container")
            ], className="widget-7", id="widget-7")
        ], className="data-dashboard-grid", id="data-dashboard-grid")
    ], className="data-dashboard", id="data-dashboard")
]

###################################
#           Run the app           #
###################################
if __name__ == '__main__':
    app.run(debug=True)
    db_conn_manager.cleanup()