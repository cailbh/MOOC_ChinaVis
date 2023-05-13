<template>
  <div id="root">
    <!-- <button1 ref="button1"></button1>
    <button v-on:click="clickHandler">按钮</button> -->
    <!-- <svg width="1200" height="1000"></svg> -->

    <div id="Container">
      <!-- <div id="Container-back"></div> -->
      <div id="head">

        <!-- <Head></Head> -->
      </div>
      <div id="allBody">
        <div id="controlPanel" class="panel">
          <ControlPanel @getToolState="getToolState"></ControlPanel>
        </div>
        <div id="procPanel" class="panel">
          <ProcPanel></ProcPanel>
        </div>
        <div id="graphContainer" v-show="showGraph" class="panel">
          <Graph :toolsState="toolsState"></Graph>
        </div>
        <!-- <div id="overviewPanel" class="panel">
          <OverviewPanel></OverviewPanel>
        </div> -->
        <!-- <transition name="sceneTran"> -->

        <!-- <div id="editPanel" class="panel"  v-if='showEdit==true'>
          <EditPanel></EditPanel>
        </div> -->
        <div id="scatterPanel" class="panel">
          <Scatter></Scatter>
        </div>
        <div id="netPPanel" class="panel">
          <NetPPanel></NetPPanel>
        </div>
        <!-- </transition> -->
      </div>
    </div>
  </div>
</template>

<script>
import Head from "@/components/Header/index.vue";
import Graph from '@/components/Graph/index.vue';
import Scatter from '@/components/Scatter/index.vue';
import ProcPanel from '@/components/ProblemContentPanel/index.vue';

