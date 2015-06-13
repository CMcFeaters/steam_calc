'''THis is to establish the basic functions of the cahracter builder
hte first things it will do will be display a webpage that allows you to generate
random numbers into a box.  this will be done by clikcing a button'''

import random

def dGen(nDice=1,nSides=6,adder=0):
	'''dice generator, defaults to rolling 1 6 sided die'''
	#to iterate is human, to recuse is divine
	if nDice==0:
		return adder
	else:
		return random.randrange(1,nSides)+dGen(nDice-1,nSides,adder)
		
if __name__=="__main__":
	print(dGen(1,50))
	print(dGen(2,50))
	print(dGen(1,10))
	print(dGen(1,6,100))