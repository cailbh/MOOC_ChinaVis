import pymongo
import json

import numpy as np
from sklearn.manifold import TSNE
from sklearn.manifold import MDS
from sklearn.manifold import SpectralEmbedding
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
mapStudent = {}
mapProblem = {}
entConcept = []
for p in collect_problem.find({}):
    entProblem.append(p)

for l in collect_userSubmissions.find({}):
    userId = l['user']['user']['id']
    if userId not in mapStudent:
        mapStudent[userId] = {}
    jageProblemContents = l['judgeResponseContents']
    submitAt = l['submitAt']
    for i in jageProblemContents:
        problemId = i['problemSetProblemId']
        if problemId not in mapProblem:
            mapProblem[problemId] = {}
        score = i['score']
        status = i['status']
        pScore = 0

        for p in entProblem:
            if p['id'] == problemId:
                pScore = p['score']
        if pScore != 0:
            if userId not in mapProblem[problemId]:
                mapProblem[problemId][userId] = {'log': [], 'best': i, "totalAttempts": 0, "totalScore": 0}
            mapProblem[problemId][userId]['totalAttempts'] += 1
            mapProblem[problemId][userId]['totalScore'] += score / pScore

            if problemId not in mapStudent[userId]:
                mapStudent[userId][problemId] = {'log': [], 'best': i, "totalAttempts": 0, "totalScore": 0}
            mapStudent[userId][problemId]['log'].append(i)
            mapStudent[userId][problemId]['totalAttempts'] += 1
            mapStudent[userId][problemId]['totalScore'] += score / pScore
            if mapStudent[userId][problemId]['best']['score'] < score:
                mapStudent[userId][problemId]['best'] = i

tsneXProblem = []
for p in mapProblem:
    tempS = {
        'id': p,
        'val': []
    }
    # print(len(mapStudent[s]))
    # for p in mapStudent[s]:
    #     print(p)
    val = []
    i = 0
    cRate = 0
    totalAttempts = 0
    bestScore = 0
    for s in mapStudent:
        sid = s
        # pScore = p['score']
        if sid in mapProblem[p]:
            # sScore = mapStudent[s][pid]['best']['score']
            # val.append(sScore / pScore)
            sScoreRate = mapProblem[p][sid]['totalScore'] / mapProblem[p][sid]['totalAttempts']
            val.append(sScoreRate)
            cRate += sScoreRate
            totalAttempts += mapProblem[p][sid]['totalAttempts']
            # bestScore += mapProblem[p][sid]['best']['score']
        else:
            val.append(0)
    tempS['val'] = val
    tempS['scoringRate'] = cRate
    tempS['totalAttempts'] = totalAttempts
    tempS['bestScore'] = bestScore
    tsneXProblem.append(tempS)

dataMat = []
idMat = []
for s in tsneXProblem:
    idMat.append(s['id'])
    dataMat.append(s['val'])
    i = 0
    for v in s['val']:
        if v < 1:
            i += 1

X = np.array(dataMat)  # [[12, 23, 3], [23, 45, 6], [4, 5, 7], [6, 3, 5]])
result = []
X_tsne = TSNE(n_components=2, perplexity=50, learning_rate=100, n_iter=5000).fit_transform(X)
color = ['c', 'b', 'g', 'r', 'm', 'y', 'k', 'w']
# X_tsne = MDS(n_components=2,).fit_transform(X)
# X_tsne = SpectralEmbedding(n_components=2).fit_transform(X)
kmeans = KMeans(n_clusters=3, random_state=0).fit(X_tsne)
ii = 0
for p in X_tsne:
    result.append({
        "id": idMat[ii],
        "x": float(p[0]),
        "y": float(p[1]),
        "kmeansC": int(kmeans.labels_[ii]),
        "scoringRate": float(tsneXProblem[ii]['scoringRate']),
        "totalAttempts": float(tsneXProblem[ii]['totalAttempts']),
        "bestScore": float(tsneXProblem[ii]['bestScore'])
    })
    plt.scatter(p[0], p[1], c=color[kmeans.labels_[ii]], edgecolors='r')
    plt.text(p[0], p[1], str(ii), fontdict={'family': 'serif', 'size': 15, 'color': color[kmeans.labels_[ii]]},
             ha='center', va='center')
    ii += 1
plt.show()

with open("proRel.json", 'w') as fw:
    json.dump(result, fw)
