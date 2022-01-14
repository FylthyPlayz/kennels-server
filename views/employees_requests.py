import sqlite3
import json
from models import Employee

EMPLOYEES = [
    {
      "id": 1,
      "name": "Jessica Younker",
      "email": "jessica@younker.com",
      "locationId": 2
    },
    {
      "id": 2,
      "name": "Jordan Nelson",
      "email": "jordan@nelson.com",
      "locationId": 2
    },
    {
      "id": 3,
      "name": "Zoe LeBlanc",
      "email": "zoe@leblanc.com",
      "locationId": 2
    },
    {
      "name": "Meg Ducharme",
      "email": "meg@ducharme.com",
      "locationId": 2,
      "id": 4
    },
    {
      "name": "Hannah Hall",
      "email": "hannah@hall.com",
      "locationId": 2,
      "id": 5
    },
    {
      "name": "Emily Lemmon",
      "email": "emily@lemmon.com",
      "locationId": 2,
      "id": 6
    },
    {
      "name": "Jordan Castelloe",
      "email": "jordan@castelloe.com",
      "locationId": 2,
      "id": 7
    },
    {
      "name": "Leah Gwin",
      "email": "leah@gwin.com",
      "locationId": 1,
      "id": 8
    },
    {
      "name": "Caitlin Stein",
      "email": "caitlin@stein.com",
      "locationId": 1,
      "id": 9
    },
    {
      "name": "Charisse Lambert",
      "email": "charisse@lambert.com",
      "locationId": 1,
      "id": 10
    },
    {
      "name": "Madi Peper",
      "email": "madi@peper.com",
      "locationId": 1,
      "id": 11
    },
    {
      "name": "Jenna Solis",
      "email": "jenna@solis.com",
      "locationId": 1,
      "id": 12
    }
]

def get_all_employees():
    # Open a connection to the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id
        FROM employee e
        """)

        # Initialize an empty list to hold all animal representations
        employees = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an employee instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Animal class above.
            employee = Employee(row['id'], row['name'], row['address'],
                            row['location_id'])

            employees.append(employee.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(employees)


# Function with a single parameter
def get_single_employee(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id
        FROM employee e
        WHERE e.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an customer instance from the current row
        employee = Employee(data['id'], data['name'], data['address'],
                            data['location_id'])

        return json.dumps(employee.__dict__)

def create_employee(employee):
    # Get the id value of the last employee in the list
    max_id = EMPLOYEES[-1]["id"]

    # Add 1 to whatever that number is
    new_id = max_id + 1

    # Add an `id` property to the employee dictionary
    employee["id"] = new_id

    # Add the employee dictionary to the list
    EMPLOYEES.append(employee)

    # Return the dictionary with `id` property added
    return employee

def delete_employee(id):
    # Initial -1 value for employee index, in case one isn't found
    employee_index = -1
    # Iterate the EMPLOYEES list, but use enumerate() so that you
    # can access the index value of each item
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            # Found the employee. Store the current index.
            employee_index = index
    # If the employee was found, use pop(int) to remove it from list
    if employee_index >= 0:
        EMPLOYEES.pop(employee_index)

def update_employee(id, new_employee):
    # Iterate the EMPLOYEES list, but use enumerate() so that
    # you can access the index value of each item.
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            # Found the employee. Update the value.
            EMPLOYEES[index] = new_employee
            break