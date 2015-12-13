''' 
  CREATE ROUTING MATRIX
  Script that create a routing matrix using a quadratic optimisation problem 
'''

import cplex

### DEFINITION OF DATA
nb_stations = 17
margin = 0.05

# Departures per day from stations
dep = [0.689265537,2.336956522,2.819672131,3.726775956,5.532608696,3.516483516,
  4.586956522,1.934782609,1.734104046,1.358695652,1.532608696,1.245714286,
  2.456521739,1.804347826,1.479768786,3.6,1.111111111,0.710382514,
  1.2,1.065217391,1.326086957]

# Arival per day in stations
arr = [0.598870056,2.25,2.808743169,3.683060109,5.543478261,3.505494505,
  4.630434783,1.836956522,1.815028902,1.489130435,1.489130435,1.325714286,
  2.489130435,1.793478261,1.572254335,3.8,1.033333333,0.677595628,1.282352941,
  1.065217391,1.369565217]

print "Arrivals : "
for val in dep:
  print val," -- ",
print " "
print "Departures : "
for val in arr:
  print val," -- ",
print " "

print "Variables tag :"
variables_tag = []
for i in range(nb_stations):
  variables_tag.append([])
  for j in range(nb_stations):
    variables_tag[i].append(str(i)+"->"+str(j))
    print variables_tag[i][j]," ",
  print " "

### OPTIMISATION : Computation of a routing Matrix

def setproblemdata(p):
  p.objective.set_sense(p.objective.sense.minimize)

  ''' VARIABLES '''

  ### Addition of variables
  obj = [] ## 0bjective value ? 
  ub  = [] ## Upper bounds
  names = [] ## Names
  for i in range(nb_stations):
    for j in range(nb_stations):
      obj.append(0.0)
      if i!=j:
        ub.append(1.0)
      else:
        ub.append(0.0)
      names.append(variables_tag[i][j])

  # ## Loss coefficient 
  # obj.append(float((nb_stations)*(nb_stations)))
  # ub.append(1.0)
  # names.append(variables_tag[i][j])
  
  p.variables.add(obj = obj, ub = ub, names = names)

  ''' CONSTRAINTS '''

  rows = []
  my_rownames = []
  my_rhs = []
  senses = []

  ### Addition of constraints that derpature correspond to arrivals
  for j in range(nb_stations):
    names_temp = [] ## names of variables in constraint
    val_temp = []   ## Val of positives coefficients in constraints

    for i in range(nb_stations):
      for j2 in range(nb_stations):
        if i!=j and j2 == j:
          names_temp.append(variables_tag[i][j])
          val_temp.append(dep[i])
        else:
          names_temp.append(variables_tag[i][j2])
          val_temp.append(0.0)          

    ## Addition of the constraint 
    my_rownames.append("A"+str(j))
    rows.append([names_temp, val_temp])
    my_rhs.append(arr[j])
    senses.append("L")

    my_rownames.append("Am"+str(j))
    rows.append([names_temp, val_temp])
    my_rhs.append(arr[j] - margin)
    senses.append("G")

  ### addition of constraints that assure that sum of proba equal to 1
  for i in range(nb_stations):
    names_temp = [] ## names of variables in constraint
    val_temp = []   ## Val of positives coefficients in constraints

    for i2 in range(nb_stations):
      for j in range(nb_stations):
        if i2 == i:
          names_temp.append(variables_tag[i][j])
          val_temp.append(1.0)
        else:
          names_temp.append(variables_tag[i2][j])
          val_temp.append(0.0)         

    ## Addition of the constraint
    my_rownames.append("P"+str(j))
    rows.append([names_temp, val_temp])
    my_rhs.append(1.0)
    senses.append("E")

  print "MATRIX ROWS"
  print rows

  print "RHS"
  print my_rhs

  print "ROW NAMES"
  print my_rownames

  print "SENSES"
  print senses

  p.linear_constraints.add(lin_expr = rows, senses = senses,
                              rhs = my_rhs, names = my_rownames)

  ''' OBJECTIVE '''
  quad_coef = [ (i,i,1.0) for i in range(nb_stations*nb_stations)]
  p.objective.set_quadratic_coefficients(quad_coef)
  coef = p.objective.get_quadratic()
  print coef 
  p.objective.set_quadratic(coef)


def setproblemdata1(p):
  p.objective.set_sense(p.objective.sense.maximize)

  p.linear_constraints.add(rhs = [20.0, 30.0], senses = "LL")

  obj  = [1.0, 2.0, 3.0]
  ub   = [40.0, cplex.infinity, cplex.infinity]
  cols = [[[0,1],[-1.0, 1.0]],
          [[0,1],[ 1.0,-3.0]],
          [[0,1],[ 1.0, 1.0]]]
  
  p.variables.add(obj = obj, ub = ub, columns = cols,
                  names = ["one", "two", "three"])

  qmat = [[[0,1],[-33.0, 6.0]],
          [[0,1,2],[ 6.0,-22.0, 11.5]],
          [[1,2],[ 11.5, -11.0]]]


  p.objective.set_quadratic(qmat)
    


# # data common to all populateby functions
# my_obj      = [1.0, 2.0, 3.0]
# my_ub       = [40.0, cplex.infinity, cplex.infinity]
# my_colnames = ["x1", "x2", "x3"]
# my_rhs      = [20.0, 30.0]
# my_rownames = ["c1", "c2"]
# my_sense    = "LL"


# def populatebyrow(prob):
#     prob.objective.set_sense(prob.objective.sense.maximize)

#     # since lower bounds are all 0.0 (the default), lb is omitted here
#     prob.variables.add(obj = my_obj, ub = my_ub, names = my_colnames)

#     # can query variables like the following:

#     # lbs is a list of all the lower bounds
#     lbs = prob.variables.get_lower_bounds()

#     # ub1 is just the first lower bound
#     ub1 = prob.variables.get_upper_bounds(0) 

#     # names is ["x1", "x3"]
#     names = prob.variables.get_names([0, 2])

#     rows = [[[0,"x2","x3"],[-1.0, 1.0,1.0]],
#             [["x1",1,2],[ 1.0,-3.0,1.0]]]

#     prob.linear_constraints.add(lin_expr = rows, senses = my_sense,
#                                 rhs = my_rhs, names = my_rownames)

#     # because there are two arguments, they are taken to specify a range
#     # thus, cols is the entire constraint matrix as a list of column vectors
#     cols = prob.variables.get_cols("x1", "x3")


def qpex1():

  p = cplex.Cplex()
  setproblemdata(p)

  p.solve()

  # solution.get_status() returns an integer code
  print "Solution status = " , p.solution.get_status(), ":"
  # the following line prints the corresponding string
  print p.solution.status[p.solution.get_status()]
  print "Solution value  = ", p.solution.get_objective_value()

  numrows = p.linear_constraints.get_num()

  for i in range(numrows):
    print "Row ", i, ":  ",
    print "Slack = %10f " %  p.solution.get_linear_slacks(i), " -- ",
    print "Pi = %10f" % p.solution.get_dual_values(i)

  numcols = p.variables.get_num()

  for j in range(numcols):
    print "Column ", j, ":  ",
    print "Value = %10f " % p.solution.get_values(j), " -- ",
    print "Reduced Cost = %10f" % p.solution.get_reduced_costs(j) 

qpex1()


### CHECK OF THE VALIDITY OF THE DATA

