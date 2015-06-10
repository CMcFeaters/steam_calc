#forms.py
'''this will store our forms'''
from flask_wtf import Form
#from wtforms import Form
from appHolder import db,app
from wtforms import TextField, BooleanField, IntegerField, DateField, FormField, SelectField, FieldList
from wtforms.validators import Required, ValidationError, Optional
import datetime


#build a form that reads the input from our character database 
#and generates entries for each value
class AttrRollForm(Form):
	#rollForm will be a standard roll value form.  it provides options to store a value
	#and then data for the number/quantity and base values for a dice roll
	value=TextField('value',validators=[Required()])
	nDice=SelectField('nDice',choices=[(1,"1"),(2,"2"),(3,"3"),(4,"4"),(5,"5")])
	nSides=SelectField('nSides',choices=[(6,'6'),(10,'10'),(20,'20'),(100,'100')])
	adder=TextField('adder')
			
class CharForm(Form):

	#NAMED TUPLES/GROUPS/OBJECTS SEEM TO BE THE WAY TO GO
	charName=TextField('charName',validators=[Required()])
	charAttrs=FieldList(FormField(AttrRollForm))
	
	def pop_attrs(self,args):
		for attr in args:
			self.charAttrs.append_entry()
	