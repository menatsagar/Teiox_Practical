lst=[0] 
def print_random_num(): 
	lst.append(lst[-1]+1) 
	a=str(id(lst[-1])) 
	num=0 
	for i in (a): 
		num+=int(i) 
	n=(str(num)[1]) 
	n=int(n) 
	return(n) 

for i in range(50): 
	print(print_random_num())