# def _(n = (0..6)):
#   pylab.clf()
#   tableau = )log(np.random.rand(10**n,]))
#   ml = pylab


import numpy as np

n = 5
p = [[0.0, 0.2, 0.3, 0.2, 0.3],
	[0.2, 0.0, 0.3, 0.2, 0.3],
	[0.2, 0.25, 0.0, 0.25, 0.3],
	[0.15, 0.2, 0.3, 0.0, 0.35],
	[0.2, 0.25, 0.35, 0.2, 0.0]]     # [n][n]
d = [2.8, 3.7, 5.5, 3.5, 4.6]     # [n]

def div_60(x) : return x/60
d = map(div_60, d)

mu = [[0, 3, 5, 7, 7],
	 [2, 0, 2, 5, 5],
	 [4, 2, 0, 3, 3],
	 [8, 6, 4, 0, 2],
	 [7, 7, 5, 2, 0]]     # [n][n]    # [n][n]
nmax = [24, 20, 20, 15, 20]  # [n]
X0 = [20, 15, 17, 13, 18,
	  0, 1, 0, 0, 0,
	  1, 0, 1, 0, 0,
	  0, 1, 0, 1, 0,
	  0, 0, 1, 0, 1,
	  0, 0, 0, 1, 0]    # [n(n+1)]


''' Function that computes randomly the next step '''
def next_step(X,t):
  coef_stations_to_paths = []
  coef_paths_to_stations = []
  sum_coef = 0

  ## Filling the coefficients vector
  for i in range(n):
    for j in range(n):
      ## Filling the coefficients that represent going from one station to 
      # the route starting from the station
      if X[i] == 0:
        coef_stations_to_paths.append(0)
      else:
        coef_stations_to_paths.append(d[i]*p[i][j])
        sum_coef += d[i]*p[i][j]

      ## Filling the coefficients that represent going out of one route to 
      # the station at the end of the route
      if X[j] == nmax[j]:
        coef_paths_to_stations.append(0)
      else:
        coef_paths_to_stations.append(X[n + i*n + j] * mu[i][j])
        sum_coef += X[n + i*n + j] * mu[i][j]

  ## Getting when a change is made
  time_to_action = np.random.exponential(sum_coef)

  ## Getting the next state
  proba = np.random.random()
  # print "proba = ",proba

  inter_sum = 0
  get_out = False
  for i in range(n):
    for j in range(n):
      ## If the transition to one station to path is selected
      if inter_sum + coef_stations_to_paths[n*i+j]/sum_coef >= proba:
        X[i] -= 1 
        X[n + i*n + j] += 1
        get_out = True
        # print (i,j),coef_stations_to_paths[n*i+j]
        break

      inter_sum += coef_stations_to_paths[n*i+j]/sum_coef

      ## If the transition to one path to one station is selected
      if inter_sum + coef_paths_to_stations[n*i+j]/sum_coef >= proba:
        X[j] += 1 
        X[n + i*n + j] -= 1
        get_out = True
        # print (i,j),coef_paths_to_stations[n*i+j]
        break

      inter_sum += coef_paths_to_stations[n*i+j]/sum_coef 

    if get_out:
      break

  ## return time
  return t + time_to_action


Z=[]
nb_itt=10000
# Nombre d'itterations dans un temps inferieur a celui voulu, ici 10 :
for i in range(nb_itt):
  t = 0
  X=X0
  while t<10:
    # print t
    t = next_step(X,t)
  Y=list(X)
  # print Y
  Z.append(Y)



# Impression des itterations
# print "/////////////////////////"
# print Z

# Moyenne sur les itterations
W=list(Z[1])
for j in range(1,len(Z)):
  for i in range(len(Z[1])):
    W[i]=W[i]+Z[j][i]
# print "/////////////////////////"
# print W
print "/////////////////////////"
def div_size_Z(x) : return x/(len(Z))
W=map(div_size_Z,W)
print W

for i in range(0,5):
  print "Places restantes dans la station ",i+1," sur une moyenne de ",nb_itt," itterations : ",nmax[i]-W[i]



