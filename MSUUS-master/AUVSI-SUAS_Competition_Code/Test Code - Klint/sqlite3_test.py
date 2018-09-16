# Code from a YouTube tutorial
# Tutorial at https://youtu.be/o-vsdfCBpsU
# Extra program is needed to actually view the db outside of a script

# All of the includes we're using. Not all of them are necessary for pure
# db, but give us values to use
import sqlite3
import time
import datetime
import random
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import style

# A random style for the graph that we output
style.use('fivethirtyeight')

# Opens a database 'tutorial.db'. Creates it if not already created
conn = sqlite3.connect('tutorial.db')

# This is a cursor object that we use to actually interact with the db
c = conn.cursor()


# This function creates a table and establishes our columns and what values those will take
def create_table():
    # 'IF NOT EXISTS' ensures that it will not keep creating the table if function runs multiple times
    # REAL, TEXT, and INTEGER are some of the valid variable types, REAL = decimal values
	c.execute('CREATE TABLE IF NOT EXISTS stuffToPlot(unix REAL, datestamp TEXT, keyword TEXT, value REAL)')

# Example function to insert in hard-coded data
def data_entry():
	c.execute("INSERT INTO stuffToPlot VALUES(12315654, '2016-01-01', 'Python', 5)")
	# Commit is the equivalent of 'save.' Needs to be done for changes to hold.
	conn.commit()

    # Cursors need to be closed before we close the db
	c.close()

    # Close our access to db
	conn.close()

# Example function of inserting in variables that aren't hard-coded
def dynamic_data_entry():
    # Establishing some variables
    unix = time.time()
    # Weird stuff at end is the format for date and time
    date = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H: %M: %S'))
    keyword = 'Python'
    value = random.randrange(0,10)

    # Insert those variables. '?' is unique to sqlite3
    c.execute("INSERT INTO stuffToPlot (unix, datestamp, keyword, value) VALUES (?, ?, ?, ?)",
              (unix, date, keyword, value))

    # Save the database
    conn.commit()

    # No close functions because we assume multiple runs of this function

# Reads data from the db
def read_from_db():
    # Pulls data from db, we can see where we specify specific columns to pull and their values
    c.execute("SELECT keyword, unix, value, timestamp FROM stuffToPlot WHERE value=3 AND keyword='Python'")

    # Next line stores all that pulled data into a variable called 'data'
    #data = c.fetchall()

    # Print it to see that it all shows up on one line as multiple lists in a list
    #print(data)

    # Alternate printing code. Each 'row' does represent one row of that database from the fetched data.
    for row in c.fetchall():
        print(row)

#
def graph_data():
    c.execute('SELECT datestamp, value FROM stuffToPlot')
    dates = []
    values = []
    for row in c.fetchall():
        #print(row[0])
        #print(datetime.datetime.fromtimestamp(row[0]))

        # Could not get this next line to work, so it's coded with a worthless value in the next line
        #dates.append(int(datetime.datetime.fromtimestamp(row[0])))
        dates.append(row[1] + 5)
        values.append(row[1])

    # These two lines display the plot of the data
    plt.plot_date(dates, values, '-')
    plt.show()

# Example function of removing data and changing values to existing data
def del_and_update():
    # At this point, we can tell that the actual db commands are inside the .execute() method as a string
    # that gets interpretted later on
    c.execute('SELECT * FROM stuffToPlot')

    # Example of a one row for loop. Needs Python3.
    #[print(row) for row in c.fetchall()]
    for row in c.fetchall():
        print(row)

    c.execute('UPDATE stuffToPlot SET value = 99 WHERE value=8')
    conn.commit()

    c.execute('DELETE FROM stuffToPlot WHERE value=99') # CAN'T LIMIT IN SQLITE3, CAN IN MYSQL
    conn.commit()

# This chunck of code was used to populate the db initially
# create_table()
# for i in range(10):
#     dynamic_data_entry()
#     time.sleep(1)
#     print('Write Successful')


# These are our function calls. Some were commented out while working through the tutorial
# read_from_db()
#graph_data()
del_and_update()
c.close()
conn.close()

# Currently our function doesn't actually put anything in the console, so I added this at one point to test.
print('Program Successful')