#!/bin/python

import sqlite3

conn = sqlite3.connect('test.db')
print 'Success, connected to database'

conn.execute('''CREATE TABLE user
    (USERNAME TEXT  PRIMARY KEY    NOT NULL,
     PASSWORD   TEXT    NOT NULL,
     EMAIL  TEXT    NOT NULL,
     ADMIN_RIGHTS  BOOLEAN  NOT NULL,
     TIMER_NAME TEXT NULL,
     TIMER_START_TIME TEXT NULL,
     TIMER_MINUTES INT NULL
    );'''
)
print 'Table created successfully'

conn.close()
