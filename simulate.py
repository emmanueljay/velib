# def _(n = (0..6)):
#   pylab.clf()
#   tableau = )log(np.random.rand(10**n,]))
#   ml = pylab

import sys
if len(sys.argv) < 2:
  print "Vous pouvez passer en paramatre le nombre d'iterations de la simulation. Par defaut, 10000"
  nb_itt = 10000
else :
  nb_itt = int(sys.argv[1])

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

## Vecteur de station
station_etat = {}
for station in range(n):
  station_etat[station] = []  

station_mean = {}
for station in range(n):
  station_mean[station] = 0

# Nombre d'itterations dans un temps inferieur a celui voulu, ici 10 :
print "Launching ",nb_itt," simulations of the Markov chain of 10 minutes"

for i in range(nb_itt):
  if (i%(nb_itt/10) == 0): print i*100/nb_itt,"%  done"
  t = 0
  X=X0
  while t<10:
    # print t
    t = next_step(X,t)

  for station in range(n):
    station_etat[station].append(X[station])
    station_mean[station] += X[station]

  Y=list(X)
  # print Y
  Z.append(Y)


print "\n/////////////////////////"
print "MOYENNE DES PLACES DISPONIBLES\n"

for station in range(n):
  station_mean[station] = float(station_mean[station]) / nb_itt
  print "Places restantes dnas la station ", station+1, " sont de ", nmax[station]-station_mean[station]


print "\n/////////////////////////"
print "PROBABILITEES DE BLOCAGE\n"

proba_blocage = {}
for station in range(n):
  proba_blocage[station] = 0.0
  for etat in station_etat[station]:
    if (etat == nmax[station]):
      proba_blocage[station] += 1.0
  proba_blocage[station] /= nb_itt
  print "La probabilite de blocage pour la station ", station+1, " est ", proba_blocage[station]

print "\n/////////////////////////"
print "INTERVALES DE CONFIANCE POUR LES PROBABILITEES DE BLOCAGE A 95%\n"

alpha = 0.95
beta = 1.96

# Calcul de la variance empirique, et des intervales de confiance
variance_empirique = {}
for station in range(n):
  variance_empirique[station] = 0.0
  for etat in station_etat[station]:
    if (etat == nmax[station]):
      variance_empirique[station] += (1.0-proba_blocage[station])*(1.0-proba_blocage[station])
    else:
      variance_empirique[station] += proba_blocage[station]*proba_blocage[station]
    variance_empirique[station] /= nb_itt-1   
    variance_empirique[station] = np.sqrt(variance_empirique[station])

  ## Affichage des intervales de confiance
  borne_inf = proba_blocage[station] - beta*variance_empirique[station]/np.sqrt(nb_itt)
  borne_sup = proba_blocage[station] + beta*variance_empirique[station]/np.sqrt(nb_itt)
  print "Variance empirique = ", variance_empirique[station]
  print "L'intervalle de confiance de la proba de blocage a 95\% pour la station ",
  print station+1, " est [", max(0.0,borne_inf),",",min(1.0,borne_sup),"]"

print "\n/////////////////////////"
print "\n/////////////////////////\n"

# Moyenne sur les itterations
W=list(Z[1])
for j in range(1,len(Z)):
  for i in range(len(Z[1])):
    W[i]=W[i]+Z[j][i]
def div_size_Z(x) : return x/(len(Z))
W=map(div_size_Z,W)
print W

for i in range(0,5):
  print "Places restantes dans la station ",i+1," sur une moyenne de ",nb_itt," iterations : ",nmax[i]-W[i]

print "\n/////////////////////////\n"


moyenne_stations = {}
for station in range(n):
  moyenne_stations[station] = np.mean(station_etat[station])
  print "Places restantes dnas la station ", station+1, " sont de ", nmax[station]-moyenne_stations[station]


