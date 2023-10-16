from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response
import sqlite3
import requests

app = Flask(__name__)

#########################################
### HTML TEMPLATES FOR USER INTERFACE ###
#########################################

# home page
@app.route('/')
def home():
    return render_template('homepage.html')

# search report page
@app.route('/filter_reports')
def filter_reports_page():
    return render_template('filter_reports.html')

# POST employee page
@app.route('/new_employee')
def new_employee_page():
    return render_template('POST_employee.html')

# POST report page
@app.route('/new_report')
def new_report_page():
    return render_template('POST_report.html')

# DELETE report page
@app.route('/del_report', methods=['GET', 'POST'])
def del_report_page():
    #code to execute after the user presses "Delete"
    if request.method == 'POST':
        report_id = request.form.get('report_id')
        if not report_id:
            return "Invalid report ID", 400

        result = delete_report(int(report_id))
        return result

    #code to execute at first call
    return render_template('DELETE_report.html')

# DELETE employee page
@app.route('/del_employee', methods=['GET', 'POST'])
def del_employee_page():
    #code to execute after the user presses "Delete"
    if request.method == 'POST':
        employee_username = request.form.get('employee_username')
        if not employee_username:
            return "Invalid employee username", 400

        result = delete_employee(employee_username)
        return result

    #code to execute at first call
    return render_template('DELETE_employee.html')

###########################################
### METHODS TO ACCESS THE FULL DATABASE ###
###########################################
'''following methods are not accessible through html interface'''

# full employee list
@app.route('/search/employees/all', methods=["GET"])
def list_all_employees():
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    all_employees = cursor.execute("SELECT * FROM employees;").fetchall()

    return jsonify(all_employees)

# full reports list
@app.route('/search/reports/all', methods=["GET"])
def list_all_reports():
    conn = sqlite3.connect('reports.db')
    cursor = conn.cursor()
    all_reports = cursor.execute("SELECT * FROM reports;").fetchall()

    return jsonify(all_reports)

#####################
### FILTER METHOD ###
#####################

#search employee by ID (for testing)
@app.route('/search/employees/id', methods=['GET'])
def get_employee_id():
    employee_id = request.args.get("id")
    conn = sqlite3.connect('employees.db') 
    cursor = conn.cursor()
    result = cursor.execute("SELECT * FROM employees WHERE id=?", (employee_id,)).fetchone()
    if result is not None:
        return jsonify(result)
    else:
        response = make_response(jsonify({"message": "Employee not found"}), 404)
        return response

#search report by ID (for testing)
@app.route('/search/reports/id', methods=['GET'])
def get_report_id():
    report_id = request.args.get("id")
    conn = sqlite3.connect('reports.db')
    cursor = conn.cursor()
    result = cursor.execute("SELECT * FROM reports WHERE id=?", (report_id,)).fetchone()
    if result is not None:
        return jsonify(result)
    else:
        response = make_response(jsonify({"message": "Employee not found"}), 404)
        return response

# filter reports by username or priority
@app.route('/search/reports', methods=['GET'])
def filter_reports():
    # define required page (1 by default) and page size
    page = request.args.get('page', default=1, type=int)
    page_size = 10
    # calculate offset for SQL query based on requested page
    offset = (page - 1) * page_size

    query_parameters = request.args
    username = query_parameters.get("username")
    priority = query_parameters.get("priority")
    query = "SELECT * FROM reports WHERE"
    to_filter = []

    if username and priority:
        query += ' employee_username=? AND priority=?'
        to_filter.append(username)
        to_filter.append(priority)
    elif username:
        query += ' employee_username=?'
        to_filter.append(username)
    elif priority:
        query += ' priority=?'
        to_filter.append(priority)

    query += " LIMIT 10 OFFSET ?"
    to_filter.append(offset)

    conn = sqlite3.connect('reports.db')
    cursor = conn.cursor()
    filtered_reports = cursor.execute(query, to_filter).fetchall()

    # calculate the total number of pages based on the total number of records
    query = "SELECT COUNT(*) FROM reports WHERE"
    to_filter = []
    if username and priority:
        query += ' employee_username=? AND priority=?'
        to_filter.append(username)
        to_filter.append(priority)
    elif username:
        query += ' employee_username=?'
        to_filter.append(username)
    elif priority:
        query += ' priority=?'
        to_filter.append(priority)
    total_records = cursor.execute(query, to_filter).fetchone()[0]
    # the following formula ensures that correct total number of pages is obtained
    # e.g: 39 gives 4 pages, also 40 gives 4 pages, but 41 gives 5 pages
    total_pages = (total_records + page_size - 1) // page_size

    # check that requested page is available
    if page > total_pages:
        return jsonify({"message": "Error: requested page {0} does not exist (last page = {1})".format(page, total_pages)}, 404)
    
    # write html page for results on-the-fly
    html_output =\
