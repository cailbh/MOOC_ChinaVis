<!-- eslint-disable no-unused-vars -->
<!-- eslint-disable no-unused-vars -->

<template>
  <div class="graph" ref="graphDiv">
    <div class="panelHead">C</div>
    <div id="graphPanel" class="panelBody">
      <div class="chartTooltip">
        <p>
          <br /><strong class="name"></strong>
          <br /><strong class="text"></strong>
        </p>
      </div>
    </div>
    <!-- <div id="moveLeft" ref="moveGraphLeft"></div>
                    <div id="moveRight" ref="moveGraphRight"></div> -->
    <!-- <div id="assistGraphPanel" class="panel">
        <div class="panelHead"></div>
      </div> -->
    <!-- <div id="zoomInDiv" @click="zoomInLayoutClk">
      <img class="icons" :src="zoomInUrl">
    </div>
    <div id="zoomOutDiv" @click="zoomOutLayoutClk">
      <img class="icons" :src="zoomOutUrl">
    </div>
    <div id="editToolDiv" @click="editToolClk">
      <img class="icons" :src="editToolUrl">
    </div> -->
  </div>
</template>
  
<script>
import * as d3 from 'd3'
import { onMounted, ref } from 'vue';
import filenames from "@/utils/fileName";
import domtoimage from 'dom-to-image';
// import TestJson from "@/assets/json/case2_fin.json";
// import TestRelJson from "@/assets/json/case2_fin_rel.json";
import tools from "@/utils/tools.js";

