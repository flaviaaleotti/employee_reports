import sqlite3

conn = sqlite3.connect('reports.db')
cursor = conn.cursor()

# Create a table and insert some sample data
cursor.execute('''
    DROP TABLE IF EXISTS reports''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        employee_username TEXT,
        priority TEXT,
        CHECK (priority in ('high', 'low'))
    )
''')
cursor.execute('INSERT INTO reports (id,\
                                     title,\
                                     description,\
                                     employee_username,\
                                     priority) VALUES (?, ?, ?, ?, ?)',\
                                    (1,\
                                     'Project XXX report',\
                                     'Information about the progresses made in the development of web project XXX',\
                                     'fmare',\
                                     'low',))
cursor.execute('INSERT INTO reports (id,\
                                     title,\
                                     description,\
                                     employee_username,\
                                     priority) VALUES (?, ?, ?, ?, ?)',\
                                    (2,\
                                     'Productivity report',\
                                     'Productivity of employee Lorenzo Bebi is too low!',\
                                     'lbebi',\
                                     'high',))
cursor.execute('INSERT INTO reports (id,\
                                     title,\
                                     description,\
                                     employee_username,\
                                     priority) VALUES (?, ?, ?, ?, ?)',\
                                    (3,\
                                     'Productivity report',\
                                     'Productivity of employee Flavia Aleotti is so high!',\
                                     'faleotti',\
                                     'high',))
cursor.execute('INSERT INTO reports (id,\
                                     title,\
                                     description,\
                                     employee_username,\
                                     priority) VALUES (?, ?, ?, ?, ?)',\
                                    (4,\
                                     'Mission report',\
                                     'Report on the last mission (July 2023)',\
                                     'mpapi',\
                                     'low',))
cursor.execute('INSERT INTO reports (id,\
                                     title,\
                                     description,\
                                     employee_username,\
                                     priority) VALUES (?, ?, ?, ?, ?)',\
                                    (5,\
                                     'Productivity report',\
                                     'Productivity of employee Laura Relli is good',\
                                     'lrelli',\
                                     'low',))
cursor.execute('INSERT INTO reports (id,\
                                     title,\
                                     description,\
                                     employee_username,\
                                     priority) VALUES (?, ?, ?, ?, ?)',\
                                    (6,\
                                     'New report',\
                                     'Some new information',\
                                     'lrelli',\
                                     'low',))
cursor.execute('INSERT INTO reports (id,\
                                     title,\
                                     description,\
                                     employee_username,\
                                     priority) VALUES (?, ?, ?, ?, ?)',\
                                    (7,\
                                     'Coffee time',\
                                     'Employees request more time for coffe break',\
                                     'faleotti',\
                                     'high',))
cursor.execute('INSERT INTO reports (id,\
                                     title,\
                                     description,\
                                     employee_username,\
                                     priority) VALUES (?, ?, ?, ?, ?)',\
                                    (8,\
                                     'New report',\
                                     'new report needed to reach ore than 10 low-priority reports',\
                                     'lbebi',\
                                     'low',))
cursor.execute('INSERT INTO reports (id,\
                                     title,\
                                     description,\
                                     employee_username,\
                                     priority) VALUES (?, ?, ?, ?, ?)',\
                                    (9,\
                                     'New report',\
                                     'new report needed to reach ore than 10 low-priority reports',\
                                     'mpapi',\
                                     'low',))
cursor.execute('INSERT INTO reports (id,\
                                     title,\
                                     description,\
                                     employee_username,\
                                     priority) VALUES (?, ?, ?, ?, ?)',\
                                    (10,\
                                     'New report',\
                                     'new report needed to reach ore than 10 low-priority reports',\
                                     'mpapi',\
                                     'low',))
cursor.execute('INSERT INTO reports (id,\
                                     title,\
                                     description,\
                                     employee_username,\
                                     priority) VALUES (?, ?, ?, ?, ?)',\
                                    (11,\
                                     'New report',\
                                     'new report needed to reach ore than 10 low-priority reports',\
                                     'lbebi',\
                                     'low',))
cursor.execute('INSERT INTO reports (id,\
                                     title,\
                                     description,\
                                     employee_username,\
                                     priority) VALUES (?, ?, ?, ?, ?)',\
                                    (12,\
                                     'New report',\
                                     'new report needed to reach ore than 10 low-priority reports',\
                                     'faleotti',\
                                     'low',))
cursor.execute('INSERT INTO reports (id,\
                                     title,\
                                     description,\
                                     employee_username,\
                                     priority) VALUES (?, ?, ?, ?, ?)',\
                                    (13,\
                                     'New report',\
                                     'new report needed to reach ore than 10 low-priority reports',\
                                     'faleotti',\
                                     'low',))
cursor.execute('INSERT INTO reports (id,\
                                     title,\
                                     description,\
                                     employee_username,\
                                     priority) VALUES (?, ?, ?, ?, ?)',\
                                    (14,\
                                     'New report',\
                                     'new report needed to reach ore than 10 low-priority reports',\
                                     'lrelli',\
                                     'low',))
cursor.execute('INSERT INTO reports (id,\
                                     title,\
                                     description,\
                                     employee_username,\
                                     priority) VALUES (?, ?, ?, ?, ?)',\
                                    (15,\
                                     'New report',\
                                     'new report needed to reach ore than 10 low-priority reports',\
                                     'lrelli',\
                                     'low',))

conn.commit()
conn.close()