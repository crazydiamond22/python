#!/usr/bin/env python3

import re

(result,lastdigit, females, males, ages, counts, groups, agerangedict,agegrangeperc, genderdict) = (None, "", 0,0, [], [], [], dict(),dict(),dict())

(seqflag, datalist) = (False, [])                                                  # Initialize

datalistclear = []
childrenCPRlist = []
father1timelist = []
mother1timelist = []
people = 0
parents = 0

age_dict= dict()
parent_child_dict=dict()
maindict = dict()

infile = open('people.db', "r")                                                   # open input file
flag = False
flag2 = False
for line in infile: 
	REresult1 = re.search(r'CPR:\s+(\d+(\d{2})\-\d+)\s*',line)                    # regex to isolate CPR
	if REresult1 is not None:
		if flag == True:

			maindict[CPR] = {'Age': age,'Firstname':firstname,                    # Store all the data collected from the Regex above and bellow in a dict (maindict: keys: CPR of each entry, values: rest of data of the entry in key-value pairs)
			'Lastname':lastname, 'Height':height, 'Weight': weight, 
			'Eyecolor':eyecolor, 'Bloodtype':bloodtype, 'Children':children}

		CPR = REresult1.group(1)
		age = 100 - int(REresult1.group(2))
		flag = True

	REresult2 = re.search(r'First name:\s+(\S+)\s*',line)                        # regex to isolate first name
	if REresult2 is not None:
		firstname = REresult2.group(1)
		
	REresult3 = re.search(r'Last name:\s+(\S+)\s*',line)                         # regex to isolate last name
	if REresult3 is not None:
		lastname = REresult3.group(1)

	REresult4 = re.search(r'Height:\s+(\S+)\s*',line)                            # regex to isolate height
	if REresult4 is not None:
		height = REresult4.group(1)

	REresult5 = re.search(r'Weight:\s+(\S+)\s*',line)                            # regex to isolate weight
	if REresult4 is not None:
		weight = REresult4.group(1)

	REresult6 = re.search(r'Eye color:\s+(\S+)\s*',line)                         # regex to isolate eyecolor
	if REresult6 is not None:
		eyecolor = REresult6.group(1)

	if flag2 == True:
		REresult8 = re.search(r'Children:(.+)',line)                             # regex to isolate children
		if REresult8 is not None:
			children = REresult8.group(1).split()
		else:
			children = None
		flag2 = False
	REresult7 = re.search(r'^\s*Blood type:\s+(\S+)\s*',line)                    # regex to isolate blood type
	if REresult7 is not None:
		bloodtype = REresult7.group(1)
		flag2 = True                                                             # flag turns true to collect children-if they exist

maindict[CPR] = {'Age': age,'Firstname':firstname, 'Lastname':lastname, 
'Height':height, 'Weight': weight, 'Eyecolor':eyecolor, 'Bloodtype':bloodtype,   # repeat the command that creates main dict to include the last entry of the input file
'Children':children}


def dividetogroups(alist):                                                       # function that takes a list and divides its elements into smaller groups
	minage = str(alist[0])[0]
	maxage = str(alist[-1])[0]
	counts = []
	string = ""
	agerangedict = dict()
	agegrangeperc = dict()

	if int(str(alist[0])[-1]) < 5 :                                              # round minimun and maximum age
		minage = int(minage)*10
	else:
		minage = int(minage)*10+5

	
	if int(str(alist[-1])[-1]) < 5 :                                             # round minimun and maximum age
		maxage = int(maxage)*10 + 5 
	else:
		maxage = (int(maxage)+1)*10

	for i in range (minage, maxage+1, 5):                                        # define the age groups
		groups.append(i)

	for m in range(len(groups)):                                                 # count how many entries belong to each group
		count1 = 0
		if m != len(groups)-1:
			for k in range(len(alist)):
				if alist[k] < groups[m+1] and alist[k] >= groups[m]:
					count1+=1
			counts.append(count1)

	for i in range (len(counts)):                                               # store results in dict
		string = str(groups[i])+'-'+str(groups[i+1])
		agerangedict[string] = counts[i]                                        # display results as normal numbers
					
		string = str(groups[i])+'-'+str(groups[i+1])
		agegrangeperc[string] = str(counts[i]*100/len(alist))+'%'               # display results as percentages

	return (agegrangeperc)


