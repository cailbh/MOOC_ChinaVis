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
  props: ["videoTime"],
  data() {
    return {
      data: '',
      problemsData: [],
      submissionsData:[],
      conceptsData: [],
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
      curProblemId:'',
      selectProblemId:'',
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
      // entProMinColor: "rgb(1, 164, 183)",
      // entProMaxColor: "rgb(106, 52, 127)",
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
      entProMinColor: "rgb(203, 230, 209)",
      entProMaxColor: "rgb(22, 144, 207)",
      entConMinColor: "rgb(255, 162, 66)",
      entConMaxColor: "rgb(252, 85, 49)",
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
    curProblemId(val) {
      const _this = this;
      _this.$bus.$emit("selectEnt", val);
      // let entityLocationData = _this.drawEntityLocation;

      // let relData = _this.relData;
      // let showJageData = _this.showEntityList;
      // let basicRel = relData['basicRel'];
      // for (let r = 0; r < basicRel.length; r++) {
      //   let sorceId = basicRel[r][0];
      //   let targetId = basicRel[r][1];
      //   let sorceJage = showJageData.find(function (d) { return d['id'] == sorceId })['show'];
      //   let targetJage = showJageData.find(function (d) { return d['id'] == targetId })['show'];
      //   if (sorceJage && targetJage) {
      //     let trnId = '-1';
      //     if (sorceId == parseInt(val)) {
      //       trnId = targetId;
      //     }
      //     else if (targetId == parseInt(val)) {
      //       trnId = sorceId;
      //     }
      //     if (trnId != '-1') {
      //       let curEnt = entityLocationData.find(function (d) { return parseInt(d['id']) == trnId });
      //       _this.assistGTransformX = parseInt(-curEnt['x']) + parseFloat(curEnt['r']) + 150;
      //       _this.assistGTransformY = parseInt(-curEnt['y']) + parseFloat(curEnt['r']) + 300;
      //       _this.updataAssistGraphPanel();
      //     }
      //   }

      // };
      // let similarityRel = relData['similarityRel'];
      // for (let r = 0; r < similarityRel.length; r++) {
      //   let sorceId = similarityRel[r][0];
      //   let targetId = similarityRel[r][1];
      //   let sorceJage = showJageData.find(function (d) { return d['id'] == sorceId })['show'];
      //   let targetJage = showJageData.find(function (d) { return d['id'] == targetId })['show'];
      //   if (sorceJage && targetJage) {
      //     let trnId = '-1';
      //     if (sorceId == parseInt(val)) {
      //       trnId = targetId;
      //     }
      //     else if (targetId == parseInt(val)) {
      //       trnId = sorceId;
      //     }
      //     if (trnId != '-1') {
      //       let curEnt = entityLocationData.find(function (d) { return parseInt(d['id']) == trnId });
      //       _this.assistGTransformX = parseInt(-curEnt['x']) + parseFloat(curEnt['r']) + 150;
      //       _this.assistGTransformY = parseInt(-curEnt['y']) + parseFloat(curEnt['r']) + 300;
      //       _this.updataAssistGraphPanel();
      //     }
      //   }

      // };


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
          _this.$bus.$emit("allProblem", _this.problemsData);
        });
    },
    getConcept() {
      const _this = this;
      this.$http
        .get("/api/concept/allConcept", {}, {})
        .then((response) => {
          _this.conceptsData = response.body;
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
          _this.updataGraph();
        });
    },
    getAllData() {
      const _this = this;
      this.getProblems();
      this.getConcept();
      this.getProblemConcept();
      this.getSubmissions();
      // .then(()=>{ 
      // _this.updataGraph();
      // })
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
      let entG = groups.append("g").attr("id", "entG").attr("width", width).attr("height", height);
      let frontG = groups.append("g").attr("id", "frontG").attr("width", width).attr("height", height);
      var defs = svg.append("defs");

      var filter = defs
        .append("filter")
        .attr("id", "coolShadow")
        .attr("x", "-100%")
        .attr("y", "-100%") //
        .attr("width", "400%")
        .attr("height", "400%"); //

      filter
        .append("feBlend")
        .attr("in", "SourceGraphic")
        .attr("mdoe", "normal")

      filter
        .append("feMorphology")
        .attr("in", "SourceGraphic")
        .attr("result", "upperLayer")
        .attr("operator", "dilate")
        .attr("radius", "0.5 0.2");
      filter
        .append("feMorphology")
        .attr("in", "SourceAlpha")
        .attr("result", "enlargedAlpha")
        .attr("operator", "dilate")
        .attr("radius", "0.2 0.2");

      filter
        .append("feGaussianBlur")
        .attr("in", "enlargedAlpha")
        .attr("result", "bluredAlpha")
        .attr("stdDeviation", "1");

      filter
        .append("feOffset")
        .attr("in", "bluredAlpha")
        .attr("result", "lowerLayer")
        .attr("dy", "0.2"); //

      var feMerge = filter.append("feMerge");
      feMerge.append("feMergeNode").attr("in", "lowerLayer");
      feMerge.append("feMergeNode").attr("in", "upperLayer");

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
        let cId = curRel['contentId'];
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
        .on("mousemove",function(d){
          let curSvgEnt= d3.select(this);
          let curType = curSvgEnt.attr("class");
          let curId = curSvgEnt.attr("id");
          let idNameList = [];
          let curEnt = {};
          let tipName  ='';
          if(curType == 'problem'){
            
            curEnt = _this.problemsData.find(function (p) {
              return (p.id).toString() == (curId.toString());
            });
            tipName = curEnt['problemPoolIndex']
            problemConceptData.forEach(rel => {
              if(rel['problem'] == curId){
                  let conID = rel['contentId'];
                  idNameList.push(`#entCon_${conID}`);
              }
            });
            idNameList.push(`#entPro_${curId}`)
          }
          else if(curType == "concept"){
            curEnt = _this.conceptsData.find(function (p) {
              return (p.id).toString() == (curId.toString());
            });
            tipName = curEnt['name']
            problemConceptData.forEach(rel => {
              if(rel['contentId'] == curId){
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
        .on("click",function(d){
          let curSvgEnt= d3.select(this);
          let curType = curSvgEnt.attr("class");
          let curId = curSvgEnt.attr("id");
          let idNameList = [];
          if(curType == 'problem'){
            idNameList.push(`#entPro_${curId}`);
            _this.curProblemId = curId;
          }
          else if(curType == "concept"){
            idNameList.push(`#entCon_${curId}`)
          }
          _this.entHover(idNameList);
        })
        .on("mouseleave",function(d){
          let curSvgEnt= d3.select(this);
          let curType = curSvgEnt.attr("class");
          let curId = curSvgEnt.attr("id");
          let idNameList = [];
          if(curType == 'problem'){
            problemConceptData.forEach(rel => {
              if(rel['problem'] == curId){
                  let conID = rel['contentId'];
                  idNameList.push(`#entCon_${conID}`)
              }
            });
            idNameList.push(`#entPro_${curId}`)
          }
          else if(curType == "concept"){
            problemConceptData.forEach(rel => {
              if(rel['contentId'] == curId){
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
        // link.attr("x1", d => d.source.x)
        //     .attr("y1", d => d.source.y)
        //     .attr("x2", d => d.target.x)
        //     .attr("y2", d => d.target.y);
        circle.attr("cx", (d) => {
          let esx = d.x;
          let esy = d.y;
          if (esx < rSize) esx = rSize;
          esx = esx > svgWidth - rSize ? svgWidth - rSize : esx;
          if (esy < rSize) esy = rSize;
          esy = esy > svgHeight - rSize ? svgHeight - rSize : esy;
          if (d.type == "problem")
              _this.updateEntity(entG,esx,esy,`entPro_${d.id}`)
          //   _this.drawEntityProblem(entG, esx, esy, `entPro_${d.id}`);
          else if (d.type == "concept")
              _this.updateEntity(entG,esx,esy,`entCon_${d.id}`)
          //   _this.drawEntityConcept(entG, esx, esy, `entCon_${d.id}`);
          if (d.x < rSize) return rSize
          return d.x > svgWidth - rSize ? svgWidth - rSize : d.x
        })
          .attr("cy", (d) => {
            if (d.y < rSize) return rSize
            return d.y > svgHeight - rSize ? svgHeight - rSize : d.y
          });
        // text.attr("x", (d) => {
        //     if (d.x < rSize) return rSize
        //     return d.x > svgWidth - rSize ? svgWidth - rSize : d.x
        // })
        //     .attr("y", (d) => {
        //         if (d.y < rSize) return rSize
        //         return d.y > svgHeight - rSize ? svgHeight - rSize : d.y
        //     });

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
        // ntext.attr("x", d => d.x)
        //     .attr("y", d => d.y);
        // etext.attr("x", function (d) { return (d.source.x + d.target.x) / 2 })
        //     .attr("y", function (d) { return (d.source.y + d.target.y) / 2 })

      });


      // let stepX = 10;
      // for(let i=0;i<problemData.length;i++){
      //   console.log(problemData[i]['type'],problemData[i]['typetext'])
      //   _this.drawCircle(circleG,1+i*stepX,100,10,"red",1,"problemEnt",`problem_${i}`);
      // }

      svg.call(graphZoom)

    },
    entHover(idList){
      for(let i=0;i<idList.length;i++){
        let transformd = d3.select(idList[i]).attr("transform");
          d3.select(idList[i])
          .transition().duration(100)
          .attr("transform", function (d) {
            return transformd.split("scale")[0] + " scale(1.2)"
          })
          // .style("filter", "url(#coolShadow)")
      }
    },
    entRemoveHover(idList){
      for(let i=0;i<idList.length;i++){
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

      let entPolygon = _this.drawPolygon(entG,points,`pro_${idn}`,'5px',entColor,entColor);

      entPolygon.on("mouseover",function(d){
      })
      let pointsList = [];
      const pathAxis = d3.path();
        pathAxis.moveTo(0,0);
      for(let i=0;i<points.length;i++){
        pathAxis.lineTo(points[i][0],points[i][1]);
        pathAxis.moveTo(0,0);
        pathAxis.lineTo(points[i][0],points[i][1]);
      }
        pathAxis.lineTo(points[0][0],points[0][1]);
      let rgbValue = tools.getRgbValue(entColor);
      let r = parseInt(rgbValue[0])*0.2;
      let g = parseInt(rgbValue[1])*0.4;
      let b = parseInt(rgbValue[2])*0.7;
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
      _this.drawPolygon(entG,pointsList,`proAttr_${idn}`,'1px',`rgb(${r},${g},${b})`,`rgba(${r},${g},${b},0.3)`);
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
          .outerRadius(h+2);
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
      if(transformd.split("scale").length>1){
        s = `scale${transformd.split("scale")[1]}`;
      }
      entG.attr("transform", `translate(${x},${y}) ${s}`);
    },
    drawPolygon(svg,points,idName,strokeWidth,stroke,fill){
      let polygon = svg.append("polygon")
        .attr("points", points)
        .attr("id",idName)
        .attr("stroke-linejoin", "round")

        .attr("stroke-width", strokeWidth)
        .attr("fill", fill)
        .attr("stroke", stroke)
      return polygon;
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
      svg.append("circle")
        .attr("id", idName)
        .attr("class", className)
        .attr("opacity", opacity)
        .attr("cx", x)
        .attr("cy", y)
        .attr("r", r)
        .attr("fill", fill)
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
      let proMaxMinDR = _this.getMaxMin(proData, 'conCount');
      let proMaxMinDC = _this.getMaxMin(proData, 'scoringRate');

      let proAttrList = ['accuracy', 'totalAttempts', 'acceptedRate', 'conCount', 'scoringRate'];
      _this.proAttrList = proAttrList;
      let proAttrMaxMinList = [];
      for (let i = 0; i < proAttrList.length; i++) {
        proAttrMaxMinList.push(_this.getMaxMin(proData, proAttrList[i]));
      }
      _this.proAttrMaxMinList = proAttrMaxMinList;

      _this.proMaxMinDR = proMaxMinDR;
      _this.proMaxMinDC = proMaxMinDC;

      let conData = _this.conceptsData;
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
      _this.getAllData();
    });
  },
  mounted() {
    const _this = this;

    this.updataGraph();
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
