
from proj08 import read_file
fp = open("pollution_tiny.csv")
D_student = read_file(fp)
D_instructor = {'Michigan': [['Detroit', '3/31/2000', 34.708333, 2.0, 4.916667, 900.0], ['Detroit', '4/1/2000', 37.666667, 19.75, 9.333333, 325.0], ['Detroit', '4/2/2000', 25.833333, 25.666999999999998, 3.958333, 275.0]], 'Maine': [['Presque Isle', '1/1/2006', 2.808696, 30.667, 2.943478, 200.0], ['Presque Isle', '1/2/2006', 3.556522, 25.375, 1.713043, 200.0]]}
print("D_instructor:",D_instructor)
print("D_student:",D_student)
assert D_student == D_instructor


from proj08 import total_years 
D = {'Michigan': [['Detroit', '3/31/2000', 34.708333, 0.002, 4.916667, 0.9], ['Detroit', '4/1/2000', 37.666667, 0.01975, 9.333333, 0.325], ['Detroit', '4/2/2000', 25.833333, 0.025667, 3.958333, 0.275]], 'Maine': [['Presque Isle', '1/1/2006', 2.808696, 0.030667, 2.943478, 0.2], ['Presque Isle', '1/2/2006', 3.556522, 0.025375, 1.713043, 0.2]]}
T_instructor= ([[98.208333, 0.047417, 18.208333, 1.5], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], 98.208333, 0)
T_student = total_years(D,'Michigan')
print("T_instructor:",T_instructor)
print("T_student:",T_student)
assert T_student == T_instructor

print()
print()

from proj08 import total_years, read_file 
fp = open("pollution_small.csv")
D = read_file(fp)
T_instructor =  ([[4082.771702, 4206.028000000003, 975.7437869999992, 50522.54300000002], [3348.641588000001, 4125.926, 796.8429829999999, 58442.695999999996], [6414.392806000004, 10074.466999999995, 1209.747425, 130065.49799999999], [6058.463629, 9388.806999999993, 1041.455613, 138250.002], [4996.965389000002, 8887.057000000008, 824.6742960000004, 122338.31200000002], [5108.685554999998, 9692.338000000005, 885.188937, 106651.459], [4408.862753, 9565.044000000009, 675.2983520000001, 111601.37800000004], [8.125, 21.0, 2.333333, 229.167], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], 138250.002, 0)
T_student = total_years(D,'Michigan')
print("T_instructor:",T_instructor)
print("T_student:",T_student)
assert T_student == T_instructor

print()
print()

from proj08 import cities 
D = {'Michigan': [['Detroit', '3/31/2000', 34.708333, 0.002, 4.916667, 0.9], ['Detroit', '4/1/2000', 37.666667, 0.01975, 9.333333, 0.325], ['Detroit', '4/2/2000', 25.833333, 0.025667, 3.958333, 0.275]], 'Maine': [['Presque Isle', '1/1/2006', 2.808696, 0.030667, 2.943478, 0.2], ['Presque Isle', '1/2/2006', 3.556522, 0.025375, 1.713043, 0.2]]}
D_instructor= {'Detroit': [98.208333, 0.047417, 18.208333, 1.5]}
D_student = cities(D,'Michigan',2000)
print("D_instructor:",D_instructor)
print("D_student:",D_student)
assert D_student == D_instructor

print()
print()

from proj08 import months, read_file 
fp = open("pollution_small.csv")
D = read_file(fp)
T_instructor = ([1007.4459379999998, 910.981578, 898.3775449999999, 886.9802479999998, 867.4222229999997], [2099.1289999999995, 1862.3470000000002, 1733.1389999999997, 1471.5560000000005, 1360.181], [208.13328399999997, 179.59141600000007, 160.52126900000005, 142.36984600000002, 110.60325999999998], [21283.334999999992, 19275.002, 19261.305, 18566.390000000003, 17852.926])
T_student = months(D,'Michigan',2005)
print("T_instructor:",T_instructor)
print("T_student:",T_student)
assert T_student == T_instructor
