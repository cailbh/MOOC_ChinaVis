<!-- eslint-disable no-unused-vars -->
<!-- eslint-disable no-unused-vars -->

<template>
  <div class="graph" ref="graphDiv">
    <div class="panelHead">C</div>
  <div id="graphPanel" class="panelBody">
    </div>
  <!-- <div id="moveLeft" ref="moveGraphLeft"></div>
                    <div id="moveRight" ref="moveGraphRight"></div> -->
    <!-- <div id="assistGraphPanel" class="panel">
        <div class="panelHead"></div>
      </div> -->

    <div id="zoomInDiv" @click="zoomInLayoutClk">
      <img class="icons" :src="zoomInUrl">
    </div>
    <div id="zoomOutDiv" @click="zoomOutLayoutClk">
      <img class="icons" :src="zoomOutUrl">
    </div>
    <div id="editToolDiv" @click="editToolClk">
      <img class="icons" :src="editToolUrl">
    </div>
  </div>
</template>
  
<script>
import * as d3 from 'd3'
import { onMounted, ref } from 'vue';
import filenames from "@/utils/fileName";
import domtoimage from 'dom-to-image';
// import TestJson from "@/assets/json/case2_fin.json";
// import TestRelJson from "@/assets/json/case2_fin_rel.json";
// import tools from "@/utils/tools.js";

