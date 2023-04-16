import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["MOOCProblemVis"]

collect_course = mydb["course"]
collect_concept = mydb["concept"]
collect_problem = mydb["problem"]

collect_concept_course = mydb["concept_course"]
collect_concept_problem = mydb["concept_problem"]
collect_exercise_problem = mydb["exercise_problem"]

filter_concept = mydb["filterDS_concept"]
filter_concept_problem = mydb["filterDS_concept_problem"]
filter_exercise_problem = mydb["filterDS_exercise_problem"]
filter_problem = mydb["filterDS_problem"]

filter_concept.delete_many({})
filter_concept_problem.delete_many({})
filter_exercise_problem.delete_many({})
filter_problem.delete_many({})

# filter_exercise_problem = mydb["filterDS_exercise_problem"]
# ---------------
# myquery = {"concept": "K_链表_计算机科学与技术"}
# mydoc = collect_concept_course.find(myquery)
# course_id = []
# for x in mydoc:
#     course_id.append(x['course'])
# print(course_id)
#
# conceptQuery = {"course": course_id[0]}
# courseName = 'dataStructure'
#
# for c in course_id:
#     cQuery = {"id": c}
#     cDoc = collect_course.find(cQuery)
#     for cc in cDoc:
#       print(cc['name'])
# -----------------------
# {resource:{$elemMatch:{resource_id:"Ex_996975"}}}
# myquery = {"name": "数据结构（Data Structures）"}
myquery = {"id": "C_680992"}
mydoc = collect_course.find(myquery)
course_id = []
exerciseIds = []
# 筛选当前课程习题集
for x in mydoc:
    course_id.append(x['id'])
    re = x['resource']
    for r in re:
        if r['resource_id'].split("_")[0] == "Ex":
            exerciseIds.append(r['resource_id'])

filterProblem = []
filterConcept = []
filterExerciseProblem = []
filterConceptProblem = []

problemIds = []
# 依据习题集id筛选problem，及其关系
for eid in exerciseIds:
    eQuery = {"exercise": eid}
    eDoc = collect_exercise_problem.find(eQuery, {"_id": 0})
    for ep in eDoc:
        problemIds.append(ep['problem'])
        filterExerciseProblem.append(ep)

conceptIds = []
for pid in problemIds:
    pQuery = {"problem_id": int(pid.split("_")[1])}
    pDoc = collect_problem.find(pQuery, {"_id": 0})

    cpQuery = {"problem": pid}
    cpDoc = collect_concept_problem.find(cpQuery, {"_id": 0})
    for p in pDoc:
        filterProblem.append(p)
    for cp in cpDoc:
        conceptIds.append(cp['concept'])
        filterConceptProblem.append(cp)


for cid in conceptIds:
    cQuery = {"id": cid}
    cDoc = collect_concept.find(cQuery, {"_id": 0})
    for c in cDoc:
        filterConcept.append(c)


filter_exercise_problem.insert_many(filterExerciseProblem)
filter_problem.insert_many(filterProblem)
filter_concept_problem.insert_many(filterConceptProblem)
filter_concept.insert_many(filterConcept)

#
# # 依据exercise筛选problem
# i = 0
# p_id = []
# for c in course_id:
#     cQuery = {"course": c}
#     cDoc = collect_concept_course.find(cQuery)
#     for cc in cDoc:
#         concept_id.append(cc['concept'])
#         i += 1
# print(i, concept_id)
