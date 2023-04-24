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
entStudent = []
for p in collect_problem.find({}):
    p['totalAttempts'] = 0
    p['acceptedAttempts'] = 0
    p['totalScore'] = 0
    p['accuracy'] = 0
    p['conCount'] = 0
    p['log'] = {}
    entProblem.append(p)
for l in collect_userSubmissions.find({}):
    print(l)
    userId = l['user']['user']['id']
    jageProblemContents = l['judgeResponseContents']
    submitAt = l['submitAt']
    for i in jageProblemContents:
        problemId = i['problemSetProblemId']
        score = i['score']
        status = i['status']

        for p in entProblem:
            if p['id'] == problemId:
                p['totalAttempts'] += 1
                if status == 'ACCEPTED':
                    p['acceptedAttempts'] += 1
                p['totalScore'] += score / p['score']
                print(p['log'].keys())
                if userId not in p['log']:
                    p['log'][userId] = [score, 1]
                else:
                    p['log'][userId] = [p['log'][userId][0], p['log'][userId][1] + 1]
                    if p['log'][userId][0] < score:
                        p['log'][userId] = [score, p['log'][userId][1]]

print(entProblem)

for r in collect_problem_concept.find({}):
    problemId = r['problem']
    for p in entProblem:
        if p['id'] == problemId:
            p['conCount'] += 1

for ep in entProblem:
    ep['scoringRate'] = ep['totalScore'] / ep['totalAttempts']
    ep['acceptedRate'] = ep['acceptedAttempts'] / ep['totalAttempts']
    num = 0
    cur = 0
    for l in ep['log']:
        num += 1
        print(l)
        if ep['log'][l][0] == ep['score']:
            cur += 1
    print(cur)
    if cur != 0:
        ep['accuracy'] = cur / num

ent_problem.insert_many(entProblem)
