# 去除没有概念相连的问题

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["MOOCProblemVis"]

collect_user_problem = mydb['user_problem']
filter_problem = mydb["filterDS_problem"]
filter_user_problem = mydb['filterDS_user_problem']
