
"""
For 50 students, the running time is appx. 60s,and i am getting a better cost of 3528. 
State space: all possible configuration of students in groups with each group size less than 4 
Successor function has in it the initial state as - each person is in a group of 1-
From here on, my successor function adds two persons at a time, therby covering every permutation and combination
of groups possible. 
I have read the file using open() and readlines funcitons.I have also written Staffwork()
function which calculates the work staff needs to do for any particular group configuration. Now, my solve() function
appends minimum of successors into the fringe (with respect to Staffwork cost) and finally spits out 
minimum and the corresponding arrangement of students. 
"""
import sys
file_name = str(sys.argv[1])
with open(file_name) as f:
    survey = f.readlines()
    #print survey
# Removing the \n
survey = [x.strip() for x in survey] 
k = int(sys.argv[2])
m = int(sys.argv[3])
n = int(sys.argv[4])

#Splitting the survey array
c= []
for x in survey:
    c.append(x.split())
#print "this is student survey \n", c, "\n"


# Creating initial configuration of groups where each group has 1 person  
initial_groups = []
for x in c:
    initial_groups.append(x[0])
#print "this is initial group \n", initial_groups, "\n"    

# This function calculates Staff work for each configuration of groups of students
def Staffwork(b):
   #Splitting the group, so it can be added later to the splitted survey array 
   be = []
   for x in b:
       be.append(x.split())
   #print "this is be",be
   # final1 array has in each of its elements, the students survey which is preference of students  
   # plus the group assigned,in other words students preference vs actual group
   final1=[]
   for x in c:
       for y in be:
           if x[0] in y:
              final1.append(x+y) 
   #print "this is final 1 \n",final1 

   # Calculating sum1,the number of times each team member did not get his preferred group size
   # sum2, number of times a team member did not get his preferred partner
   # sum3, number of times a team member got his not-preferred student
   sum1 = 0
   sum2 = 0
   sum3 = 0
   for x in range(0,len(final1)):
        
       if  int(final1[x][1]) != 0  and int(final1[x][1]) != len(final1[x][4:]):
               sum1 = sum1+1 
                
       for y in final1[x][2].split(','):
           if y not in  final1[x][4:] and y != '_':
               sum2 = sum2+1
       for z in final1[x][3].split(','):
           if z in final1[x][4:]:
               sum3 = sum3+1
   #print "final sum1 is", sum1
   #print "final sum2 is", sum2
   #print "final sum3 is", sum3           
   #print ((len(b)*160)+sum1+(sum2*10)+(sum3*31))
   return [b,(len(b)*k)+sum1+(sum2*n)+(sum3*m)]
def successor(group,i,j):
  List1=[]  
  add = group[i]+' '+group[j]
  if add.count(' ')<=2:
      List1.append(add)
      for x in range(0,len(group)):
          if x !=i and x !=j:
             List1.append(group[x]) 
  return List1
     
def ListofSuccessors(group):
   List2 = [] 
   for i in range(0,len(group)):
       for j in range(i+1,len(group)):
           if i!=j and len(successor(group,i,j))>0 :
               List2.append(successor(group,i,j))
   return List2


def solve(group):
    mini =100000000
    fringe = [group]
    
    while len(fringe) > 0:
        for z in ListofSuccessors( fringe.pop() ):          
            x = Staffwork(z)
            if x[1]< mini:
                finalg = x[0]
                mini = x[1]
                fringe.append(z)
            
    for x in finalg:
        print x 
    print mini
    
#Staffwork(v)

solve (initial_groups)



