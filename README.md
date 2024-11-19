# JasonLai

## Title of Application
Hot Topic

## Purpose
**Users**: Prospective undergraduate or graduate computer science students

**Application Scenario**: The application scenario is suppose you are a prospective undergraduate or graduate computer science student who plans to do research and wants to know what research topics are currently popular or have been popular in recent time to help decide on a topic to pursue. Then suppose, once you've decided on a topic, you want to find universities and professors who are highly involved with that topic and will give the best guidance on it.

**Objective**: Hot Topic is an application whose objective is to provide users a solution to the above scenario with an interface to discover relevant research topics and follow/record universities and professors who are related to topics the user is interested in.

## Demo
### https://mediaspace.illinois.edu/media/t/1_9sboye7s

## Installation
To install the application, you just need Python 3, the requisite libraries: plotly, dash, pandas, sqlalchemy, pymongo, and neo4j using the installation method of your choice (I just used `pip install`), and of course the three databases (MySQL, MongoDB, and Neo4j) with the AcademicWorld dataset loaded onto them. Then, you need to run the SQL statements I've put in the file titled `stored_procedures.txt` for the AcademicWorld database on MySQL. The SQL statements essentially create two new tables used by the dashboard and a series of stored procedures that the application code uses to update, insert, delete, and query those two tables. You can put the statements into a `.sql` file and run it, but I personally ran them manually as I was writing and testing them.

After everything is set up, you should be able to run the application by executing `python3 app.py` on your terminal inside the project directory.

