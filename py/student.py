import pymongo
import json

import numpy as np
from sklearn.manifold import TSNE
from sklearn.manifold import MDS
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["PTADATA"]

collect_concept = mydb["concepts"]
collect_problem = mydb["problems"]

collect_problem_concept = mydb["problem_concept"]
collect_userSubmissions = mydb["submissions"]

entProblem = []
entStudent = {}
entConcept = []
for p in collect_problem.find({}):
    entProblem.append(p)

for l in collect_userSubmissions.find({}):
    userId = l['user']['user']['id']
    if userId not in entStudent:
        entStudent[userId] = {}
    jageProblemContents = l['judgeResponseContents']
    submitAt = l['submitAt']
    for i in jageProblemContents:
        problemId = i['problemSetProblemId']
        score = i['score']
        status = i['status']

        if problemId not in entStudent[userId]:
            entStudent[userId][problemId] = {'log': [], 'best': i}
        entStudent[userId][problemId]['log'].append(i)
        if entStudent[userId][problemId]['best']['score'] < score:
            entStudent[userId][problemId]['best'] = i

# print(entStudent)
tsneXStudent = []
for s in entStudent:
    print(s)
    tempS = {
        'id': s,
        'val': []
    }
    # print(len(entStudent[s]))
    # for p in entStudent[s]:
    #     print(p)
    val = []
    i = 0
    for p in entProblem:
        pid = p['id']
        pScore = p['score']
        if pid in entStudent[s]:
            sScore = entStudent[s][pid]['best']['score']
            val.append(sScore / pScore)
        else:
            val.append(0)
    tempS['val'] = val
    tsneXStudent.append(tempS)
print(tsneXStudent)
dataMat = []
idMat = []
for s in tsneXStudent:
    print(s)
    idMat.append(s['id'])
    dataMat.append(s['val'])
    i = 0
    for v in s['val']:
        if v < 1:
            i += 1
    print(i)

X = np.array(dataMat)  # [[12, 23, 3], [23, 45, 6], [4, 5, 7], [6, 3, 5]])
print(X)
result = []
# X_tsne = TSNE(n_components=2, learning_rate=500).fit_transform(X)
color = ['c', 'b', 'g', 'r', 'm', 'y', 'k', 'w']
X_tsne = MDS(n_components=2).fit_transform(X)
kmeans = KMeans(n_clusters=7, random_state=0).fit(X_tsne)
print(kmeans.labels_)
ii = 0
for p in X_tsne:
    result.append({
        "id": idMat[ii],
        "x": p[0],
        "y": p[1],
        "kmeansC": int(kmeans.labels_[ii])
    })
    plt.scatter(p[0], p[1], c=color[kmeans.labels_[ii]], edgecolors='r')
    plt.text(p[0], p[1], str(ii), fontdict={'family': 'serif', 'size': 15, 'color': color[kmeans.labels_[ii]]},
             ha='center', va='center')
    ii += 1
plt.show()
print(X_tsne)

with open("group.json", 'w') as fw:
    json.dump(result, fw)