export default {
  props: ["toolsState"],
  data() {
    return {
      data: '',
      graphHeight: 0,
      toolAddRel: false,
      toolAddRelMain: false,
      toolDelRel: false,
      detailsEntPro: [],
      SelectingStudentId:"",
      groupData: [],
      SelectStudentList: [],
      problemsData: [],
      proSetOriData: [],
      submissionsData: [],
      maxSetCon: 0,
      studentsData: [],
      conceptsData: [],
      conceptTree: [],
      proSetData: [],
      interY: 10,
      problemConceptData: [],
      createdProblemConceptData: [],
      userProblemData: [],
      proMaxMinDR: [],
      proMaxMinDC: [],
      proAttrList: [],
      proAttrMaxMinList: [],
      conMaxMinDR: [],
      conMaxMinDC: [],
      conAttrList: [],
      conAttrMaxMinList: [],
      Ent_problem: [],
      Ent_concept: [],
      entG: "",
      entSetG: "",
      entbySetG: "",
      relG: "",
      frontG: "",
      curProblemId: '',
      curConceptId: '',
      curProblemSetId: '',
      selectProblemId: '',
      selectConceptId: '',
      proX: 450,
      proY: 30,
      setWidth: 300,
      setX: 830,
      setY: 30,
      treeX: 50,
      treeY: 30,
      proStepY: 0,
      conStepY: 0,
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
      graphGTransformK: 1,
      graphGTransformX: 10,
      graphGTransformY: 10,
      graphSvgScale: 1,
      moveTimer: null,
      moveFlag: false,
      entProMinColor: "rgb(203, 230, 209)",
      entProMaxColor: "rgb(22, 144, 207)",

      setMaxColor: "rgb(180, 212, 217)",
      setMinColor: "rgb(190, 253, 147)",

      entConMaxColor: "rgb(220, 4, 52)",
      entConMinColor: "rgb(231, 201, 203)",

      entConRectMaxColor: "rgb(56, 191, 201)",
      entConRectMinColor: "rgb(200, 200, 200)",

      setConCountColorMax: "rgb(36, 123, 178)",
      setConCountColorMin: "rgb(146, 189, 217)",

      setTypeCountColorMax: "rgb(251, 104, 20)",
      setTypeCountColorMin: "rgb(253, 209, 161)",
      stepX: 80,
      stepY: 100,
      typeXMap: {
        "TRUE_OR_FALSE": 0,
        "MULTIPLE_CHOICE": 1,
        "FILL_IN_THE_BLANK": 2,
        "PROGRAMMING": 3,
        // "CODE_COMPLETION":4,
        // "MULTIPLE_CHOICE_MORE_THAN_ONE_ANSWER":5
      },
      circleInterval: 55,
      width: 0,
      height: 0,
      curToolState: 'unEdit',
      margin: { top: 10, right: 20, bottom: 0, left: 20 },
      attrColorList: [],
      stuColorList: [],
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
    };
  },

  watch: {
    type(val) {
    },
    toolAddRel(val) {
    },
    toolsState: {
      deep: true,
      handler(val) {
        console.log(val)
        this.toolAddRel = val['addRel'];
        this.toolAddRelMain = val['addRelMain'];
        this.toolDelRel = val['delRel'];
      }
    },
    SelectStudentList: {
      deep: true,
      handler(val) {
        this.updataSelectStudentListColor();
      }
    },
    SelectingStudentId(val){
      console.log(val);
      if(val == ""){
          d3.selectAll(`.stuSetScoreLine`).attr("opacity", 1);
          d3.selectAll(`.stuScoreLine`).attr("opacity", 1);
      }
      else{
          d3.selectAll(`.stuSetScoreLine`).attr("opacity", 0.1).attr('stroke-width', 1);
          d3.selectAll(`.stuScoreLine`).attr("opacity", 0.1).attr('stroke-width', 1);
          
          d3.select(`#stuScoreLine_av`).attr("opacity", 1).attr('stroke-width', 3);
          d3.select(`#stuSetScoreLine_av`).attr("opacity", 1).attr('stroke-width', 3);
          d3.select(`#stuSetScoreLine_${val}`).attr("opacity", 1).attr('stroke-width', 3);
          d3.select(`#stuScoreLine_${val}`).attr("opacity", 1).attr('stroke-width', 3);
      }
    },
    graphGTransformY() {
      const _this = this;
      _this.updataPro_ProSetRel(_this.graphGTransformY);
      // this.updataPro_ProSelfRel(this.graphGTransformY);
    },
    curConceptId(val) {
      const _this = this;
      // _this.$bus.$emit("selectEntCon", val);
      let Ent_concept = _this.Ent_concept;
      let Ent_problem = _this.Ent_problem;
      let pro_conRelData = tools.deepClone(_this.problemConceptData);
      let curproId = _this.curProblemId;
      let setEnt = [];//tools.deepClone() ;
      if (_this.toolAddRel) {
        let type = 0;
        if (_this.toolAddRelMain) {
          type = 1;
        }
        // createdProblemConceptData
        // pro_conRelData.push({
        //   "problem":curproId,
        //   "conceptId":val,
        // })
        // _this.problemConceptData = pro_conRelData;
        _this.createRel(curproId, val, type);

      }
      else if (_this.toolDelRel) {
        _this.delRel(curproId, val);
      }
      else {
        d3.selectAll(`.entPro`)
          .attr("opacity", "0.1");
        d3.selectAll(`.entCon`)
          .attr("opacity", "0.1");
        d3.select(`#entCon_${val}`)
          .attr("opacity", "1");
        d3.selectAll(`.proConRel`)
          .attr("opacity", "0.1");
        d3.selectAll(`.proSetConRel`)
          .attr("opacity", "0.1");
        pro_conRelData.forEach(rel => {
          let proId = rel['problem'];
          let conId = rel['conceptId'];
          let proData = Ent_problem.find(function (d) { return d['id'] == proId; })
          let proSetId = proData['problemSetId'];
          if (conId == val) {
            // d3.select(`#entCon_${conId}`)
            // .attr("opacity","1");
            if(setEnt.find(function(s){return s['id'] == proId})==undefined)
              setEnt.push(proData);
            d3.select(`#entPro_${proId}`)
              .attr("opacity", "1");
            d3.select(`#proSetConRel_${conId}_${proSetId}`)
              .attr("opacity", "1");
          }
        })
        
      var compare = function (x, y) {//比较函数
        return x["problemSetId"] > y["problemSetId"] 
      };
        setEnt.sort(compare)
        _this.detailsEntPro = setEnt;
      }
    },
    curProblemId(val) {
      const _this = this;
      _this.$bus.$emit("selectEnt", val);
      let Ent_concept = _this.Ent_concept;
      let Ent_problem = _this.Ent_problem;
      let pro_conRelData = _this.problemConceptData;
      _this.$bus.$emit("selectEntData", [val, Ent_problem]);
      // entCon
      d3.selectAll(`.entCon`)
        .attr("opacity", "0.1");
      d3.selectAll(`.proConRel`)
        .attr("opacity", "0.1");
      d3.selectAll(`.proSetConRel`)
        .attr("opacity", "0.1");
      pro_conRelData.forEach(rel => {
        let proId = rel['problem'];
        let conId = rel['conceptId'];
        let proData = Ent_problem.find(function (d) { return d['id'] == proId; })
        let proSetId = proData['problemSetId'];
        if (proId == val) {
          d3.select(`#entCon_${conId}`)
            .attr("opacity", "1");
          d3.select(`#proConRel_${conId}_${proId}`)
            .attr("opacity", "1");
          d3.select(`#proSetConRel_${conId}_${proSetId}`)
            .attr("opacity", "1");
        }
      })
    },
    problemConceptData: {
      deep: true,
      handler(val) {
        if (this.toolAddRel) {
          // this.updataPro_ConRel();
          this.updataProSet_ConRel();
          this.$bus.$emit("Updata_Pro_Con", val);
        }
      }
    },
    curProblemSetId(val) {
      const _this = this;
      let Ent_concept = _this.Ent_concept;
      let Ent_problem = _this.Ent_problem;
      let pro_conRelData = _this.problemConceptData;
      this.updataEntProblemDetailBySet("none", 0);
      // this.updataPro_ProSelfRel(this.graphGTransformY);// entCon
      d3.selectAll(`.entCon`)
        .attr("opacity", "0.1");
      d3.selectAll(`.proConRel`)
        .attr("opacity", "0.1");
      d3.selectAll(`.proSetConRel`)
        .attr("opacity", "0.1");
      pro_conRelData.forEach(rel => {
        let proId = rel['problem'];
        let conId = rel['conceptId'];
        let proData = Ent_problem.find(function (d) { return d['id'] == proId; })
        let proSetId = proData['problemSetId'];
        if (proSetId == val) {
          d3.select(`#entCon_${conId}`)
            .attr("opacity", "1");
          d3.select(`#proConRel_${conId}_${proId}`)
            .attr("opacity", "1");
          d3.select(`#proSetConRel_${conId}_${proSetId}`)
            .attr("opacity", "1");
        }
      })
    },
    detailsEntPro(val) {


      this.$bus.$emit("selectedPro", val);

      this.updataEntProblemDetail();
      this.updataParallelCoordinatesplotByPro();
      // this.updataPro_ProSelfRel(this.graphGTransformY);
    },
    Ent_problem: {
      deep: true,
      handler() {
        // this.updataEntProblem();
        this.updataEntProblemSetBack();
        // this.updataPro_ConRel();
        this.updataProSet_ConRel();
      }
    },
    Ent_concept: {
      deep: true,
      handler() {
        this.updataEntConcept();
        // this.updataPro_ConRel();
        this.updataProSet_ConRel();
      }
    }
    // groupsSvg: {
    //   deep: true,
    //   handler() {
    //     this.updataAssistGraphPanel();
    //   }
    // }
  },
  methods: {

    createRel(problemId, conceptId, type) {
      const _this = this;
      this.$http
        .post("/api/conceptProblem/createRel", {
          params: {
            problem: problemId,
            conceptId: conceptId,
            type: type
          }
        }, {})
        .then((response) => {
          _this.$message({
            message: 'add success',
            type: 'success',
            duration: 1000
          });
        });
    },
    delRel(problemId, conceptId) {
      const _this = this;
      this.$http
        .post("/api/conceptProblem/delRel", {
          params: {
            problem: problemId,
            conceptId: conceptId,
          }
        }, {})
        .then((response) => {
          _this.$message({
            message: 'del success',
            type: 'warning',
            duration: 1000
          });
        });
    },
    drawMainO(svg) {
      let _this = this;
      let data = _this.data;
      let margin = _this.margin;

      let width = _this.width - margin.left - margin.right;
      let height = _this.height - margin.top - margin.bottom;

      let graphGTransformX = _this.graphGTransformX;
      let graphGTransformY = _this.graphGTransformY;
      let graphGTransformK = _this.graphGTransformK;
      let groups = svg.append("g").attr("id", "groups").attr("width", width).attr("height", height)
      // .attr("transform", "translate(" + graphGTransformX + ',' + graphGTransformY + ") scale(" + graphGTransformK + ")");
      this.groupsSvg = groups;

      let backG = groups.append("g").attr("id", "backG").attr("width", width).attr("height", height);
      let arcG = groups.append("g").attr("id", "arcG").attr("width", width).attr("height", height);
      let relG = groups.append("g").attr("id", "relG").attr("width", width).attr("height", height);
      let entG = groups.append("g").attr("id", "entG").attr("width", width).attr("height", height);
      let frontG = groups.append("g").attr("id", "frontG").attr("width", width).attr("height", height);

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

      let problemConceptData = _this.problemConceptData;
      let ent_node = [];
      let ent_edge = []
      for (let r = 0; r < problemConceptData.length; r++) {
        let curRel = problemConceptData[r];
        let pId = curRel['problem'];
        let cId = curRel['conceptId'];
        ent_edge.push({
          source: pId,
          target: cId
        })
        if (ent_node.find(function (d) { return d['id'] == pId }) == undefined) {
          ent_node.push({ "id": pId, "type": "problem" })
        }
        if (ent_node.find(function (d) { return d['id'] == cId }) == undefined) {
          ent_node.push({ "id": cId, "type": "concept" })
        }
      }
      var forceSimulation = d3.forceSimulation()
        .force("link", d3.forceLink().id((d) => { return d.id }))
        .force("charge", d3.forceManyBody().strength(-150))
        .force("center", d3.forceCenter(width / 2, height / 2));
      forceSimulation.nodes(ent_node)
        .on("tick");

      forceSimulation.force("link")
        .links(ent_edge)
        .distance(120);

      let rSize = 10;
      let svgWidth = width;
      let svgHeight = height;

      const drags = () => {

        function dragstarted(event, d) {
          if (!event.active) forceSimulation.alphaTarget(0.3).restart();
          d.fx = d.x;
          d.fy = d.y;
        }
        function dragged(event, d) {
          d.fx = event.x;
          d.fy = event.y;
        }

        function dragended(event, d) {
          if (!event.active) forceSimulation.alphaTarget(0);
          d.fx = null;
          d.fy = null;
        }
        return d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended);
      }

      var circle = frontG.selectAll('circle')
        .data(ent_node)
        .enter()
        .append("circle")
        .attr("id", function (d) { return d.id })
        .attr("class", function (d) { return d.type })
        .attr("cx", function (d) {
          if (d.type == "problem")
            _this.drawEntityProblem(entG, d.x, d.y, `entPro_${d.id}`);
          else if (d.type == "concept")
            _this.drawEntityConcept(entG, d.x, d.y, `entCon_${d.id}`);
          return d.x
        })
        .attr("cy", function (d) { return d.y })
        .attr("r", 30)
        .attr("opacity", "0")
        .on("mousemove", function (d) {
          let curSvgEnt = d3.select(this);
          let curType = curSvgEnt.attr("class");
          let curId = curSvgEnt.attr("id");
          let idNameList = [];
          let curEnt = {};
          let tipName = '';
          if (curType == 'problem') {

            curEnt = _this.problemsData.find(function (p) {
              return (p.id).toString() == (curId.toString());
            });
            tipName = curEnt['problemPoolIndex']
            problemConceptData.forEach(rel => {
              if (rel['problem'] == curId) {
                let conID = rel['conceptId'];
                idNameList.push(`#entCon_${conID}`);
              }
            });
            idNameList.push(`#entPro_${curId}`)
          }
          else if (curType == "concept") {
            curEnt = _this.conceptTree.find(function (p) {
              return (p.id).toString() == (curId.toString());
            });
            tipName = curEnt['name']
            problemConceptData.forEach(rel => {
              if (rel['conceptId'] == curId) {
                let proID = rel['problem'];
                idNameList.push(`#entPro_${proID}`);
              }
            });
            idNameList.push(`#entCon_${curId}`);
          }
          _this.entHover(idNameList);

          var yPosition = d.clientY + 20;
          var xPosition = d.clientX + 20;
          var chartTooltip = d3
            .select(".chartTooltip")
            .style("left", xPosition + "px")
            .style("top", yPosition + "px");
          // 更新浮层内容
          chartTooltip.select(".name").text(curType);
          chartTooltip.select(".text").text(tipName);
          // 移除浮层hidden样式，展示浮层
          chartTooltip.classed("hidden", false);

        })
        .on("click", function (d) {
          let curSvgEnt = d3.select(this);
          let curType = curSvgEnt.attr("class");
          let curId = curSvgEnt.attr("id");
          let idNameList = [];
          if (curType == 'problem') {
            idNameList.push(`#entPro_${curId}`);
            _this.curProblemId = curId;
          }
          else if (curType == "concept") {
            idNameList.push(`#entCon_${curId}`)
          }
          _this.entHover(idNameList);
        })
        .on("mouseleave", function (d) {
          let curSvgEnt = d3.select(this);
          let curType = curSvgEnt.attr("class");
          let curId = curSvgEnt.attr("id");
          let idNameList = [];
          if (curType == 'problem') {
            problemConceptData.forEach(rel => {
              if (rel['problem'] == curId) {
                let conID = rel['conceptId'];
                idNameList.push(`#entCon_${conID}`)
              }
            });
            idNameList.push(`#entPro_${curId}`)
          }
          else if (curType == "concept") {
            problemConceptData.forEach(rel => {
              if (rel['conceptId'] == curId) {
                let proID = rel['problem'];
                idNameList.push(`#entPro_${proID}`)
              }
            });
            idNameList.push(`#entCon_${curId}`)
          }
          _this.entRemoveHover(idNameList);

          d3.select(".chartTooltip").classed("hidden", true);
        })
        .call(drags());

      var path = relG.selectAll('.path')
        .data(ent_edge)
        .enter()
        .append('path')
        .attr("class", function (d) { return "s-" + d.source.id + "-t-" + d.target.id })
        .attr('d', function (d) {
          let eSource = d.source
          let eTarget = d.target
          let startA = [eSource.x, eSource.y]
          let endA = [eTarget.x, eTarget.y]
          let path = d3.path()
          path.moveTo(startA[0], startA[1])
          path.quadraticCurveTo(startA[0], startA[1], endA[0], endA[1]);
          return path.toString()
        })
        .style('stroke', "grey")
        .style("stroke-opacity", "0.3")
        .style('stroke-width', "2")

      forceSimulation.on("tick", () => {
        circle.attr("cx", (d) => {
          let esx = d.x;
          let esy = d.y;
          if (esx < rSize) esx = rSize;
          esx = esx > svgWidth - rSize ? svgWidth - rSize : esx;
          if (esy < rSize) esy = rSize;
          esy = esy > svgHeight - rSize ? svgHeight - rSize : esy;
          if (d.type == "problem")
            _this.updateEntity(entG, esx, esy, `entPro_${d.id}`)
          //   _this.drawEntityProblem(entG, esx, esy, `entPro_${d.id}`);
          else if (d.type == "concept")
            _this.updateEntity(entG, esx, esy, `entCon_${d.id}`)
          //   _this.drawEntityConcept(entG, esx, esy, `entCon_${d.id}`);
          if (d.x < rSize) return rSize
          return d.x > svgWidth - rSize ? svgWidth - rSize : d.x
        })
          .attr("cy", (d) => {
            if (d.y < rSize) return rSize
            return d.y > svgHeight - rSize ? svgHeight - rSize : d.y
          });

        path.attr("d", (d) => {
          let eSource = d.source;
          let eTarget = d.target;
          let esx = eSource.x;
          let esy = eSource.y;
          if (esx < rSize) esx = rSize;
          esx = esx > svgWidth - rSize ? svgWidth - rSize : esx;
          if (esy < rSize) esy = rSize;
          esy = esy > svgHeight - rSize ? svgHeight - rSize : esy;
          let etx = eTarget.x;
          let ety = eTarget.y;
          if (etx < rSize) etx = rSize;
          etx = etx > svgWidth - rSize ? svgWidth - rSize : etx;
          if (ety < rSize) ety = rSize;
          ety = ety > svgHeight - rSize ? svgHeight - rSize : ety;
          let path = d3.path();
          path.moveTo(esx, esy);
          path.quadraticCurveTo(esx, esy, etx, ety);
          return path.toString();
        })

      });

      svg.call(graphZoom)

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
      // .attr("transform", "translate(" + graphGTransformX + ',' + graphGTransformY + ") scale(" + graphGTransformK + ")");
      this.groupsSvg = groups;

      let backG = groups.append("g").attr("id", "backG").attr("width", width).attr("height", height);
      let arcG = groups.append("g").attr("id", "arcG").attr("width", width).attr("height", height);
      let relG = groups.append("g").attr("id", "relG").attr("width", width).attr("height", height);
      let entSetG = groups.append("g").attr("id", "entSetG").attr("width", width).attr("height", height);
      let entbySetG = groups.append("g").attr("id", "entbySetG").attr("width", width).attr("height", height);
      let entG = groups.append("g").attr("id", "entG").attr("width", width).attr("height", height);
      let frontG = groups.append("g").attr("id", "frontG").attr("width", width).attr("height", height);

      _this.arcG = arcG;
      _this.entG = entG;
      _this.entSetG = entSetG;
      _this.entbySetG = entbySetG;
      _this.relG = relG;
      _this.frontG = frontG;
      let interval = _this.circleInterval;


      let scalePre = _this.graphSvgScale;
      let stx = 0;
      let sty = 0;
      let stk = 1;
      var graphZoom = d3.zoom()
        .scaleExtent([0, 100])
        .on("start", (e) => {
          sty = e.transform.y;
          stx = e.transform.x;
          stk = e.transform.k;
        })
        .on('zoom', (e) => {
          graphGTransformX = _this.graphGTransformX //+ e.transform.x - stx;
          graphGTransformY = _this.graphGTransformY + e.transform.y - sty;
          graphGTransformK = _this.graphGTransformK //+ e.transform.k - stk;
          _this.updataPro_ProSetRel(graphGTransformY);
          // _this.updataPro_ProSelfRel(graphGTransformY);
          entbySetG.attr('transform', 'translate(' + (graphGTransformX) + ',' + (graphGTransformY) + ') scale(' + (graphGTransformK) + ')')
        })
        .on('end', (e) => {
          _this.graphGTransformX = graphGTransformX;
          _this.graphGTransformY = graphGTransformY;
          _this.graphGTransformK = graphGTransformK;
          entbySetG.attr('transform', 'translate(' + (graphGTransformX) + ',' + (graphGTransformY) + ') scale(' + (graphGTransformK) + ')')
        });

      svg.call(graphZoom);
      const dragCon = () => {

        function dragstarted(event, d) {
          console.log("s", event, d)
        }
        function dragged(event, d) {
          console.log("s", event, d)
        }

        function dragended(event, d) {
          console.log("e", event, d)
        }
        return d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended);
      }
      let problemConceptData = _this.problemConceptData;
      let conceptTree = _this.conceptTree;

      let problemData = tools.deepClone(_this.problemsData);
      // let treeData = _this.getTreeData(conceptTree);
      // console.log(treeData)

      let conMaxMinDR = _this.conMaxMinDR;
      let conMaxMinDC = _this.conMaxMinDC;
      let conAttrMaxMinList = _this.conAttrMaxMinList;
      let currentConMaxColor = _this.entConMaxColor;
      let currentConMinColor = _this.entConMinColor;
      let importanceConColor_linear = d3.scaleLinear().domain([conMaxMinDC[0], conMaxMinDC[1]]).range([0, 1]);
      let importanceConCompute_color = d3.interpolate(currentConMinColor, currentConMaxColor);
      let rConSize_linear = d3.scaleLinear().domain([conMaxMinDR[1], conMaxMinDR[0]]).range([3, 6]);
      let r1ConSize_linear = d3.scaleLinear().domain([conMaxMinDR[1], conMaxMinDR[0]]).range([6, 9]);
      let r2ConSize_linear = d3.scaleLinear().domain([conMaxMinDR[1], conMaxMinDR[0]]).range([9, 12]);
      let linearList = [rConSize_linear, r1ConSize_linear, r2ConSize_linear];

      let currentConRectMaxColor = _this.entConRectMaxColor;
      let currentConRectMinColor = _this.entConRectMinColor;

      let rectConColor_linear = d3.scaleLinear().domain([conAttrMaxMinList[2][1], conAttrMaxMinList[2][0]]).range([0, 1]);
      let rectConWidth_linear = d3.scaleLinear().domain([conAttrMaxMinList[1][1], conAttrMaxMinList[1][0]]).range([30, 100]);

      let rectConCompute_color = d3.interpolate(currentConRectMinColor, currentConRectMaxColor);

      // concept---------
      let treeX = _this.treeX;
      let treeY = _this.treeY;
      let stepY = (height - 90) / (conceptTree.length);

      let tempConDistribution = {};

      let proSetData = [];
      let setOd = 0;
      _this.conStepY = stepY;
      let interY = _this.interY;
      let Ent_concept = [];
      for (let i = 0; i < conceptTree.length; i++) {
        let tempCon = tools.deepClone(conceptTree[i]);
        let cy = treeY + i * stepY;
        let cid = tempCon['id'];

        tempConDistribution[cid] = 0;

        tempCon['lay'] = cid.split("-").length;
        let cx = treeX * tempCon['lay'];
        tempCon['cx'] = cx;
        tempCon['cy'] = cy;
        tempCon['fill'] = importanceConCompute_color(importanceConColor_linear(tempCon['scoringRate']));
        tempCon['rectFill'] = rectConCompute_color(rectConColor_linear(tempCon['acceptedRate']));
        tempCon['rectW'] = rectConWidth_linear(tempCon['totalAttempts']);
        tempCon['r'] = linearList[parseInt(3 - tempCon['lay'])](tempCon['proCount']);
        tempCon['opacity'] = 1;
        Ent_concept.push(tempCon);
      }
      _this.Ent_concept = Ent_concept;
      //------------

      let proMaxMinDR = _this.proMaxMinDR;
      let proMaxMinDC = _this.proMaxMinDC;
      let proAttrMaxMinList = _this.proAttrMaxMinList;
      let currentMaxColor = _this.entProMaxColor;
      let currentMinColor = _this.entProMinColor;
      let importanceColor_linear = d3.scaleLinear().domain([proMaxMinDC[0], proMaxMinDC[1]]).range([0, 1]);
      let importanceCompute_color = d3.interpolate(currentMinColor, currentMaxColor);
      let rSize_linear = d3.scaleLinear().domain([proMaxMinDR[1], proMaxMinDR[0]]).range([15, 120]);

      let setMaxColor = _this.setMaxColor;
      let setMinColor = _this.setMinColor;
      let setColor_linear = d3.scaleLinear().domain([0, 1]).range([0, 1]);
      let setCompute_color = d3.interpolate(setMinColor, setMaxColor);

      let typeXMap = _this.typeXMap;
      //problem -----------
      let proX = _this.proX;
      let proY = _this.proY;
      let Ent_problem = [];
      let proStepY = (height - _this.interY * 12) / (problemData.length + 12);
      _this.proStepY = proStepY;
      _this.graphHeight = height;
      for (let i = 0; i < problemData.length; i++) {
        let tempPro = tools.deepClone(problemData[i]);
        let pid = tempPro['id'];
        let pSetId = tempPro['problemSetId'];
        if (proSetData.find(function (ps) { return ps['id'] == pSetId; }) == undefined) {
          proSetData.push({
            "id": pSetId,
            "order": setOd,
            "set": [tempPro]
          })
          setOd++;
        }
        else {
          proSetData.find(function (ps) { return ps['id'] == pSetId; })['set'].push(tempPro);
        }
        let cy = proY + i * proStepY + interY * setOd;
        // let lay = cid.split("-").length;
        let cx = proX;
        let r = proStepY;
        let fill = "grey";
        let opacity = 0.8;
        let scoreValueList = _this.getMaxMinValue(tempPro['stuData'], "scoringRate");
        let acceptedValueList = _this.getMaxMinValue(tempPro['stuData'], "acceptedRate");
        let totalAttemptsValueList = _this.getMaxMinValue(tempPro['stuData'], "totalAttempts");
        let groupVal = tempPro['groupVal'];

        groupVal.forEach((group,g)=>{
          let gscoreValueList = _this.getMaxMinValue(group['stuData'], "scoringRate",true);
          let gacceptedValueList = _this.getMaxMinValue(group['stuData'], "acceptedRate",true);
          let gtotalAttemptsValueList = _this.getMaxMinValue(group['stuData'], "totalAttempts",true);

          tempPro['groupVal'][g]['scoreValueList'] = gscoreValueList;
          tempPro['groupVal'][g]['acceptedValueList'] = gacceptedValueList;
          tempPro['groupVal'][g]['totalAttemptsValueList'] = gtotalAttemptsValueList;
        })

        // let Cname  = tempPro['name'];
        tempPro['scoreValueList'] = scoreValueList;
        tempPro['acceptedValueList'] = acceptedValueList;
        tempPro['totalAttemptsValueList'] = totalAttemptsValueList;


        tempPro['cx'] = cx//+typeXMap[tempPro['type']]*100;
        tempPro['cy'] = cy;
        tempPro['order'] = i;
        tempPro['width'] = rSize_linear(tempPro["conCount"]);
        tempPro['fill'] = importanceCompute_color(importanceColor_linear(tempPro['scoringRate']));
        tempPro['height'] = proStepY;
        Ent_problem.push(tempPro);
        // let circle = _this.drawCircle(entG, cx, cy, r, fill, opacity, );t text = _this.drawTxt(entG, cx+20, cy+3.5, Cname, "black", 12, `entConText_${cid}`);
      }
      let setStepY = (height - 90) / proSetData.length;
      let colorList = _this.mcolor;
      let tempTypeDistribution = {};
      Object.keys(typeXMap).forEach(t => {
        tempTypeDistribution[t] = 0;
      })
      for (let i = 0; i < proSetData.length; i++) {
        let psid = proSetData[i]['id'];
        let set = proSetData[i]['set'];
        proSetData[i]['cx'] = _this.proX - 3;
        proSetData[i]['width'] = _this.setWidth;
        let conDistribution = tools.deepClone(tempConDistribution);
        let typeDistribution = tools.deepClone(tempTypeDistribution);
        let scoringRate = 0;
        set.forEach(sPro => {
          let conList = sPro['conList'];
          scoringRate += sPro['scoringRate'];
          conList.forEach(c => {
            conDistribution[c]++;
            if (conDistribution[c] > _this.maxSetCon)
              _this.maxSetCon = conDistribution[c];
          });
          let type = sPro['type'];
          if (type == 'MULTIPLE_CHOICE_MORE_THAN_ONE_ANSWER')
            type = "MULTIPLE_CHOICE";
          if (type == 'CODE_COMPLETION')
            type = "PROGRAMMING";
          typeDistribution[type]++;
          // let groupData = sPro['groupVal'];
          // console.log(groupData)
        })
        proSetData[i]['scoringRate'] = scoringRate / set.length;
        proSetData[i]['conDistribution'] = conDistribution;
        proSetData[i]['typeDistribution'] = typeDistribution;
        // proSetData[i]['fill'] = colorList[proSetData[i]['order']];
        // console.log
        proSetData[i]['fill'] = setCompute_color(setColor_linear(proSetData[i]['scoringRate']));
        // -----------------------------------
        // proSetData[i]['cy'] = Ent_problem.find(function(ep){return ep['id'] == set[0];})['cy'];
        // let edP = Ent_problem.find(function(ep){return ep['id'] == set[set.length-1];})
        // proSetData[i]['height'] = edP['cy'] - proSetData[i]['cy']+edP['height'];
        // -----------------------------------
        proSetData[i]['cy'] = 30 + setStepY * i;
        proSetData[i]['height'] = setStepY - 10;
        // -------------------------------------
      }
      // let conDistributiondomainList = []
      // conceptTree.forEach(con=>{
      //   let domain = _this.getMaxMin(proSetData, 'conCount');
      // })
      _this.Ent_problem = Ent_problem;
      // ---------------------
      _this.proSetData = proSetData;
      // this.updataPro_ConRel(); 
      _this.updataEntProblemSetBack();
      _this.updataProSet_ConRel();
      _this.updataParallelCoordinatesplotBySet();
      if (_this.detailsEntPro != [])
        _this.updataEntProblemDetail();
      _this.drawFigureAnnotation();

    },
    drawFigureAnnotation() {
      const _this = this;
      let frontG = _this.frontG;

      let currentConMaxColor = _this.entConMaxColor;
      let currentConMinColor = _this.entConMinColor;
      let len = 6;

      let Color_linear = d3.scaleLinear().domain([0, len]).range([0, 1]);
      let Color_linear2 = d3.scaleLinear().domain([0, len * 3]).range([0, 1]);
      let Rsize_linear = d3.scaleLinear().domain([0, len]).range([1, 6]);
      let Compute_color = d3.interpolate(currentConMinColor, currentConMaxColor);
      let Compute_color1 = d3.interpolate("white", _this.setConCountColorMax);
      let Compute_color2 = d3.interpolate("white", _this.setTypeCountColorMax);
      let Compute_color3 = d3.interpolate(_this.setMinColor, _this.setMaxColor);

      let currentConRectMaxColor = _this.entConRectMaxColor;
      let currentConRectMinColor = _this.entConRectMinColor;
      let rectConColor_linear = d3.scaleLinear().domain([0, len]).range([0, 1]);
      let rectConCompute_color = d3.interpolate("white", currentConRectMaxColor);
      // _this.drawCircle(frontG, 20, 1000, 10, currentConMaxColor, 1, currentConMaxColor, "1", 'FigAtt', `FigAtt_conColor`);

      let textcon = _this.drawTxt(frontG, 10, 1065, "Concepts Value:", "black", 13, `FigAtt_con`);
      let textset = _this.drawTxt(frontG, 350, 1065, "Set Value:", "black", 13, `FigAtt_set`);
      let textsetSR = _this.drawTxt(frontG, 540, 1085, "ScoringRate:", "black", 10, `FigAtt_conColor`);

      let textsetR = _this.drawTxt(frontG, 480, 15, "Concepts", "black", 13, `FigAtt_conColor`, "middle");
      let textsetcon = _this.drawTxt(frontG, 560, 15, "Type", "black", 13, `FigAtt_conColor`, "middle");
      let textsettype = _this.drawTxt(frontG, 640, 15, "ScoringRate", "black", 13, `FigAtt_conColor`, "middle");
      let textsetRscor = _this.drawTxt(frontG, 720, 15, "Attempts", "black", 13, `FigAtt_conColor`, "middle");

      // let textpro = _this.drawTxt(frontG, 800, 1065, "Problems Value:", "black", 13, `FigAtt_pro`);
      let text1 = _this.drawTxt(frontG, 10, 1085, "ScoringRate:", "black", 10, `FigAtt_conColor`);
      let text2 = _this.drawTxt(frontG, 10, 1105, "Connection Nums:", "black", 10, `FigAtt_Rsize`);

      // let text3 = _this.drawTxt(frontG, 100, 1070, "Low", "black", 10, `FigAtt_Low`);
      // let text4 = _this.drawTxt(frontG, 100+10*len, 1070, "High", "black", 10, `FigAtt_High`);

      let text5 = _this.drawTxt(frontG, 180, 1085, "Attempts:", "black", 10, `FigAtt_conColor`);
      let text6 = _this.drawTxt(frontG, 180, 1105, "AcceptedRate:", "black", 10, `FigAtt_Rsize`);
      let textsetnum = _this.drawTxt(frontG, 350, 1085, "Connection Nums:", "black", 10, `FigAtt_proConDis`);
      let textsetTypenum = _this.drawTxt(frontG, 350, 1105, "Type Nums:", "black", 10, `FigAtt_proConDis`);

      let text7 = _this.drawTxt(frontG, 602, 1095, "Low", "black", 10, `FigAtt_Low`);
      let text8 = _this.drawTxt(frontG, 695, 1095, "High", "black", 10, `FigAtt_High`);
      let prex = 0;
      let prerx = 0;
      for (let i = 0; i < len * 3; i++) {
        let color3 = Compute_color3(Color_linear2(i));

        _this.drawRect(frontG, 620 + 4 * i, 1077, 4, 10, 0, color3, "1", "none", "1", `FigAtt_setColor${i}`, 'FigAtt');
      }
      for (let i = 0; i < len; i++) {
        let color = Compute_color(Color_linear(i));
        let color1 = Compute_color1(Color_linear(i));
        let color2 = Compute_color2(Color_linear(i));
        // let color3 = Compute_color3(Color_linear(i));
        let rcolor = rectConCompute_color(rectConColor_linear(i));

        _this.drawCircle(frontG, 110 + 10 * i, 1082, 3, color, 1, "red", "1", 'FigAtt', `FigAtt_conColor${i}`);

        _this.drawCircle(frontG, 110 + prex, 1102, Rsize_linear(i), Compute_color(Color_linear(7)), 1, "red", "1", 'FigAtt', `FigAtt_conRsize${i}`);

        prex += Rsize_linear(i) * 2 + 4;

        _this.drawRect(frontG, 250 + 12 * i, 1077, 10, 10, 0, rcolor, "1", "grey", "1", `FigAtt_conRectColor${i}`, 'FigAtt');

        _this.drawRect(frontG, 250 + prerx, 1097, i * 4, 10, 0, rectConCompute_color(rectConColor_linear(6)), "1", "grey", "1", `FigAtt_conRectWidth${i}`, 'FigAtt');

        _this.drawRect(frontG, 450 + prerx, 1077, i * 4, 10, 0, color1, "1", "grey", "1", `FigAtt_setconRectWidth${i}`, 'FigAtt');

        _this.drawRect(frontG, 450 + prerx, 1097, i * 4, 10, 0, color2, "1", "grey", "1", `FigAtt_settypeRectWidth${i}`, 'FigAtt');

        prerx += i * 4 + 2;
      }
    },
    updataSelectStudentListColor() {
      const _this = this;
      let SelectStudentList = _this.SelectStudentList;
      let colorList = _this.stuColorList;
      for (let i = 0; i < SelectStudentList.length; i++) {
        for (let j = 0; j < SelectStudentList[i].length; j++) {
          let stuId = SelectStudentList[i][j];
          d3.select(`#stuSetScoreLine_${stuId}`).attr("stroke", colorList[i]);
          d3.select(`#stuScoreLine_${stuId}`).attr("stroke", colorList[i]);
        }
      }
    },
    updataParallelCoordinatesplotBySet() {
      const _this = this;
      let entG = _this.entG;
      let relG = _this.relG;
      let Ent_concept = tools.deepClone(_this.Ent_concept);
      let Ent_problem = tools.deepClone(_this.Ent_problem);
      let pro_conRelData = tools.deepClone(_this.problemConceptData);
      let studentsData = tools.deepClone(_this.studentsData);
      let proSetData = tools.deepClone(_this.proSetData);
      let proSetOriData = tools.deepClone(_this.proSetOriData);
      let groupData = tools.deepClone(_this.groupData);
      console.log(groupData);
      let colorList = _this.mcolor;

      //轴
      let paraX = 1100;
      let stepY = (_this.graphHeight - 90) / (proSetData.length);
      let avpath = d3.path();
      let prex = 0;
      let prey = 0;
      for (let i = 0; i < proSetData.length; i++) {
        let cx = paraX;
        let cy = proSetData[i]['cy'] + proSetData[i]['height'] / 2//;stepY*(i+1)
        let width = 200;
        let height = 3;
        let psId = proSetData[i]['id'];
        let fill = proSetData[i]['fill'];
        proSetData[i]['axisX'] = cx;
        proSetData[i]['axisY'] = cy;
        proSetData[i]['axisW'] = width;
        proSetData[i]['axisH'] = height;
        let axis = _this.drawRect(entG, cx, cy, width, height, 0, fill, "0", "none", "1", `proSetAxis_${psId}`, 'proSetAxis');
        let av = 0;
        let num = 0;
        let totalScore = 0
        for (let j = 0; j < studentsData.length; j++) {
          let proSetScore = studentsData[i]['proSetScore'];
          let psData = proSetScore.find(function (psd) { return psd['id'] == psId; });
          av += psData['score'];
          totalScore = psData['totalScore'];
          num += 1;
        }
        av /= num;
        let val_linear = d3.scaleLinear().domain([0, totalScore]).range([cx, cx + width]);
        let pointy = cy;
        let pointx = val_linear(av);
        if (i == 0) {
          avpath.moveTo(pointx, pointy);
          prex = pointx;
          prey = pointy;
        }
        else {
          let c1x = prex;
          let c1y = (pointy + prey) / 2;
          let c2x = pointx;
          let c2y = c1y;
          avpath.bezierCurveTo(c1x, c1y, c2x, c2y, pointx, pointy);
          prey = pointy
          prex = pointx
        }
      }
      _this.drawLine(relG, avpath, "grey", 3, '0', "1", `stuSetScoreLine_av`, 'stuSetScoreLine');
      prex = 0;
      prey = 0;
      for (let i = 0; i < studentsData.length; i++) {
        let path = d3.path();
        let proSetScore = studentsData[i]['proSetScore'];
        let stuId = studentsData[i]['id'];
        for (let s = 0; s < proSetScore.length; s++) {
          let psId = proSetScore[s]['id'];
          let psData = proSetData.find(function (psd) { return psd['id'] == psId; });
          let cx = psData['axisX'];
          let w = psData['axisW'];
          let val_linear = d3.scaleLinear().domain([0, proSetScore[s]['totalScore']]).range([cx, cx + w]);
          let pointy = psData['axisY'];
          let pointx = val_linear(proSetScore[s]['score']);
          if (s == 0) {
            path.moveTo(pointx, pointy);
            prex = pointx;
            prey = pointy;
          }
          else {
            let c1x = prex;
            let c1y = (pointy + prey) / 2;
            let c2x = pointx;
            let c2y = c1y;
            path.bezierCurveTo(c1x, c1y, c2x, c2y, pointx, pointy);
            prey = pointy
            prex = pointx
          }
        }
        let groupD = groupData.find(function (d) { return d['id'] == stuId; });
        let fill = "grey";
        _this.drawLine(relG, path, fill, 1, '0', "0.3", `stuSetScoreLine_${stuId}`, 'stuSetScoreLine');
      }
    },
    updataParallelCoordinatesplotByPro() {
      d3.selectAll(`.proSetAxis`).remove();
      d3.selectAll(`.proAxis`).remove();
      d3.selectAll(`.stuSetScoreLine`).remove();
      const _this = this;
      let entG = _this.entG;
      let relG = _this.relG;
      let studentsData = tools.deepClone(_this.studentsData);
      let proSetData = tools.deepClone(_this.proSetData);
      let proSetOriData = tools.deepClone(_this.proSetOriData);
      let setEnt = tools.deepClone(_this.detailsEntPro);
      let colorList = _this.mcolor;
      let groupData = tools.deepClone(_this.groupData);
      //轴
      let paraX = 1100;
      let stepY = _this.graphHeight / (setEnt.length);
      let avpath = d3.path();
      let prex = 0;
      let prey = 0;
      for (let i = 0; i < setEnt.length; i++) {
        let cx = paraX;
        let cy = 10 +
          stepY * i;//setEnt[i]['cy']+setEnt[i]['height']/2//;stepY*(i+1)
        let width = 200;
        let height = 2;
        let psId = setEnt[i]['id'];
        let fill = setEnt[i]['fill'];
        setEnt[i]['axisX'] = cx;

        setEnt[i]['axisY'] = cy;
        setEnt[i]['axisW'] = width;
        setEnt[i]['axisH'] = height;
        let axis = _this.drawRect(entG, cx, cy, width, height, 0, fill, "0", "none", "1", `proAxis_${psId}`, 'proAxis');
        let av = 0;
        let num = 0;
        let maxv = 0
        for (let j = 0; j < studentsData.length; j++) {
          let proList = studentsData[j]['pro'];
          let psData = proList.find(function (psd) { return psd['id'] == psId; });
          if (psData['totalScore'] != undefined) {
            // console.log(psData)
            av += psData['totalScore'] / psData['totalAttempts'];
          }
          // av+=psData['totalScore']/psData['totalAttempts'];
          // else
          num += 1;
        }
        av /= num;
        // console.log(av)
        let val_linear = d3.scaleLinear().domain([0, 1]).range([cx, cx + width]);
        let pointy = cy;
        let pointx = val_linear(av);
        if (i == 0) {
          avpath.moveTo(pointx, pointy);
          prex = pointx;
          prey = pointy;
        }
        else {
          let c1x = prex;
          let c1y = (pointy + prey) / 2;
          let c2x = pointx;
          let c2y = c1y;
          avpath.bezierCurveTo(c1x, c1y, c2x, c2y, pointx, pointy);
          prey = pointy
          prex = pointx
        }

      }
      _this.drawLine(relG, avpath, "grey", 3, '0', "1", `stuScoreLine_av`, 'stuScoreLine');
      prex = 0;
      prey = 0;
      for (let i = 0; i < studentsData.length; i++) {
        let path = d3.path();
        let proList = studentsData[i]['pro'];
        let stuId = studentsData[i]['id'];
        let s = 0;
        setEnt.forEach(se => {
          let pId = se['id'];
          let proaxisD = proList.find(function (se) { return se['id'] == pId });
          let cx = se['axisX'];
          let w = se['axisW'];
          let pointy = se['axisY'];
          // ----------------------------------
          // let val_linear = d3.scaleLinear().domain([0,se['score']]).range([cx, cx+w]);
          // let pointx = val_linear(proaxisD['best']['score']); 
          // --------------------------------------
          let val_linear = d3.scaleLinear().domain([0, 1]).range([cx, cx + w]);
          let pointx = val_linear(proaxisD['totalScore'] / proaxisD['totalAttempts']);
          if (proaxisD['totalScore'] == undefined)
            pointx = val_linear(0)
          // -------------------------------------------
          if (s == 0) {
            path.moveTo(pointx, pointy);
            prex = pointx;
            prey = pointy;
            s += 1;
          }
          else {

            let c1x = prex;
            let c1y = (pointy + prey) / 2;
            let c2x = pointx;
            let c2y = c1y;
            path.bezierCurveTo(c1x, c1y, c2x, c2y, pointx, pointy);
            prey = pointy;
            prex = pointx;
            // path.lineTo();
          }
        })

        let groupD = groupData.find(function (d) { return d['id'] == stuId; });
        let fill = 'grey'//colorList[groupD['kmeansC']*3];
        let line = _this.drawLine(entG, path, fill, 1, '0', '0.3', `stuScoreLine_${stuId}`, 'stuScoreLine');
        // let proSetScore = studentsData[i]['proSetScore'];
        // let stuId = studentsData[i]['id'];
        // for(let s=0;s<proSetScore.length;s++){
        //   let psId = proSetScore[s]['id'];
        //   let psData = proSetData.find(function(psd){return psd['id'] == psId;});
        //   let cx = psData['axisX'];
        //   let w = psData['axisW'];
        //   let val_linear = d3.scaleLinear().domain([0,proSetScore[s]['totalScore']]).range([cx, cx+w]);
        //   let pointy = psData['axisY'];
        //   let pointx = val_linear(proSetScore[s]['score']); 
        //   if(s==0){
        //     path.moveTo(pointx,pointy);
        //   }
        //   else{
        //     path.lineTo(pointx,pointy);
        //   }
        // }
        // _this.drawLine(relG, path, "rgb(200,200,200)", 2, '0', `stuSetScoreLine_${stuId}`, 'stuSetScoreLine');
      }
    },
    updataPro_ConRel() {
      const _this = this;
      let entG = _this.entG;
      let relG = _this.relG;
      let typeXMap = _this.typeXMap;
      let Ent_concept = tools.deepClone(_this.Ent_concept);
      let Ent_problem = tools.deepClone(_this.Ent_problem);
      let pro_conRelData = tools.deepClone(_this.problemConceptData);
      for (let i = 0; i < pro_conRelData.length; i++) {
        let curRel = pro_conRelData[i];
        let conId = curRel['conceptId'];
        let proId = curRel['problem'];
        let conData = Ent_concept.find(function (d) { return d['id'] == conId; });
        let proData = Ent_problem.find(function (d) { return d['id'] == proId; });
        let sx = conData['cx'] + conData['rectW'] + 30;
        let sy = conData['cy'];
        let tx = proData['cx'];
        let ty = proData['cy'] + proData['height'] / 2;
        let c1x = (sx) + 100;
        let c1y = (sy)
        let c2x = (sx);
        let c2y = (ty)
        _this.drawBsLine(relG, sx, sy, c1x, c1y, c2x, c2y, tx, ty, "grey", "0.5px", "1", `proConRel_${conId}_${proId}`, "proConRel");
      }
    },
    updataProSet_ConRel() {
      const _this = this;
      let entG = _this.entG;
      let relG = _this.relG;
      let typeXMap = _this.typeXMap;
      let Ent_concept = tools.deepClone(_this.Ent_concept);
      let Ent_problem = tools.deepClone(_this.Ent_problem);
      let proSetData = tools.deepClone(_this.proSetData);
      let pro_conRelData = tools.deepClone(_this.problemConceptData);
      for (let i = 0; i < pro_conRelData.length; i++) {
        let curRel = pro_conRelData[i];
        let conId = curRel['conceptId'];
        let proId = curRel['problem'];
        let type = curRel['type'];
        let conData = Ent_concept.find(function (d) { return d['id'] == conId; });
        let proData = Ent_problem.find(function (d) { return d['id'] == proId; });
        let curproSetData = proSetData.find(function (pd) { return pd['id'] == proData['problemSetId'] });
        let sx = conData['cx'] + 130;
        let sy = conData['cy'];
        let tx = curproSetData['cx'];
        let ty = curproSetData['cy'] + curproSetData['height'] / 2;
        let c1x = (sx) + 150;
        let c1y = (sy);
        let c2x = (sx);
        let c2y = (ty);
        let fill = "grey";
        if (type == "1") { fill = 'red' }
        _this.drawBsLine(relG, sx, sy, c1x, c1y, c2x, c2y, tx, ty, fill, "1px", "0.2", `proSetConRel_${conId}_${proData['problemSetId']}`, "proSetConRel");
      }
    },
    updataPro_ProSelfRel(tranY) {
      const _this = this;
      let entG = _this.entG;
      let relG = _this.relG;
      let selectSetId = _this.curProblemSetId;
      let Ent_problem = tools.deepClone(_this.Ent_problem);
      for (let i = 0; i < Ent_problem.length; i++) {
        let pid = Ent_problem[i]['id'];
        if (Ent_problem[i]["problemSetId"] == selectSetId) {
          let proData = Ent_problem.find(function (d) { return d['id'] == pid; });
          let prog = d3.select(`#entPro_${pid}`)
          let proSlefg = d3.select(`#probySet_${pid}`)
          let sx = parseFloat(prog.attr("x")) + parseFloat(prog.attr("width"));
          let sy = parseFloat(prog.attr("y")) + parseFloat(prog.attr("height")) / 2;
          let tx = parseFloat(proSlefg.attr("x"));
          let ty = parseFloat(proSlefg.attr("y")) + tranY + parseFloat(proSlefg.attr("height")) / 2;
          // console.log(sx,sy,tx,ty,prog.attr("x"),proSlefg.attr("y"),prog.attr("width"),prog.attr("height"),proSlefg.attr("height"))
          let c1x = (sx) + 100;
          let c1y = (sy)
          let c2x = (tx) - 100;
          let c2y = (ty)
          let fill = proData['fill']
          _this.drawBsLine(relG, sx, sy, c1x, c1y, c2x, c2y, tx, ty, fill, "2px", "0.4", `proSelfRel_${pid}`, "proSelfRel");
        }
      }
    },
    updataPro_ProSetRel(tranY) {
      const _this = this;
      let entG = _this.entG;
      let relG = _this.relG;
      let selectSetId = _this.curProblemSetId;
      let Ent_problem = tools.deepClone(_this.detailsEntPro);
      let proSetData = tools.deepClone(_this.proSetData);
      d3.selectAll(`.proSetRel`).remove();
      for (let i = 0; i < Ent_problem.length; i++) {
        let pid = Ent_problem[i]['id'];
        let proSetId = Ent_problem[i]['problemSetId'];
        let proSlefg = d3.select(`#proDetil_${pid}`)
        let prog = d3.select(`#proSet_${proSetId}`)
        let sx = parseFloat(prog.attr("x")) + parseFloat(prog.attr("width"));
        let sy = parseFloat(prog.attr("y")) + parseFloat(prog.attr("height")) / 2;
        let tx = parseFloat(proSlefg.attr("x"));
        let ty = parseFloat(proSlefg.attr("y")) + tranY + parseFloat(proSlefg.attr("height")) / 2;
        // console.log(sx,sy,tx,ty,prog.attr("x"),proSlefg.attr("y"),prog.attr("width"),prog.attr("height"),proSlefg.attr("height"))
        let c1x = (sx) + 60;
        let c1y = (sy);
        let c2x = (tx) - 60;
        let c2y = (ty);
        let fill = Ent_problem[i]['fill'];
        _this.drawBsLine(relG, sx, sy, c1x, c1y, c2x, c2y, tx, ty, fill, "1px", "0.4", `proSetRel_${pid}`, "proSetRel");
        // }
      }
    },
    updataEntConcept() {
      const _this = this;
      let entG = _this.entG;
      let relG = _this.relG;
      let Ent_concept = tools.deepClone(_this.Ent_concept);

      let conX = _this.treeX;
      let conY = _this.treeY;
      let conStepY = _this.conStepY;
      for (let i = 0; i < Ent_concept.length; i++) {
        let curEntCon = Ent_concept[i];
        let cid = curEntCon['id'];
        let cx = curEntCon['cx'];
        let cy = curEntCon['cy'];
        let r = curEntCon['r'];
        let Cname = curEntCon['name'];
        let fill = curEntCon['fill'];
        let opacity = curEntCon['opacity'];

        let fillRect = curEntCon['rectFill'];
        let widthRect = curEntCon['rectW'];

        let circle = _this.drawCircle(entG, cx, cy, r, fill, opacity, "red", "1", 'entCon', `entCon_${cid}`);

        circle.on("click", function (d) {
          let selectCon = d3.select(this);
          let selectConId = selectCon.attr("id").split("_")[1];
          _this.curConceptId = selectConId;
        })

        // let cG = entG.append("g")
        // .attr("transform", `translate(${cx},${cy})`);

        // _this.drawEntityConcept(entG, cx, cy, `entCon_${cid}`);


        let rectB = _this.drawRect(entG, cx + 20, cy - 8, 100, 16, 1, "rgb(200,200,200)", "0", "none", "1", `entConRectB_${cid}`, 'entConRect');
        let rect = _this.drawRect(entG, cx + 20, cy - 8, widthRect, 16, 1, fillRect, "0", "none", "1", `entConRect_${cid}`, 'entConRect');
        rectB.on("click", function (d) {
          let selectCon = d3.select(this);
          let selectConId = selectCon.attr("id").split("_")[1];
          _this.curConceptId = selectConId;
        })
        rect.on("click", function (d) {
          let selectCon = d3.select(this);
          let selectConId = selectCon.attr("id").split("_")[1];
          _this.curConceptId = selectConId;
        })
        let text = _this.drawTxt(entG, cx + 20, cy + 3.5, Cname, "white", 12, `entConText_${cid}`);

        let fatherId = curEntCon['father'];
        if (parseInt(fatherId) != -1) {
          let curCon = Ent_concept.find(function (d) { return d['id'] == cid; });
          let fatherCon = Ent_concept.find(function (d) { return d['id'] == fatherId; });
          let sx = fatherCon['cx'];
          let sy = fatherCon['cy'] + fatherCon['r'];
          let tx = curCon['cx'] - curCon['r'];
          let ty = curCon['cy'];

          _this.drawBsLine(relG, sx, sy, sx, ty, sx, ty, tx, ty, "grey", "2px", "0.4", `conRel_${fatherId}_${cid}`, "conRel");
        }
      }
    },
    updataEntProblem() {
      const _this = this;
      let entG = _this.entG;
      let Ent_problem = tools.deepClone(_this.Ent_problem);
      let proSetData = tools.deepClone(_this.proSetData);
      let proX = _this.proX;
      let proY = _this.proY;
      let typeColorMap = {
        "TRUE_OR_FALSE": _this.mcolor[1],
        "MULTIPLE_CHOICE": _this.mcolor[3],
        "FILL_IN_THE_BLANK": _this.mcolor[5],
        "PROGRAMMING": _this.mcolor[7],
        "CODE_COMPLETION": _this.mcolor[9],
        "MULTIPLE_CHOICE_MORE_THAN_ONE_ANSWER": _this.mcolor[11]
      }
      let interY = _this.interY;
      let typeXMap = _this.typeXMap;
      let proStepY = _this.proStepY;
      let attrList = _this.proAttrList;
      let attrLen = attrList.length;
      let proAttrMaxMinList = _this.proAttrMaxMinList;

      let proMaxMinDR = _this.proMaxMinDR;
      let wSize_linear = d3.scaleLinear().domain([proMaxMinDR[1], proMaxMinDR[0]]).range([20, 100]);
      for (let i = 0; i < Ent_problem.length; i++) {
        let curEntPro = Ent_problem[i];
        let type = curEntPro['type'];
        let pid = curEntPro['id'];
        let cx = curEntPro['cx']//+typeXMap[type]*30;
        let cy = curEntPro['cy'];
        let cH = curEntPro['height'];
        let cW = curEntPro['width'];
        let fill = curEntPro['fill'];
        let pOrder = curEntPro['order'];
        let inter = 1;
        let typeColor = typeColorMap[type]
        let circle = _this.drawCircle(entG, cx, cy + _this.proStepY / 2, proStepY / 2, typeColor, '1', "none", "1", 'entProCir', `entProCir_${pid}`);
        // let rect = _this.drawRect(entG, cx+cH/2, cy, cW, cH, 1, fill, "0", "none","1", `entPro_${pid}`, 'entPro');
        let rect = _this.drawRect(entG, cx + cH / 2, cy, 180, cH, 1, fill, "0", "none", "0.5", `entPro_${pid}`, 'entPro');
        rect.on("mousemove", function (d) {
          let selectPro = d3.select(this);
          let selectProId = selectPro.attr("id").split("_")[1];
          let proD = Ent_problem.find(function (p) { return p['id'] == selectProId });
          let pSetId = proD['problemSetId'];
          let pSet = proSetData.find(function (ps) { return ps['id'] == pSetId; })
          let pSetOd = pSet['order'] + 1;
          let od = proD['order'];
          Ent_problem.forEach(entPro => {
            if (entPro['id'] == selectProId) {
              entPro['cy'] = proY + entPro['order'] * proStepY + interY * pSetOd;
              entPro['height'] = (proStepY - inter) * 5;
              od = entPro['order'];
            }
            else if (entPro['order'] < od) {
              let cproD = Ent_problem.find(function (p) { return p['id'] == entPro['id'] });
              let cpSetId = cproD['problemSetId'];
              let cpSet = proSetData.find(function (ps) { return ps['id'] == cpSetId; })
              let cpSetOd = cpSet['order'] + 1;

              entPro['cy'] = proY + entPro['order'] * proStepY + interY * cpSetOd;
              entPro['height'] = (proStepY - inter)
            }
            else if (entPro['order'] > od) {
              let cproD = Ent_problem.find(function (p) { return p['id'] == entPro['id'] });
              let cpSetId = cproD['problemSetId'];
              let cpSet = proSetData.find(function (ps) { return ps['id'] == cpSetId; })
              let cpSetOd = cpSet['order'] + 1;
              entPro['cy'] = proY + entPro['order'] * proStepY + (proStepY - 1) * 4 + interY * cpSetOd;
              entPro['height'] = (proStepY - inter)
            }
          })
          _this.Ent_problem = Ent_problem;
        }).on("click", function (d) {
          let selectPro = d3.select(this);
          let selectProId = selectPro.attr("id").split("_")[1];
          _this.curProblemId = selectProId;
        })
        let attrW = 30
        // for (let j = 0; j < attrLen; j++) {
        //   let curP = _this.calcRsize(proAttrMaxMinList[j], curEntPro[attrList[j]], 30);
        //   let attColor = _this.mLigntcolor[j*2]
        //   let rectAttr = _this.drawRect(entG, cx+j*attrW, cy, curP, cH, 1, attColor, "0.8", "grey","1", `prottr_${pid}_${attrList[j]}`, 'proAttr');
        // }
        // le

      }
    },
    updataEntProblemDetailBySet(type, name) {
      const _this = this;
      let selectSetId = _this.curProblemSetId;
      let Ent_problem = tools.deepClone(_this.Ent_problem);
      let setEnt = [];
      if (type == 'con') {
        let pro_conRelData = tools.deepClone(_this.problemConceptData);
        pro_conRelData.forEach(rel => {
          let proId = rel['problem'];
          let conId = rel['conceptId'];
          if (conId == name) {
            let proData = Ent_problem.find(function (d) { return d['id'] == proId; })
            let proSetId = proData['problemSetId'];
            if (proSetId == selectSetId) {
              setEnt.push(proData);
            }
          }
        })
        _this.detailsEntPro = setEnt;
        return;
      }
      for (let i = 0; i < Ent_problem.length; i++) {
        if (Ent_problem[i]["problemSetId"] == selectSetId) {
          let entSetPro = tools.deepClone(Ent_problem[i]);
          if (type == "none") {
            setEnt.push(entSetPro);
          }
          else if (type == 'type') {
            if (Ent_problem[i]["type"] == name) {
              setEnt.push(entSetPro);
            }
          }
        }
      }
      _this.detailsEntPro = setEnt;
    },

    updataEntProblemDetail() {
      const _this = this;
      let entG = _this.entbySetG;
      let selectSetId = _this.curProblemSetId;
      let Ent_problem = tools.deepClone(_this.Ent_problem);
      let proMaxMinDR = _this.proMaxMinDR;
      let setX = _this.setX;
      let setY = _this.setY;

      let attrList = ["scoringRate", "acceptedRate", "totalAttempts"];
      let attrLen = attrList.length;

      entG.selectAll(".proDetil").remove();
      entG.selectAll(".proDetilB").remove();
      entG.selectAll(".proDetilAttr").remove();

      let setEnt = _this.detailsEntPro;

      let setStepY = 50;
      let setProWidth = 200;
      let proAttrMaxMinList = _this.proAttrMaxMinList;
      let wSize_linear = d3.scaleLinear().domain([proMaxMinDR[1], proMaxMinDR[0]]).range([20, 100]);

      let j = 0;
      for (let i = 0; i < setEnt.length; i++) {
        let curEntPro = setEnt[i];
        let pid = curEntPro['id'];
        let gpro = Ent_problem.find(function (p) { return p['id'] == pid; });

        if (gpro != undefined) {
          let groupVal = gpro['groupVal'];
          let groupLen = groupVal.length;
          setStepY = 50 + 10*groupLen;
          let cx = setX;
          let cy = setY + j * setStepY;
          let cH = setStepY -20;
          let cW = curEntPro['width']//wSize_linear(curEntPro['scoringRate']);
          let fill = curEntPro['fill'];
          let pOrder = curEntPro['order'];
          let rectback = _this.drawRect(entG, cx, cy, setProWidth, cH, 5, "grey", "10", "grey", "0.3", `proDetilB_${pid}_${j}`, 'proDetilB');
          let rect = _this.drawRect(entG, cx, cy, cW, cH, 5, fill, "10", fill, "1", `proDetil_${pid}`, 'proDetil');
          j++;
          rect.on("click", function (d) {
            let selectPro = d3.select(this);
            let selectProId = selectPro.attr("id").split("_")[1];
            _this.curProblemId = selectProId;
          })
          let scoreValueList = curEntPro['scoreValueList'];
          let acceptedValueList = curEntPro['acceptedValueList'];
          let totalAttemptsValueList = curEntPro['totalAttemptsValueList'];
          let dmList = [scoreValueList, acceptedValueList, totalAttemptsValueList];
          let interW = setProWidth / (attrLen);
          let attrW = interW;
          let attrWA = interW/(groupLen+2);
          for (let j = 0; j < attrLen; j++) {
            let attColor = _this.attrColorList[j];
            let Compute_color = d3.interpolate("white", attColor);
            let maxMin = proAttrMaxMinList[j];
            let color_linear = d3.scaleLinear().domain([maxMin[1], maxMin[0]]).range([0, 1]);
            let curAttrColor = Compute_color(color_linear(curEntPro[attrList[j]]));
            let curP = _this.calcRsize(proAttrMaxMinList[j], curEntPro[attrList[j]], cH);

            _this.drawAttrreact(entG, cx + j * (interW), cy, attrW *0.8, cH, dmList[j], attrList[j], curAttrColor, `proDetilsAttr_${pid}_${attrList[j]}`,"grey",attColor);
          } // let rectAttr = _this.drawRect(entG, cx+j*attrW, cy+cH-curP, attrW-10, curP, 1, attColor, "0.2", "grey","1", `proDetilAttr_${pid}_${attrList[j]}`, 'proDetilAttr');

          let groupStepY = 10;
          let gs_linear = d3.scaleLinear().domain([0, 1]).range([0, cH]);
          for (let g = 0; g < groupLen; g++) {
            let curP = gs_linear(groupVal[g]['scoringRate']);

            // let 
            let gscoreValueList = groupVal[g]['scoreValueList'];
            let gacceptedValueList = groupVal[g]['acceptedValueList'];
            let gtotalAttemptsValueList = groupVal[g]['totalAttemptsValueList'];
            let gdmList = [gscoreValueList, gacceptedValueList, gtotalAttemptsValueList];
            let gColor = _this.stuColorList[g];
            // let rectgroup = _this.drawRect(entG, cx + attrW * 3 + g * groupStepY, cy + cH - curP, groupStepY - 5, curP, 1, gColor, "0.2", "grey", "1", `proDetilGroup_${pid}_${g}`, 'proDetilGroup');
            
            for (let j = 0; j < attrLen; j++) {
              let attColor = _this.attrColorList[j];
              let Compute_color = d3.interpolate("white", attColor);
              let Compute_colorg = d3.interpolate("white", gColor);
              let maxMin = proAttrMaxMinList[j];
              let color_linear = d3.scaleLinear().domain([maxMin[1], maxMin[0]]).range([0, 1]);
              let gcurAttrColor = Compute_color(color_linear(groupVal[g][attrList[j]]));
              let gcurAttrGColor = Compute_colorg(color_linear(groupVal[g][attrList[j]]));

              _this.drawAttrreact(entG, cx + j * (interW)+2+(g+0.5)*(attrWA), cy, attrWA, cH, gdmList[j], attrList[j], gcurAttrGColor, `proDetilsGroupAttr_${pid}_${g}_${attrList[j]}`,"grey",gColor);
              // console.log(gdmList[j],attrList[j],curEntPro[attrList[j]],dmList[j])
            }
          }
        }
      }

      _this.updataPro_ProSetRel(_this.graphGTransformY);
    },
    getMaxMinValue(data, valueName,isGroupData = false) {

      let mind = 1000000;
      let maxd = -1000000;
      let av = 0;
      let num = 0;
      let arr = []
      Object.keys(data).forEach(stuD => {
        if((!isGroupData)||(data[stuD]['gvjg'] != -1))
        {
        maxd = (data[stuD][valueName] > maxd) ? data[stuD][valueName] : maxd;
        mind = (data[stuD][valueName] < mind) ? data[stuD][valueName] : mind;
        if (data[stuD][valueName] != undefined) {
          av += data[stuD][valueName];
          num += 1;
          arr.push(data[stuD][valueName])
        }
      }
      });
      
      if (num != 0)
        av /= num;
      else
        av = 0;
      let fc = 0;
      
      arr.forEach(stuD => {
          fc+=Math.pow(stuD - av, 2);
      });

      if (num != 0)
        fc /= num;
      else
        fc = 0;

      var compare = function (x, y) {//比较函数
        return x > y
      };
      var mid; //中位数
      arr.sort(compare); //数组排序
      if (arr.length % 2 == 0) {
        mid = (arr[arr.length / 2] + arr[arr.length / 2 + 1]) / 2
      }
      if (arr.length % 2 != 0) {
        mid = arr[(arr.length + 1) / 2]
      }
      return [mind, maxd, av, mid, arr[parseInt(arr.length / 4)], arr[parseInt(arr.length / 4 * 3)],fc]
    },
    drawAttrreactO(svg, cx, cy, w, h, data, valueName, attrColor, idN,boxColor = "grey" ) {
      const _this = this;
      let proAttrMaxMinList = _this.proAttrMaxMinList;
      let attrList = _this.proAttrList;
      let maxMin = proAttrMaxMinList[attrList.indexOf(valueName)];
      let mind = data[0]
      let maxd = data[1]
      let av = data[2]
      let mid = data[3]
      let q1 = data[4]
      let q2 = data[5]
      let len_linear = d3.scaleLinear().domain([0, 1]).range([0, h]);
      if (valueName == "totalAttempts") {
        len_linear = d3.scaleLinear().domain([0, Math.sqrt(67)]).range([0, h]);
        mind = Math.sqrt(mind);
        maxd = Math.sqrt(maxd);
        av = Math.sqrt(av);
        q1 = Math.sqrt(q1);
        q2 = Math.sqrt(q2);
      }
      let avp = len_linear(av);
      let maxp = len_linear(maxd);
      let minp = len_linear(mind);
      let midp = len_linear(mid);
      let q1p = len_linear(q1);
      let q2p = len_linear(q2);
      // let boxColor = "grey"
      // _this.drawRect(svg, cx, cy, w, h, 1, attrColor, "0.2", "grey", "1", `B_${idN}`, 'proDetilAttr');
      _this.drawRect(svg, cx + 3, cy + h - q2p, w - 6, q2p - q1p, 1, attrColor, "1", boxColor, "1", `${idN}`, 'proDetilAttr');
      // _this.drawRect(svg, cx, cy + h - avp, w, 2, 1, "white", "0.2", "none", "1", `av_${idN}`, 'proDetilAttr');
      _this.drawRect(svg, cx + 3, cy + h - midp, w - 6, 1, 1, boxColor, "0.2", "none", "1", `mid_${idN}`, 'proDetilAttr');
      _this.drawRect(svg, cx, cy + h - maxp, w, 1, 1, boxColor, "0.2", "none", "1", `max_${idN}`, 'proDetilAttr');
      _this.drawRect(svg, cx, cy + h - minp, w, 1, 1, boxColor, "0.2", "none", "1", `min_${idN}`, 'proDetilAttr');

      _this.drawRect(svg, cx + w / 2 - 1, cy + h - maxp, 1, maxp - q2p, 1, boxColor, "0", "none", "1", `maxl_${idN}`, 'proDetilAttr');
      _this.drawRect(svg, cx + w / 2 - 1, cy + h - q1p, 1, q1p - minp, 1, boxColor, "0", "none", "1", `minl_${idN}`, 'proDetilAttr');
      // _this.drawRect(svg, cx, cy + h - q1p, w, 2, 1, boxColor, "0.2", "none", "1", `q1_${idN}`, 'proDetilAttr');
      // _this.drawRect(svg, cx, cy + h - q2p, w, 2, 1, boxColor, "0.2", "none", "1", `q2_${idN}`, 'proDetilAttr');

    },
    drawAttrreact(svg, cx, cy, w, h, data, valueName, attrColor, idN,boxColor = "grey",attColorO = 'none' ) {
      const _this = this;
      let proAttrMaxMinList = _this.proAttrMaxMinList;
      let attrList = _this.proAttrList;
      let maxMin = proAttrMaxMinList[attrList.indexOf(valueName)];
      let mind = data[0];
      let maxd = data[1];
      let av = data[2];
      let mid = data[3];
      let q1 = data[4];
      let q2 = data[5];
      let fc = data[6];
      console.log(fc)
      let zfc = av+fc;
      let ffc = av-fc;
      let len_linear = d3.scaleLinear().domain([0, 1]).range([0, h]);
      if (valueName == "totalAttempts") {
        len_linear = d3.scaleLinear().domain([0, Math.sqrt(67)]).range([0, h]);
        mind = Math.sqrt(mind);
        maxd = Math.sqrt(maxd);
        av = Math.sqrt(av);
        q1 = Math.sqrt(q1);
        q2 = Math.sqrt(q2);
        zfc = Math.sqrt(zfc);
        ffc = Math.sqrt(ffc);
      }
      let avp = len_linear(av);
      let maxp = len_linear(maxd);
      let minp = len_linear(mind);
      let midp = len_linear(mid);
      let q1p = len_linear(q1);
      let q2p = len_linear(q2);
      let zfcp = len_linear(zfc);
      let ffcp = len_linear(ffc);
      // let boxColor = "grey"
      // _this.drawRect(svg, cx, cy, w, h, 1, attrColor, "0.2", "grey", "1", `B_${idN}`, 'proDetilAttr');
      // _this.drawRect(svg, cx, cy + h - avp, w, 2, 1, "white", "0.2", "none", "1", `av_${idN}`, 'proDetilAttr');

      _this.drawRect(svg, cx, cy + h - avp, w , avp - minp, 1, attrColor, "0.2", "white", "1", `mid_${idN}`, 'proDetilAttr');

      _this.drawRect(svg, cx, cy + h - zfcp, w , zfcp - avp, 1, attColorO, "0.2", "none", "1", `zfc_${idN}`, 'proDetilAttr');
      _this.drawRect(svg, cx, cy + h - avp, w , avp - ffcp, 1, attColorO, "0.2", "none", "1", `ffc_${idN}`, 'proDetilAttr');

      _this.drawRect(svg, cx, cy + h - maxp, w, maxp - minp, 1, "none", "1", boxColor, "1", `${idN}`, 'proDetilAttr');
      // _this.drawRect(svg, cx, cy + h - maxp, w, 1, 1, boxColor, "0.2", "none", "1", `max_${idN}`, 'proDetilAttr');
      // _this.drawRect(svg, cx, cy + h - minp, w, 1, 1, boxColor, "0.2", "none", "1", `min_${idN}`, 'proDetilAttr');

      // _this.drawRect(svg, cx + w / 2 - 1, cy + h - maxp, 1, maxp - q2p, 1, boxColor, "0", "none", "1", `maxl_${idN}`, 'proDetilAttr');
      // _this.drawRect(svg, cx + w / 2 - 1, cy + h - q1p, 1, q1p - minp, 1, boxColor, "0", "none", "1", `minl_${idN}`, 'proDetilAttr');
      // _this.drawRect(svg, cx, cy + h - q1p, w, 2, 1, boxColor, "0.2", "none", "1", `q1_${idN}`, 'proDetilAttr');
      // _this.drawRect(svg, cx, cy + h - q2p, w, 2, 1, boxColor, "0.2", "none", "1", `q2_${idN}`, 'proDetilAttr');

    },
    updataEntProblemSetBack() {
      const _this = this;
      let entSetG = _this.entSetG;
      let proSetData = tools.deepClone(_this.proSetData);
      let Ent_problem = tools.deepClone(_this.Ent_problem);
      let maxSetCon = _this.maxSetCon
      for (let i = 0; i < proSetData.length; i++) {
        let fill = proSetData[i]['fill'];
        let psid = proSetData[i]['id'];
        let set = proSetData[i]['set'];
        let conDistribution = proSetData[i]['conDistribution'];
        let typeDistribution = proSetData[i]['typeDistribution'];
        let num = 0;
        // ------------------------------
        // let edP = Ent_problem.find(function(ep){return ep['id'] == set[set.length-1];})
        // proSetData[i]['cy'] = Ent_problem.find(function(ep){return ep['id'] == set[0];})['cy'];
        // proSetData[i]['height'] = edP['cy'] - proSetData[i]['cy']+edP['height'];
        // ------------------------------

        // ------------------------------
        let cx = proSetData[i]['cx'];
        let cy = proSetData[i]['cy'];
        let width = proSetData[i]['width'];
        let height = proSetData[i]['height'];
        let rect = _this.drawRect(entSetG, cx, cy, width, height, 10, fill, "5", "none", "1", `proSet_${psid}`, 'proSet');
        // let rect1 = _this.drawRect(entSetG, cx, cy+height/3, width, 1, 1, "grey", "5", "none","1", `proSet1_${psid}`, 'proSet');
        // let rect2 = _this.drawRect(entSetG, cx, cy+height/3*2, width, 1, 1, "grey", "5", "none","1", `proSet2_${psid}`, 'proSet');
        let rect1 = _this.drawRect(entSetG, cx + width / 3 - 25, cy, 1, height, 1, "white", "5", "none", "1", `proSet1_${psid}`, 'proSet');
        let rect2 = _this.drawRect(entSetG, cx + width / 3 * 2 - 50, cy, 1, height, 1, "white", "5", "none", "1", `proSet2_${psid}`, 'proSet');
        rect.on("click", function (d) {
          let selectSet = d3.select(this);
          d3.selectAll(".proSet").attr("opacity", 0.1);
          selectSet.attr("opacity", 1)
          let selectSetId = selectSet.attr("id").split("_")[1];
          _this.curProblemSetId = selectSetId;
        })

        // _this.drawRiver(entSetG,cx+width/3*2+3,cy,height,width/3,`proSetRiver_${psid}`,proSetData[i]['set']);
        _this.drawSetValuePoly(entSetG, cx + width / 2 + 1, cy, height - 2, width / 2, `proSetValuePoly_${psid}`, proSetData[i]['set']);
        // let min1w = height/3;
        // let max1w = width/9;       
        // let min1h = 10;
        // let max1h = height/3;

        let min1w = 0;
        let max1w = width / 3 - 30;
        let min1h = 10;
        let max1h = (height - 6) / 8;
        let j = 0
        let setConCount_linear = d3.scaleLinear().domain([0, Math.sqrt(maxSetCon)]).range([min1w, max1w]);
        let currentMinColor = _this.setConCountColorMin;
        let currentMaxColor = _this.setConCountColorMax;

        let setConCountColor_linear = d3.scaleLinear().domain([0, maxSetCon]).range([0, 1]);
        let setConCountCompute_color = d3.interpolate(currentMinColor, currentMaxColor);
        let conRootDistribution = {};
        let maxnum = 0;

        Object.keys(conDistribution).forEach(conD => {
          let conid = conD;
          let idSpilt = conid.split("-");
          let rootId = idSpilt[0];
          maxnum += conDistribution[conD];
          if (conRootDistribution[rootId] != undefined)
            conRootDistribution[rootId] += conDistribution[conD];
          else {
            conRootDistribution[rootId] = 0;
          }
          // --------------------------
          if (idSpilt.length == 1) {
            // conRootDistribution[rootId] = conDistribution[conD];
            let cw = setConCount_linear(Math.sqrt(conDistribution[conD]));
            let color = setConCountCompute_color(setConCountColor_linear(conDistribution[conD]))
            // let disRect = _this.drawRect(entSetG, cx+(max1w)*j, cy+max1h - ch,max1w-5, ch, 1, color, "1", "white","1", `proSetConAttr_${psid}_${conid}`, 'proSetConAttr');
            // let disRectB = _this.drawRect(entSetG, cx+5, cy+(max1h)*j,max1w, height/9-3, 1, "none", "1", "white","1", `proSetConAttrB_${psid}_${conid}`, 'proSetConAttr');
            let disRect = _this.drawRect(entSetG, cx + 5, cy + 3 + (max1h) * j, cw, height / 8 - 3, 1, color, "1", "white", "1", `proSetConAttr_${psid}_${conid}`, 'proSetConAttr');
            disRect.on("click", function (d) {
              let selectProAtt = d3.select(this);
              let Ids = selectProAtt.attr("id").split("_");
              let setId = Ids[1];
              let conId = Ids[2];
              _this.curProblemSetId = setId;
              _this.updataEntProblemDetailBySet("con", conId)
            })
            j++;
          }
          // -------------------------------------
        })
        // let curx = cx+3;
        // Object.keys(conRootDistribution).forEach(conrD=>{
        //   let c_linear = d3.scaleLinear().domain([0, maxnum]).range([0, width-(min1w*9)]);
        //   let cColor_linear = d3.scaleLinear().domain([0, maxnum]).range([0, 1]);
        //   let cCompute_color = d3.interpolate(currentMinColor, currentMaxColor);
        //   let afw = c_linear(conRootDistribution[conrD]);
        //   console.log(conRootDistribution[conrD],afw,min1w+afw)
        //   let color = cCompute_color(cColor_linear(conRootDistribution[conrD]))
        //   let disRect = _this.drawRect(entSetG, curx, cy+3,min1w+afw, height/3-6, 1, color, "1", "white","1", `proSetConAttr_${psid}_${conrD}`, 'proSetConAttr');
        //   disRect.on("click",function(d){
        //     let selectProAtt = d3.select(this);
        //     let Ids = selectProAtt.attr("id").split("_");
        //     let setId = Ids[1];
        //     let conId = Ids[2];
        //     _this.curProblemSetId = setId;
        //     _this.updataEntProblemDetailBySet("con",conId)
        //   })
        //   j++
        //   curx+=min1w+afw+2;
        // })


        // let min2w = 10;
        // let max2w = width/6;       
        // let min2h = 10;
        // let max2h = height/3;
        let min2w = 0;
        let max2w = width / 3 - 30;
        let min2h = 10;
        let max2h = height / 4;
        j = 0;
        let prolen = proSetData[i]['set'].length;
        let settype_linear = d3.scaleLinear().domain([0, Math.sqrt(prolen)]).range([min2w, max2w]);
        let typeMinColor = _this.setTypeCountColorMin;
        let typeMaxColor = _this.setTypeCountColorMax;
        let typeColor_linear = d3.scaleLinear().domain([0, prolen]).range([0, 1]);
        let typeCompute_color = d3.interpolate(typeMinColor, typeMaxColor);
        // console.log(proSetData[i]['set'],typeDistribution)
        Object.keys(typeDistribution).forEach(typeD => {
          let ch = settype_linear(Math.sqrt(typeDistribution[typeD]));
          let color = typeCompute_color(typeColor_linear(typeDistribution[typeD]))
          // let disRect = _this.drawRect(entSetG, cx+(max2w)*j, cy+max2h+max2h - ch,max2w-5, ch, 1, color, "1", "white","1", `proSettypeAttr-${psid}-${typeD}`, 'proSettypeAttr');
          // let disRectB = _this.drawRect(entSetG, cx + (width / 3)-25 , cy + (max2h) * j, max2w, max2h - 3, 1, "none", "1", "white", "1", `proSettypeAttrB-${psid}-${typeD}`, 'proSettypeAttrB');
          let disRect = _this.drawRect(entSetG, cx + (width / 3) - 23, cy + (max2h) * j, ch, max2h - 3, 1, color, "1", "white", "1", `proSettypeAttr-${psid}-${typeD}`, 'proSettypeAttr');
          disRect.on("click", function (d) {
            let selectProAtt = d3.select(this);
            let Ids = selectProAtt.attr("id").split("-");
            let setId = Ids[1];
            let typeD = Ids[2];
            _this.curProblemSetId = setId;
            _this.updataEntProblemDetailBySet("type", typeD);
          })
          j++;
        })


      }
    },
    drawSetValuePoly(svg, cx, cy, height, width, idN, set) {
      const _this = this;
      // let groupData = 
      let data = [];
      let keys = [];
      let stepy = height / (set.length - 1);
      let pathav = d3.path();
      let pathavat = d3.path();
      let pathavtd = d3.path();
      let pathfcf = d3.path();
      let pathfcz = d3.path();
      let wScale = d3.scaleLinear().domain([0, 1]).range([1, width / 2 - 2]);
      let maxOriAttempts = 30;
      let wScaleat = d3.scaleLinear().domain([0, maxOriAttempts]).range([width / 2 + 5, width - 5]);

      let minOriTimeDur = _this.proAttrMaxMinList[1][0];
      let maxOriTimeDur = _this.proAttrMaxMinList[1][1];
      let proSetData = tools.deepClone(_this.proSetData);
      // for(let j=0;j<proSetData.length;j++){
      //   let sets = proSetData[j]['set'];
      for (let i = 0; i < set.length; i++) {
        let proStuData = set[i]['stuData'];
        let minTimeD = 10000000001;
        let maxTimeD = -100000000000;
        Object.keys(proStuData).forEach((s) => {
          maxTimeD = (proStuData[s]['timeDur'] > maxTimeD) ? proStuData[s]['totalTimeDur'] : maxTimeD;
          minTimeD = (proStuData[s]['timeDur'] < minTimeD) ? proStuData[s]['totalTimeDur'] : minTimeD;
        })
        maxOriTimeDur = (maxOriTimeDur > maxTimeD) ? maxOriTimeDur : maxTimeD;
        minOriTimeDur = (minOriTimeDur < minTimeD) ? minOriTimeDur : minTimeD;
      }
      // }
      let wScaletd = d3.scaleLinear().domain([minOriTimeDur, maxOriTimeDur]).range([width / 3 * 2 + 3, width - 5]);

      let points = [];
      let pointsfc = [];
      let pointsav = [];

      let pointsat = [];
      let pointsfcat = [];
      let pointsavat = [];

      let pointstd = [];
      let pointsfctd = [];


      for (let i = 0; i < set.length; i++) {
        let proData = set[i];
        let proStuData = set[i]['stuData'];
        let minScoreRate = 1;
        let maxScoreRate = 0;
        let avScoreRate = 0;
        let minAttempts = 1;
        let maxAttempts = 0;
        let avAttempts = 0;

        let minTimeDur = 100000000;
        let maxTimeDur = -1000000000000;
        let avTimeDur = 0;
        let num = 0;
        Object.keys(proStuData).forEach((s) => {
          maxScoreRate = (proStuData[s]['scoringRate'] > maxScoreRate) ? proStuData[s]['scoringRate'] : maxScoreRate;
          minScoreRate = (proStuData[s]['scoringRate'] < minScoreRate) ? proStuData[s]['scoringRate'] : minScoreRate;

          maxAttempts = (proStuData[s]['totalAttempts'] > maxAttempts) ? proStuData[s]['totalAttempts'] : maxAttempts;
          minAttempts = (proStuData[s]['totalAttempts'] < minAttempts) ? proStuData[s]['totalAttempts'] : minAttempts;

          maxTimeDur = (proStuData[s]['timeDur'] > maxTimeDur) ? proStuData[s]['totalTimeDur'] : maxTimeDur;
          minTimeDur = (proStuData[s]['timeDur'] < minTimeDur) ? proStuData[s]['totalTimeDur'] : minTimeDur;

          avScoreRate += proStuData[s]['scoringRate'];
          avAttempts += proStuData[s]['totalAttempts'];
          avTimeDur += proStuData[s]['timeDur'];
          num++;
        });
        avScoreRate /= num;
        avAttempts /= num;
        avTimeDur /= num;

        let fcScoreRate = 0;
        let fcTimeDur = 0;
        let fcAttempts = 0;
        Object.keys(proStuData).forEach((s) => {
          fcScoreRate += Math.pow(proStuData[s]['scoringRate'] - avScoreRate, 2);
          fcAttempts += Math.pow(proStuData[s]['totalAttempts'] - avAttempts, 2);
          fcTimeDur += Math.pow(proStuData[s]['timeDur'] - avTimeDur, 2);
        })
        fcScoreRate /= num;
        fcAttempts /= num;
        fcTimeDur /= num;

        set[i]['maxScoreRate'] = maxScoreRate;
        set[i]['minScoreRate'] = minScoreRate;
        set[i]['avScoreRate'] = avScoreRate;
        set[i]['fcScoreRate'] = fcScoreRate;

        set[i]['maxAttempts'] = maxAttempts;
        set[i]['minAttempts'] = minAttempts;
        set[i]['avAttempts'] = avAttempts;
        set[i]['fcAttempts'] = fcAttempts;

        set[i]['maxTimeDur'] = maxTimeDur;
        set[i]['minTimeDur'] = minTimeDur;
        set[i]['avTimeDur'] = avTimeDur;
        set[i]['fcTimeDur'] = fcTimeDur;

        if (i == 0) {
          pathav.moveTo(cx + wScale(avScoreRate), cy + stepy * i);
          pathavat.moveTo(cx + wScaleat(avAttempts), cy + stepy * i);
          pathavtd.moveTo(cx + wScaletd(avTimeDur), cy + stepy * i);
        }

        pathav.lineTo(cx + wScale(avScoreRate), cy + stepy * i);
        pathavat.lineTo(cx + wScaleat(avAttempts), cy + stepy * i);
        pathavtd.lineTo(cx + wScaletd(avTimeDur), cy + stepy * i);

        points.push([cx + wScale(maxScoreRate), cy + stepy * i])
        pointsav.push([cx + wScale(avScoreRate), cy + stepy * i])
        pointsfc.push([cx + wScale(avScoreRate + fcScoreRate), cy + stepy * i])
        if (maxAttempts > maxOriAttempts)
          maxAttempts = maxOriAttempts;
        if (maxAttempts == 1) {
          maxAttempts = 5
        }
        pointsat.push([cx + wScaleat(maxAttempts), cy + stepy * i]);
        pointsavat.push([cx + wScaleat(avAttempts), cy + stepy * i])
        pointsfcat.push([cx + wScaleat(avAttempts + Math.sqrt(fcAttempts)), cy + stepy * i])

        pointstd.push([cx + wScaletd(maxTimeDur), cy + stepy * i]);
        pointsfctd.push([cx + wScaletd(avTimeDur + Math.sqrt(fcTimeDur)), cy + stepy * i])
      };
      for (let i = set.length - 1; i >= 0; i--) {
        let proData = set[i];
        let proStuData = set[i]['stuData'];
        let minScoreRate = 1;
        let maxScoreRate = 0;
        let avScoreRate = set[i]['avScoreRate'];
        let fcScoreRate = set[i]['fcScoreRate'];

        let avAttempts = set[i]['avAttempts'];
        let fcAttempts = set[i]['fcAttempts'];

        let avTimeDur = set[i]['avTimeDur'];
        let fcTimeDur = set[i]['fcTimeDur'];

        let minAttempts = set[i]['minAttempts'];
        let minTimeDur = set[i]['minTimeDur'];
        Object.keys(proStuData).forEach((s) => {
          maxScoreRate = (proStuData[s]['scoringRate'] > maxScoreRate) ? proStuData[s]['scoringRate'] : maxScoreRate;
          minScoreRate = (proStuData[s]['scoringRate'] < minScoreRate) ? proStuData[s]['scoringRate'] : minScoreRate;
        })
        points.push([cx + wScale(minScoreRate), cy + stepy * i])
        pointsfc.push([cx + wScale(avScoreRate - fcScoreRate), cy + stepy * i])

        pointsat.push([cx + wScaleat(minAttempts), cy + stepy * i])
        pointsfcat.push([cx + wScaleat(avAttempts - Math.sqrt(fcAttempts)), cy + stepy * i])

        pointstd.push([cx + wScaletd(minTimeDur), cy + stepy * i])
        pointsfctd.push([cx + wScaletd(avTimeDur - Math.sqrt(fcTimeDur)), cy + stepy * i])
      };

      let curve_generator = d3.line()
        .x((d) => d[0])
        .y((d) => d[1])
        .curve(d3.curveBasisClosed)
      let curve_generatorb = d3.line()
        .x((d) => d[0])
        .y((d) => d[1])
        .curve(d3.curveBasis)
      // .curve(d3.curveLinearClosed)

      let linepoly = _this.drawLine(svg, curve_generator(points), "none", 1, '0', '1', `setstuScoreLine_${idN}`, 'setstuScoreLine', "rgba(253, 195, 190,0.6)");
      let linepolyfc = _this.drawLine(svg, curve_generator(pointsfc), "none", 1, '0', '1', `setstuScoreLinefc_${idN}`, 'setstuScoreLine', "rgba(255, 77, 109,0.6)");
      let lineav = _this.drawLine(svg, curve_generatorb(pointsav), "white", 1, '0', '1', `setstuScoreLineAv_${idN}`, 'setstuScoreLine');

      let linepolyat = _this.drawLine(svg, curve_generator(pointsat), "none", 1, '0', '1', `setstuAttemptsLine_${idN}`, 'setstuAttemptsLine', "rgba(250, 210, 50,0.6)");
      let linepolyfcat = _this.drawLine(svg, curve_generator(pointsfcat), "none", 1, '0', '1', `setstuAttemptsLinefc_${idN}`, 'setstuAttemptsLine', "rgba(181, 146, 9,0.6)");
      let lineavat = _this.drawLine(svg, curve_generatorb(pointsavat), "white", 1, '0', '1', `setstuAttemptsLineAv_${idN}`, 'setstuAttemptsLine');

      // let linepolytd = _this.drawLine(svg, curve_generator(pointstd), "none", 1, '0','1' ,`setstuTimeDurLine_${idN}`, 'setstuTimeDurLine',"rgb(5, 13, 159)");
      // let linepolyfctd = _this.drawLine(svg, curve_generator(pointsfctd), "none", 1, '0','1' ,`setstuTimeDurLinefc_${idN}`, 'setstuTimeDurLine',"rgb(5, 20, 90)");
      // let lineavtd = _this.drawLine(svg, pathavtd, "white", 1, '0','1' ,`setstuTimeDurLineAv_${idN}`, 'setstuTimeDurLine');
      // let linefcf = _this.drawLine(svg, pathfcf, "white", 1, '0','1' ,`setstuScoreLineFcf_${idN}`, 'setstuScoreLine');
      // let linefcz = _this.drawLine(svg, pathfcz, "white", 1, '0','1' ,`setstuScoreLineFcz_${idN}`, 'setstuScoreLine');
    },

    drawRiver(svg, cx, cy, height, width, idN, set) {
      const _this = this;
      // let groupData = 
      let data = [];
      let keys = []
      for (let i = 0; i < set.length; i++) {
        let groupVal = set[i]['groupVal']
        let temp = { "od": i };
        for (let j = 0; j < groupVal.length; j++) {
          if (keys.indexOf(("" + j)) == -1) {
            keys.push("" + j);
          }
          let curScoringRate = groupVal[j]['scoringRate'];
          temp[("" + j)] = curScoringRate;
        }
        data.push(temp)
        // let curScoringRate = 
      }
      console.log(data)
      var stack = d3.stack()
        .keys(keys)
        .order(d3.stackOrderInsideOut)
        .offset(d3.stackOffsetWiggle);

      let yRangeWidth = width;
      let xStep = (width) / (data.length);
      let stackData = stack(data)
      // let maxx = Math.max.apply(Math, stackData.map(function (d) { return Math.max.apply(Math, d.map(function (c) { return c[1]; }));; }));
      // let minx = Math.min.apply(Math, stackData.map(function (d) { return Math.max.apply(Math, d.map(function (c) { return c[1]; })); }));
      console.log(stackData, minx, maxx)
      let yScale = d3.scaleLinear().domain([-1, 1]).range([0, height]);

      var area = d3.area()

        .curve(d3.curveBasis)
        .x(function (d) {
          return d.data.od * xStep;
        })
        .y0(function (d) {
          return yScale(d[0]);
        })
        .y1(function (d) {
          return yScale(d[1]);
        });

      // let areaG = svg.append("g")
      let typeColor = _this.stuColorList;
      let colorLi = _this.mcolor;
      for (let i = 0; i < stackData.length; i++) {

        svg.append("path")
          .attr("id", function (d) { return `${idN}_${stackData[i].key}` })
          .attr("class", "river")
          .attr("d", function (d) {
            return area(stackData[i])
          })
          .attr("fill", function (d) {
            return typeColor[stackData[i].key]
          })
          .attr("transform", `translate(${cx},${cy})`)
          .on("mouseover", function (d) {
            d3.selectAll(".river")
            // .style("filter", "url()")
            d3.select(this)
            // .style("filter", "url(#coolShadow)")
          })
      }
    },
    drawBsLine(svg, sx, sy, c1x, c1y, c2x, c2y, tx, ty, stroke, width, opacity, idName, className) {
      d3.select(`#${idName}`).remove();
      let line = svg.append('path')
        .attr("class", className)
        .attr("id", idName)
        .attr('d', function (d) {
          let path = d3.path();
          path.moveTo(sx, sy);
          // path.quadraticCurveTo(cx, cy, tx, ty);
          path.bezierCurveTo(c1x, c1y, c2x, c2y, tx, ty);
          return path.toString();
        })
        .style("fill", "none")
        .style('stroke', stroke)
        .style("stroke-opacity", opacity)
        .style('stroke-width', width);
      return line;
    },
    drawTxt(svg, x, y, text, fill, fontsize = 12, idN, an = 'start') {
      let txt = svg.append("text")
        .attr("y", y)
        .attr("x", x)
        .attr("id", idN)
        .attr("fill", fill)
        .attr("font-size", fontsize)
        .style("text-anchor", an)
        .text(text)
      return txt;
    },
    drawLine(svg, path, stroke, width, stroke_dasharray = "0", opacity, idName, className, fill = 'none') {
      d3.select(`#${idName}`).remove();
      let line = svg.append('path')
        .attr('d', path.toString())
        .attr('stroke', stroke)
        .attr('class', className)
        .attr('id', idName)
        .attr("stroke-dasharray", stroke_dasharray)
        .attr('stroke-width', width)
        .style("stroke-opacity", opacity)
        .attr('fill', fill)
      return line;
    },
    getTreeData(data) {
      const _this = this;
      let oriData = tools.deepClone(this.data);
      var treeData = {
        "name": "root",
        "children": []
      };
      for (let i = data.length - 1; i >= 0; i--) {
        console.log(data[i])
        if (parseInt(data[i]['father']) == -1) {
          treeData['children'].push(data[i]);
        }
        else {
          let fId = data[i]['father'];
          let fatherD = data.find(function (d) { return d['id'] == fId; });
          if (!fatherD['children']) {
            fatherD['children'] = [data[i]]
          }
          else
            fatherD['children'].push(data[i])
        }
      }
      return treeData;
    },
    entHover(idList) {
      for (let i = 0; i < idList.length; i++) {
        let transformd = d3.select(idList[i]).attr("transform");
        d3.select(idList[i])
          .transition().duration(100)
          .attr("transform", function (d) {
            return transformd.split("scale")[0] + " scale(1.2)"
          })
        // .style("filter", "url(#coolShadow)")
      }
    },
    entRemoveHover(idList) {
      for (let i = 0; i < idList.length; i++) {
        let transformd = d3.select(idList[i]).attr("transform")
        d3.select(idList[i])
          .transition().duration(100)
          .attr("transform", function (d) {
            return transformd.split("scale")[0] + " scale(1)"
          }).style("filter", "url()")
      }
    },
    drawEntityProblem(svg, x, y, pId) {
      const _this = this;
      d3.select("#" + pId).remove();
      let entG = svg.append("g").attr("id", pId);
      entG.attr("transform", `translate(${x},${y})`);
      let proData = tools.deepClone(_this.problemsData);
      let idn = pId.split("_")[1];
      let curEnt = proData.find(function (p) {
        return (p.id).toString() == (idn.toString())
      });
      // let attrList =[{attrName:'difficulty',attrValue:curEnt['difficulty']},];
      let attrList = _this.proAttrList;

      let attrLen = attrList.length;

      let proMaxMinDR = _this.proMaxMinDR;
      let proMaxMinDC = _this.proMaxMinDC;
      let proAttrMaxMinList = _this.proAttrMaxMinList;
      let currentMaxColor = _this.entProMaxColor;
      let currentMinColor = _this.entProMinColor;
      let importanceColor_linear = d3.scaleLinear().domain([proMaxMinDC[0], proMaxMinDC[1]]).range([0, 1]);
      let importanceCompute_color = d3.interpolate(currentMinColor, currentMaxColor);
      let rSize_linear = d3.scaleLinear().domain([proMaxMinDR[1], proMaxMinDR[0]]).range([20, 40]);

      let rSize = rSize_linear(curEnt['conCount']);

      let points = _this.calcRegularPolygonPoints(attrLen, 0, 0, rSize);
      let entColor = importanceCompute_color(importanceColor_linear(curEnt['scoringRate']));

      let entPolygon = _this.drawPolygon(entG, points, `pro_${idn}`, '5px', entColor, entColor);

      entPolygon.on("mouseover", function (d) {
      })
      let pointsList = [];
      const pathAxis = d3.path();
      pathAxis.moveTo(0, 0);
      for (let i = 0; i < points.length; i++) {
        pathAxis.lineTo(points[i][0], points[i][1]);
        pathAxis.moveTo(0, 0);
        pathAxis.lineTo(points[i][0], points[i][1]);
      }
      pathAxis.lineTo(points[0][0], points[0][1]);
      let rgbValue = tools.getRgbValue(entColor);
      let r = parseInt(rgbValue[0]) * 0.2;
      let g = parseInt(rgbValue[1]) * 0.4;
      let b = parseInt(rgbValue[2]) * 0.7;
      _this.drawPathLine(entG, pathAxis, `rgb(${r},${g},${b})`, 0.2, "10,3", `proAxis_${idn}`, "");
      // -------------------------
      const path = d3.path();
      let startP = _this.calcattrPoint(attrLen, 0, proAttrMaxMinList[0], curEnt[attrList[0]], 0, 0, rSize)
      path.moveTo(startP[0], startP[1]);
      pointsList.push(startP)
      let startP2 = _this.calcattrPoint(attrLen, 1, proAttrMaxMinList[1], curEnt[attrList[1]], 0, 0, rSize)
      path.bezierCurveTo(startP2[0], startP2[1], startP2[0], startP2[1], startP2[0], startP2[1]);
      pointsList.push(startP2)
      for (let i = 2; i < attrLen; i++) {
        let curP = _this.calcattrPoint(attrLen, i, proAttrMaxMinList[i], curEnt[attrList[i]], 0, 0, rSize)
        // path.lineTo(curP[0],curP[1]);
        pointsList.push(curP);
        path.bezierCurveTo(curP[0], curP[1], curP[0], curP[1], curP[0], curP[1])
      }
      path.bezierCurveTo(startP[0], startP[1], startP[0], startP[1], startP[0], startP[1])

      pointsList.push(startP)
      path.bezierCurveTo(startP2[0], startP2[1], startP2[0], startP2[1], startP2[0], startP2[1])
      pointsList.push(startP2)
      // ----------------
      let curve_generator = d3.line()
        .x((d) => d[0])
        .y((d) => {
          return d[1];
        })
        .curve(d3.curveCatmullRom)
      // .curve(d3.curveBundle)
      _this.drawPolygon(entG, pointsList, `proAttr_${idn}`, '1px', `rgb(${r},${g},${b})`, `rgba(${r},${g},${b},0.3)`);
      // .attr("opacity","0.3")
      // _this.drawPathLine(entG, curve_generator(pointsList), "rgb(200,200,200)", 2, "0", "", "");

    },
    drawEntityConcept(svg, x, y, pId) {
      const _this = this;
      d3.select("#" + pId).remove();
      let entG = svg.append("g").attr("id", pId);
      entG.attr("transform", `translate(${x},${y})`);
      let conData = tools.deepClone(_this.conceptTree);
      let idn = pId.split("_")[1];
      let curEnt = conData.find(function (p) {
        return (p.id).toString() == (idn.toString())
      });
      // let attrList =[{attrName:'difficulty',attrValue:curEnt['difficulty']},];
      let attrList = _this.conAttrList;

      let attrLen = attrList.length;

      let conMaxMinDR = _this.conMaxMinDR;
      let conMaxMinDC = _this.conMaxMinDC;
      let conAttrMaxMinList = _this.conAttrMaxMinList;
      let currentMaxColor = _this.entConMaxColor;
      let currentMinColor = _this.entConMinColor;
      let importanceColor_linear = d3.scaleLinear().domain([conMaxMinDC[0], conMaxMinDC[1]]).range([0, 1]);
      let importanceCompute_color = d3.interpolate(currentMinColor, currentMaxColor);
      let rSize_linear = d3.scaleLinear().domain([conMaxMinDR[1], conMaxMinDR[0]]).range([20, 50]);

      let rSize = rSize_linear(curEnt['proCount']);

      let points = _this.calcRegularPolygonPoints(attrLen, 0, 0, rSize);


      let StartR = 0//Math.PI/4;
      let StepInterR = Math.PI * 2 / 15;

      let StepR = (Math.PI * 2 - StepInterR * attrLen) / attrLen;


      for (let i = 0; i < attrLen; i++) {
        let curP = _this.calcattrPoint(attrLen, i, conAttrMaxMinList[i], curEnt[attrList[i]], 0, 0, rSize);
        let h = _this.calcRsize(conAttrMaxMinList[i], curEnt[attrList[i]], rSize)
        var dataset = { startAngle: StartR + i * (StepR + StepInterR) + StepInterR, endAngle: StartR + (i + 1) * (StepR + StepInterR) }; //创建一个弧生成器
        var arcPath = d3.arc()
          .innerRadius(1)
          .outerRadius(h);
        var arcPathBack = d3.arc()
          .innerRadius(1)
          .outerRadius(h + 2);
        var pathArc = arcPath(dataset);
        let entColor = _this.attrColorList[i];//importanceCompute_color(importanceColor_linear(curEnt['scoringRate']));
        // _this.drawArc(entG, 0, 0, arcPathBack(dataset), "#000", "#000", 'type', 0, 3);
        _this.drawArc(entG, 0, 0, pathArc, entColor, entColor, 'type', 0, 3);
      }



    },
    updateEntity(svg, x, y, pId) {
      const _this = this;
      let entG = svg.select(`#${pId}`);
      let transformd = entG.attr("transform")
      let s = 'scale(1)';
      if (transformd.split("scale").length > 1) {
        s = `scale${transformd.split("scale")[1]}`;
      }
      entG.attr("transform", `translate(${x},${y}) ${s}`);
    },
    drawPolygon(svg, points, idName, strokeWidth, stroke, fill) {
      let polygon = svg.append("polygon")
        .attr("points", points)
        .attr("id", idName)
        .attr("stroke-linejoin", "round")

        .attr("stroke-width", strokeWidth)
        .attr("fill", fill)
        .attr("stroke", stroke)
      return polygon;
    },
    drawRect(svg, x, y, w, h, rx, fill, strokeWidth, stroke, opacity, idName, className) {
      d3.select(`#${idName}`).remove();
      let rect = svg.append("rect")
        .attr("x", x)
        .attr("y", y)
        .attr("width", w)
        .attr("height", h)
        .attr("id", idName)
        .attr("class", className)
        .attr("opacity", opacity)
        .attr("fill", fill)
        .attr("rx", rx)
        .attr("stroke", stroke)
        .attr("stroke-width", strokeWidth)
      return rect;
    },
    calcRsize(domin, value, r) {
      let point_linear = d3.scaleLinear().domain([domin[1], domin[0]]).range([r / 3, r]);
      let rarc = point_linear(value);
      return rarc;
    },
    calcattrPoint(totalNum, index, domin, value, x, y, r) {
      const _this = this;
      let arcStep = Math.PI * 2 / totalNum;
      let rarc = _this.calcRsize(domin, value, r);
      let point = [x - Math.sin(arcStep * index) * rarc, y + Math.cos(arcStep * index) * rarc];
      return point
    },

    calcRegularPolygonPoints(num, x, y, r) {
      let arcStep = Math.PI * 2 / num;
      let points = [];
      for (let i = 0; i < num; i++) {
        points.push([x - Math.sin(arcStep * i) * r, y + Math.cos(arcStep * i) * r])
      }
      return points
    },
    drawPathLine(svg, path, stroke, width, stroke_dasharray = "0", idName, className) {
      svg.append('path')
        .attr('d', path.toString())
        .attr('stroke', stroke)
        .attr('class', className)
        .attr('id', idName)
        .attr("stroke-dasharray", stroke_dasharray)
        .attr('stroke-width', width)
        .attr('fill', 'none')
    },
    drawCircle(svg, x, y, r, fill, opacity, stroke, width, className = 'entCircle', idName) {
      const _this = this;
      const oData = _this.data
      let circle = svg.append("circle")
        .attr("id", idName)
        .attr("class", className)
        .attr("opacity", opacity)
        .attr("cx", x)
        .attr("cy", y)
        .attr("r", r)
        .attr('stroke', stroke)
        .attr('stroke-width', width)
        .attr("fill", fill)
      return circle;
    },

    drawArc(svg, x, y, arcPath, stroke, fill, className, stroke_dasharray = "0", width = 3) {
      svg.append("path")
        .attr("d", arcPath)
        .attr("class", className)
        .attr("transform", "translate(" + x + "," + y + ")")
        .attr("stroke", stroke)
        .attr('stroke-width', width)
        .attr("stroke-dasharray", stroke_dasharray)
        .attr("stroke-linejoin", "round")
        .attr("fill", fill)
    },
    getMaxMin(data, attrname) {
      return [
        Math.max.apply(Math, data.map(function (d) { return d[attrname]; })),
        Math.min.apply(Math, data.map(function (d) { return d[attrname]; }))
      ]
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
      let proData = _this.problemsData;
      console.log(proData);
      let proMaxMinDR = _this.getMaxMin(proData, 'conCount');
      let proMaxMinDC = _this.getMaxMin(proData, 'scoringRate');

      // let proAttrList = ['scoringRate', 'timeDur', 'totalAttempts',"totalAttemptsPeople", 'acceptedRate', 'conCount'];
      let proAttrList = ['scoringRate', 'acceptedRate', 'totalAttempts', 'conCount'];
      _this.proAttrList = proAttrList;
      let proAttrMaxMinList = [];
      for (let i = 0; i < proAttrList.length; i++) {
        proAttrMaxMinList.push(_this.getMaxMin(proData, proAttrList[i]));
      }
      _this.proAttrMaxMinList = proAttrMaxMinList;
      _this.proMaxMinDR = proMaxMinDR;
      _this.proMaxMinDC = proMaxMinDC;

      let conData = _this.conceptTree;
      let conMaxMinDR = _this.getMaxMin(conData, 'proCount');
      let conMaxMinDC = _this.getMaxMin(conData, 'scoringRate');

      let conAttrList = ['scoringRate', 'totalAttempts', 'acceptedRate', 'proCount'];
      _this.conAttrList = conAttrList;
      let conAttrMaxMinList = [];
      for (let i = 0; i < conAttrList.length; i++) {
        conAttrMaxMinList.push(_this.getMaxMin(conData, conAttrList[i]));
      }
      _this.conAttrMaxMinList = conAttrMaxMinList;

      _this.conMaxMinDR = conMaxMinDR;
      _this.conMaxMinDC = conMaxMinDC;

      this.$bus.$emit("Domin", [proAttrList, proAttrMaxMinList, conAttrList, conAttrMaxMinList]);
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
      // _this.createRel('1234','4321',0);
      // _this.createRel('123','321',0);
      // _this.delRel('1234','4321',0);

      // _this.getProblems();
      // _this.getConcept();
      // _this.getConceptProblem();
      // _this.getUserProblem();
      // _this.updataGraph();
    });
  },
  mounted() {
    const _this = this;

    d3.select(".chartTooltip").classed("hidden", true);
    // this.updataGraph();

    this.$bus.$on('stuColorList', (val) => { _this.stuColorList = val; });
    this.$bus.$on('attrColorList', (val) => {
      _this.attrColorList = val;
    });
    this.$bus.$on('groupData', (val) => {
      _this.groupData = val;
    });
    this.$bus.$on('allProblem', (val) => {
      _this.problemsData = val;
      _this.updataGraph();
      _this.updataSelectStudentListColor();
      // _this.updataParallelCoordinatesplotByPro();
    });
    this.$bus.$on('Submission', (val) => {
      _this.submissionsData = val;
    });
    this.$bus.$on('Student', (val) => {
      _this.studentsData = val;
    });
    this.$bus.$on('proSet', (val) => {
      _this.proSetOriData = val;
    });
    this.$bus.$on('Pro_Con', (val) => {
      _this.problemConceptData = val;
    });
    this.$bus.$on('SelectedStu', (val) => {
      _this.SelectStudentList = val;
      // _this.calStudent();
    });
    this.$bus.$on('SelectingStu', (val) => {
      _this.SelectingStudentId = val;
      // _this.calStudent();
    });
    // this.$bus.$on('Concept', (val) => {
    //   _this.conceptsData = val;
    // });
    this.$bus.$on('ConceptTree', (val) => {
      _this.conceptTree = val;
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

<style>@import './index.css';</style>
