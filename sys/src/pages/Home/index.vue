<template>
  <div id="root">
    <!-- <button1 ref="button1"></button1>
    <button v-on:click="clickHandler">按钮</button> -->
    <!-- <svg width="1200" height="1000"></svg> -->

    <div id="Container" >
      <!-- <div id="Container-back"></div> -->
      <div id="head">

        <!-- <Head></Head> -->
      </div>
      <div id="allBody">
        <div id="controlPanel" class="panel">
          <ControlPanel></ControlPanel>
        </div>
        <div id="graphContainer" v-show="showGraph" class="panel">
          <Graph></Graph>
        </div>
        <!-- <div id="overviewPanel" class="panel">
          <OverviewPanel></OverviewPanel>
        </div> -->
        <!-- <transition name="sceneTran"> -->

        <!-- <div id="editPanel" class="panel"  v-if='showEdit==true'>
          <EditPanel></EditPanel>
        </div> -->
        <div id="procPanel" class="panel">
          <ProcPanel></ProcPanel>
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
import ProcPanel from '@/components/ProblemContentPanel/index.vue';
import NetPPanel from '@/components/NetProblemPanel/index.vue';
export default{
  components: { Head, Graph, ProcPanel,NetPPanel},
  /* eslint-disable no-unused-vars */
  data() {
    return {
      problemsData: [],
      submissionsData:[],
      studentsData:[],
      conceptsData: [],
      conceptTree: [],
      problemConceptData: [],
      userProblemData: [],
      timer: null,
      showVideo: true,
      showGraph: true,
      showEdit: false,
      selectEntId:"0",
      selectEnt: "0",
      toolState:'',
      timeDur: "",
      videoTime: 0,
      windowWidth: document.documentElement.clientWidth, //实时屏幕宽度
      windowHeight: document.documentElement.clientHeight, //实时屏幕高度
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
    toolState(val){
      if(val=='edit')
        this.showEdit = true;
      else
        this.showEdit = false;
    },
    selectEnt(val){
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
          _this.$bus.$emit("allProblem", _this.problemsData);
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
          console.log(_this.conceptTree)
          _this.$bus.$emit("ConceptTree", _this.conceptTree);
        });
    },
    getSubmissions() {
      const _this = this;
      this.$http.get("/api/Submission/allLog", {}, {})
        .then((response) => {
          _this.submissionsData = response.body;
          _this.$bus.$emit("Submission", _this.submissionsData);
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
          _this.$bus.$emit("Student", _this.studentsData);
        });
    },
    getAllData() {
      const _this = this;
      this.getConceptTree();
      this.getStudents();
      this.getProblems();
      this.getConcept();
      this.getSubmissions();
      this.getProblemConcept();
      // .then(()=>{ 
      // _this.updataGraph();
      // })
    },
    getSelectEnt(val){
      console.log(val)
      this.selectEntId = val;
    },
    getTimeDur(value) {
      this.timeDur = value
    },
    getToolState(val){
      this.toolState = val;
    },
    getVideoTime(value) {
      this.videoTime = value
    },
    getShowLabelState(value) {
      this.showLabelState = value
    },

    clickHandler() {
      console.log(111111);
    },
  },
  created: function () {
    var _this = this;
  },
  mounted() {
    this.$el.style.setProperty("--heightStyle", this.windowHeight + "px");
    this.showVideo = true;
    
    this.getAllData();
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