## Usage
At a high level, the design of the application is meant to follow a very natural line of thought through the functionalities of the widgets and their ordering. The intended usage of the dashboard is something like this: 

  1. Find popular keywords by year (**Top 10 Trending Keywords** widget)
  2. Choose a keyword
  3. Look at how relevant the keyword has been over time (**Keyword Performance over Time** widget)
  4. Find universities strongly correlated with this keyword (**Top 5 Universities for Keyword** widget)
  5. Find professors who are involved with this keyword at those universities (**Faculty Member List at University for Keyword** widget)
  6. Look at information about the professor to decide whether or not you want to research under them (**Search Professor** widget)
  7. Record universities and any of their faculty you want to research under and rank them by which university you want to attend the most (**Universities You're Interested in** & **Professors You're Interested in at Universities You're Following** widgets)

Below describes how to use each widget.

### Widget 1: Top 10 Trending Keywords
From the dropdown, select a year to see what 10 keywords had the most publications for that year.

### Widgets 2 & 3: Keyword Performance over Time, Top 5 Universities for Keyword
Enter a keyword (exact spelling and casing) and click the "Show Results" button to see a line graph of how the keyword has trended in number of publications by year and the top 5 universities according to the average score across all faculty members at each institution who are related to the keyword and the number of faculty at each institution.

### Widget 4: Faculty Member List at University for Keyword
Enter a university's name and keyword (exact spelling and casing) and click the "View Faculty" button to see a table that lists all the faculty at that university that are associated with that keyword and their respective scores for how relevant that keyword is to them.

### Widget 5: Search Professor
Enter a professor's name (exact spelling and casing) and click the "View Professor" button to see general information about a professor including name, position, email, phone, university they're affiliated with, all keywords relevant to them, and a photo of them.

### Widget 6: Universities You're Interested in
Enter a university's name (exact spelling and casing) and click the "Add University" button to add it to the table of universities you're interested in; newly added universities are automatically ranked last on your list. To remove a university you're no longer interested in, you can click the "X" to the left of the row to delete it (this also removes all professors at that university that you are following in Widget 7). To view professors you are following at a university you're interested in for Widget 7, click the circle to the left of the row. To change a university's ranking, you can double click its cell of its rank in the "Rank" column to edit the university's rank by entering in a number. Changing a university's rank will preserve the order of all the other universities but insert the modified university at its new rank. If the entered rank is less than 1 or greater than the lowest ranked university, then the modified university will be inserted at 1st or last place respectively.

### Widget 7: Professors You're Interested in at Universities You're Following
**NOTE: You MUST select a university in Widget 6 in order to view tables in this widget and perform any operations.** Once you've selected a university, you can add a professor you want to follow and a research topic for them (both must be provided) by entering in the professor's name and the keyword (exact spelling and casing) into the search fields and clicking the "Add Professor" button. The professor you add must be a faculty member of the selected university. To remove a professor you're no longer want to follow, you can click the "X" to the left of the row to delete it. To change the research topic attached to a professor you're following, you can double click the cell of the keyword in the "Research Interest" column and enter a new keyword to change it. The new keyword must be a keyword that is relevant to the professor in question.

## Design
The overall architecture and design of the Hot Topic application can be broken down into 4 key components (5 if you count the databases themselves): the database connection manager, the database querying utility functions, the Dash callback functions, and the main Dash application.

First, the database connection manager is basically a singleton object that creates and stores the database connections for our three databases: MySQL, MongoDB, and Neo4j. Next, the database querying utility functions serve as our way of talking to the databases by using the database connections set up by the database connection manager and implementing functions that make specific queries on each of these connections. Then, we have the Dash callback functions which call the database querying utility functions to perform queries whenever specific HTML components on the dashboard are interacted with. These callback functions essentially perform the business logic for our application that modifies the databases and retrieves data from them to serve to the user. And finally, the main Dash application defines the frontend of our application using Dash HTML objects and the Plotly graphing library to convert data from the callback functions to a visualization that is more user-friendly.

In summary, the architecture of the application and flow of data is very linear and looks something like this:

**Databases (MySQL, MongoDB, Neo4j)** <--> **Database Connection Manager** <--> **Database Querying Utilities** <--> **Callbacks** <--> **Dash Application**

So when a user performs an action on the Dash application, a callback is triggered and the appropriate database utility function is called. The utility function then makes a query through the connections handled by the database connection manager, and the database executes the query accordingly. If the callback also sent any queries upstream that request data to be returned, then the database will retrieve the data and send that back downstream until it reaches the Dash application and is served to the user.

## Implementation
To implement the application, I used MySQL, MongoDB, and Neo4j databases with the AcademicWorld dataset to hold all the pertinent data for the dashboard. The application itself uses the sqlalchemy, pymongo, and neo4j libraries to establish the database connections and provide the APIs for querying them, the plotly library and dash framework to implement the actual dashboard and its components, and the pandas library to convert database query results to data frames usable by plotly and dash. This was all done using Python written with Jupyter Notebook.

Going back to the **Design** section, below is a short, technical summary on each of the components I implemented to supplement my application.

### Database Connection Manager
The DatabaseConnectionManager() class is a singleton class that creates database connections and stores them as self attributes. It's implemented in `db_connection_manager.py` and its purpose is to hide information about our connections to the three databases: MySQL, MongoDB, and Neo4j, spin up and manage connections to said databases, and ensure that the same connections are used over the lifetime of our application. It uses sqlalchemy to connect to MySQL, pymongo to connect to MongoDB, and neo4j to connect to Neo4j. Calling the setter functions of an instance of the class will set up the database connections accordingly, and using the getter functions, you can retrieve the connections to execute queries on them. `db_connection_setup.py` is where I instantiate this database connection manager object and where I import the connections to be used for querying the databases from for the rest of the application.

### Database Querying Utility Functions
These functions are divided into three separate files (`mysql_utils.py`, `mongodb_utils.py`, and `neo4j_utils.py`) according to which database the functions are querying and import the connection to that database from the `db_connection_setup.py` respectively. Each file has three major components: the helper functions for executing general queries on databases as well as converting database query results to pandas DataFrame() objects, functions that use the helpers for executing specific queries to get data used for the dashboard application, and formatted query strings to be used for parameterized queries (to sanitize queries and protect against injection attacks) for the query-specific functions just mentioned.

### Dash Callback Functions
The Dash application callback functions in `callbacks.py` are the primary consumer of the **database querying utility functions**, and is responsible for executing business logic when a user uses the application and serving data to the Dash application to make it responsive. Basically, for each widget of our Dash application, we define a callback function in `callbacks.py`, and when an action is performed on a widget on the HTML components that the callback functions target, a callback is triggered and performs the appropriate logic to insert, delete, update, or retrieve data from the databases via the **database querying utility functions**, and returns data to the application through the targeted HTML components to be served to the user.

### Dash Application
The main Dash application stored in `app.py` is where we intialize, define the layout for, and start the Dash application. The layout for it is organized using various Dash HTML objects which use Dash tables and Plotly graphing tools to convert pandas DataFrames to a more consumable representation in our final application. For the Dash components that will display data in the final application, we assign IDs to them so that the callback functions in `callbacks.py` can target these components as either inputs to trigger the callback on or outputs to return data to, which is how the application monitors changes or actions peformed on the widgets and displays data to our dashboard reactively.

### Styling
I also implemented CSS styling classes in a file called `dashboard.css` which is stored in a directory called `assets`. Dash conveniently applies any CSS styling defined in an `assets` directory, and to organize which HTML elements receive which styling class, you can set the *className* parameter to the name of the styling class on the Dash HTML object for that element.

## Database Techniques
The database techniques I've implemented are `CONSTRAINT`, `TRIGGER`, `STORED PROCEDURE`, and `TRANSACTION`. I did this by introducing two new tables to the AcademicWorld dataset called `university_picks` and `professor_university_pick` which are used to allow users to track universities they're interested in and professors at those universities that they are interested in. To make the utilization of these techniques more interesting, I even introduced a problem to solve through the use of SQL's capabilities by enabling users to rank universities they're interested in. Because the ranking has to be comprised of a set (no duplicates) of consecutive integers starting with 1, you can imagine what kind of issues arise when you allow users to change the rank of individual universities and delete universities from the `university_picks` table. Namely, changing the rank of a university means the order of the ranking must be updated, and deleting a university leaves a gap which also means the ranking must be updated (only if the target university isn't the last place one in both cases). I explain how I've implemented these techniques for these tables and why below. 

Note: All of these techniques I've applied can be seen in the `stored_procedures.txt` file.

### Constraint
The constraints I use for these two tables are the `FOREIGN KEY` constraint and `UNIQUE` constraint. The `university_picks` table stores an `id` attribute, which is a foreign key that references the `id` attribute of the `university` table, and a `ranking` attribute, which is a nullable integer with the unique constraint applied to it, because again, the ranking must be a set (no duplicates) of consecutive integers starting with 1. The `professor_university_pick` table has the attributes `university_id`, `professor_id`, and `keyword_id` which are foreign keys that reference the `id` attributes in the `university_picks`, `faculty`, and `keyword` tables respectively. For all of the above foreign keys, it makes sense to use this constraint because these attributes are the primary keys in other tables and all of them are set to `CASCADE` upon update and delete, because we assume that any changes to the original table should be reflected in these table. For instance, the `university_id` attribute references the `id` attribute in `university_picks` which references the `id` attribute in `university` thereby creating this chain. If a user removes a university they're no longer interested in from the `university_picks` table, the deletion will cascade to all of the professors they are following for that university in the `professor_university_pick` table, because logically they can't be interested in researching under professors at universities they're not interested in attending. Furthermore, if a university is deleted from the `university` table, we assume this university is off the table, so we cascade this deletion to `university_picks` which cascades to the `professor_university_pick` table because it's no longer an option.

### Stored Procedure
Both tables have one widget each that operate on them through updating, inserting, deleting, and querying, and every operation performed is done through a stored procedure. My rationale for using stored procedures here is because these are queries tied to fixed functionalities on the widgets so these database operations are going to be repeated again and again by the user interacting with the dashboard, so its nicer to have these long SQL statements stored for repeated usage and the shorter syntax, especially because most of the stored procedures contain transactions where multiple SQL statements are being executed.

### Transaction
Most of the stored procedures contain a transaction. In particular, the ones with multiple SQL statements being executed are placed in transactions, since the use case for transactions is to package up statements that are meant to be executed in succession to create a single unit. I will admit not all of the stored procedures that have transactions need them, since some of them only have a single statement that modify the database with the rest being innocuous `SELECT` statements. However, it is imperative for the procedures that affect the university rankings to be placed in transactions, because they have multiple statements that modify the database and we can leverage the other advantage of transactions: being able to rollback or commit changes depending on if every the SQL statement executes successfully or not.

As mentioned before, if a user changes a university's rank or deletes a university of from `university_picks`, then the ranking of universities must be reordered accordingly if it is no longer a clean set of consecutive integers starting with 1. Since I have SQL do the work in maintaining the rankings, the process for updating them is something like this. If a university has its rank changed, it must have its rank first set to `NULL`, since I can't directly set its rank to the new rank as another university might be occupying that rank and the unique constraint on this attribute doesn't allow duplicates. Then we have to both make space for insertion of the university at its new rank while simulateously closing the "gap" that the university's change-of-rank is leaving behind, which means we decrement or increment other unversities' ranks accordingly. After we've successfully vacated the university's new rank and changed the ranking to ensure it still meets the "set of consecutive integers..." requirement, we can then update the university's rank from `NULL` to its new rank. Deletion of a university is a similar process, except in that instance, we are only closing the gap in ranking that the university leaves behind.

The main point here is that, if at any point during this process of updating the rankings and performing any sort of database modifications a `SQLEXCEPTION` is thrown, then one of the SQL statements has likely failed. However, if some of the SQL statements with side effects already successfully executed, then this could present a problem if the changes made to the database are allowed to persist without the transaction in its entirety being successfully executed. The work is only "half done" so to speak. This is where the nice design pattern of using `ROLLBACK` or `COMMIT` depending on if every statement in the transaction is successful is really nice, because we can make it so that all changes made in the transaction are rolled back upon a `SQLEXCEPTION` being raised, which is how I've implemented the transactions in the stored procedures for this application.

### Trigger
Originally, I wrote a trigger that was intended to be a catch-all solution to updating university rankings when a university is deleted from the `university_picks` table. However, I learned that `CASCADE` on deletion for foreign keys does not cause triggers to fire, and also that SQL doesn't allow you to update the table in a trigger that the original action that caused the trigger to fire is operating on. So now, we have an issue here for how to update university rankings if a university is deleted from the `university` table, causing a row in `university_picks` to be deleted. My solution here was to write a trigger that handles updating the rankings if a deletion is made on the `university` table, while a stored procedure with a transaction handles updating the rankings when a university is deleted from `university_picks` by the user. That way, both scenarios for how a university is removed from `university_picks`, either by user input or through `CASCADE`, are covered. The logic in this trigger I implemented follows the same logic for updating university rankings that I outlined above in **Stored Procedure**.

## Extra-Credit Capabilities
I'm not sure if this counts as multi-database querying, but I use MongoDB to get a list of all the years that have a publication in the Academic World dataset and use them to populate a dropdown. The dropdown is then used to query SQL to get the top 10 keywords with the most publications in a given year. This is widget 1 which I've named **Top 10 Trending Keywords**.

## Contributions
I did the project on my own, so all me :P
