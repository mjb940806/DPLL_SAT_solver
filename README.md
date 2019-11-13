[IMS697 2019 FW] DPLL 알고리즘을 사용하는 SAT Solver 구현
======================
## 1. 동작환경
Python2.7, macOS Catalina
## 2. 가정사항
- 입력 파일은 DIMACS 포맷이다.
- 입력 파일 내의 공백은 스페이스 한 칸으로 간주한다.
- 실행 시 한 개의 파일을 argument로 입력받아 동작한다.
## 3. 상세 기능
### 3.0. 사용 모듈
```python
import sys # for getting an input file
import random # for choosing a literal l
import copy # for deepcopying a list
```
### 3.1. removeAllOccur(l,i)
리스트 `l` 내의 특정 원소 `i`를 모두 제거한다. 전처리 중 발생하는 literal `''`,`'0'`을 제거하기 위해 사용된다.
```
parameter: list l, element i
return value: None
```
```python
# remove all l in the list
def removeAllOccur(l, i):
    try:
        while True : l.remove(i)
    except ValueError:
        pass
```
### 3.2. preprocess()
입력 받은 DIMAC 포맷 파일을 전처리한다. 파일을 라인 별로 읽어 공백을 기준으로 split하고 `0`이 들어오기 전까지를 한 clause로 묶어 `clauseset`에 append 한다.
```
parameter: None
return value: None
```
```python
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
```
### 3.3. unitPropagation(clauseset)
clauseset 내에 unit clause `l`이 있는 동안 반복한다. `l`이 포함된 clause를 지우고 literal `-l`을 지운다.
```
parameter: clauseset
return value: clauseset
```
```python
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
		print "UNIT PROPAGATION: [\'"+str(l)+"\']"

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
```
### 3.4. DPLL(clauseset)
unitPropagation 수행 후 `clauseset`에 clause `[]`가 포함되어 있으면 `False`를, `clauseset`이 비어 있으면 `True`를 반환한다. `clauseset`에 포함된 random literal `l`을 선택하여 branch 도중 `True`가 반환되면 `True`를 반환하고 아닌 경우 `False`를 반환한다. 
```
parameter: clauseset
return value: Boolean value (True/False)
```
```python
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
```
## 4. 실행 예제
```bash
$ python dpll.py sample_input/test3.cnf
--------------------------------------------------------------------------------
START DPLL
INPUT: [['1', '2', '-3'], ['1', '-2'], ['-1'], ['3'], ['4']]
--------------------------------------------------------------------------------
UNIT PROPAGATION: ['4']
#. After deleting clauses containing 4 from S
 -> [['1', '2', '-3'], ['1', '-2'], ['-1'], ['3']]
#. After deleting -4 from all clauses in S
 -> [['1', '2', '-3'], ['1', '-2'], ['-1'], ['3']]
--------------------------------------------------------------------------------
UNIT PROPAGATION: ['3']
#. After deleting clauses containing 3 from S
 -> [['1', '2', '-3'], ['1', '-2'], ['-1']]
#. After deleting -3 from all clauses in S
 -> [['1', '2'], ['1', '-2'], ['-1']]
--------------------------------------------------------------------------------
UNIT PROPAGATION: ['-1']
#. After deleting clauses containing -1 from S
 -> [['1', '2'], ['1', '-2']]
#. After deleting 1 from all clauses in S
 -> [['2'], ['-2']]
--------------------------------------------------------------------------------
UNIT PROPAGATION: ['-2']
#. After deleting clauses containing -2 from S
 -> [['2']]
#. After deleting 2 from all clauses in S
 -> [[]]
--------------------------------------------------------------------------------
OUTPUT: UNSATISFIABLE
--------------------------------------------------------------------------------
```
