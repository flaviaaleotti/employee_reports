import sqlite3

conn = sqlite3.connect('employees.db')
cursor = conn.cursor()

# Create a table and insert some sample data
cursor.execute('''
    DROP TABLE IF EXISTS employees''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        username TEXT NOT NULL UNIQUE,
        email TEXT,
        gender TEXT,
        title TEXT,
        department TEXT
    )
''')
cursor.execute('INSERT INTO employees (id,\
                                       first_name,\
                                       last_name,\
                                       username,\
                                       email,\
                                       gender,\
                                       title,\
                                       department) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',\
                                      (1,\
                                       'Flavia',\
                                       'Mare',\
                                       'fmare',\
                                       'flavia.mare@company.com',\
                                       'F',\
                                       'junior developer',\
                                       'A'))
cursor.execute('INSERT INTO employees (id,\
                                       first_name,\
                                       last_name,\
                                       username,\
                                       email,\
                                       gender,\
                                       title,\
                                       department) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',\
                                      (2,\
                                       'Lorenzo',\
                                       'Bebi',\
                                       'lbebi',\
                                       'lorenzo.bebi@company.com',\
                                       'M',\
                                       'senior developer',\
                                       'A'))
cursor.execute('INSERT INTO employees (id,\
                                       first_name,\
                                       last_name,\
                                       username,\
                                       email,\
                                       gender,\
                                       title,\
                                       department) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',\
                                      (3,\
                                       'Massimo',\
                                       'Papi',\
                                       'mpapi',\
                                       'massimo.papi@company.com',\
                                       'M',\
                                       'CEO',\
                                       'B'))
cursor.execute('INSERT INTO employees (id,\
                                       first_name,\
                                       last_name,\
                                       username,\
                                       email,\
                                       gender,\
                                       title,\
                                       department) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',\
                                      (4,\
                                       'Laura',\
                                       'Relli',\
                                       'rlaura',\
                                       'laura.relli@company.com',\
                                       'F',\
                                       'HR Manager',\
                                       'C'))

conn.commit()
conn.close()