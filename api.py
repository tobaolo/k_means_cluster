# Importing necessary libraries
import urllib
import requests
import time
import numpy as np
import random
import math
import matplotlib.pyplot as plt

#this function picks a random oint in a data set
def centroid_rand(data, n):
    size = len(data['ide'])
    centroids_indx = []
    centroids = []
    for i in range(n):
        gre_avg = 0
        gpa_avg = 0
        val = random.randint(0, size) 
        while (val in centroids):           #checks to make sure that  point is not already a centroid
            val = random.randint(0, size) 
            gre_avg = data['gre'][val]
            gpa_avg = data['gpa'][val]
        gre_avg = data['gre'][val]
        gpa_avg = data['gpa'][val]
        cent = {}
        cent['gre_avg'] = gre_avg
        cent['gpa_avg'] = gpa_avg
        centroids_indx.append(val)
        centroids.append(cent)

    return centroids  

#calculates distance between 2 points
def distance(x1, x2, y1,y2):
    distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    return distance

#creates a list where each index references one data point and the value at that index is the cluster group
def cluster(data, centroids): 
    gre = data['gre']
    gpa = data['gpa']
    size = len(data['ide'])
    clusters = []                               #clusters is the list of all clusters groups..index is the data point in reference
    # loop through each gre and gpa
    for i in range(size):
        distances = []
        cluster_id = 0                          #cluster_id is the cluster group each point is in
        #calculates the distance between one data point and all centroids into array
        for cent in centroids:
            x1 = gre[i]
            x2 = cent['gre_avg']
            y1 = gpa[i]
            y2 = cent['gpa_avg']
            distances.append(distance(x1, x2, y1, y2))
        low = distances[0]
        for i in range(len(distances)-1):        
            if(low > distances[i+1]):
                low = distances[i+1]
                cluster_id = i+1
        clusters.append(cluster_id)
    return(clusters)
    
#recalculates the centroids using the data set, n number of clusters, and clustered data
def recalc_centroid(n,clusters,data):
    avgs = []
    cntr = 0
    count = 0
    for i in range(n):
        gre_sum = 0
        gpa_sum = 0
        cntr = 0
        
        for index in range(len(clusters)): 
            if (clusters[index] == i):
                cntr += 1
                gre_sum += data['gre'][index]
                gpa_sum += data['gpa'][index]
                count = cntr
            else:
                cntr = cntr
        avgs.append({})
        avgs[i]['gre_avg'] = gre_sum/(count)
        avgs[i]['gpa_avg'] = gpa_sum/(count)
    return avgs

ide, gre, gpa  = np.loadtxt('Admission_Predict.csv',delimiter = ',',skiprows=1,usecols=[0,1,6],unpack=True)

NUM_OF_CLUSTERS = 5

data = {}
data['ide'] = ide
data['gre'] = gre
data['gpa'] = gpa

centroid_dict = centroid_rand(data,NUM_OF_CLUSTERS)
cluster1 = cluster(data, centroid_dict)
new_cents = recalc_centroid(NUM_OF_CLUSTERS,cluster1,data)
cluster2 = cluster(data, new_cents)

#reruns the clustering until the center of the first run is the same as the center of the second run
while (cluster1 != cluster2):
    new_cents1 = recalc_centroid(NUM_OF_CLUSTERS,cluster2,data)
    cluster1 = cluster(data, new_cents1)
    new_cents2 = recalc_centroid(NUM_OF_CLUSTERS,cluster1,data)
    cluster2 = cluster(data, new_cents2)

plt.scatter(gre,gpa,c=cluster2)
plt.show()