import requests
import json
import sys

BASE_URL = 'http://127.0.0.1:8000/'
END_POINT = 'restapi/'


def create_data():
	eno = input('Enter the employee number :\t')
	ename = input('Enter the employee name :\t')
	esalary = input('Enter the employee salary :\t')
	eaddress = input('Enter the employee address :\t')

	emp_data = {
		 'eno': eno, 'ename': ename, 'esalary': esalary, 'eaddress': eaddress
	}

	response = requests.post(BASE_URL + END_POINT, data = json.dumps(emp_data) )
	print(response.status_code)
	print(response.json())

def select_data():
	data = {}
	id = int(input('Enter the id to Select resource: \t'))
	if id is not None:
		data = { 'id': id }
	response = requests.get(BASE_URL + END_POINT, data = json.dumps(data))
	print(response.json())
	print(response.status_code)


def select_complete_data(id = None):
	data = { 'id': id }
	response = requests.get(BASE_URL + END_POINT, data = json.dumps(data))
	print(response.json())
	print(response.status_code)

def update_partial_data():
	id = int(input('Enter the id : \t'))
	update_data =  {'id': id, 'esalary': 200000, 'eaddress': 'mysore'}
	response = requests.patch(BASE_URL + END_POINT, data = json.dumps(update_data))
	print(response.json())
	print(response.status_code)

def update_complete_data():
	id = input('Enter the id to update record :\t')
	eno = int(input('Enter the Employee Number :\t'))
	ename = input('Enter the Employee Name :\t')
	esalary = int(input('Enter the Employee salary  :\t'))
	eaddress = input('Enter the Employee address :\t')	

	update_data = { 'id': id, 'eno': eno, 'ename':ename, 'esalary': esalary, 'eaddress': eaddress}
	response = requests.put(BASE_URL + END_POINT , data = json.dumps(update_data))
	print(response.status_code)
	print(response.json())

def delete_data():
	id = int(input('Enter the id to delete record : \t'))
	emp_data = {'id': id }
	response = requests.delete(BASE_URL + END_POINT, data = json.dumps(emp_data))
	print(response.json())
	print(response.status_code)

def exit():
	sys.exit()

def invalidOption():
	print('please provide valid option(1-7)')
	

if __name__ == '__main__':

	while(1):
		print(''' 
			Please Select the below operation.
			1. Create the data.
			2. Select the data.
			3. Select Complete data.
			4. Update partial data.
			5. Update complete data.
			6. Delete the data.
			7. To Exit.
			 ''')

		choice = int(input('Enter your choice(number):'))

		options = {
			1: create_data,
			2: select_data,
			3: select_complete_data,
			4: update_partial_data,
			5: update_complete_data,
			6: delete_data,
			7: exit
		}
		options.get(choice, invalidOption)()

