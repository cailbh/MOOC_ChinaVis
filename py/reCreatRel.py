import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["PTADATA"]

collect_concept = mydb["concepts"]
collect_problem = mydb["problems"]

collect_problem_concept = mydb["createdRel"]
collect_userSubmissions = mydb["submissions"]

ent_rel_Rew = mydb["createdRelNew"]

ent_rel_Rew.delete_many({})

entProblem = []
entStudent = {}
entRel = []
newRel = []
for r in collect_problem_concept.find({}):
    problemId = r['problem']
    conceptId = r['conceptId']
    if conceptId == '':



ent_rel_Rew.insert_many(entRel)
ent_concept.insert_many(entConcept)
# ent_user.insert_many([entStudent])
