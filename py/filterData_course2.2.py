import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["MOOCProblemVis"]

collect_user_problem = mydb['user_problem']
filter_problem = mydb["filterDS_problem"]
filter_user_problem = mydb['filterDS_user_problem']

filter_user_problem.delete_many({})

problemIds = []
# 筛选当前课程习题集
for x in filter_problem.find({}):
    problemIds.append(x['problem_id'])

print(problemIds)

filterUserProblem = []

conceptIds = []

for up in collect_user_problem.find({}, {"_id": 0}):

    # print(up['problem_id'])
    pid = int(up['problem_id'].split("_")[1])
    # print(pid)
    if pid in problemIds:
        filterUserProblem.append(up)

# filter_concept.insert_many(filterConcept)
filter_user_problem.insert_many(filterUserProblem)