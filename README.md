EMPLOYEES/REPORT DATABASE MANAGEMENT

This is a REST API written in Python to manage a database of employees and related reports
The app is ment to run locally with local databases that can easily be created via some Python scripts (see instruction below)

Requirements:
- Python 3.6 or + 
- Python modules: flask, sqlite3, requests, uuid, subprocess
- pytest for testing the app

any missing python module as well as pytest can be easily be installed with pip (e.g: pip install flask). Make sure you are using pip3 version.

The following setup instructions (as well as the launch of the Python API) are meant to be performed from a terminal.
After the app is launched and running, its functionalities can be accessed via browser (see instructions below) or via terminal (e.g. curl)

SETUP INSTRUCTIONS
Download the repository from github:

git clone https://github.com/flaviaaleotti/employee_reports.git)https://github.com/flaviaaleotti/employee_reports.git

and enter the employee_reports/ directory
Inside the repository, you will find two python scripts that will automatically generate two basic default SQL databases (for employees and related reports)
Genarate the employees.db and reports.db databases by running

python3 build_employees_database.py
python3 build_report_database.py

from terminal inside the employee_reports/ directory
The pre-generated databases employees.db and reports.db are already available in teh repository, but you can run the above scripts to reset the database to the starting records at anytime in the future.

Now you are ready to start the API! run from terminal

python3 RESTAPI.py

TESTING
Before using the API through your browser, you can test it with pytest in order to assess all endpoints.
To run the tests, open another terminal (leave the API running, otherwise all tests will fail), go to the employee_reports/ directory and simply type

pytest

you can also run the above pytest command  with -v option to increase verbosity if you want to check each single endpoint test.
If all tests are successfully passed, you can open your browser and start using the API!
REMEMBER that the API should be always kept running in order to use it, so make sure that you do not close the terminal where you have your 'python3 RESTAPI.py' command running :)





