#!/bin/python

import sqlite3

conn = sqlite3.connect('test.db')
print 'Success, connected to database'

conn.execute('''CREATE TABLE user
    (USERNAME TEXT  PRIMARY KEY    NOT NULL,
     PASSWORD   TEXT    NOT NULL,
     EMAIL  TEXT    NOT NULL
    );'''
    )
print 'Table created successfully'

conn.close()
