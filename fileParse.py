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
		f_parse: parses the file lines into new arrays,  extracting necessary data types, results in mArray
		obj_assemble: assembles mArray into an array of objects
		node_assemble: assembles node from objects
		find_obj: finds a node and determines if it exists
		get_obj: returns an object
		f_out: will output array to a file
	
	members:
		mFile = the name of the file being parsed, assumed local directory
		mArray = an array of raw object data, used to create objects
		objects = an array of objects, created from mArray, used to create the nodes
		nodes = an array of nodes used in calcluations
	'''
	def __init__(self,mFile,oFile=""):
		'''
			initiate the mesh, this function automatically assembles the mesh and returns any necessary errors 
			to the usre regarding the input file
			inputs: mFile- the file to be parsed and created
		'''
		self.mFile=mFile
		self.mArray=self.f_parse()
		self.objects=self.obj_assemble()
		self.nodes=[]
		self.node_assemble()
		self.oFile=oFile
		
		
	def __repr__(self):
		'''
			self defined print function.  will output a narrative till more data is needed
		'''
		print(self.objects)	
		print(self.nodes)
		return ("I didn't have time to put on my face, I'm a mesh!")
	
	def f_parse(self):
		'''
			parses the file into an array usable by the m_assemble function
			input: file location
			output: mArray
		'''
		
		#parses the file array and  appends an object type to mArray
		f=open(self.mFile,'r')
		mArray=[]
		
		for line in f.readlines():
			tArray=[item.strip() for item in line.split(" ") if item!=""]
			tArray.insert(0,tArray[0][0].lower())
			mArray.append(tArray)	#remove excess whitespace and any escape characters tab, endline, etc
			
		f.close()
		return mArray
		
	def obj_assemble(self):
		'''
			uses the data in mArray to create an instance of each object class and appends it to oArray which becomes self.objects
			input: none (uses mArray)
			output: oArray, an array of objects created here
		'''
		
		#creates and puts each object in its specific array	
		oArray=[]
		#add any other object types here as needed
		for obj in self.mArray:
			if obj[0]=='p':
				#create pipe
				tObj=Pipe(obj[1],obj[2],obj[3],obj[4])
			elif obj[0]=='v':
				#create valve
				tObj=Valve(obj[1],obj[2],obj[3])
			oArray.append(tObj)
		return oArray
			
	def node_assemble(self):
		'''
			assembles a node array based on the current objects in its containers
		'''
		#build out each array
		for obj in self.objects:
		#create the nodes for the obj
			for node in [obj.n1,obj.n2]:
				if self.find_obj(node):
					self.get_obj(node).nObjs+=1
					self.get_obj(node).conObjs.append("{}".format(obj.name))
				else:
					self.nodes.append(Node(node,1,["{}".format(obj.name)]))
		
	def find_obj(self,num,type='n'):
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
		else:
			return [obj for obj in self.objects if obj.name==criteria][0]

		
	def f_out(self):
		'''
			prints to an output file
		'''
		print ("Outputing to file: {}".format(self.oFile))
		if self.oFile!=None:
			
			f=open(self.oFile,'w')
			f.truncate()
			for object in self.objects:
				print (str(object))
				f.write(str(object))
				f.write('\n')
			
			for node in self.nodes:
				f.write(str(node))
				f.write('\n')
				
			f.close()

class Object():
	'''
		basic object class
		has a name and 2 nodes
	'''
	
	def __init__(self,name,n1,n2):
		self.name=name
		self.n1=n1
		self.n2=n2
		 
	def __repr__(self):
		return ("I'm object {}.  I exist between these nodes: {}".format(self.name,[self.n1,self.n2]))
	
	def __str__(self):
		return("I'm object {}.  I exist between these nodes: {}".format(self.name,[self.n1,self.n2]))
		 
class Pipe(Object):
	'''the pipe class
	this class will have allof our pipe data
	a pipe has a start node, an end node and  a length'''
	def __init__(self,name,n1,n2,length=0):
		self.name=name
		self.n1=n1
		self.n2=n2
		self.length=length
		
	#def __repr__(self):
	#	return ("I'm pipe %s  N1: %s  N2: %s  Length: %s"%(self.name,self.n1,self.n2,self.length))

class Valve(Object):
	'''
		the valve class
		this is a nother type of item in the line
		has a name, valve type, an array of nodes and a status (optional)
	'''
	
	def __init__(self,name,n1,n2,vStatus=""):
		self.name=name
		self.n1=n1
		self.n2=n2
		self.vStatus=vStatus
	
	#def __repr__(self):
	#	return ("I'm valve {}.  my nodes are {}, my status is {}".format(self.name,[self.n1,self.n2],self.vStatus))
		
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
	parser.add_argument("fileName",help="the name of a file containing the mesh code(default active directory)")
	parser.add_argument("-o","--outFile",help="the name of an output file to output the text to (default active directory)")
	
	return parser
	
	
if __name__ == "__main__":
	
	parser=create_parser()
	args=parser.parse_args()
	
	print ("Your file: "+(args.fileName))
	mesh=Mesh(args.fileName,args.outFile)
	mesh.f_out()
	print(mesh)