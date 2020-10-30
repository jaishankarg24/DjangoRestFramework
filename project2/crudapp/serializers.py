from rest_framework import serializers
from crudapp.models import Employee

class EmployeeSerializers(serializers.Serializer):
	eno = serializers.IntegerField()
	ename = serializers.CharField(max_length=50)
	esalary = serializers.IntegerField()
	eaddress = serializers.CharField(max_length=50)

	def create(self, validated_data):
		return Employee.objects.create(**validated_data)

	def update(self, instance, validated_data):
		instance.eno = validated_data.get('eno', instance.eno)
		instance.ename = validated_data.get('ename', instance.ename)
		instance.esalary = validated_data.get('esalary', instance.esalary)
		instance.eaddress = validated_data.get('eaddress', instance.eaddress)
		instance.save()
		return instance