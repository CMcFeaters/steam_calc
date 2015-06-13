'''#fileParse.py
#this program takes in a command line reference to a user file, 
#parses the data in that file and returns a narrative describing the
#file in piping terms
#
#The file will be  in the form of
#[O][name] [node1] [node2] [length]
#where O is the object type (P: pipe, V: valve)
#eventually more objects will be added
#eventually object characteristics will be added to the line to allow the lookup of
#data relevant to that object (i.e. pipe type data)
'''
import argparse

########################
#
#Need to add error checking to the program
#
########################


class Mesh():
	'''mesh class'
	the mesh class is an object where the file is converted to a mesh structure
	this class creates a network of pipe objects and node objects
	
	methods:
		assemble: this assembles the mesh from a file
		print: prints the mesh narrative to a command line
		out: outputs the narrative to a designated file
	'''
	def __init__(self,mFile):
		'''
			initiate the mesh, this function automatically assembles the mesh and returns any necessary errors 
			to the usre regarding the input file
			inputs: mFile- the file to be parsed and created
		'''
		self.mFile=mFile
		self.mArray=self.f_parse()
		self.nodes=[]
		self.pipes=[]
		self.m_assemble()
		
	def __repr__(self):
		'''
			self defined print function.  will output a narrative till more data is needed
		'''
		print(self.pipes)
		print(self.nodes)
		return ("I didn't have time to put on my face, I'm a mesh!")
	
	def f_parse(self):
		'''
			parses the file into an array usable by the m_assemble function
			input: file location
			output: mArray
		'''
		f=open(self.mFile,'r')
		mArray=[]
		
		for line in f.readlines():
			mArray.append([item.strip() for item in line.split(" ") if item!=""] )	#remove excess whitespace and any escape characters tab, endline, etc
		return mArray
		
	
	def m_assemble(self):
		''''
			this assembles the mesh based on the existing self.mArray
			Input: none (self.mArray)
			outpute: none, modifies self.nodes and self.pipes to match the current input file
		'''

		#find and create the pipes in the mesh
		for line in self.mArray:
			if line[0][0].lower()=='p':
				self.pipes.append(Pipe(line[0].lower().replace('p','',1),line[1],line[2],line[3]))
		
		#find and create the nodes in mesh
		for pipe in self.pipes:
			#if pipe.n1 does not exist, create it
			#if ipipe n2 does not exist, create it
			#if pipe n1 exists, add 1 to the node counter
			#if pipie n2 exists, add 1 to the node counter
			for n in [pipe.n1,pipe.n2]:
				if self.find_obj(n):
					self.get_obj(n).nObjs+=1
					self.get_obj(n).conObjs.append("Pipe {}".format(pipe.name))
				else:
					self.nodes.append(Node(n,1,["Pipe {}".format(pipe.name)]))
				

		
	def find_obj(self,num):
		'''
			a funcitno that searches through all of its nodes to determine if a nod already exists
			in: node number
			out: true/false depending on existnece
		'''
		if len([node for node in self.nodes if node.num==num])>0: return True
		else: return False
		
		
	def get_obj(self,criteria,type='n'):
		'''
			a funcitno that searches through all of its nodes and returns the node equal to the node num
			in: criteria to search for and  the type of object to search for
			out: object type (n=node, p=pipe)
		'''
		if type=='n':
			return [node for node in self.nodes if node.num==criteria][0]
		elif type=='p':
			return [pipe for pipe in self.pipes if pipe.name==criteria][0]

		
	def f_out(self,outFile):
		'''
			prints to an output file
		'''
		pass

class Pipe():
	'''the pipe class
	this class will have allof our pipe data
	a pipe has a start node, an end node and  a length'''
	def __init__(self,name,n1,n2,length=0):
		self.name=name
		self.n1=n1
		self.n2=n2
		self.length=length
		
	def __repr__(self):
		return ("I'm pipe %s  N1: %s  N2: %s  Length: %s"%(self.name,self.n1,self.n2,self.length))

class Valve():
	'''
		the valve class
		this is a nother type of item in the line
		has a name, valve type, an array of nodes and a status (optional)
	'''
	
	def __init__(self,vName,vNodes,vStatus=""):
		self.vName=vName
		self.vNodes=vNodes	
		self.vStatus=vStatus
	
	def __repr__(self):
		return ("I'm a valve.  my nodes are {}, my status is {}".format(self.vName,self.vNodes,self.vStatus))
		
class Node():
	'''
		this is the node class
		each node has a name(number), the number of pipes connecting to it and a list of connected pipe names
	'''
	
	def __init__(self,num,nObjs=0,conObjs=[]):
		self.num=num
		self.nObjs=nObjs
		self.conObjs=conObjs
		
	def  __repr__(self):
		return("I'm node {}.  I connect {} objects, the objects are {}".format(self.num,self.nObjs,self.conObjs))
		


def create_parser():
#this function creates the parser based on user input

#input:  none
#output: parse object
	parser=argparse.ArgumentParser(description="Enter a filename to have it parsed into a piping model")
	parser.add_argument("fileName",help="the name of a file (default active directory)")
	parser.add_argument("-o","--outFile",help="the name of an output file (default active directory)")
	
	return parser
	
	
if __name__ == "__main__":
	
	parser=create_parser()
	args=parser.parse_args()
	
	print ("Your file: "+(args.fileName))
	mesh=Mesh(args.fileName)
	print(mesh)