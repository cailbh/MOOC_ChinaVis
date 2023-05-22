import pymongo
import json
import time
from datetime import datetime
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
entStudent = {}
entConcept = []


def t2s(t):
    rq, ti = t.strip().split("T")
    tim, z = ti.split("Z")

    st = str(rq) + ' ' + str(tim)
    dt = datetime.strptime(st, '%Y-%m-%d %H:%M:%S')
    tp = dt.timetuple()

    return time.mktime(tp)


def s2t(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d:%02d" % (h, m, s)


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
        pScore = 0

        for p in entProblem:
            if p['id'] == problemId:
                pScore = p['score']

        if pScore != 0:
            if problemId not in entStudent[userId]:
                entStudent[userId][problemId] = {'log': [], 'best': i, "totalAttempts": 0, "totalScore": 0,
                                                 "timeStamp": 0, 'bestScoreRate': 0}
            entStudent[userId][problemId]['log'].append(i)

            entStudent[userId][problemId]['totalAttempts'] += 1
            entStudent[userId][problemId]['timeStamp'] += t2s(l['submitAt'])
            entStudent[userId][problemId]['totalScore'] += score / pScore
            # print(score / pScore)
            if entStudent[userId][problemId]['best']['score'] < score:
                entStudent[userId][problemId]['best'] = i
                entStudent[userId][problemId]['bestScoreRate'] = entStudent[userId][problemId]['best']['score'] / pScore

# print(entStudent)
tsneXStudent = []
for s in entStudent:
    tempS = {
        'id': s,
        'val': []
    }
    # print(len(entStudent[s]))
    # for p in entStudent[s]:
    #     print(p)
    val = []
    i = 0
    cRate = 0
    totalAttempts = 0
    bestScore = 0
    bestScoreRate = 0
    acceptedNUm = 0
    ctimeS = 0
    for p in entProblem:
        pid = p['id']
        pScore = p['score']
        if pid in entStudent[s]:
            # sScore = entStudent[s][pid]['best']['score']
            # val.append(sScore / pScore)
            sScoreRate = entStudent[s][pid]['totalScore'] / entStudent[s][pid]['totalAttempts']
            cRate += sScoreRate
            ctimeS += entStudent[s][pid]['timeStamp'] / entStudent[s][pid]['totalAttempts']
            i += 1
            totalAttempts += entStudent[s][pid]['totalAttempts']
            bestScore += entStudent[s][pid]['best']['score']
            bestScoreRate += entStudent[s][pid]['bestScoreRate']
            # val.append(sScoreRate)
            val.append(bestScoreRate)
            if entStudent[s][pid]['best']['score'] == pScore:
                acceptedNUm += 1
        else:
            val.append(0)

    tempS['val'] = val
    tempS['scoringRate'] = cRate / i
    tempS['totalAttempts'] = totalAttempts
    tempS['acceptedNum'] = acceptedNUm
    tempS['bestScore'] = bestScore
    tempS['bestScoreRate'] = bestScoreRate/i
    tempS['time'] = ctimeS / i
    tsneXStudent.append(tempS)

dataMat = []
idMat = []
for s in tsneXStudent:
    idMat.append(s['id'])
    dataMat.append(s['val'])
    i = 0
    for v in s['val']:
        if v < 1:
            i += 1

X = np.array(dataMat)  # [[12, 23, 3], [23, 45, 6], [4, 5, 7], [6, 3, 5]])
result = []
X_tsne = TSNE(n_components=2, perplexity=25, learning_rate=500, n_iter=5000).fit_transform(X)
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
        "scoringRate": float(tsneXStudent[ii]['scoringRate']),
        "bestScoringRate": float(tsneXStudent[ii]['bestScoreRate']),
        "totalAttempts": float(tsneXStudent[ii]['totalAttempts']),
        "bestScore": float(tsneXStudent[ii]['bestScore']),
        "time": float(tsneXStudent[ii]['time']),
        "acceptedNum": float(tsneXStudent[ii]['acceptedNum']),
    })
    plt.scatter(p[0], p[1], c=color[kmeans.labels_[ii]], edgecolors='r')
    plt.text(p[0], p[1], str(ii), fontdict={'family': 'serif', 'size': 15, 'color': color[kmeans.labels_[ii]]},
             ha='center', va='center')
    ii += 1
plt.show()

with open("group.json", 'w') as fw:
    json.dump(result, fw)






















