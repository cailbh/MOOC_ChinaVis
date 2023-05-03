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
      graphHeight:0,
      toolAddRel:false,
      detailsEntPro:[],
      problemsData: [],
      proSetOriData: [],
      submissionsData: [],
      studentsData: [],
      conceptsData: [],
      conceptTree: [],
      proSetData:[],
      interY:10,
      problemConceptData: [],
      userProblemData: [],
      proMaxMinDR: [],
      proMaxMinDC: [],
      proAttrList: [],
      proAttrMaxMinList: [],
      conMaxMinDR: [],
      conMaxMinDC: [],
      conAttrList: [],
      conAttrMaxMinList: [],
      Ent_problem:[],
      Ent_concept:[],
      entG:"",
      entSetG:"",
      entbySetG:"",
      relG:"",
      curProblemId: '',
      curConceptId: '',
      curProblemSetId:'',
      selectProblemId: '',
      curConceptId: '',
      selectConceptId: '',
      proX:500,
      proY:0,
      setX:800,
      setY:0,
      treeX:50,
      treeY:0,
      proStepY:0,
      conStepY:0,
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
      entConMinColor: "rgb(255, 162, 66)",
      entConMaxColor: "rgb(252, 85, 49)",
      stepX: 80,
      stepY: 100,
      typeXMap: {
        "TRUE_OR_FALSE":0,
        "MULTIPLE_CHOICE":1,
        "FILL_IN_THE_BLANK":2,
        "PROGRAMMING":3,
        "CODE_COMPLETION":4,
        "MULTIPLE_CHOICE_MORE_THAN_ONE_ANSWER":5
      },
      circleInterval: 55,
      width: 0,
      height: 0,
      curToolState: 'unEdit',
      margin: { top: 10, right: 20, bottom: 0, left: 20 },
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
    toolAddRel(val){
      console.log(val);
    },
    toolsState:{
      deep:true,
      handler(val){
      this.toolAddRel = val['addRel']
    }},
    graphGTransformY(){
      
      // this.updataPro_ProSelfRel(this.graphGTransformY);
    },
    curConceptId(val) {
      const _this = this;
      // _this.$bus.$emit("selectEntCon", val);
      let Ent_concept = _this.Ent_concept;
      let Ent_problem = _this.Ent_problem;
      let pro_conRelData = tools.deepClone(_this.problemConceptData);
      let curproId = _this.curProblemId;
      // entCon
      if(_this.toolAddRel){
        pro_conRelData.push({
          "problem":curproId,
          "conceptId":val,
        })
        _this.problemConceptData = pro_conRelData;
      }
      else{
        d3.selectAll(`.entPro`)
        .attr("opacity","0.1");
        d3.selectAll(`.entCon`)
        .attr("opacity","0.1");
        d3.selectAll(`.proConRel`)
          .attr("opacity","0.1");
        pro_conRelData.forEach(rel=>{
          let proId = rel['problem'];
          let conId = rel['conceptId'];
          if(conId == val){
            // d3.select(`#entCon_${conId}`)
            // .attr("opacity","1");
            d3.select(`#entPro_${proId}`)
            .attr("opacity","1");
            d3.select(`#proConRel_${conId}_${proId}`)
            .attr("opacity","1");
          }
        })
      }
      
    },
    curProblemId(val) {
      const _this = this;
      _this.$bus.$emit("selectEnt", val);
      let Ent_concept = _this.Ent_concept;
      let Ent_problem = _this.Ent_problem;
      let pro_conRelData = _this.problemConceptData;
      // entCon
      d3.selectAll(`.entCon`)
        .attr("opacity","0.1");
      d3.selectAll(`.proConRel`)
        .attr("opacity","0.1");
      pro_conRelData.forEach(rel=>{
        let proId = rel['problem'];
        let conId = rel['conceptId'];
        if(proId == val){
          d3.select(`#entCon_${conId}`)
          .attr("opacity","1");
          d3.select(`#proConRel_${conId}_${proId}`)
          .attr("opacity","1");
        }
      })
    },
    problemConceptData:{
      deep:true,
      handler(val){
        if(this.toolAddRel){
          // this.updataPro_ConRel();
          this.updataProSet_ConRel();
          this.$bus.$emit("Updata_Pro_Con", val);
        }
      }
    },
    curProblemSetId(val){
      this.updataEntProblemDetailBySet();
      // this.updataPro_ProSelfRel(this.graphGTransformY);
    },
    detailsEntPro(val){
      this.updataEntProblemDetail();
      // this.updataPro_ProSelfRel(this.graphGTransformY);
    },
    Ent_problem:{
      deep:true,
      handler(){
        // this.updataEntProblem();
        this.updataEntProblemSetBack();
          // this.updataPro_ConRel();
          this.updataProSet_ConRel();
      }
    },
    Ent_concept:{
      deep:true,
      handler(){
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
        .attr("transform", "translate(" + graphGTransformX + ',' + graphGTransformY + ") scale(" + graphGTransformK + ")");
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
      console.log(ent_node);
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
        .attr("transform", "translate(" + graphGTransformX + ',' + graphGTransformY + ") scale(" + graphGTransformK + ")");
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
          console.log("s",event,d)
        }
        function dragged(event, d) {
          console.log("s",event,d)
        }

        function dragended(event, d) {
          console.log("e",event,d)
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
      let rConSize_linear = d3.scaleLinear().domain([conMaxMinDR[1], conMaxMinDR[0]]).range([5, 10]);

      // concept---------
      let treeX = _this.treeX;
      let treeY = _this.treeY;
      let stepY = height / (conceptTree.length + 2);

      let proSetData = [];
      let setOd = 0;
      _this.conStepY = stepY;
      let interY = _this.interY;
      let Ent_concept = [];
      for (let i = 0; i < conceptTree.length; i++) {
        let tempCon = tools.deepClone(conceptTree[i]);
        let cy = treeY + i * stepY;
        let cid = tempCon['id'];
        tempCon['lay'] = cid.split("-").length;
        let cx = treeX * tempCon['lay'];
        tempCon['cx'] = cx;
        tempCon['cy'] = cy;
        tempCon['fill'] = importanceConCompute_color(importanceConColor_linear(tempCon['scoringRate']));
        tempCon['r'] =  rConSize_linear(tempCon['proCount']);
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

      
      let typeXMap = _this.typeXMap;
      console.log(proMaxMinDR,proMaxMinDC,proAttrMaxMinList)
      //problem -----------
      let proX = _this.proX;
      let proY = _this.proY;
      let Ent_problem = [];
      let proStepY = (height - _this.interY*12)/(problemData.length+12); 
      _this.proStepY = proStepY;
      _this.graphHeight = height;
      for (let i = 0; i < problemData.length; i++) {
        let tempPro = tools.deepClone(problemData[i]);
        let pid = tempPro['id'];
        let pSetId = tempPro['problemSetId'];
        if(proSetData.find(function(ps){return ps['id'] == pSetId;})==undefined){
          proSetData.push({
            "id":pSetId,
            "order":setOd,
            "set":[pid]
          })
          setOd++;
        }
        else{
          proSetData.find(function(ps){return ps['id'] == pSetId;})['set'].push(pid);
        }
        let cy = proY + i * proStepY + interY*setOd;
        // let lay = cid.split("-").length;
        let cx = proX;
        let r = proStepY;
        let fill = "grey";
        let opacity = 0.8;
        // let Cname  = tempPro['name'];
        tempPro['cx'] = cx//+typeXMap[tempPro['type']]*100;
        tempPro['cy'] = cy;
        tempPro['order'] = i;
        tempPro['width'] =rSize_linear(tempPro['scoringRate']);
        tempPro['fill'] = importanceCompute_color(importanceColor_linear(tempPro["conCount"]));
        tempPro['height'] = proStepY;
        Ent_problem.push(tempPro);
        // let circle = _this.drawCircle(entG, cx, cy, r, fill, opacity, );t text = _this.drawTxt(entG, cx+20, cy+3.5, Cname, "black", 12, `entConText_${cid}`);
      }
      let setStepY = height/proSetData.length;
      let colorList = _this.mcolor;
      for(let i=0;i<proSetData.length;i++){
        proSetData[i]['fill'] = colorList[proSetData[i]['order']];
        let psid = proSetData[i]['id'];
        let set = proSetData[i]['set'];
        proSetData[i]['cx'] = _this.proX-3;
        proSetData[i]['width'] = 30*6+16;
        // -----------------------------------
        // proSetData[i]['cy'] = Ent_problem.find(function(ep){return ep['id'] == set[0];})['cy'];
        // let edP = Ent_problem.find(function(ep){return ep['id'] == set[set.length-1];})
        // proSetData[i]['height'] = edP['cy'] - proSetData[i]['cy']+edP['height'];
        // -----------------------------------
        proSetData[i]['cy'] = setStepY*i;
        proSetData[i]['height'] = setStepY-10;
        // -------------------------------------
      }
      _this.Ent_problem = Ent_problem;
      // ---------------------
      _this.proSetData =proSetData;
          // this.updataPro_ConRel();
          this.updataProSet_ConRel();

      _this.updataParallelCoordinatesplot();

      
    },
    updataParallelCoordinatesplot(){
       const _this = this;
      let entG = _this.entG;
      let relG = _this.relG;
      let Ent_concept = tools.deepClone(_this.Ent_concept);
      let Ent_problem = tools.deepClone(_this.Ent_problem);
      let pro_conRelData = tools.deepClone(_this.problemConceptData);
      let studentsData = tools.deepClone(_this.studentsData);
      let proSetData = tools.deepClone(_this.proSetData);
      let proSetOriData = tools.deepClone(_this.proSetOriData);
      console.log(studentsData,proSetData,proSetOriData);
      //轴
      let paraX = 1100;
      let stepY = _this.graphHeight/(proSetData.length+2);
      for(let i = 0;i<proSetData.length;i++){
        let cx = paraX;
        let cy = proSetData[i]['cy']+proSetData[i]['height']/2//;stepY*(i+1)
        let width = 200;
        let height = 3;
        let psId = proSetData[i]['id'];
        let fill = proSetData[i]['fill'];
        proSetData[i]['axisX'] = cx;
        proSetData[i]['axisY'] = cy;
        proSetData[i]['axisW'] = width;
        proSetData[i]['axisH'] = height;
        let axis = _this.drawRect(entG, cx, cy, width, height, 0, fill, "0", "none","0.5", `proSetAxis_${psId}`, 'proSetAxis');
      }

      for(let i =0 ;i<studentsData.length;i++){
        let path = d3.path();
        let proSetScore = studentsData[i]['proSetScore'];
        let stuId = studentsData[i]['id'];
        for(let s=0;s<proSetScore.length;s++){
          let psId = proSetScore[s]['id'];
          let psData = proSetData.find(function(psd){return psd['id'] == psId;});
          let cx = psData['axisX'];
          let w = psData['axisW'];
          let val_linear = d3.scaleLinear().domain([0,proSetScore[s]['totalScore']]).range([cx, cx+w]);
          let pointy = psData['axisY'];
          let pointx = val_linear(proSetScore[s]['score']); 
          if(s==0){
            path.moveTo(pointx,pointy);
          }
          else{
            path.lineTo(pointx,pointy);
          }
        }
        _this.drawLine(relG, path, "rgb(200,200,200)", 2, '0', `stuSetScoreLine_${stuId}`, 'stuSetScoreLine');
      }
    },
    updataPro_ConRel(){
      const _this = this;
      let entG = _this.entG;
      let relG = _this.relG;
      let typeXMap = _this.typeXMap;
      let Ent_concept = tools.deepClone(_this.Ent_concept);
      let Ent_problem = tools.deepClone(_this.Ent_problem);
      let pro_conRelData = tools.deepClone(_this.problemConceptData);
      for(let i=0;i<pro_conRelData.length;i++){
        let curRel = pro_conRelData[i];
        let conId = curRel['conceptId'];
        let proId = curRel['problem'];
        let conData = Ent_concept.find(function(d){return d['id'] == conId;});
        let proData = Ent_problem.find(function(d){return d['id'] == proId;});
          let sx = conData['cx']+50;
          let sy = conData['cy'];
          let tx = proData['cx'];
          let ty = proData['cy']+proData['height']/2;
          let c1x = (sx)+100;
          let c1y = (sy)
          let c2x = (sx);
          let c2y = (ty)
        _this.drawBsLine(relG, sx, sy,c1x,c1y,c2x,c2y, tx, ty, "grey", "0.5px", "1", `proConRel_${conId}_${proId}`, "proConRel");
      }
    },  
    updataProSet_ConRel(){
      const _this = this;
      let entG = _this.entG;
      let relG = _this.relG;
      let typeXMap = _this.typeXMap;
      let Ent_concept = tools.deepClone(_this.Ent_concept);
      let Ent_problem = tools.deepClone(_this.Ent_problem);
      let proSetData = tools.deepClone(_this.proSetData);
      let pro_conRelData = tools.deepClone(_this.problemConceptData);
      for(let i=0;i<pro_conRelData.length;i++){
        let curRel = pro_conRelData[i];
        let conId = curRel['conceptId'];
        let proId = curRel['problem'];
        let conData = Ent_concept.find(function(d){return d['id'] == conId;});
        let proData = Ent_problem.find(function(d){return d['id'] == proId;});
        let curproSetData = proSetData.find(function(pd){return pd['id'] == proData['problemSetId']});
        let sx = conData['cx']+50;
        let sy = conData['cy'];
        let tx = curproSetData['cx'];
        let ty = curproSetData['cy']+curproSetData['height']/2;
        let c1x = (sx)+100;
        let c1y = (sy);
        let c2x = (sx);
        let c2y = (ty);
        _this.drawBsLine(relG, sx, sy,c1x,c1y,c2x,c2y, tx, ty, "grey", "2px", "0.2", `proSetConRel_${conId}_${proData['problemSetId']}`, "proSetConRel");
      }
    },  
    updataPro_ProSelfRel(tranY){
      const _this = this;
      let entG = _this.entG;
      let relG = _this.relG;
      let selectSetId = _this.curProblemSetId;
      let Ent_problem = tools.deepClone(_this.Ent_problem);
      for(let i=0;i<Ent_problem.length;i++){
        let pid = Ent_problem[i]['id'];
        if(Ent_problem[i]["problemSetId"] == selectSetId){
          let proData = Ent_problem.find(function(d){return d['id'] == pid;});
          let prog = d3.select(`#entPro_${pid}`)
          let proSlefg = d3.select(`#probySet_${pid}`)
            let sx = parseFloat(prog.attr("x"))+parseFloat(prog.attr("width"));
            let sy = parseFloat(prog.attr("y"))+parseFloat(prog.attr("height"))/2;
            let tx = parseFloat(proSlefg.attr("x"));
            let ty = parseFloat(proSlefg.attr("y"))+tranY+parseFloat(proSlefg.attr("height"))/2;
          // console.log(sx,sy,tx,ty,prog.attr("x"),proSlefg.attr("y"),prog.attr("width"),prog.attr("height"),proSlefg.attr("height"))
            let c1x = (sx)+100;
            let c1y = (sy)
            let c2x = (tx)-100;
            let c2y = (ty)
            let fill = proData['fill']
          _this.drawBsLine(relG, sx, sy,c1x,c1y,c2x,c2y, tx, ty, fill, "2px", "0.4", `proSelfRel_${pid}`, "proSelfRel");
        }
      }
    },  
    updataEntConcept(){
      const _this = this;
      let entG = _this.entG;
      let relG = _this.relG;
      let Ent_concept = tools.deepClone(_this.Ent_concept);
      
      let conX = _this.treeX;
      let conY = _this.treeY;
      let conStepY = _this.conStepY;
      for(let i = 0;i<Ent_concept.length;i++){
        let curEntCon = Ent_concept[i];
        let cid = curEntCon['id'];
        let cx = curEntCon['cx'];
        let cy = curEntCon['cy'];
        let r = curEntCon['r'];
        let Cname  = curEntCon['name'];
        let fill = curEntCon['fill'];
        let opacity = curEntCon['opacity'];

        let circle = _this.drawCircle(entG, cx, cy, r, fill, opacity, 'entCon', `entCon_${cid}`);
        
        circle.on("click",function(d){
          let selectCon = d3.select(this);
          let selectConId = selectCon.attr("id").split("_")[1];
          _this.curConceptId = selectConId;
        })
        // let text = _this.drawTxt(entG, cx+20, cy+3.5, Cname, "black", 12, `entConText_${cid}`);
        // let rect =  _this.drawRect(relG, cx+20, cy, 100, 12, 1, fill, "0", "none","1", `entConRect_${cid}`, 'entConRect');
        let fatherId = curEntCon['father'];
        if (parseInt(fatherId) != -1) {
          let curCon = Ent_concept.find(function (d) { return d['id'] == cid; });
          let fatherCon = Ent_concept.find(function (d) { return d['id'] == fatherId; });
          let sx = fatherCon['cx'];
          let sy = fatherCon['cy'];
          let tx = curCon['cx'];
          let ty = curCon['cy'];

          _this.drawBsLine(relG, sx, sy,sx,ty,sx,ty, tx, ty, "grey", "2px", "0.4", `conRel_${fatherId}_${cid}`, "conRel");
        }
      }
    },  
    updataEntProblem(){
      const _this = this;
      let entG = _this.entG;
      let Ent_problem = tools.deepClone(_this.Ent_problem);
      let proSetData = tools.deepClone(_this.proSetData);
      let proX = _this.proX;
      let proY = _this.proY;
      let typeColorMap = {
        "TRUE_OR_FALSE":_this.mcolor[1],
        "MULTIPLE_CHOICE":_this.mcolor[3],
        "FILL_IN_THE_BLANK":_this.mcolor[5],
        "PROGRAMMING":_this.mcolor[7],
        "CODE_COMPLETION":_this.mcolor[9],
        "MULTIPLE_CHOICE_MORE_THAN_ONE_ANSWER":_this.mcolor[11]
      }
      let interY = _this.interY;
      let typeXMap = _this.typeXMap;
      let proStepY = _this.proStepY;
      let attrList = _this.proAttrList;
      let attrLen = attrList.length;
      let proAttrMaxMinList = _this.proAttrMaxMinList;

      let proMaxMinDR = _this.proMaxMinDR;
      let wSize_linear = d3.scaleLinear().domain([proMaxMinDR[1], proMaxMinDR[0]]).range([20, 100]);
      for(let i = 0;i<Ent_problem.length;i++){
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
        let circle = _this.drawCircle(entG, cx, cy+_this.proStepY/2, proStepY/2, typeColor, '1', 'entProCir', `entProCir_${pid}`);
        // let rect = _this.drawRect(entG, cx+cH/2, cy, cW, cH, 1, fill, "0", "none","1", `entPro_${pid}`, 'entPro');
        let rect = _this.drawRect(entG, cx+cH/2, cy, 180, cH, 1, fill, "0", "none","0.5", `entPro_${pid}`, 'entPro');
        rect.on("mousemove",function(d){
          let selectPro = d3.select(this);
          let selectProId = selectPro.attr("id").split("_")[1];
          let proD = Ent_problem.find(function(p){return p['id'] == selectProId});
          let pSetId = proD['problemSetId'];
          let pSet = proSetData.find(function(ps){return ps['id'] == pSetId;})
          let pSetOd = pSet['order']+1;
          let od = proD['order'];
          Ent_problem.forEach(entPro=>{
            if(entPro['id'] == selectProId){
              entPro['cy']=proY + entPro['order'] * proStepY + interY*pSetOd;
              entPro['height']=(proStepY -inter) * 5;
              od = entPro['order'];
            }
            else if(entPro['order']<od){
              let cproD = Ent_problem.find(function(p){return p['id'] == entPro['id']});
              let cpSetId = cproD['problemSetId'];
              let cpSet = proSetData.find(function(ps){return ps['id'] == cpSetId;})
              let cpSetOd = cpSet['order']+1;
              
              entPro['cy']=proY + entPro['order'] * proStepY+ interY*cpSetOd;
              entPro['height']=(proStepY -inter)
            }
            else if(entPro['order']>od){
              let cproD = Ent_problem.find(function(p){return p['id'] == entPro['id']});
              let cpSetId = cproD['problemSetId'];
              let cpSet = proSetData.find(function(ps){return ps['id'] == cpSetId;})
              let cpSetOd = cpSet['order']+1;
              entPro['cy']=proY + entPro['order'] * proStepY+(proStepY -1)*4+ interY*cpSetOd;
              entPro['height']=(proStepY -inter)
            }
          })
          _this.Ent_problem =Ent_problem;
        }).on("click",function(d){
          let selectPro = d3.select(this);
          let selectProId = selectPro.attr("id").split("_")[1];
          _this.curProblemId = selectProId;
        })
        let attrW = 30
        for (let j = 0; j < attrLen; j++) {
          let curP = _this.calcRsize(proAttrMaxMinList[j], curEntPro[attrList[j]], 30);
          let attColor = _this.mLigntcolor[j*2]
          let rectAttr = _this.drawRect(entG, cx+j*attrW, cy, curP, cH, 1, attColor, "0.8", "grey","1", `prottr_${pid}_${attrList[j]}`, 'proAttr');
        }
        // le

      }
    },      
    updataEntProblemDetailBySet(){
      const _this = this;
      let entG = _this.entbySetG;
      let selectSetId = _this.curProblemSetId;
      let Ent_problem = tools.deepClone(_this.Ent_problem);
      let proMaxMinDR = _this.proMaxMinDR;
      let setX = _this.setX;
      let setY = _this.setY;
      let setEnt = [];

      for(let i = 0;i<Ent_problem.length;i++){
        if(Ent_problem[i]["problemSetId"] == selectSetId){
          let entSetPro =tools.deepClone(Ent_problem[i]);
          setEnt.push(entSetPro);
          // setEnt[cx] = 
        }
      }

      _this.detailsEntPro = setEnt;
    },   
    updataEntProblemDetail(){
      const _this = this;
      let entG = _this.entbySetG;
      let selectSetId = _this.curProblemSetId;
      let Ent_problem = tools.deepClone(_this.Ent_problem);
      let proMaxMinDR = _this.proMaxMinDR;
      let setX = _this.setX;
      let setY = _this.setY;
      
      entG.selectAll(".proDetil").remove();
      entG.selectAll(".proDetilB").remove();
      entG.selectAll(".proDetilAttr").remove();

      let setEnt = _this.detailsEntPro ;

      let setStepY = 50;
      let attrList = _this.proAttrList;
      let attrLen = attrList.length;
      let setProWidth = 100;
      let attrW = setProWidth/(attrLen);
      let proAttrMaxMinList = _this.proAttrMaxMinList;
      let wSize_linear = d3.scaleLinear().domain([proMaxMinDR[1], proMaxMinDR[0]]).range([20, 100]);
        
      for(let i = 0;i<setEnt.length;i++){
        let curEntPro = setEnt[i];
        let pid = curEntPro['id'];
        let cx = setX;
        let cy = setY+i*setStepY;
        let cH = setStepY-20;
        let cW = wSize_linear(curEntPro['scoringRate']);
        let fill = curEntPro['fill'];
        let pOrder = curEntPro['order'];
        let rectback = _this.drawRect(entG, cx, cy, 100, cH, 5, "grey", "10", "grey","0.3", `proDetilB_${pid}`, 'proDetilB');
        let rect = _this.drawRect(entG, cx, cy, cW, cH, 5, fill, "10", fill,"1", `proDetil_${pid}`, 'proDetil');
        rect.on("click",function(d){
          let selectPro = d3.select(this);
          let selectProId = selectPro.attr("id").split("_")[1];
          _this.curProblemId = selectProId;
        })
        for (let j = 0; j < attrLen; j++) {
          let curP = _this.calcRsize(proAttrMaxMinList[j], curEntPro[attrList[j]], cH);
          let attColor = _this.mLigntcolor[j*2]
          let rectAttr = _this.drawRect(entG, cx+j*attrW, cy+cH-curP, attrW-10, curP, 1, attColor, "0.2", "grey","1", `proDetilAttr_${pid}_${attrList[j]}`, 'proDetilAttr');
        }
      }
    },
    updataEntProblemSetBack(){
      const _this = this;
      let entSetG = _this.entSetG;
      let proSetData = tools.deepClone(_this.proSetData);
      let Ent_problem = tools.deepClone(_this.Ent_problem);
      for(let i=0;i<proSetData.length;i++){
        let fill = proSetData[i]['fill'];
        let psid = proSetData[i]['id'];
        let set = proSetData[i]['set'];
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
        let rect = _this.drawRect(entSetG, cx, cy, width, height, 10, fill, "5", "none","0.1", `proSet_${psid}`, 'proSet');
        rect.on("click",function(d){
          let selectSet = d3.select(this);
          d3.selectAll(".proSet").attr("opacity",0.1);
          d3.selectAll(".proSelfRel").remove();
          // _this.updataPro_ProSelfRel();
          selectSet.attr("opacity",0.5)
          let selectSetId = selectSet.attr("id").split("_")[1];
          _this.curProblemSetId = selectSetId;
        })
      }
    }, 
    drawBsLine(svg, sx, sy,c1x,c1y,c2x,c2y, tx, ty, stroke, width, opacity, idName, className) {
      d3.select(`#${idName}`).remove();
      let line = svg.append('path')
        .attr("class", className)
        .attr("id", idName)
        .attr('d', function (d) {
          let path = d3.path();
          path.moveTo(sx, sy);
          // path.quadraticCurveTo(cx, cy, tx, ty);
          path.bezierCurveTo(c1x,c1y,c2x, c2y, tx, ty);
          return path.toString();
        })
        .style("fill", "none")
        .style('stroke', stroke)
        .style("stroke-opacity", opacity)
        .style('stroke-width', width);
      return line;
    },
    drawTxt(svg, x, y, text, fill, fontsize = 12, idN) {
        let txt = svg.append("text")
          .attr("y", y)
          .attr("x", x)
          .attr("id", idN)
          .attr("fill", fill)
          .attr("font-size", fontsize)
          .style("text-anchor", "start")
          .text(text)
        return txt;
    },
    drawLine(svg, path, stroke, width, stroke_dasharray = "0", idName, className) {
      let line = svg.append('path')
        .attr('d', path.toString())
        .attr('stroke', stroke)
        .attr('class', className)
        .attr('id', idName)
        .attr("stroke-dasharray", stroke_dasharray)
        .attr('stroke-width', width)
        .attr('fill', 'none')
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
      let conData = tools.deepClone(_this.conceptsData);
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
        let entColor = importanceCompute_color(importanceColor_linear(curEnt['scoringRate']));
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
    drawCircle(svg, x, y, r, fill, opacity, className = 'entCircle', idName) {
      const _this = this;
      const oData = _this.data
      let circle = svg.append("circle")
        .attr("id", idName)
        .attr("class", className)
        .attr("opacity", opacity)
        .attr("cx", x)
        .attr("cy", y)
        .attr("r", r)
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
      let proMaxMinDR = _this.getMaxMin(proData, 'scoringRate');
      let proMaxMinDC = _this.getMaxMin(proData, 'conCount');

      let proAttrList = ['accuracy', 'totalAttempts', 'acceptedRate', 'conCount', 'scoringRate'];
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

      let conAttrList = ['accuracy', 'totalAttempts', 'acceptedRate', 'proCount', 'scoringRate'];
      _this.conAttrList = conAttrList;
      let conAttrMaxMinList = [];
      for (let i = 0; i < conAttrList.length; i++) {
        conAttrMaxMinList.push(_this.getMaxMin(conData, conAttrList[i]));
      }
      _this.conAttrMaxMinList = conAttrMaxMinList;

      _this.conMaxMinDR = conMaxMinDR;
      _this.conMaxMinDC = conMaxMinDC;

      console.log(conAttrMaxMinList)

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
    this.updataGraph();

    this.$bus.$on('allProblem', (val) => {
      _this.problemsData = val;
      _this.updataGraph();
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

<style>
@import './index.css';
</style>