def averagefunc(alist):                                                        # function that takes a list and calculates its elements' mean
	
	sumlist = 0
	
	for i in range(len(alist)):
		sumlist+= int(alist[i])
	average = sumlist/len(alist)

	return average

#Question1 & 6
agelist = list()                                                               # initialize dicts
mothers = dict()
fathers = dict()

nc_men = 0                                                                     # initialize counters
nc_women = 0

 
CPRlist = list(maindict.keys())                                                # store all CPRs in a list (CPRlist)              



for i in range(len(CPRlist)):
	
	lastdigit = CPRlist[i][-1]                                                 # isolate last CPR digit

	if int(lastdigit)%2 == 0:                                                  # count males and females
		females +=1
		
		if maindict[CPRlist[i]]['Children'] is not None:                       # check for each woman, if she is a mother
			mothers[CPRlist[i]]= maindict[CPRlist[i]]['Children']              # store mothers and their children in dict (mothers: keys:mothers, values: children)
		else:
			nc_women += 1                                                      # count women without children

	else:
		males+=1
		
		if maindict[CPRlist[i]]['Children'] is not None:                       # check for each man, if he is a father
			fathers[CPRlist[i]]= maindict[CPRlist[i]]['Children']              # store fathers and their children in dict (fathers: keys:fathers, values: children)
		else:
			nc_men += 1                                                        # count men without children


	agelist.append(maindict[CPRlist[i]]['Age'])

#question 1
agelist.sort()
print('Question 1---------')
print(dividetogroups(agelist))
print('Percentage of men:', (males/len(CPRlist))*100, '%')
print('Percentage of women:', (females/len(CPRlist))*100, '%')
print('---------------')
print('   ')

#question6
print('Question 6---------')
print('Percentage of men without children :', (nc_men/males) *100, "%")
print('Percentage of women without children :', (nc_women/females) *100, "%")

print('Percentage of all the mothers:',(len(list(mothers.keys()))/females)*100,' %')
print('Percentage of all the fathers:',(len(list(fathers.keys()))/males)*100,' %')
print('---------------')
print('   ')

#-----------


#making childrens dictionary---------                              
kids_age = list()
kidlist = list()
firstfatherlist = list()
childict = dict()
motherlist = list(mothers.keys())
fatherlist = list(fathers.keys())


for i in range(len(fatherlist)):                                             
	kidlist = []
	kids_age = []
	kidlist = fathers[fatherlist[i]]
	
	for j in range (len(kidlist)):
		for k,v in mothers.items():
			if kidlist[j] in v:
				childict[kidlist[j]] = [fatherlist[i], k]
#-------------


#question7------
ChildCPR_sortlist = sorted(childict.keys(), key=childict.get)                  
kids_age = list()
parent_agediff = list()

for i in range(len(ChildCPR_sortlist)):                                     
	if i != len(ChildCPR_sortlist)-1:
		if childict[ChildCPR_sortlist[i]] != childict[ChildCPR_sortlist[i+1]]:
			father = childict[ChildCPR_sortlist[i]][0]
			mother = childict[ChildCPR_sortlist[i]][1]
			parent_agediff.append(abs(maindict[father]['Age'] - maindict[mother]['Age']))

		elif childict[ChildCPR_sortlist[i]] == childict[ChildCPR_sortlist[i+1]] and i == len(ChildCPR_sortlist)-2:
			mother = childict[ChildCPR_sortlist[i]][1]
			father = childict[ChildCPR_sortlist[i]][0]
			parent_agediff.append(abs(maindict[father]['Age'] - maindict[mother]['Age']))

	elif i == len(ChildCPR_sortlist)-1 and childict[ChildCPR_sortlist[i-1]] != childict[ChildCPR_sortlist[i]]:
		mother = childict[ChildCPR_sortlist[i]][1]
		father = childict[ChildCPR_sortlist[i]][0]
		parent_agediff.append(abs(maindict[father]['Age'] - maindict[mother]['Age']))
