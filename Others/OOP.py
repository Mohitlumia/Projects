
class class1:
	
	def __init__(self, name, age):
		self.name1 = name 
		self.age1 = age
		# assigning two argument with object
		print('Print init')
	
	def method1(self, other):
		print('Print method1', self.name1)
		print('Print method1', other.name1)
	
	def method2(self, other):
		if self.age1 == other.age1:
			return True
		else:
			return False



object1 = class1('Mohit', 20)
object2 = class1('Rohan', 14)
 # argument self is the object it self
 # if we are not calling any method with 
 #object it calls automatically init method

object1.method1(object2)
print('\n')
if object1.method2(object2):
	print('same age')
else:
	print('different age')


class class2:
	class_variable = 10
	# class variable is a variable outside 
	# the init function and it can change
	# at once for all the objects
	def __init__(self):
		self.instance_variable = 20
	
	@classmethod
	def class_method(cls):
		# when we work with class variable we use cls
		#instead of self argument 
		print(cls.class_variable)
	
	@staticmethod
	def static_method():
		print('Print Static method')
	# static method do not take class or instance variable 


obj1 = class2
obj2 = class2
# Here for both objects instance variable 
# and class variable are 20 and 10 respectively
# we can change them for perticular object

obj1.class_variable = 30
obj1.instance_variable = 40
# by this we can change variable for one object 
# but if we want to change for all object we use
class2.class_variable = 30
# only class variable can be changed for all object at once
obj1.class_method()
# using decorator 
# class variable and class method belongs with every object that's why we first go with class then method while taking object as an argument 
obj1.static_method()

# class inside a class
class class3:
	
	def __init__(self, argument):
		self.class3_argument = argument
		self.inner_class = self.inner_class()
		
		
	def outer_method(self):
		print(self.class3_argument)
			
	class inner_class:
	
		def __init__(self, inner_argument):
			self.inner_class_argument = inner_argument
			
		def inner_method(self):
			print(self.inner_class_argumenprint





