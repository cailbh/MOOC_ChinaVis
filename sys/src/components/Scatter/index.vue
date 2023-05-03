<!-- eslint-disable no-unused-vars -->
<!-- eslint-disable no-unused-vars -->

<template>
  <div class="scatter" ref="scatterDiv">
    <div class="panelHead">C</div>
    <div id="scatterCantain" ref="scatterCantain" class="panelBody">
    </div>
    <!-- <div id="moveLeft" ref="movescatterLeft"></div>
                    <div id="moveRight" ref="movescatterRight"></div> -->
    <!-- <div id="assistscatterCantain" class="panel">
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
      scatterHeight:0,
      selectStartX:0,
      selectStartY:0,
      selectEndX:0,
      selectEndY:0,
      SelectStudentList:[],
      groupData:[],
      selectClick:0,
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
      MaxMinX: [],
      MaxMinY: [],
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
      scatterGTransformK: 1,
      scatterGTransformX: 10,
      scatterGTransformY: 10,
      scatterSvgScale: 1,
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
    SelectStudentList(val){
      this.updataScatter();
      this.$bus.$emit("SelectedStu", val);
    },
    type(val) {
    },
  },
  methods: {

    drawMain(svg) {
      let _this = this;
      let data = _this.data;
      let margin = _this.margin;

      let width = _this.width - margin.left - margin.right;
      let height = _this.height - margin.top - margin.bottom;

      let scatterGTransformX = _this.scatterGTransformX;
      let scatterGTransformY = _this.scatterGTransformY;
      let scatterGTransformK = _this.scatterGTransformK;
      let groups = svg.append("g").attr("id", "ggroups").attr("width", width).attr("height", height)
        .attr("transform", "translate(" + scatterGTransformX + ',' + scatterGTransformY + ") scale(" + scatterGTransformK + ")");
      this.groupsSvg = groups;

      let backG = groups.append("g").attr("id", "gbackG").attr("width", width).attr("height", height);
      let arcG = groups.append("g").attr("id", "garcG").attr("width", width).attr("height", height);
      let relG = groups.append("g").attr("id", "grelG").attr("width", width).attr("height", height);
      let entSetG = groups.append("g").attr("id", "gentSetG").attr("width", width).attr("height", height);
      let entbySetG = groups.append("g").attr("id", "gentbySetG").attr("width", width).attr("height", height);
      let entG = groups.append("g").attr("id", "gentG").attr("width", width).attr("height", height);
      let frontG = groups.append("g").attr("id", "gfrontG").attr("width", width).attr("height", height);

      let MaxMinX =_this.MaxMinX;
      let MaxMinY = _this.MaxMinY;
      let xSize_linear = d3.scaleLinear().domain([MaxMinX[1], MaxMinX[0]]).range([10,width]);
      let ySize_linear = d3.scaleLinear().domain([MaxMinY[1], MaxMinY[0]]).range([10,height]);

      _this.arcG = arcG;
      _this.entG = entG;
      _this.entSetG = entSetG;
      _this.entbySetG = entbySetG;
      _this.relG = relG;
      let interval = _this.circleInterval;


      let scalePre = _this.scatterSvgScale;
      let stx = 0;
      let sty = 0;
      let stk = 1;
      var scatterZoom = d3.zoom()
        .scaleExtent([0, 100])
        .on("start", (e) => {
          sty = e.transform.y;
          stx = e.transform.x;
          stk = e.transform.k;
        })
        .on('zoom', (e) => {
          scatterGTransformX = _this.scatterGTransformX + e.transform.x - stx;
          scatterGTransformY = _this.scatterGTransformY + e.transform.y - sty;
          scatterGTransformK = _this.scatterGTransformK + e.transform.k - stk;
          groups.attr('transform', 'translate(' + (scatterGTransformX) + ',' + (scatterGTransformY) + ') scale(' + (scatterGTransformK) + ')')
        })
        .on('end', (e) => {
          _this.scatterGTransformX = scatterGTransformX;
          _this.scatterGTransformY = scatterGTransformY;
          _this.scatterGTransformK = scatterGTransformK;
          groups.attr('transform', 'translate(' + (scatterGTransformX) + ',' + (scatterGTransformY) + ') scale(' + (scatterGTransformK) + ')')
        });

        // svg.call(scatterZoom);

        let groupData = tools.deepClone(_this.groupData);
        console.log(groupData);
        let colorList = _this.mcolor;
        for(let i=0;i<groupData.length;i++){
          let cx = xSize_linear(groupData[i]['x']);
          let cy = ySize_linear(groupData[i]['y']);
          let sId = groupData[i]['id']
          groupData[i]['cx'] = cx;
          groupData[i]['cy'] = cy;
          groupData[i]['r'] = 5;
          groupData[i]['fill'] = colorList[parseInt(groupData[i]['kmeansC'])];
        }
      _this.groupData =groupData;
      _this.updataScatter();
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
    drawCircle(svg, x, y, r, fill, opacity, className = 'entCircle', idName) {
      const _this = this;
      const oData = _this.data
      d3.select(`#${idName}`).remove();
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
    getMaxMin(data, attrname) {
      return [
        Math.max.apply(Math, data.map(function (d) { return d[attrname]; })),
        Math.min.apply(Math, data.map(function (d) { return d[attrname]; }))
      ]
    },
    mouseDown(event){
      console.log(event)
      const _this = this;
      let entG = _this.entG
      let sx = event.layerX-_this.scatterGTransformX;
      let sy = event.layerY-_this.scatterGTransformY-40;
      _this.selectStartX = sx;
      _this.selectStartY = sy;
      // _this.drawRect(entG, sx, sy, 100, 100, 10, "grey", "5", "none","0.1", `SelectRect`, 'SelectRect');
      this.$refs.scatterCantain.addEventListener("mousemove", _this.mouseMove);
    },
    mouseMove(event){
      const _this = this;
      let entG = _this.entG
      let tx = event.layerX-_this.scatterGTransformX;
      let ty = event.layerY-_this.scatterGTransformY-40;
      
      _this.selectEndX = tx;
      _this.selectEndY = ty;
      let sx =_this.selectStartX;
      let sy = _this.selectStartY;
      
      
      let minx = sx<tx?sx:tx;
      let miny = sy<ty?sy:ty;
      let maxx = sx>tx?sx:tx;
      let maxy = sy>ty?sy:ty;
      _this.drawRect(entG, minx, miny, maxx-minx, maxy-miny, 10, "grey", "5", "none","0.1", `SelectRect`, 'SelectRect');
      this.$refs.scatterCantain.addEventListener("mouseup", _this.mouseUp);
      // this.$refs.scatterC.addEventListener("mousedown", _this.mouseDown);
    },
    mouseUp(event){
      const _this = this;
      this.$refs.scatterCantain.removeEventListener("mousemove", _this.mouseMove);
      this.getSelectStudentList();
      // this.$refs.scatterCantain.removeEventL("mouseup", _this.mouseUp);
      // this.$refs.scatterC.addEventListener("mousedown", _this.mouseDown);
    },
    getSelectStudentList(){
      const _this = this;
      let groupData =   _this.groupData;
      let sx =_this.selectStartX;
      let sy = _this.selectStartY;
      let tx =_this.selectEndX;
      let ty = _this.selectEndY;
      let minx = sx<tx?sx:tx;
      let miny = sy<ty?sy:ty;
      let maxx = sx>tx?sx:tx;
      let maxy = sy>ty?sy:ty;
      let SelectStudentList = [];
        for(let i=0;i<groupData.length;i++){
          let cx = groupData[i]['cx'];
          let cy = groupData[i]['cy'];
          let sId = groupData[i]['id'];
          if(((cx>minx)&&(cx<maxx))&&((cy>miny)&&(cy<maxy))){
            SelectStudentList.push(sId);
          }
        }
      _this.SelectStudentList = SelectStudentList;
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
    updataScatter(){
      const _this = this;
      let entG = _this.entG;
      let groupData =   _this.groupData;
      let SelectStudentList  = _this.SelectStudentList;
        for(let i=0;i<groupData.length;i++){
          let cx = groupData[i]['cx'];
          let cy = groupData[i]['cy'];
          let r=groupData[i]['r']
          let sId = groupData[i]['id']
          let fill = groupData[i]['fill'];
          let opacity =0.3;
          if(SelectStudentList.indexOf(sId)!=-1){
            opacity = 1;
          }
          _this.drawCircle(entG, cx, cy, r, fill, opacity, 'entStu', `entStu_${sId}`);
        }
    },
    updataAll() {
      var _this = this;
      let margin = _this.margin
      let width = _this.$refs.scatterDiv.offsetWidth - margin.left - margin.right;
      let height = document.getElementById("scatterCantain").clientHeight - margin.top - margin.bottom;
      _this.width = width;
      _this.height = height;
      d3.select("#scatterCantain").select("svg").remove()
      var svg = d3.select("#scatterCantain").append("svg")
        .attr("width", width)
        .attr("height", height);
      _this.rootSvg = svg;

      let data = _this.groupData;
      let MaxMinX = _this.getMaxMin(data, 'x');
      let MaxMinY = _this.getMaxMin(data, 'y');

      _this.MaxMinX = MaxMinX;
      _this.MaxMinY = MaxMinY;

      _this.drawMain(svg);
      // });
    },
  },
  created() {
    var _this = this;
    let margin = _this.margin
    this.$nextTick(() => {
    });
  },
  mounted() {
    const _this = this;

    d3.select(".chartTooltip").classed("hidden", true);
    this.$bus.$on('groupData', (val) => {
      _this.groupData = val;
      this.updataAll();
    });
    this.$refs.scatterCantain.addEventListener("mousedown", _this.mouseDown); // 监听点击事件
    // this.$refs.movescatterRight.addEventListener("mousemove", _this.movescatterRight); // 监听点击事件
    // this.$refs.movescatterLeft.addEventListener("mouseleave", _this.leavescatterMove); // 监听点击事件
    // this.$refs.movescatterRight.addEventListener("mouseleave", _this.leavescatterMove); // 监听点击事件

  },
  beforeDestroy() {
    clearInterval(this.moveTimer);
  },
} 
</script>

<style>
@import './index.css';
</style>