export default {
  props: ["videoTime"],
  data() {
    return {
      data: '',
      problemsData: [],
      conceptData: [],
      conceptProblemData: [],
      userProblemData: [],
      assistGTransformX: 10,
      assistGTransformY: 100,
      drawEntityLocation: [],
      showEntityList: [],
      rootSvg: null,
      groupsSvg: null,
      arcG: null,
      curEntId: '',
      minDImportance: 0,
      maxDImportance: 0,
      minDRelevance: 0,
      maxDRelevance: 0,
      maxDDuration: 0,
      maxTotalDuration: 0,
      videoDuration: 672,
      totalDuration: 1000,
      importanceColor_linear: null,
      importanceCompute_color: null,
      relevanceScale_linear: null,
      totalDurationScale_linear: null,
      // importanceMinColor: "rgb(1, 164, 183)",
      // importanceMaxColor: "rgb(106, 52, 127)",
      zoomInUrl: require("@/assets/img/zoomIn.png"),
      zoomOutUrl: require("@/assets/img/zoomOut.png"),
      editToolUrl: require("@/assets/img/edit.png"),
      layoutShow: 2,
      graphGTransformK: 1,
      graphGTransformX: 10,
      graphGTransformY: 100,
      graphSvgScale: 1,
      moveTimer: null,
      moveFlag: false,
      importanceMinColor: "rgb(203, 230, 209)",
      importanceMaxColor: "rgb(22, 144, 207)",
      stepX: 80,
      stepY: 100,
      circleInterval: 55,
      width: 0,
      height: 0,
      curToolState: 'unEdit',
      margin: { top: 80, right: 20, bottom: 0, left: 20 },
      color: [
        "rgb(255,60,60)",
        "rgb(255,83,255)",
        "rgb(235,135,162)",
        "rgb(255,178,101)",
        "rgb(63,151,134)",
        "rgb(83,255,255)",
        "rgb(0,122,244)",
        "rgb(168,168,255)",
        "rgb(200,200,200)",
      ],
      mcolor: [
        "rgb(91, 107, 255)",
        "rgb(6, 214, 160)",
        "rgb(255, 120, 90)",
        "rgb(125, 98, 211)",
        "rgb(255, 113, 212)",
        "rgb(112, 214, 255)",
        "rgb(255, 159, 28)",
        "rgb(255, 77, 109)",
      ],
      // mcolor: [
      //   "rgb(255,60,60)",
      //   "rgb(155,20,100)",
      //   "rgb(255,83,255)",
      //   "rgb(200,100,50)",
      //   "rgb(235,135,162)",
      //   "rgb(200,200,102)",
      //   "rgb(255,178,101)",
      //   "rgb(63,151,134)",
      //   "rgb(83,155,255)",
      //   "rgb(50,200,120)",
      //   "rgb(2,50,200)",
      //   "rgb(0,122,244)",
      //   "rgb(150,122,244)",
      //   "rgb(168,168,255)",
      //   "rgb(200,200,200)",
      // ],
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
    };
  },

  watch: {
    type(val) {
    },
    curEntId(val) {
      const _this = this;
      _this.$bus.$emit("selectEnt", val);
      let entityLocationData = _this.drawEntityLocation;

      let relData = _this.relData;
      let showJageData = _this.showEntityList;
      let basicRel = relData['basicRel'];
      for (let r = 0; r < basicRel.length; r++) {
        let sorceId = basicRel[r][0];
        let targetId = basicRel[r][1];
        let sorceJage = showJageData.find(function (d) { return d['id'] == sorceId })['show'];
        let targetJage = showJageData.find(function (d) { return d['id'] == targetId })['show'];
        if (sorceJage && targetJage) {
          let trnId = '-1';
          if (sorceId == parseInt(val)) {
            trnId = targetId;
          }
          else if (targetId == parseInt(val)) {
            trnId = sorceId;
          }
          if (trnId != '-1') {
            let curEnt = entityLocationData.find(function (d) { return parseInt(d['id']) == trnId });
            _this.assistGTransformX = parseInt(-curEnt['x']) + parseFloat(curEnt['r']) + 150;
            _this.assistGTransformY = parseInt(-curEnt['y']) + parseFloat(curEnt['r']) + 300;
            _this.updataAssistGraphPanel();
          }
        }

      };
      let similarityRel = relData['similarityRel'];
      for (let r = 0; r < similarityRel.length; r++) {
        let sorceId = similarityRel[r][0];
        let targetId = similarityRel[r][1];
        let sorceJage = showJageData.find(function (d) { return d['id'] == sorceId })['show'];
        let targetJage = showJageData.find(function (d) { return d['id'] == targetId })['show'];
        if (sorceJage && targetJage) {
          let trnId = '-1';
          if (sorceId == parseInt(val)) {
            trnId = targetId;
          }
          else if (targetId == parseInt(val)) {
            trnId = sorceId;
          }
          if (trnId != '-1') {
            let curEnt = entityLocationData.find(function (d) { return parseInt(d['id']) == trnId });
            _this.assistGTransformX = parseInt(-curEnt['x']) + parseFloat(curEnt['r']) + 150;
            _this.assistGTransformY = parseInt(-curEnt['y']) + parseFloat(curEnt['r']) + 300;
            _this.updataAssistGraphPanel();
          }
        }

      };


    },
    // groupsSvg: {
    //   deep: true,
    //   handler() {
    //     this.updataAssistGraphPanel();
    //   }
    // }
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
          _this.updataGraph();
        });
    },
    getConcept() {
      const _this = this;
      this.$http
        .get("/api/concept/allConcept", {}, {})
        .then((response) => {
        });
    },
    getUserProblem() {
      const _this = this;
      this.$http.get("/api/userProblem/allLog", {}, {})
        .then((response) => {
        });
    },
    getConceptProblem() {
      const _this = this;
      this.$http.get("/api/conceptProblem/allRel", {}, {})
        .then((response) => {
        });
    },
    drawMain(svg) {
      let _this = this;
      let data = _this.data;
      let margin = _this.margin;

      let width = _this.width - margin.left - margin.right;
      let height = _this.height - margin.top - margin.bottom;

      let graphGTransformX = _this.graphGTransformX;
      let graphGTransformY = _this.graphGTransformY;
      let graphGTransformK = _this.graphGTransformK;
      let groups = svg.append("g").attr("id", "groups").attr("width", width).attr("height", height)
        .attr("transform", "translate(" + graphGTransformX + ',' + graphGTransformY + ") scale(" + graphGTransformK + ")");
      this.groupsSvg = groups;

      let backG = groups.append("g").attr("id", "backG").attr("width", width).attr("height", height);
      let arcG = groups.append("g").attr("id", "arcG").attr("width", width).attr("height", height);
      let timeLineG = groups.append("g").attr("id", "timeLineG").attr("width", width).attr("height", height);
      let circleG = groups.append("g").attr("id", "circleG").attr("width", width).attr("height", height);

      _this.arcG = arcG;
      let stepY = _this.stepY;
      let interval = _this.circleInterval;


      let scalePre = _this.graphSvgScale;
      let stx = 0;
      let sty = 0;
      let stk = 1;
      var graphZoom = d3.zoom()
        .scaleExtent([0, 10])
        .on("start", (e) => {
          sty = e.transform.y;
          stx = e.transform.x;
          stk = e.transform.k;
        })
        .on('zoom', (e) => {
          graphGTransformX = _this.graphGTransformX + e.transform.x - stx;
          graphGTransformY = _this.graphGTransformY + e.transform.y - sty;
          graphGTransformK = _this.graphGTransformK + e.transform.k - stk;

          groups.attr('transform', 'translate(' + (graphGTransformX) + ',' + (graphGTransformY) + ') scale(' + (graphGTransformK) + ')')
        })
        .on('end', (e) => {
          _this.graphGTransformX = graphGTransformX;
          _this.graphGTransformY = graphGTransformY;
          _this.graphGTransformK = graphGTransformK;
          groups.attr('transform', 'translate(' + (graphGTransformX) + ',' + (graphGTransformY) + ') scale(' + (graphGTransformK) + ')')
        });

      let problemData = _this.problemsData;
      console.log(problemData)
      let stepX = 10;
      for(let i=0;i<problemData.length;i++){
        console.log(problemData[i]['type'],problemData[i]['typetext'])
        _this.drawCircle(circleG,1+i*stepX,100,10,"red",1,"problemEnt",`problem_${i}`);
      }

      svg.call(graphZoom)

    },
    drawCircle(svg, x, y, r, fill, opacity, className = 'entCircle', idName) {
      const _this = this;
      const oData = _this.data
      svg.append("circle")
        .attr("id", idName)
        .attr("class", className)
        .attr("opacity", opacity)
        .attr("cx", x)
        .attr("cy", y)
        .attr("r", r)
        .attr("fill", fill)
    },
    updataGraph() {
      var _this = this;
      let margin = _this.margin
      let width = _this.$refs.graphDiv.offsetWidth - margin.left - margin.right;
      let height = document.getElementById("graphPanel").clientHeight - margin.top - margin.bottom;
      _this.width = width;
      _this.height = height;
      d3.select("#graphPanel").select("svg").remove()
      var svg = d3.select("#graphPanel").append("svg")
        .attr("width", width)
        .attr("height", height);
      _this.rootSvg = svg;

      _this.drawMain(svg);
      // });
    },
    click_Ent(time) {
      this.$emit("timeDur", time);
    },
  },
  created() {
    var _this = this;
    let margin = _this.margin
    this.$nextTick(() => {
      _this.getProblems();
      _this.getConcept();
      _this.getConceptProblem();
      _this.getUserProblem();
      _this.updataGraph();
    });
  },
  mounted() {
    const _this = this;
    this.$bus.$on('graphData', (val) => {
      _this.data = val;
      let showEntityList = tools.deepClone(_this.data);
      for (let e in showEntityList) {
        showEntityList[e]['show'] = true;
      }
      _this.showEntityList = showEntityList;
      _this.updataGraph();
    });

    // this.$refs.moveGraphLeft.addEventListener("mouseover", _this.moveGraphLeft); // 监听点击事件
    // this.$refs.moveGraphRight.addEventListener("mousemove", _this.moveGraphRight); // 监听点击事件
    // this.$refs.moveGraphLeft.addEventListener("mouseleave", _this.leaveGraphMove); // 监听点击事件
    // this.$refs.moveGraphRight.addEventListener("mouseleave", _this.leaveGraphMove); // 监听点击事件

  },
  beforeDestroy() {
    clearInterval(this.moveTimer);
  },
} 
</script>

<style>
@import './index.css';
</style>
