import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["PTADATA"]

collect_concept = mydb["concepts"]
collect_problem = mydb["problems"]

collect_problem_problem = mydb["problem_problem"]

collect_problem_problem.delete_many({})

entProblemRel = []


collect_problem_problem.insert_many(entProblemRel)