'''<!DOCTYPE html>
<html>
<head>
    <title>Filtered reports</title>
</head>
<style>
    h1 {
        font-family: 'Arial', sans-serif;
        font-size: 16px;
    }
    h2 {
        font-family: 'Arial', sans-serif;
        font-size: 16px;
    }
    h3 {
        font-family: 'Arial', sans-serif;
        font-size: 14px;
        font-weight:normal;
    }
    main {
        font-family: 'Arial', sans-serif;
        font-size: 14px;
        font-weight:normal;
    }
</style>
<body>
    <h1>Found reports:</h1>\n'''
    for record in filtered_reports:
        html_output += "\n<h2>Title: {0}<h2>".format(record[1])
        html_output += "\n<h3>ID: {0}<h3>".format(record[0])
        html_output += "\n<h3>employee: {0}<h3>".format(record[3])
        html_output += "\n<h3>priority: {0}<h3>".format(record[4])
        html_output += "\n<main>description: {0} <main>".format(record[2])
        html_output +="\n<br>"
    #add links for next page, prev page and home page
    string_for_next_page = "/search/reports?"
    string_for_prev_page = "/search/reports?"
    if priority and username:
        string_for_next_page += "priority={0}&username={1}&page={2}".format(priority, username, page+1)
        string_for_prev_page += "priority={0}&username={1}&page={2}".format(priority, username, page-1)
    elif priority:
        string_for_next_page += "priority={0}&page={1}".format(priority, page+1)
        string_for_prev_page += "priority={0}&page={1}".format(priority, page-1)
    elif username:
        string_for_next_page += "username={0}&page={1}".format(username, page+1)
        string_for_prev_page += "username={0}&page={1}".format(username, page-1)
    html_output += "\n<h2> Page {0} of {1}<h2>\n".format(page, total_pages)
    if page > 1:
        html_output += "<a href=\"{0}\" class=\"button\">Previous Page</a>\n".format(string_for_prev_page)
    if page < total_pages:
        html_output += "<a href=\"{0}\" class=\"button\">Next Page</a>\n".format(string_for_next_page)
    html_output += "<br>\n<a href=\"/\" class=\"button\">Home page</a>\n"
    html_output +=\
'''</body>
</html>'''
    with open('templates/filter_results.html', 'w') as htmlfile:
        htmlfile.write(html_output)

    return render_template('filter_results.html')

####################
### POST METHODS ###
####################

# add a new employee to database
''' (since we need at least one report per employee (in report database), a new default "First report"
     is created and posted to report.db whenever a new employee is created)'''
@app.route('/create/employees', methods=['POST'])
def create_new_employee_item():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        data = request.get_json()
    else:
        data = request.form

    first_name = data['first_name']
    last_name = data['last_name']
    username = data['username']
    email = data['email']
    gender = data['gender']
    title = data['title']
    department = data['department']

    # check that all required fields are passed
    for required_field in (first_name, last_name, username, email, gender, title, department):
        if not required_field:
            return jsonify({"message": "One or more mandatory fields missing!"}, 400)
    
    # try block is executed if username satisfies "UNIQUE" SQL requirement
    try:
        conn = sqlite3.connect('employees.db')
        cursor = conn.cursor()
    
        cursor.execute('INSERT INTO employees (first_name,\
                                           last_name,\
                                           username,\
                                           email,\
                                           gender,\
                                           title,\
                                           department) VALUES (?, ?, ?, ?, ?, ?, ?)',\
                                          (first_name,\
                                           last_name,\
                                           username,\
                                           email,\
                                           gender,\
                                           title,\
                                           department))
        conn.commit()
        #id of new generated item (automaltically set by SQL database)
        new_employee_id = cursor.lastrowid
        conn.close()
    
        #default first report (to be added in report database)
        default_report = {"title": "First report",\
                          "description": "First report on the new hired employee",\
                          "employee_username": username,\
                          "priority":"low"}
        conn = sqlite3.connect('reports.db')
        cursor = conn.cursor()
    
        cursor.execute('INSERT INTO reports (title,\
                                             description,\
                                             employee_username,\
                                             priority) VALUES (?, ?, ?, ?)',\
                                            (default_report["title"],\
                                             default_report["description"],\
                                             default_report["employee_username"],\
                                             default_report["priority"]))
        conn.commit()
        #id of new generated item (automaltically set by SQL database)
        new_report_id = cursor.lastrowid
        conn.close()
        
        if content_type == 'application/json':
            data['id'] = new_employee_id
            default_report['id'] = new_report_id
            return jsonify({'employee' : data, 'report' : default_report}, 200)
        else:
            return render_template('new_employee_added.html',\
                            message="New employee item has successfully been added to the database with a default report",\
                            new_employee_id=new_employee_id,\
                            new_report_id=new_report_id)
        
    
    # handle SQL error in case uniqueness of username is not satisfied
    except sqlite3.IntegrityError as e:
        conn.close()
        return jsonify({"message": "Error: Employee username must be unique."}, 400)

