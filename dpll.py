import sys
import random
import copy

input = sys.argv[1] # input file
clauseset = []

# remove all l in the list
def removeAllOccur(l, i):

    try:
        while True : l.remove(i)
    except ValueError:
        pass

# preprocess the input file
def preprocess():
	f = open(input, 'r')
	lines = f.readlines()
	tmp = []
	for line in lines:
		if line[0] == 'c': pass # comment
		elif line[0] == 'p': # p cnf nbvar nbclauses
			nbvar = int(line.split(' ')[2]) # nbvar
			nbclauses = int(line.split(' ')[3]) # nbclauses
		else: # clauses
			line = line.replace('\n',' ')
			clause = line.split(' ')
			removeAllOccur(clause,'')
			if '0' in clause: # '0': end of clause
				removeAllOccur(clause,'0')
				tmp = tmp[:] + clause[:]
				clauseset.append(tmp)
				tmp = []
			else: 
				tmp = tmp[:] + clause[:]	
	f.close()

# unit propagation
def unitPropagation(clauseset):
	while 1: # while S contains a unit clause {l}
		clauseset_u = []
		# check if there is any unit clause
		unit_num = 0
		for i in range(len(clauseset)):
			if len(clauseset[i]) == 1: 
				unit_num = unit_num + 1
				l = clauseset[i][0] # get an unit clause
		if unit_num == 0: 
			# end unit propagation if no unit clause
			return clauseset

		print "-"*80
		print "START UNIT PROPAGATION: [\'"+str(l)+"\']"

		# delete clauses containing l from S 
		for i in range(len(clauseset)):
			status = 0
			for j in range(len(clauseset[i])):	
				if (clauseset[i][j] == l):
					status = 1	
					break
			if status == 0: clauseset_u.append(clauseset[i]) 	
		clauseset = copy.deepcopy(clauseset_u)	
		print "#. After deleting clauses containing "+str(l)+" from S"
		print " -> "+str(clauseset)

		# literal negation
		if l[0] == "-": l = l[1:]
		else: l = "-"+l		

		# delete -l from all clauses in S
		for	i in range(0,len(clauseset)):
			for j in range(0,len(clauseset[i])):
					if(clauseset[i][j] == (l)):				
						del clauseset[i][j]
						break
		print "#. After deleting "+str(l)+" from all clauses in S"
		print " -> "+str(clauseset)

# DPLL
def DPLL(clauseset):
	clauseset = unitPropagation(clauseset)

	if [] in clauseset:
		return False
	if len(clauseset) == 0:
		return True	

	# copy clauseset for branches
	clauseset_1 = copy.deepcopy(clauseset)
	clauseset_2 = copy.deepcopy(clauseset)

	# choose a literal l occuring in S
	rand = random.choice(random.choice(clauseset))
	print "#. Choosing a literal l occuring in S ("+str(rand)+")"
	if [rand] in clauseset_1: pass
	else: 
		clauseset_1.append([rand])

	# first branch: if (DPLL(S U {{l}})) return True
	print "-"*80
	print "FIRST BRANCH"
	print " -> "+str(clauseset_1)	
	result1 = DPLL(clauseset_1)
	if result1:
		return True

	# literal negation
	if rand[0] == "-": rand = rand[1:]
	else: rand = "-"+rand	

	if [rand] in clauseset_2: 
		pass
	else:
		clauseset_2.append([rand])

	# second branch: else if (DPLL(S U {{-l}})) return True
	print "-"*80
	print "SECOND BRANCH"
	print " -> "+str(clauseset_2)
	result2 = DPLL(clauseset_2)
	if result2:
		return True

	# else return False
	return False

if __name__ == "__main__":
	preprocess()
	print "-"*80	
	print "INPUT: "+str(clauseset)

	print "-"*80	
	print "START DPLL"	
	result = DPLL(clauseset)

	print "-"*80
	if(result): print "OUTPUT: SATISFIABLE"
	else: print "OUTPUT: UNSATISFIABLE"
	print "-"*80