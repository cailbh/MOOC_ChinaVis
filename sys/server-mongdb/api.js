/* eslint-disable no-unused-vars */
"use strict";
const models = require('./db');
const express = require('express');
const router = express.Router();


router.post('/api/test/createData', (req, res) => {
    // 这里的req.body能够使用就在index.js中引入了const bodyParser = require('body-parser')
    let newAccount = new models.Login({
        account: req.body.account,
        password: req.body.password
    });
    // 保存数据newAccount数据进mongoDB
    newAccount.save((err, data) => {
        if (err) {
            res.send(err);
        } else {
            res.send('createAccount successed');
        }
    });
});
// 获取问题接口
router.get('/api/problem/allProblem', (req, res) => {
    // 通过模型去查找数据库
    models.Problem.find((err, data) => {
        if (err) {
            res.send(err);
        } else {
            res.send(data);
        }
    });
});


// 获取user做题记录接口
router.get('/api/Submission/allLog', (req, res) => {
    // 通过模型去查找数据库
    models.Submission.find((err, data) => {
        if (err) {
            res.send(err);
        } else {
            res.send(data);
        }
    });
});
// 获取概念接口
router.get('/api/concept/allConcept', (req, res) => {
    // 通过模型去查找数据库
    models.Concept.find((err, data) => {
        if (err) {
            res.send(err);
        } else {
            res.send(data);
        }
    });
});
// 获取概念树接口
router.get('/api/concept/conceptTree', (req, res) => {
    // 通过模型去查找数据库
    models.ConceptTree.find((err, data) => {
        if (err) {
            res.send(err);
        } else {
            res.send(data);
        }
    });
});
// 获取学生接口
router.get('/api/student/allStudent', (req, res) => {
    // 通过模型去查找数据库
    const aggregate = [
        {
            "$project":
            {
                "_id": 0
            }
        }
    ]
    models.Student.aggregate(aggregate).then((err, data) => {
        if (err) {
            res.send(err);
        } else {
            res.send(data);
        }
    });
});

// 获取问题关联概念接口
router.get('/api/conceptProblem/allRel', (req, res) => {
    // 通过模型去查找数据库
    models.ProblemConcept.find((err, data) => {
        if (err) {
            res.send(err);
        } else {
            res.send(data);
        }
    });
});
router.get('/api/cube/searchCubeMsg', (req, res) => {
    console.log("req", req.query, "req")
    var pageNum = req.query['page']
    var pageSize = req.query['pagesize']
    console.log(pageSize, pageNum)
    const aggregate = [
        {
            "$project":
            {
                "_id": 0,
                "userName": 1,
                "courseName": 1,
                "conceptName": 1,
                //   "cnt": {"$size": '$seq'}
            }
        },
        //  {"$sort": {"cnt": -1}},
        // {"$match": {"cnt": {"$gt": 300, "$lte": 1000}}},
        { "$skip": (parseInt(pageNum) - 1) * parseInt(pageSize) },
        { "$limit": parseInt(pageSize) }
    ]
    // 通过模型去查找数据库
    models.Cube.aggregate(aggregate).then((err, data) => {
        if (err) {
            res.send(err);
            console.log(err)
        } else {
            res.send([data]);
        }
    });
});
module.exports = router;