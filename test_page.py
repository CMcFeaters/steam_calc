#test_page to establish some basic functionality for the caharacter builder
#_X_step 1 roll a dice
#_X _step two roll multiple dice
#step 3 roll  once times to fill in multiple entries with different rolls
#step 4 roll  once to fill in multiple entries then roll once to change an entry


from appHolder import db, app
from cth_tables import testClass
import cth_forms
from testwork import dGen
import datetime
import re
from flask import Flask, render_template,redirect,url_for, flash, request, session


@app.route('/')
def welcome():
	#creates a blank text box for a dice rolling test
	#setup tables
	#create a new DB entry
	#CREATE THE TABLES
	return render_template("welcome.html")

@app.route('/charMod',methods=['GET','POST'])
def charMod():
	#create a blank new character
	if request.method!="POST":
		#create a new characters
		#nChar=testClass()
		#db.session.add(nChar)
		#create a blank form
		cForm=cth_forms.CharForm()
		print(cForm.charName)
		print(cForm.charAttrs)
		cForm.pop_attrs(['STR','DEX'])
		print(cForm.charAttrs)
		return render_template('char_Page.html',cForm=cForm)
	'''else:
		# a new form is not being created.  we will either update all of the values
		#Or just the value being re-rolled
		dForm=cth_forms.attrForm()
		#errors start here when you press the button
		if request.form['roll']=="RollAll":
			for thing in dForm:
				thing.data=dGen()
		else:
			dForm[request.form['roll']].data=dGen()
		#render template
		return render_template('char_Page.html',form=dForm)'''
	
	
if __name__=='__main__':
	db.create_all()
	app.run()