print('Question 7----------')
print ('Average age difference between parents: ',averagefunc(parent_agediff))	
print('---------------')
print('   ')
#--------------

#Question 4 & 5
motherlist = list(mothers.keys())
kids_age = list()
kidlist = list()
firstmotherlist = list()
for i in range(len(motherlist)):
	kidlist =[]
	kids_age =[]
	kidlist = mothers[motherlist[i]]
	for j in range(len(kidlist)):
		Ag_e = maindict[kidlist[j]]['Age']
		kids_age.append(Ag_e)
	kids_age.sort()
	firstmotherlist.append(maindict[motherlist[i]]['Age'] - kids_age[-1])
print('Question 4 and 5')
print(dividetogroups(firstmotherlist))
print ('Average age at which a person became a mother for the first time: ',averagefunc(firstmotherlist))
firstmotherlist.sort()
print('The oldest age at which a person became a mother: ',firstmotherlist[-1])
print('The youngest age at which a person became a mother: ',firstmotherlist[0])
print('---------------')
print('   ')
#--------------

#Question2 & 3
fatherlist = list(fathers.keys())
for i in range(len(fatherlist)):
	kidlist =[]
	kids_age =[]
	kidlist = fathers[fatherlist[i]]
	for j in range(len(kidlist)):
		Ag_e = maindict[kidlist[j]]['Age']
		kids_age.append(Ag_e)
	kids_age.sort()
	firstfatherlist.append(maindict[fatherlist[i]]['Age'] - kids_age[-1])
print('Question 2 and 3')
print(dividetogroups(firstfatherlist))
print ('Average age at which a person became a father for the first time: ',averagefunc(firstfatherlist))
firstfatherlist.sort()
print('The oldest age at which a person became a father: ',firstfatherlist[-1])
print('The youngest age at which a person became a father: ',firstfatherlist[0])
print('---------------')
print('   ')

#-------------------

#Question8------------
grandkids = set()
Children_keylist = list(childict.keys())

for g in range(len(Children_keylist)):
	if childict[Children_keylist[g]][0] in Children_keylist or childict[Children_keylist[g]] in Children_keylist:
		grandkids.add(Children_keylist[g])

print('Question 8')
print('Number of people with atleast one grandparent being alive : ',len(grandkids))                                             
print('percentage of people with atleast one grandparent: ',(len(grandkids)/len(maindict))*100,'%')
print('---------------')
print('   ')


#--------------------
#question 9

cousins_m = 0
siblings_M =list()
cousinsdict = dict()
siblist= list()
childlist = list(childict.keys())
for i in range(len(childlist)):
	siblings_M = []
	cousins_m = 0
	cousins_f = 0
	siblings_F = []
	totcousins = 0
	mother = childict[childlist[i]][1]
	father = childict[childlist[i]][0]
	for CPR in maindict:
		if maindict[CPR]['Children'] is not None and cousins_m ==0 :
			if mother in maindict[CPR]['Children']:
				siblings_M = maindict[CPR]['Children']
				for k in range(len(siblings_M)):
					if maindict[siblings_M[k]]['Children'] is not None and siblings_M[k]!= mother:
						cousins_m += len(maindict[siblings_M[k]]['Children'])
	
	for CPR in maindict:
		if maindict[CPR]['Children'] is not None and cousins_f ==0 :
			if father in maindict[CPR]['Children']:
				siblings_F = maindict[CPR]['Children']
				for v in range(len(siblings_F)):
					if maindict[siblings_F[v]]['Children'] is not None and siblings_F[v]!= father:
						cousins_f += len(maindict[siblings_F[v]]['Children'])

	cousinsdict[childlist[i]] = (cousins_f+cousins_m)
print('Question 9')
print(cousinsdict)