# add a new report to database
@app.route('/create/reports', methods=['POST'])
def create_new_report_item():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        data = request.get_json()
    else:
        data = request.form

    title = data['title']
    description = data['description']
    employee_username = data['employee_username']
    priority = data['priority']

    # check that all required fields are passed
    for required_field in (title, description, employee_username, priority):
        if not required_field:
            return jsonify({"message": "One or more mandatory fields missing!"}, 400)
    # check priority to avoid SQL error
    if priority not in ('high', 'low'):
        return jsonify({"message": "Priority must be either high or low"}, 400)

    # Check if the employee with the specified username exists
    conn_employees = sqlite3.connect('employees.db')
    cursor_employees = conn_employees.cursor()

    cursor_employees.execute("SELECT id FROM employees WHERE username = ?", (employee_username,))
    employee_id = cursor_employees.fetchone()

    conn_employees.close()
    
    if employee_id is not None:
        conn = sqlite3.connect('reports.db')
        cursor = conn.cursor()

        cursor.execute('INSERT INTO reports (title,\
                                             description,\
                                             employee_username,\
                                             priority) VALUES (?, ?, ?, ?)',\
                                            (title,\
                                             description,\
                                             employee_username,\
                                             priority))
        conn.commit()
        #id of new generated item (automaltically set by SQL database)
        new_id = cursor.lastrowid
        conn.close()

        if content_type == 'application/json':
            data['id'] = new_id
            return jsonify(data, 200)
        else:
            return render_template('new_report_added.html',\
                               message="New report item has successfully been added to database",\
                               username=employee_username,\
                               new_report_id=new_id)
    else:
        return jsonify({"message": "Employee not found"}, 400)

######################
### DELETE METHODS ###
######################

# delete report from database (using id)
@app.route('/delete/reports/<int:report_id>', methods=['DELETE'])
def delete_report(report_id):
    conn = sqlite3.connect('reports.db')
    cursor = conn.cursor()

    # Check if the report with the specified ID exists
    cursor.execute("SELECT * FROM reports WHERE id = ?", (report_id,))
    existing_report = cursor.fetchone()

    if existing_report:
        cursor.execute("DELETE FROM reports WHERE id = ?", (report_id,))
        conn.commit()
        conn.close()
        return render_template('deleted_output.html', id=report_id, message='')
    else:
        conn.close()
        return jsonify({"message": "Report not found", "id": report_id}, 404)

# delete employee (using username) and all related reports from database 
@app.route('/delete/employees/<string:username>', methods=['DELETE'])
def delete_employee(username):
    conn_employees = sqlite3.connect('employees.db')
    cursor_employees = conn_employees.cursor()

    # Check if the employee with the specified username exists
    cursor_employees.execute("SELECT * FROM employees WHERE username = ?", (username,))
    existing_employee = cursor_employees.fetchone()

    if existing_employee:
        # Delete the employee from the employees database
        cursor_employees.execute("DELETE FROM employees WHERE username = ?", (username,))

        conn_reports = sqlite3.connect('reports.db')
        cursor_reports = conn_reports.cursor()

        # Delete all reports related to the employee's ID
        cursor_reports.execute("DELETE FROM reports WHERE employee_username = ?", (username,))

        conn_employees.commit()
        conn_reports.commit()

        conn_employees.close()
        conn_reports.close()

        return render_template('deleted_output.html',\
                               message="all related reports have also been deleted",\
                               id=username)
    else:
        conn_employees.close()
        return jsonify({"message": "Employee not found"}, 404)

