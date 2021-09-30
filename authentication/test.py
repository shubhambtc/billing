# from random import random
# def randbags(bags):
#     lst=list()
#     while(len(lst)<8):
#         r = random()
#         if r > 0.3 and r not in lst:
#             lst.append(r)

#     s = sum(lst)
#     lst = [round(i/s,0) for i in lst]
#     if sum(lst) ==bags:
#         lst_final = lst
#     elif sum(lst) >bags:
#         lst[6] = lst[6] - (sum(lst)-bags)
#     else:
#         lst[6] = lst[6] + (bags-sum(lst))
#     return lst
# # def randomrate(minr,maxr,x):
# #     pass

# def dara(bags,weight):
#     x = bags*0.6-weight
#     lst2 = randbags(bags-x/0.05)
#     lst_weights = [round(i*0.6,2) for i in lst2]
#     lst2.append(x/0.05)
#     lst_weights.append(x/0.05*0.55)
#     print(lst_weights)
#     # randomrate(minr,maxr,len(lst2))
# dara(500,298.5)
weight = [20.4, 35.4, 42.6, 22.2, 41.4, 25.8]
weight =[i/0.6 for i in weight]
rate_less= [2120,2121,2125,2135]
rate_more = [2141,2145,2150,2151]
#weight.sort()
s = sum(weight)
x = rate_less[0]*weight[0] + rate_less[1]*weight[1] 
y = rate_more[0]*weight[2] + rate_more[4]*weight[3] + rate_more[3]*weight[4] + rate_more[5]*weight[3]
k = x+y
z = (500*2142.3)
left = z-k
print(left)
a  = (left-(rate_less[2]*(500-s)))/(rate_less[3]-rate_less[2])
b = 500 - a -s
print(a*0.6,b*0.6)