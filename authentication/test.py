from random import random
def randbags(bags):
    lst=list()
    while(len(lst)<8):
        r = random()
        if r > 0.3 and r not in lst:
            lst.append(r)

    s = sum(lst)
    lst = [round(i/s*bags,0) for i in lst]
    if sum(lst) ==bags:
        lst_final = lst
    elif sum(lst) >bags:
        lst[6] = lst[6] - (sum(lst)-bags)
    else:
        lst[6] = lst[6] + (bags-sum(lst))
    return lst
def randomrate(minr,maxr,x):
    pass

def dara(bags,weight, minr,maxr,rate):
    x = bags*0.6-weight
    lst2 = randbags(bags-x/0.05)
    lst_weights = [round(i*0.6,2) for i in lst2]
    lst2.append(x/0.05)
    lst_weights.append(x/0.05*0.55)
    randomrate(minr,maxr,len(lst2))
dara(500,298.5)
