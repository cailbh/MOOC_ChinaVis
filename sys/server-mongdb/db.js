// Schema、Model、Entity或者Documents的关系:Schema生成Model，Model创造Entity，Model和Entity都可对数据库操作造成影响，但Model比Entity更具操作性。
const mongoose = require('mongoose');
// 连接数据库 
mongoose.connect('mongodb://127.0.0.1:27017/MOOCProblemVis');

// 为这次连接绑定事件
const db = mongoose.connection;
db.once('error', () => console.log('Mongo connection error'));
db.once('open', () => console.log('Mongo connection successed'));
/************** 定义模式Schema **************/
const problemSchema = mongoose.Schema({
    problem_id: Number,
    title: String,
    content: String,
    option: Object,
    answer: String,
    score: Number,
    type: Number,
    typetext: String,
    location: String,
    context_id: Array,
    exercise_id: String,
    lanuage: String,
});
const userProblemSchema = mongoose.Schema({
    log_id: String,
    problem_id: String,
    user_id:String,
    is_correct:Number,
    attempts:Number,
    score:Number,
    submit_time:String
});

const conceptProblemSchema = mongoose.Schema({
    concept: String,
    problem: String
})
const conceptSchema = mongoose.Schema({
    id: String,
    name: String,
    context:Array
})


/************** 定义模型Model **************/
const Models = {
   
    Concept: mongoose.model('concept', conceptSchema, 'filterDS_concept'),
    UserProblem: mongoose.model('userProblem', userProblemSchema, 'filterDS_user_problem'),
    ConceptProblem: mongoose.model('conceptProblem', conceptProblemSchema, 'filterDS_concept_problem'),
    Problem:mongoose.model('problem', problemSchema, 'filterDS_problem'),
}

module.exports = Models;
