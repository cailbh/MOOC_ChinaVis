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
filter_problem = mydb["filterDS_problem"]
# filter_exercise_problem = mydb["filterDS_exercise_problem"]
# ---------------
myquery = {"concept": "K_链表_计算机科学与技术"}
mydoc = collect_concept_course.find(myquery)
course_id = []
for x in mydoc:
    course_id.append(x['course'])
print(course_id)

conceptQuery = {"course": course_id[0]}
courseName = 'dataStructure'

for c in course_id:
    cQuery = {"id": c}
    cDoc = collect_course.find(cQuery)
    for cc in cDoc:
      print(cc['name'])
# -----------------------
myquery = {"name": "操作系统"}
mydoc = collect_course.find(myquery)
course_id = []
for x in mydoc:
    course_id.append(x['id'])
print(course_id)

conceptQuery = {"course": course_id[0]}
courseName = 'dataStructure'

# 依据课程筛选概念-课程联系
i = 0
concept_id = []
for c in course_id:
    cQuery = {"course": c}
    cDoc = collect_concept_course.find(cQuery)
    for cc in cDoc:
        concept_id.append(cc['concept'])
        i += 1
print(i, concept_id)

# 筛选概念
# ----------------
# filterConcepts = []
# for c in concept_id:
#     cQuery = {"id": c}
#     cDoc = collect_concept.find(cQuery, {"_id": 0, "id": 1, "name": 1, "context": 1})
#     for cc in cDoc:
#       filterConcepts.append(cc)
#
# filter_concept.insert_many(filterConcepts)
# -------------------------
#
# 筛选问题
# -------------------
# filterConceptsProblem = []
# filterProblem = []
# for c in concept_id:
#     cQuery = {"concept": c}
#     cDoc = collect_concept_problem.find(cQuery, {"_id": 0, "concept": 1, "problem": 1})
#     for cc in cDoc:
#         # print(int(cc['problem'].split("_")[1]))
#         filterConceptsProblem.append(cc)
#
#         pQuery = {"problem_id": int(cc['problem'].split("_")[1])}
#         pDoc = collect_problem.find(pQuery, {"_id": 0})
#         for p in pDoc:
#             filterProblem.append(p)
#
# filter_problem.insert_many(filterProblem)
# filter_concept_problem.insert_many(filterConceptsProblem)
# -------------------------
# filter_concept.insert_many(filterConceptsProblem)

# filterDoc = collect_concept_course.find(conceptQuery)
# # filterDB =
# for r in filterDoc:
#     print(r)
