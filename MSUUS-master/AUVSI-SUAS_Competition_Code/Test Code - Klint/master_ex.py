import time
import random
import sqlite3
from insert_ex import *
from  change_ex import *

create_necessary()
counter = 0
conn = sqlite3.connect('test/tut.db')
c = conn.cursor()

while True:
    # Add Data
    name = 'image' + str(counter)
    counter += 1
    insert(name, 'False', random.randint(0,1), conn, c)
    print("Added Data")
    # Change Data
    if counter % 4 == 0:
        update_val(conn, c)
        print("Changed Data")
    time.sleep(0.25)
