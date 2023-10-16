import requests
import uuid
import subprocess

# endpoint (home page)
ENDPOINT = "http://localhost:5000"

# basic functions
def create_employee(employee_json):
    return requests.post(ENDPOINT + '/create/employees', json=employee_json)

def create_report(report_json):
    return requests.post(ENDPOINT + '/create/reports', json=report_json)

def get_employee(employee_id):
    return requests.get(ENDPOINT + '/search/employees/id?id={0}'.format(employee_id))

def get_report(report_id):
    return requests.get(ENDPOINT + '/search/reports/id?id={0}'.format(report_id))

def update_employee(employee_id, employee_json):
    return requests.put(ENDPOINT + '/update/employees/{0}'.format(employee_id), json=employee_json)

def update_report(report_id, report_json):
    return requests.put(ENDPOINT + '/update/reports/{0}'.format(report_id), json=report_json)

def delete_employee(employee_username):
    command = f'curl -X DELETE http://localhost:5000/delete/employees/{employee_username}'
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    return result

def delete_report(report_id):
    command = f'curl -X DELETE http://localhost:5000/delete/reports/{report_id}'
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    return result

def filter_reports(username='', priority=''):
    return requests.get(ENDPOINT + '/search/reports?username={0}&priority={0}'.format(username,priority))

# generate json for new employee with unique new username (random)
def new_employee_json():
    username = uuid.uuid4().hex
    return {'first_name' : 'test_name',\
            'last_name' : 'test_surname',\
            'username' : username,\
            'email' : 'test_email',\
            'gender' : 'F',\
            'title' : 'test_job_title',\
            'department' : 'T'\
            }

# TESTS
def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200

def test_can_list_all_employees():
    response = requests.get(ENDPOINT + '/search/employees/all')
    assert response.status_code == 200

def test_can_list_all_reports():
    response = requests.get(ENDPOINT + '/search/reports/all')
    assert response.status_code == 200

def test_filter_reports():
    # first we create an employee
    test_employee = new_employee_json()
    create_employee_response = create_employee(test_employee)
    assert create_employee_response.status_code == 200
    data = create_employee_response.json()
    username = data[0]['employee']['username']
    filter_reports_response = filter_reports(username=username, priority='low')
    assert filter_reports_response.status_code == 200

def test_can_create_employee():
    test_employee = new_employee_json()
    # test for employee creation
    create_employee_response = create_employee(test_employee)
    assert create_employee_response.status_code == 200
    data = create_employee_response.json()
    employee_id = data[0]['employee']['id']
    #verify success by retrieving result through id
    get_employee_response = get_employee(employee_id)
    assert get_employee_response.status_code == 200

def test_can_create_report():
    #to test the POST report method, we first need to create a test employee
    test_employee = new_employee_json()
    create_employee_response = create_employee(test_employee)
    assert create_employee_response.status_code == 200
    data = create_employee_response.json()
    employee_username = data[0]['employee']['username']
    test_report = {'title' : 'test_title',\
                   'description' : 'test_description',\
                   'employee_username' : employee_username,\
                   'priority' : 'high',\
                   }
    create_report_response = create_report(test_report)
    assert create_report_response.status_code == 200
    data_report = create_report_response.json()
    report_id = data_report[0]['id']
    #verify success by retrieving the high priority report just created
    get_report_response = get_report(report_id)
    assert get_report_response.status_code == 200

def test_can_update_employee():
    #to test the PUT employee method, we first need to create a test employee
    test_employee = new_employee_json()
    create_employee_response = create_employee(test_employee)
    assert create_employee_response.status_code == 200
    data = create_employee_response.json()
    employee_id = data[0]['employee']['id']
    #if employee was successfully created, we try to update it
    updated_employee = {'title' : 'NEW_test_job_title'}
    update_employee_response = update_employee(employee_id, updated_employee)
    assert update_employee_response.status_code == 200
    #if update was successful, we check by getting the employee and checking the new job title
    get_employee_response = get_employee(employee_id)
    assert get_employee_response.status_code == 200
    data_updated = get_employee_response.json()
    assert data_updated[-2] == updated_employee['title']

def test_can_update_report():
    #to test the PUT report method, we first need to create a test employee
    test_employee = new_employee_json()
    create_employee_response = create_employee(test_employee)
    assert create_employee_response.status_code == 200
    data = create_employee_response.json()
    #if employee was successfully created, we try to update its first report
    employee_username = data[0]['employee']['username']
    report_id = data[0]['report']['id']
    updated_report = {'title' : 'updated test title',\
                      'description' : 'test updated descritpion ',\
                      'priority' : 'low'\
                     }
    update_report_response = update_report(report_id, updated_report)
    assert update_report_response.status_code == 200
    get_report_response = get_report(report_id)
    assert get_report_response.status_code == 200
    data_updated = get_report_response.json()
    assert data_updated[1] == updated_report['title']
    assert data_updated[2] == updated_report['description']
    assert data_updated[4] == updated_report['priority']

def test_can_delete_employee():
    #first create a test employee
    test_employee = new_employee_json()
    create_employee_response = create_employee(test_employee)
    assert create_employee_response.status_code == 200
    data = create_employee_response.json()
    username = data[0]['employee']['username']
    employee_id = data[0]['employee']['id']
    delete_employee_response = delete_employee(username)
    assert delete_employee_response.returncode == 0
    get_employee_response = get_employee(employee_id)
    assert get_employee_response.status_code == 404

def test_can_delete_report():
    #first create a test employee
    test_employee = new_employee_json()
    create_employee_response = create_employee(test_employee)
    assert create_employee_response.status_code == 200
    data = create_employee_response.json()
    report_id = data[0]['report']['id']
    delete_report_response = delete_report(report_id)
    assert delete_report_response.returncode == 0
    get_report_response = get_report(report_id)
    assert get_report_response.status_code == 404