import ControlPanel from '@/components/ControlPanel/index.vue'
import NetPPanel from '@/components/NetProblemPanel/index.vue';
import GroupJson from "@/assets/json/group.json";
import SetJson from "@/assets/json/quz.json";
import tools from "@/utils/tools.js";
export default {
  components: { Head, Graph, Scatter, ProcPanel, NetPPanel, ControlPanel },
  /* eslint-disable no-unused-vars */
  data() {
    return {
      problemsData: [],
      submissionsData: [],
      groupData: GroupJson,
      setTimeData: SetJson,
      netData: [],
      problemRelByConcept: [],
      problemListByConcept: [],
      studentsData: [],
      conceptsData: [],
      SelectStudentList: [],
      conceptTree: [],
      proSetData: [],
      problemConceptData: [],
      userProblemData: [],
      toolsState: {},
      timer: null,
      showVideo: true,
      showGraph: true,
      showEdit: false,
      selectEntId: "0",
      selectEnt: "0",
      toolState: {},
      timeDur: "",
      videoTime: 0,
      windowWidth: document.documentElement.clientWidth, //实时屏幕宽度
      windowHeight: document.documentElement.clientHeight, //实时屏幕高度
      // attrColorList:[
      //   "rgb(255, 77, 109)",
      //   "rgb(255, 113, 212)",
      //   "rgb(255, 120, 90)",
      //   "rgb(255, 159, 28)",
      //   "rgb(6, 214, 160)",
      //   "rgb(125, 98, 211)",
      // ],
      attrColorList:[
        "rgb(253, 174, 134)",
        "rgb(115, 230, 163)",
        "rgb(255, 233, 141)",
        "rgb(56, 191, 201)",
        "rgb(255, 122, 125)",
        "rgb(224, 207, 243)",
      ],
      attrColorLightList:[
        "rgb(255, 176, 200)",
        "rgb(255, 184, 240)",
        "rgb(255, 173, 159)",
        "rgb(255, 208, 133)",
        "rgb(145, 226, 199)",
        "rgb(167, 158, 221)",
      ],
      stuColorList:[
        "rgb(254, 33, 79)",
        "rgb(252, 171, 1)",
        "rgb(85, 6, 134)",
        "rgb(203, 64, 156)",
        "rgb(73, 178, 101)",
      ],
      mcolor: [
        "rgb(255,60,60)",
        "rgb(155,20,100)",
        "rgb(255,83,255)",
        "rgb(200,100,50)",
        "rgb(235,135,162)",
        "rgb(200,200,102)",
        "rgb(255,178,101)",
        "rgb(63,151,134)",
        "rgb(83,155,255)",
        "rgb(50,200,120)",
        "rgb(2,50,200)",
        "rgb(0,122,244)",
        "rgb(150,122,244)",
        "rgb(168,168,255)",
        "rgb(200,200,200)",
      ],
      mLigntcolor: [
        "#ff9c9c",
        "#cc88b0",
        "#ffa8ff",
        "#e3b097",
        "#f4c3d0",
        "#f4f4d0",
        "#ffd8b1",
        "#9ecac2",
        "#a8ccff",
        "#97e3ba",
        "#6f8be0",
        "rgb(0,122,244)",
        "#b6a2f7",
        "rgb(168,168,255)",
        "rgb(200,200,200)",
      ],
      marge: {
        top: 6,
        right: 10,
        bottom: 16,
        left: 6,
      },
      barType: "Teaching",
    };
  },
  watch: {
    toolState(val) {
      if (val == 'edit')
        this.showEdit = true;
      else
        this.showEdit = false;
    },
    selectEnt(val) {
      this.selectEntId = val;
    },
    timeDur() {
    },
    cube_data() {
      this.$nextTick(() => { });
    },
    cluData() {
      this.$nextTick(() => {
      });
    },
  },
  methods: {
    getProblems() {
      const _this = this;
      let data = [];
      this.$http
        // .get("/api/problem/allProblem", { params: { name: "12345" } }, {})
        .get("/api/problem/allProblem", {}, {})
        .then((response) => {
          _this.problemsData = response.body;
        });
    },
    getConcept() {
      const _this = this;
      this.$http
        .get("/api/concept/allConcept", {}, {})
        .then((response) => {
          _this.conceptsData = response.body;
          _this.$bus.$emit("Concept", _this.conceptsData);
        });
    },
    getConceptTree() {
      const _this = this;
      this.$http
        .get("/api/concept/conceptTree", {}, {})
        .then((response) => {
          _this.conceptTree = response.body;
          _this.$bus.$emit("ConceptTree", _this.conceptTree);
        });
    },
    getSubmissions() {
      const _this = this;
      this.$http.get("/api/Submission/allLog", {}, {})
        .then((response) => {
          _this.submissionsData = response.body;
          _this.$bus.$emit("Submission", _this.submissionsData);
          _this.calStudent();
          _this.calcNetData();
        });
    },
    getProblemConcept() {
      const _this = this;
      this.$http.get("/api/conceptProblem/allRel", {}, {})
        .then((response) => {
          _this.problemConceptData = response.body;
          _this.$bus.$emit("Pro_Con", _this.problemConceptData);
        });
    },
    getStudents() {
      const _this = this;
      this.$http.get("/api/student/allStudent", {}, {})
        .then((response) => {
          _this.studentsData = response.body;
        });
    },
    calStudent() {
      const _this = this;
      let entStudent = [];
      let entConcept = [];
      let entProblem = [];
      let entProSet = [];

      let SelectStudentList = _this.SelectStudentList;
      let setTimeData = _this.setTimeData;

      let conceptTree = tools.deepClone(_this.conceptTree);
      let problemsData = tools.deepClone(_this.problemsData);
      let submissionsData = tools.deepClone(_this.submissionsData);
      let problemConceptData = tools.deepClone(_this.problemConceptData);
      
      let groupData = _this.groupData;

      console.log(SelectStudentList);

      let valetemp = {
        'totalTimeDur':0,
        'timeDur':0,
        'totalAttempts':0,
        'acceptedAttempts':0,
        'totalAttemptsPeople':0,
        'acceptedAttemptsPeople':0,
        'totalScore':0,
        'accuracy':0,
        'conCount':0,
        'gvjg':-1,
        'conList':[],
        'scoringRate':0,
        'stu':[]
      }
        let tempStudent = [];
        let tempAllStudent = {};
        let StudentMap = {};
      for (let i = 0; i < groupData.length; i++) {
        let uid = groupData[i]['id'];
        let tp = tools.deepClone(valetemp);
        tp['id'] = uid;
        tempAllStudent[uid] = (tp);
      }
      valetemp['stuData']= tools.deepClone(tempAllStudent);
      setTimeData.forEach(set=>{
        set['timeSt'] = tools.time2mktime(set['time']);
      })
      for (let i = 0; i < SelectStudentList.length; i++) {
          for(let j=0;j<SelectStudentList[i].length;j++){
              StudentMap[SelectStudentList[i][j]] = i;
          }
          tempStudent.push(tools.deepClone(valetemp));
      }
      for (let i = 0; i < problemsData.length; i++) {
        // let id = problemsData[i]['id'];
        // problemsData[i] = tools.deepClone(valetemp);
        // problemsData[i]['id'] = id;
        problemsData[i]['totalTimeDur'] = 0;
        problemsData[i]['timeDur'] = 0;
        problemsData[i]['totalAttempts'] = 0;
        problemsData[i]['acceptedAttempts'] = 0;
        problemsData[i]['totalAttemptsPeople'] = 0;
        problemsData[i]['acceptedAttemptsPeople'] = 0;
        problemsData[i]['totalScore'] = 0;
        problemsData[i]['accuracy'] = 0;
        problemsData[i]['conCount'] = 0;
        problemsData[i]['conList'] = [];
        problemsData[i]['scoringRate'] = 0;
        problemsData[i]['groupVal'] = tools.deepClone(tempStudent);
        problemsData[i]['stu'] = [];
        problemsData[i]['stuData'] = tools.deepClone(tempAllStudent);
        let proSetId = problemsData[i]['problemSetId'];

        let protime = setTimeData.find(function(s){return s['problemSetId'] == proSetId})['timeSt'];

        problemsData[i]['timeSp'] = protime;
        
        if (entProSet.find(function (es) { return es['id'] == proSetId; }) == undefined) {
          entProSet.push({
            "id": proSetId,
            "pro": [],
            'totalScore': 0,
          })
        }
        let ePS = entProSet.find(function (es) { return es['id'] == proSetId; });
        ePS['pro'].push(problemsData[i]);
        ePS['totalScore'] += problemsData[i]['score'];
      }
      for (let c = 0; c < conceptTree.length; c++) {
        conceptTree[c]['timeDur'] = 0;
        conceptTree[c]['totalAttempts'] = 0;
        conceptTree[c]['acceptedAttempts'] = 0;
        conceptTree[c]['totalScore'] = 0;
        conceptTree[c]['accuracy'] = 0;
        conceptTree[c]['proCount'] = 0;
        conceptTree[c]['scoringRate'] = 0;
        conceptTree[c]['groupVal'] = tools.deepClone(tempStudent);

      }
      for (let l = 0; l < submissionsData.length; l++) {
        let userId = submissionsData[l]['user']['user']['id'];

        // if (SelectStudentList.indexOf(userId)!=-1){
          if (entStudent.find(function (eS) { return eS['id'] == userId; }) == undefined) {
            entStudent.push({ 'id': userId, "pro": [] });
          }
          let entStu = entStudent.find(function (eS) { return eS['id'] == userId; });
          let jageProblemContents = submissionsData[l]['judgeResponseContents'];
          let submitAt = submissionsData[l]['submitAt'];
          
          for (let i = 0; i < jageProblemContents.length; i++) {
            let problemId = jageProblemContents[i]['problemSetProblemId'];
            let score = jageProblemContents[i]['score'];
            let proStatus = jageProblemContents[i]['status'];

            if (entStu['pro'].find(function (p) { return p['id'] == problemId; }) == undefined) {
              entStu['pro'].push({ "id": problemId, 'log': [], 'best': jageProblemContents[i], "totalAttempts": 0, "totalScore": 0 })
            }
            
            let eSP = entStu['pro'].find(function (p) { return p['id'] == problemId; })
            // eSP['log'].push(jageProblemContents[i]);

            if (eSP['best']['score'] < score) {
              eSP['best'] = jageProblemContents[i];
            }
            let pro = problemsData.find(function (p) { return p['id'] == problemId; })
            if (pro != undefined) {
              let timeSp = pro['timeSp']
              // if (SelectStudentList.indexOf(userId)!=-1){
                // console.log(StudentMap[userId],pro['groupVal'])
              if(StudentMap[userId]!=undefined){
                pro['groupVal'][StudentMap[userId]]['stuData'][userId]['totalAttempts'] += 1;
                pro['groupVal'][StudentMap[userId]]['stuData'][userId]['gvjg'] = 1;
                pro['groupVal'][StudentMap[userId]]['stu'][userId] = 0;
                pro['groupVal'][StudentMap[userId]]['totalAttempts'] +=1;
                pro['groupVal'][StudentMap[userId]]['totalTimeDur'] += tools.time2mktime(submitAt) - timeSp;
                if (proStatus == 'ACCEPTED'){
                  pro['groupVal'][StudentMap[userId]]['acceptedAttempts'] += 1;
                  pro['groupVal'][StudentMap[userId]]['stuData'][userId]['acceptedAttempts'] += 1;
                  pro['groupVal'][StudentMap[userId]]['stu'][userId] = 1;
                }
                pro['groupVal'][StudentMap[userId]]['totalScore'] += score / pro['score'];
                
                pro['groupVal'][StudentMap[userId]]['stuData'][userId]['totalScore'] += score / pro['score'];
              }
              pro['stuData'][userId]['totalAttempts'] += 1;
              pro['stuData'][userId]['totalTimeDur'] += tools.time2mktime(submitAt) - timeSp;

              pro['stu'][userId] =0;
              pro['totalAttempts'] += 1;
              pro['totalTimeDur'] += tools.time2mktime(submitAt) - timeSp;

              eSP['totalAttempts'] += 1;
              if (proStatus == 'ACCEPTED'){
                
                pro['acceptedAttempts'] += 1;
                pro['stu'][userId] = 1;

                pro['stuData'][userId]['acceptedAttempts'] += 1;

              }
              pro['totalScore'] += score / pro['score'];
              
              pro['stuData'][userId]['totalScore'] += score / pro['score'];
              // }
              eSP['totalScore'] += score / pro['score'];
            }
          }
        // }
      }
      for (let i = 0; i < problemConceptData.length; i++) {
        let conceptId = problemConceptData[i]['conceptId'];
        let problemId = problemConceptData[i]['problem'];
        let Pro = problemsData.find(function (p) { return p['id'] == problemId; });
        Pro['conCount']++;
        Pro['conList'].push(conceptId);
      }


      for (let i = 0; i < problemsData.length; i++) {
        if (problemsData[i]['totalAttempts'] != 0) {
          problemsData[i]['scoringRate'] = problemsData[i]['totalScore'] / problemsData[i]['totalAttempts'];
          problemsData[i]['acceptedRate'] = problemsData[i]['acceptedAttempts'] / problemsData[i]['totalAttempts'];
          problemsData[i]['timeDur'] = problemsData[i]['totalTimeDur'] / problemsData[i]['totalAttempts'];
        }
        let groupVal = problemsData[i]['groupVal'];
        
        for (let j = 0; j < groupVal.length; j++) {
          if (groupVal[j]['totalAttempts'] != 0) {
            groupVal[j]['scoringRate'] = groupVal[j]['totalScore'] / groupVal[j]['totalAttempts'];
            groupVal[j]['acceptedRate'] = groupVal[j]['acceptedAttempts'] / groupVal[j]['totalAttempts'];
            groupVal[j]['timeDur'] = groupVal[j]['totalTimeDur'] / groupVal[j]['totalAttempts'];

            let stuData = groupVal[j]['stuData'];
            Object.keys(stuData).forEach((s) => {

              if (stuData[s]['totalAttempts'] != 0) {
                stuData[s]['scoringRate'] = stuData[s]['totalScore'] / stuData[s]['totalAttempts'];
                stuData[s]['acceptedRate'] = stuData[s]['acceptedAttempts'] / stuData[s]['totalAttempts'];
                // stuData[s]['timeDur'] = stuData[s]['totalTimeDur'] / stuData[s]['totalAttempts'];
              }
            })
          }
        }

        let stuData = problemsData[i]['stuData'];
        Object.keys(stuData).forEach((s)=>{
            
          if (stuData[s]['totalAttempts'] != 0) {
            stuData[s]['scoringRate'] = stuData[s]['totalScore'] / stuData[s]['totalAttempts'];
            stuData[s]['acceptedRate'] = stuData[s]['acceptedAttempts'] / stuData[s]['totalAttempts'];
            stuData[s]['timeDur'] = stuData[s]['totalTimeDur'] / stuData[s]['totalAttempts'];
          }
        })
        
        let num = 0;
        let cur = 0;
        let stu = problemsData[i]['stu'];
        Object.keys(stu).forEach((s)=>{
          if(stu[s]==1){
            num++;
            cur++;
          }
          if(stu[s]==0){
            num++;
          }
        })
        // for l in ep['log']:
        //     num += 1
        //     if ep['log'][l][0] == ep['score']:
        //         cur += 1
        // if cur != 0:
        problemsData[i]['totalAttemptsPeople'] = num;
        problemsData[i]['acceptedAttemptsPeople'] = cur;
      }
      for (let c = 0; c < conceptTree.length; c++) {
        let pcount = 0;
        for (let i = 0; i < problemConceptData.length; i++) {
          let conceptId = problemConceptData[i]['conceptId'];
          if (conceptId == conceptTree[c]['id']) {
            pcount++;
            let problemId = problemConceptData[i]['problem'];
            let ProBycon = problemsData.find(function (p) { return p['id'] == problemId; });
            conceptTree[c]['proCount'] += 1;
            conceptTree[c]['totalAttempts'] += ProBycon['totalAttempts'];
            conceptTree[c]['acceptedAttempts'] += ProBycon['acceptedAttempts'];
            conceptTree[c]['scoringRate'] += ProBycon['scoringRate'];
            conceptTree[c]['accuracy'] += ProBycon['accuracy'];
            conceptTree[c]['totalAttemptsPeople'] = ProBycon['totalAttemptsPeople'];
            conceptTree[c]['acceptedAttemptsPeople'] = ProBycon['acceptedAttemptsPeople'];
          }
        }
        if (conceptTree[c]['totalAttempts'] != 0)
          conceptTree[c]['acceptedRate'] = conceptTree[c]['acceptedAttempts'] / conceptTree[c]['totalAttempts'];
        else
          conceptTree[c]['acceptedRate'] = 0;
        if (pcount != 0) {
          conceptTree[c]['scoringRate'] = conceptTree[c]['scoringRate'] / pcount;
          conceptTree[c]['accuracy'] = conceptTree[c]['accuracy'] / pcount;
        }
      }
      let logLen = 0;
      for (let i = 0; i < entStudent.length; i++) {
        let tempProSetScore = [];
        for (let j = 0; j < entProSet.length; j++) {
          tempProSetScore.push({
            "id": entProSet[j]['id'],
            "totalScore": entProSet[j]['totalScore'],
            "score": 0
          })
        }
        for (let l = 0; l < entStudent[i]['pro'].length; l++) {
          let proId = entStudent[i]['pro'][l]['id'];
          let proSetDa = problemsData.find(function (ep) { return ep['id'] == proId })
          if (proSetDa != undefined) {
            let proSetId = proSetDa['problemSetId'];
            let bestScore = entStudent[i]['pro'][l]['best']['score'];
            if (bestScore == NaN) {

            }

            tempProSetScore.find(function (tpss) { return tpss['id'] == proSetId })['score'] += bestScore;
          }
        }
        entStudent[i]['proSetScore'] = tempProSetScore;
      }
      console.log(problemsData,entProSet,entStudent)
      _this.studentsData = entStudent;
      _this.$bus.$emit("Student", _this.studentsData);
      _this.proSetData = entProSet;
      _this.$bus.$emit("proSet", _this.proSetData);
      _this.conceptTree = conceptTree;
      _this.$bus.$emit("ConceptTree", _this.conceptTree);
      _this.problemsData = problemsData;
      _this.$bus.$emit("allProblem", _this.problemsData);
      _this.calcNetData();
    },
    calStudentbyGroup() {
      const _this = this;
      let entStudent = [];
      let entConcept = [];
      let entProblem = [];
      let entProSet = [];

      let SelectStudentList = _this.SelectStudentList;

      let conceptTree = tools.deepClone(_this.conceptTree);
      let problemsData = tools.deepClone(_this.problemsData);
      let submissionsData = tools.deepClone(_this.submissionsData);
      let problemConceptData = tools.deepClone(_this.problemConceptData);

      console.log(SelectStudentList);
      let tempStudent = [];
      for (let i = 0; i < SelectStudentList.length; i++) {
        let curnodelist = SelectStudentList[i];
        tempStudent.push([])
      }
      
      for (let i = 0; i < problemsData.length; i++) {
        problemsData[i]['totalAttempts'] = 0;
        problemsData[i]['acceptedAttempts'] = 0;
        problemsData[i]['totalAttemptsPeople'] = 0;
        problemsData[i]['acceptedAttemptsPeople'] = 0;
        problemsData[i]['totalScore'] = 0;
        problemsData[i]['accuracy'] = 0;
        problemsData[i]['conCount'] = 0;
        problemsData[i]['conList'] = [];
        problemsData[i]['scoringRate'] = 0;
        problemsData[i]['stu'] = tools.deepClone(tempStudent);
        let proSetId = problemsData[i]['problemSetId'];
        if (entProSet.find(function (es) { return es['id'] == proSetId; }) == undefined) {
          entProSet.push({
            "id": proSetId,
            "pro": [],
            'totalScore': 0,
          })
        }
        let ePS = entProSet.find(function (es) { return es['id'] == proSetId; });
        ePS['pro'].push(problemsData[i]);
        ePS['totalScore'] += problemsData[i]['score'];
      }
      for (let c = 0; c < conceptTree.length; c++) {
        conceptTree[c]['totalAttempts'] = 0;
        conceptTree[c]['acceptedAttempts'] = 0;
        conceptTree[c]['totalScore'] = 0;
        conceptTree[c]['accuracy'] = 0;
        conceptTree[c]['proCount'] = 0;
        conceptTree[c]['scoringRate'] = 0;

      }
      for (let l = 0; l < submissionsData.length; l++) {
        let userId = submissionsData[l]['user']['user']['id'];

        // if (SelectStudentList.indexOf(userId)!=-1){
          if (entStudent.find(function (eS) { return eS['id'] == userId; }) == undefined) {
            entStudent.push({ 'id': userId, "pro": [] });
          }
          let entStu = entStudent.find(function (eS) { return eS['id'] == userId; });
          let jageProblemContents = submissionsData[l]['judgeResponseContents'];
          let submitAt = submissionsData[l]['submitAt'];
          for (let i = 0; i < jageProblemContents.length; i++) {
            let problemId = jageProblemContents[i]['problemSetProblemId'];
            let score = jageProblemContents[i]['score'];
            let proStatus = jageProblemContents[i]['status'];

            if (entStu['pro'].find(function (p) { return p['id'] == problemId; }) == undefined) {
              entStu['pro'].push({ "id": problemId, 'log': [], 'best': jageProblemContents[i], "totalAttempts": 0, "totalScore": 0 })
            }
            
            let eSP = entStu['pro'].find(function (p) { return p['id'] == problemId; })
            // eSP['log'].push(jageProblemContents[i]);

            if (eSP['best']['score'] < score) {
              eSP['best'] = jageProblemContents[i];
            }
            let pro = problemsData.find(function (p) { return p['id'] == problemId; })
            if (pro != undefined) {
              // if (SelectStudentList.indexOf(userId)!=-1){
              pro['stu'][userId] =0;
              pro['totalAttempts'] += 1;
              eSP['totalAttempts'] += 1;
              if (proStatus == 'ACCEPTED'){
                pro['acceptedAttempts'] += 1;
                pro['stu'][userId] = 1;
              }
              pro['totalScore'] += score / pro['score'];
              // }
              eSP['totalScore'] += score / pro['score'];
            }
          }
        // }
      }
      for (let i = 0; i < problemConceptData.length; i++) {
        let conceptId = problemConceptData[i]['conceptId'];
        let problemId = problemConceptData[i]['problem'];
        let Pro = problemsData.find(function (p) { return p['id'] == problemId; });
        Pro['conCount']++;
        Pro['conList'].push(conceptId);
      }


      for (let i = 0; i < problemsData.length; i++) {
        if (problemsData[i]['totalAttempts'] != 0) {
          problemsData[i]['scoringRate'] = problemsData[i]['totalScore'] / problemsData[i]['totalAttempts'];
          problemsData[i]['acceptedRate'] = problemsData[i]['acceptedAttempts'] / problemsData[i]['totalAttempts'];
        }
        let num = 0;
        let cur = 0;
        let stu = problemsData[i]['stu'];
        Object.keys(stu).forEach((s)=>{
          if(stu[s]==1){
            num++;
            cur++;
          }
          if(stu[s]==0){
            num++;
          }
        })
        // for l in ep['log']:
        //     num += 1
        //     if ep['log'][l][0] == ep['score']:
        //         cur += 1
        // if cur != 0:
        problemsData[i]['totalAttemptsPeople'] = num;
        problemsData[i]['acceptedAttemptsPeople'] = cur;
      }
      for (let c = 0; c < conceptTree.length; c++) {
        let pcount = 0;
        for (let i = 0; i < problemConceptData.length; i++) {
          let conceptId = problemConceptData[i]['conceptId'];
          if (conceptId == conceptTree[c]['id']) {
            pcount++;
            let problemId = problemConceptData[i]['problem'];
            let ProBycon = problemsData.find(function (p) { return p['id'] == problemId; });
            conceptTree[c]['proCount'] += 1;
            conceptTree[c]['totalAttempts'] += ProBycon['totalAttempts'];
            conceptTree[c]['acceptedAttempts'] += ProBycon['acceptedAttempts'];
            conceptTree[c]['scoringRate'] += ProBycon['scoringRate'];
            conceptTree[c]['accuracy'] += ProBycon['accuracy'];
            conceptTree[c]['totalAttemptsPeople'] = ProBycon['totalAttemptsPeople'];
            conceptTree[c]['acceptedAttemptsPeople'] = ProBycon['acceptedAttemptsPeople'];
          }
        }
        if (conceptTree[c]['totalAttempts'] != 0)
          conceptTree[c]['acceptedRate'] = conceptTree[c]['acceptedAttempts'] / conceptTree[c]['totalAttempts'];
        else
          conceptTree[c]['acceptedRate'] = 0;
        if (pcount != 0) {
          conceptTree[c]['scoringRate'] = conceptTree[c]['scoringRate'] / pcount;
          conceptTree[c]['accuracy'] = conceptTree[c]['accuracy'] / pcount;
        }
      }
      let logLen = 0;
      for (let i = 0; i < entStudent.length; i++) {
        let tempProSetScore = [];
        for (let j = 0; j < entProSet.length; j++) {
          tempProSetScore.push({
            "id": entProSet[j]['id'],
            "totalScore": entProSet[j]['totalScore'],
            "score": 0
          })
        }
        for (let l = 0; l < entStudent[i]['pro'].length; l++) {
          let proId = entStudent[i]['pro'][l]['id'];
          let proSetDa = problemsData.find(function (ep) { return ep['id'] == proId })
          if (proSetDa != undefined) {
            let proSetId = proSetDa['problemSetId'];
            let bestScore = entStudent[i]['pro'][l]['best']['score'];
            if (bestScore == NaN) {

            }

            tempProSetScore.find(function (tpss) { return tpss['id'] == proSetId })['score'] += bestScore;
          }
        }
        entStudent[i]['proSetScore'] = tempProSetScore;
      }
      _this.studentsData = entStudent;
      _this.$bus.$emit("Student", _this.studentsData);
      _this.proSetData = entProSet;
      _this.$bus.$emit("proSet", _this.proSetData);
      _this.conceptTree = conceptTree;
      _this.$bus.$emit("ConceptTree", _this.conceptTree);
      _this.problemsData = problemsData;
      _this.$bus.$emit("allProblem", _this.problemsData);
      _this.calcNetData();
    },
    calcNetData() {
      const _this = this;
      let problemData = _this.problemsData;
      let submissionsData = _this.submissionsData;
      let studentsData = _this.studentsData;
      let minSupport = 0.1;
      let minConfidence = 0.1;
      let frequentItemset2 = {};
      let frequentItemset1 = {};
      let netData = {};
      let studPro = {};
      for (let i = 0; i < problemData.length; i++) {
        let problemId = problemData[i]['id'];
        frequentItemset1[`${problemId}`] = 0;
        studentsData.forEach((s) => {
          // if(studentLog.find(function(sd){return sd['id'] == s['id'];})){
          //   studentLog.push({"id":s['id'],"pro":[]});
          // }
          if(studPro[s['id']] == undefined){
            studPro[s['id']] = {}
          }
          // let st = studentLog.find(function(sd){return sd['id'] == s['id'];});
          let problemI = s['pro'].find(function (pro) { return pro['id'] == problemId });
          if (problemI == undefined) {
              frequentItemset1[`${problemId}`]++;
              studPro[s['id']][problemId] = '0';
              s['pro'].push({
                "id":problemId,
                "log":[],"best":{"status":"none","score":0}
              })
          }
          else{
            studPro[s['id']][problemId] = problemI['best']['score'];
            if (problemI['status'] != 'ACCEPTED') {
              frequentItemset1[`${problemId}`]++;
            }
          }
        })
      }
      for (let i = 0; i < problemData.length - 1; i++) {
        let problemIId = problemData[i]['id'];
        let problemScore = problemData[i]['score']
        if (frequentItemset1[`${problemIId}`] > 0) {
          for (let j = i + 1; j < problemData.length; j++) {
            let problemJId = problemData[j]['id'];
            frequentItemset2[`${problemIId}_${problemJId}`] = 0;
            frequentItemset2[`${problemJId}_${problemIId}`] = 0;
            let supportCount = 0;
            if (frequentItemset1[`${problemJId}`] > 0) {
              studentsData.forEach((s) => {
                let problemI = studPro[s['id']][problemIId];
                let problemJ = studPro[s['id']][problemJId];
                if ((problemI<problemScore) && (problemJ <problemScore)) {
                  frequentItemset2[`${problemIId}_${problemJId}`]++;
                  frequentItemset2[`${problemJId}_${problemIId}`]++;
                }
              })
              netData[`${problemIId}_${problemJId}`] = frequentItemset2[`${problemIId}_${problemJId}`] / frequentItemset1[`${problemIId}`];
              netData[`${problemJId}_${problemIId}`] = frequentItemset2[`${problemJId}_${problemIId}`] / frequentItemset1[`${problemJId}`];
            }
          }
        }
      }
      _this.netData = netData;
      _this.$bus.$emit("netData",netData);
    },
    getAllData() {
      const _this = this;
      this.getConceptTree();
      // this.getStudents();
      this.getProblems();
      // this.getConcept();
      this.getProblemConcept();
      this.getSubmissions();
      // .then(()=>{ 
      // _this.updataGraph();
      // })
    },
    getSelectEnt(val) {
      this.selectEntId = val;
    },
    getTimeDur(value) {
      this.timeDur = value
    },
    getToolState(val) {
      this.toolsState = val;
    },
    // getToolState:{
    //   deep:true,
    //   handler(val) {
    //     console.log(val)
    //   this.toolsState = val;
    // }
    // },
    getShowLabelState(value) {
      this.showLabelState = value
    }
    ,

    clickHandler() {
      console.log(111111);
    },
  },
  created: function () {
    var _this = this;
  },
  mounted() {
    const _this = this;
    this.$el.style.setProperty("--heightStyle", this.windowHeight + "px");
    this.showVideo = true;
    this.$bus.$emit("attrColorList", _this.attrColorList);
    this.$bus.$emit("attrColorLightList", _this.attrColorLightList);
    this.$bus.$emit("stuColorList", _this.stuColorList);
    this.$bus.$emit("groupData", _this.groupData);
    this.toolState = {
      "addRel": false,
      "addRelMain": false,
      "delRel":false,
    }
    this.getAllData();
    this.$bus.$on('Updata_Pro_Con', (val) => {
      _this.problemConceptData = val;
      _this.calStudent();
    });

    this.$bus.$on('renew', (val) => {
      if(val){
        _this.getProblemConcept();
          _this.calStudent();
      }
    });
    this.$bus.$on('SelectedStu', (val) => {
      _this.SelectStudentList = val;
      // _this.calStudentbyGroup();
      _this.calStudent();
    });
    // this.getData();
  },
  beforeDestroy() {
    clearTimeout(this.timer);
  }
};
</script>

<style>
@import '../../assets/style/home.css';
</style>