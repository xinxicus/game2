from itertools import permutations
number=[]
do_not=[]
random_list=[1, 2, 3, 4, 5, 6, 7, 8, 9]
answer=[1, 1, 1, 1, 1, 1, 1, 1, 1]
for i in permutations(random_list):
  answer=i
  print(answer)
  if answer[0]*answer[1]-answer[2] ==3 and (answer[3]+answer[4])/answer[5] == 3 and answer[6]-answer[7]+answer[8]==3 and answer[0]*answer[3]-answer[6]==3 and (answer[1]-answer[4])*answer[7] ==3 and answer[2]-answer[5]+answer[8]==3:
    print(answer)
    break