###################
### PUT METHODS ###
###################
''' following methods cen edit employee and report data (based on id, because it is the only field meant to be immutable)
in case the username field of an employee gets changed, the update_employee() method is designed to
edit the corresponding employee_username field in all the related reports.
The two following methods work from command line (curl) but not with html pages (not implemented yet)'''

# edit (update) fields of an existing employee (except id)
# if employee username is among the fields to edit, automatically update also report database
@app.route('/update/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    data = request.json

    conn_employees = sqlite3.connect('employees.db')
    # Set row factory to return rows as dictionaries (so that it is esier to serch for fields)
    conn_employees.row_factory = sqlite3.Row  
    cursor_employees = conn_employees.cursor()

    # Check if the employee with the specified ID exists
    cursor_employees.execute("SELECT * FROM employees WHERE id = ?", (employee_id,))
    existing_employee = cursor_employees.fetchone()

    if existing_employee:
        existing_username = existing_employee['username']

        # Create a list of fields to be updated
        fields_to_update = []
        for key, value in data.items(): 
            if key != 'id' and key in existing_employee.keys():
                fields_to_update.append((key, value))
            else:
                conn_employees.close()
                return jsonify({"message": "Invalid fields to update"}, 400)

        if fields_to_update:
            # Generate the SET clause for SQL
            set_clause = ', '.join(["{0} = ?".format(field[0]) for field in fields_to_update])
            values = [field[1] for field in fields_to_update]

            # Update the specified fields for the employee
            update_query = "UPDATE employees SET {0} WHERE id = ?".format(set_clause)
            values.append(employee_id)
            cursor_employees.execute(update_query, tuple(values))

            conn_employees.commit()
            conn_employees.close()

            if 'username' in data:
                # If 'username' was updated, update related reports in the reports.db database
                conn_reports = sqlite3.connect('reports.db')
                cursor_reports = conn_reports.cursor()

                cursor_reports.execute("UPDATE reports SET employee_username = ? WHERE employee_username = ?",
                                      (data['username'], existing_username))

                conn_reports.commit()
                conn_reports.close()

            return jsonify({"message": "Employee fields and related reports successfully updated"})
        else:
            conn_employees.close()
            return jsonify({"message": "No valid fields to update"}, 400)
    else:
        conn_employees.close()
        return jsonify({"message": "Employee not found"}, 404)

# edit (update) fields of an existing report (except id and employee_username)
@app.route('/update/reports/<int:report_id>', methods=['PUT'])
def update_report(report_id):
    data = request.json

    conn_reports = sqlite3.connect('reports.db')
    # Set row factory to return rows as dictionaries (so that it is esier to serch for fields)
    conn_reports.row_factory = sqlite3.Row  
    cursor_reports = conn_reports.cursor()

    # Check if the employee with the specified ID exists
    cursor_reports.execute("SELECT * FROM reports WHERE id = ?", (report_id,))
    existing_report = cursor_reports.fetchone()

    if existing_report:
        # Create a list of fields to be updated
        fields_to_update = []
        for key, value in data.items():  
            if key != 'id' and key != 'employee_username' and key in existing_report.keys():
                fields_to_update.append((key, value))
            else:
                conn_reports.close()
                return jsonify({"message": "Invalid fields to update"}, 400)

        if fields_to_update:
            # Generate the SET clause for SQL
            set_clause = ', '.join(["{0} = ?".format(field[0]) for field in fields_to_update])
            values = [field[1] for field in fields_to_update]

            # Update the specified fields for the employee
            update_query = "UPDATE reports SET {0} WHERE id = ?".format(set_clause)
            values.append(report_id)
            cursor_reports.execute(update_query, tuple(values))

            conn_reports.commit()
            conn_reports.close()

            return jsonify({"message": "Report fields successfully updated"})
        else:
            conn_employees.close()
            return jsonify({"message": "No valid fields to update"}, 400)
    else:
        conn_reports.close()
        return jsonify({"message": "Report not found"}, 404)


if __name__ == '__main__':
    app.run(debug=True)