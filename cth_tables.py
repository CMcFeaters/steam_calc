#cth_tables.  
#the creation page for the call of cthulhu table database

from appHolder import db
import datetime, inspect, types
import sys, string, os

class testClass(db.Model):
	'''test class will have 2 storable values
	'''
	__tablename__="chars"
	#values
	id=db.Column(db.Integer,primary_key=True)
	test1=db.Column(db.Integer)
	test2=db.Column(db.Integer)
	
		
	'''account class'''
	def __init__(self,test1=0,test2=0):
		self.test1=test1
		self.test2=test2
		
	