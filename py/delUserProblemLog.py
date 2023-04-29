import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["PTADATA"]

collect_concept = mydb["concepts"]
collect_problem = mydb["problems"]

collect_problem_concept = mydb["problem_concept"]
collect_userSubmissions = mydb["submissions"]

ent_problem = mydb["ent_problem"]
ent_user = mydb["ent_student"]
ent_concept = mydb["ent_concept"]

ent_problem.delete_many({})
ent_user.delete_many({})
ent_concept.delete_many({})

entProblem = []
entStudent = {}
entConcept = []
for p in collect_problem.find({}):
    p['totalAttempts'] = 0
    p['acceptedAttempts'] = 0
    p['totalScore'] = 0
    p['accuracy'] = 0
    p['conCount'] = 0
    p['log'] = {}
    entProblem.append(p)

for c in collect_concept.find({}):
    c['totalAttempts'] = 0
    c['acceptedAttempts'] = 0
    c['scoringRate'] = 0
    c['accuracy'] = 0
    c['proCount'] = 0
    entConcept.append(c)

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
            entStudent[userId][problemId] = {'log': [i], 'best': i}
        entStudent[userId][problemId]['log'].append(i)
        if entStudent[userId][problemId]['best']['score'] < score:
            entStudent[userId][problemId]['best'] = i
        for p in entProblem:
            if p['id'] == problemId:
                p['totalAttempts'] += 1
                if status == 'ACCEPTED':
                    p['acceptedAttempts'] += 1
                p['totalScore'] += score / p['score']
                if userId not in p['log']:
                    p['log'][userId] = [score, 1]
                else:
                    p['log'][userId] = [p['log'][userId][0], p['log'][userId][1] + 1]
                    if p['log'][userId][0] < score:
                        p['log'][userId] = [score, p['log'][userId][1]]

pro_con_list = []
for r in collect_problem_concept.find({}):
    problemId = r['problem']
    conceptId = r['conceptId']
    pro_con_list.append(r)
    for p in entProblem:
        if p['id'] == problemId:
            p['conCount'] += 1

    # c['proCount'] += 1

for ep in entProblem:
    ep['scoringRate'] = ep['totalScore'] / ep['totalAttempts']
    ep['acceptedRate'] = ep['acceptedAttempts'] / ep['totalAttempts']
    num = 0
    cur = 0
    for l in ep['log']:
        num += 1
        if ep['log'][l][0] == ep['score']:
            cur += 1
    if cur != 0:
        ep['accuracy'] = cur / num

for c in entConcept:
    i = 0
    for r in pro_con_list:
        if str(r['conceptId']) == str(c['id']):
            i += 1
            problemId = r['problem']
            for p in entProblem:
                if p['id'] == str(problemId):
                    c['proCount'] += 1
                    c['totalAttempts'] += p['totalAttempts']
                    c['acceptedAttempts'] += p['acceptedAttempts']
                    c['scoringRate'] += p['scoringRate']
                    c['accuracy'] += p['accuracy']
    print(i, c)
    if c['totalAttempts'] != 0:
        c['acceptedRate'] = c['acceptedAttempts'] / c['totalAttempts']
    else:
        c['acceptedRate'] = 0
    if i != 0:
        c['scoringRate'] = c['scoringRate'] / i
        c['accuracy'] = c['accuracy'] / i

ent_problem.insert_many(entProblem)
ent_concept.insert_many(entConcept)
# ent_user.insert_many([entStudent])
