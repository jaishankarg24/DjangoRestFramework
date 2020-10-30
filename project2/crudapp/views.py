from django.shortcuts import render
import io
from rest_framework.parsers import JSONParser
from crudapp.serializers import EmployeeSerializers
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from crudapp.models import Employee
from django.views.generic import View 
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name = 'dispatch')
class EmployeeCrudOperation(View):

	#post method to create resource
	def post(self, request, *args, **kwargs):
		json_data = request.body

		#Converting Json data into Python Dictionary --> DESERIALIZATION
		stream = io.BytesIO(json_data)
		python_data = JSONParser().parse(stream)

		#converting Python Dictionary into database code
		employee_serializer = EmployeeSerializers(data = python_data)
		if employee_serializer.is_valid():
			employee_serializer.save()
			msg = {'msg':'Record created/Added successfully'}
			json_data = JSONRenderer().render(data = msg)
			return HttpResponse(json_data, content_type = 'application/json')
		
		json_data = JSONRenderer().render(employee_serializer.errors)
		return HttpResponse(json_data, content_type = 'application/json', status = 400)

	#method to return employee object
	def get_object_data_by_id(self, id):
		try:
			employee = Employee.objects.get(id = id)
		except Employee.DoesNotExist:
			employee = None
		return employee

	#get method to select resource
	def get(self, request, *args, **kwargs):
		json_data = request.body

		#Converting Json data into Python Dictionary---> DESERIALIZATION
		stream = io.BytesIO(json_data)
		python_data = JSONParser().parse(stream)

		id = python_data.get('id', None)
		if id is not None:
			employee = self.get_object_data_by_id(id)
			if employee is None:
				msg = {'msg':'Record is not available for the id provided'}
				json_data = JSONRenderer().render(msg)
				return HttpResponse(json_data, content_type = 'application/json')

			emp = Employee.objects.get(id = id)
			#converting Python Dictionary into database code
			employee_serializer = EmployeeSerializers(emp)
			json_data = JSONRenderer().render(data = employee_serializer.data)
			return HttpResponse(json_data, content_type='application/json')

		query_string = Employee.objects.all()
		employee_serializer = EmployeeSerializers(query_string, many = True)
		json_data = JSONRenderer().render(data = employee_serializer.data)
		return HttpResponse(json_data, content_type='application/json')

	#patch method to update partial data
	def patch(self, request, *args, **kwargs):
		json_data = request.body

		#Converting Json data into Python Dictionary--->DESERIALIZATION
		stream = io.BytesIO(json_data)
		python_data = JSONParser().parse(stream)

		id = python_data.get('id')
		if id is not None:
			employee = self.get_object_data_by_id(id)
			if employee is None:
				msg = {'msg':'Record is not available for the id provided, update not possible'}
				json_data = JSONRenderer().render(msg)
				return HttpResponse(json_data, content_type = 'application/json')

			emp = Employee.objects.get(id = id)

			# perform Deserialization
			#convert Python Dictionary into Database code
			employee_serializer = EmployeeSerializers(emp, data = python_data, partial = True)
			if employee_serializer.is_valid():
				employee_serializer.save()
				msg={'msg':'Resource Updated successfully'}
				json_data = JSONRenderer().render(msg)
				return HttpResponse(json_data, content_type = 'application/json')

			json_data = JSONRenderer().render(employee_serializer.errors)
			return HttpResponse(json_data, content_type = 'application/json')

	#put method to update complete data for the provided id	
	def put(self, request, *args, **kwargs):
		json_data = request.body
		#Converting Json data into Python Dictionary--->DESERIALIZATION
		stream = io.BytesIO(json_data)
		python_data = JSONParser().parse(stream)
		
		id = python_data.get('id')

		if id is not None:
			employee = self.get_object_data_by_id(id)
			if employee is None:
				msg = {'msg':'Record is not available for the id provided, update not successful.'}
				json_data = JSONRenderer().render(msg)
				return HttpResponse(json_data, content_type = 'application/json')

			emp = Employee.objects.get(id = id)

			# perform Deserialization
			#convert Python Dictionary into Database code
			employee_serializer = EmployeeSerializers(emp, data = python_data)
			if employee_serializer.is_valid():
				employee_serializer.save()
				msg={'msg':'Resource Updated successfully'}
				json_data = JSONRenderer().render(msg)
				return HttpResponse(json_data, content_type = 'application/json')

			json_data = JSONRenderer().render(employee_serializer.errors)
			return HttpResponse(json_data, content_type = 'application/json')

	#delete method to delete record
	def delete(self,request,*args,**kwargs):
		json_data = request.body

		#Converting Json data into Python Dictionary-----> Deserialization
		stream = io.BytesIO(json_data)
		python_data = JSONParser().parse(stream)

		id = python_data.get('id')
		if id is not None:
			employee = self.get_object_data_by_id(id)
			if employee is None:
				msg = {'msg':'Record is not available for the id provided, Deletion not possible.'}
				json_data = JSONRenderer().render(msg)
				return HttpResponse(json_data, content_type = 'application/json')

			emp = Employee.objects.get(id = id)

			emp.delete()

			msg = {'msg':'Resource Deleted successfully'}
			json_data = JSONRenderer().render(msg)
			return HttpResponse(json_data, content_type = 'application/json')
	



		