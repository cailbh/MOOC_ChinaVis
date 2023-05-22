<!-- eslint-disable no-unused-vars -->
<!-- eslint-disable no-unused-vars -->

<template>
  <div class="scatter" ref="scatterDiv">
    <div class="panelHead">Performance View</div>
    <div id="scatterCantain" ref="scatterCantain" class="panelBody">
    </div>

    <div class="scatterTooltip toolTip">
      <p>
          <br /><strong class="name toolTipAttr"></strong>
          <br /><strong class="text toolTipAttr"></strong>
          <br /><strong class="attr0 toolTipAttr"></strong>
          <br /><strong class="attr1 toolTipAttr"></strong>
          <br /><strong class="attr2 toolTipAttr"></strong>
          <br /><strong class="attr3 toolTipAttr"></strong>
          <br /><strong class="attr4 toolTipAttr"></strong>
        </p>
    </div>
    <div class="close" ref="listen">
    </div>
    <div id="addGroupDiv" @click="addGroupClk" ref="addBtn">
      <img class="icons" :src="addGroupUrl">
    </div>
    <div id="delGroupDiv" @click="delGroupClk" ref="addBtn">
      <img class="icons" :src="delGroupUrl">
    </div>
    <div id="confirmGroupDiv" @click="confirmGroupClk" ref="addBtn">
      <img class="icons" :src="confirmGroupUrl">
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
import contour from "@/utils/contour";

export default {
  props: ["toolsState"],
  data() {
    return {
      data: '',
      addGroupUrl: require("@/assets/img/addGroup.png"),
      delGroupUrl: require("@/assets/img/delGroup.png"),
      confirmGroupUrl: require("@/assets/img/confirmGroup.png"),
      scatterHeight: 0,
      selectStartX: 0,
      selectStartY: 0,
      selectEndX: 0,
      selectEndY: 0,
      selectGroupId: -1,
      selectGroup: [],
      stuAttrList: [],
      stuAttrMaxMinList: [],
      SelectStudentList: [],
      groupData: [],
      selectClick: 0,
      problemsData: [],
      proSetOriData: [],
      submissionsData: [],
      studentsData: [],
      conceptsData: [],
      conceptTree: [],
      proSetData: [],
      interY: 10,
      attrColorList: [],
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
      Ent_problem: [],
      Ent_concept: [],
      entG: "",
      entSetG: "",
      entbySetG: "",
      relG: "",
      curProblemId: '',
      curConceptId: '',
      curProblemSetId: '',
      selectProblemId: '',
      curConceptId: '',
      selectConceptId: '',
      proX: 500,
      proY: 0,
      setX: 800,
      setY: 0,
      treeX: 50,
      treeY: 0,
      proStepY: 0,
      conStepY: 0,
      rootSvg: null,
      rootSvgf: null,
      groupsSvg: null,
      arcG: null,
      backG: null,
      scatterZoom: null,
      jgDrag: true,
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
      scatterGTransformX: 0,
      scatterGTransformY: 0,
      scatterSvgScale: 1,
      moveTimer: null,
      moveFlag: false,
      stuMinColor: "rgb(255, 255, 255)",
      stuMaxColor: "rgb(76, 141, 5)",
      stepX: 80,
      stepY: 100,
      typeXMap: {
        "TRUE_OR_FALSE": 0,
        "MULTIPLE_CHOICE": 1,
        "FILL_IN_THE_BLANK": 2,
        "PROGRAMMING": 3,
        "CODE_COMPLETION": 4,
        "MULTIPLE_CHOICE_MORE_THAN_ONE_ANSWER": 5
      },
      circleInterval: 55,
      width: 0,
      height: 0,
      curToolState: 'unEdit',
      margin: { top: 1, right: 2, bottom: 0, left: 2 },
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
      attrColorList:[
      "rgb(255, 77, 109)",
        "rgb(255, 231, 32)",
        "rgb(250, 210, 50)",
        "rgb(255, 120, 90)",
        "rgb(255, 159, 28)",
        "rgb(6, 214, 160)",
        "rgb(125, 98, 211)",
      ],
    };
  },

  watch: {
    selectGroupId(val) {
      const _this = this;
      this.$refs.listen.addEventListener("mousedown", _this.mouseDown);
    },
    groupsSvg: {
      deep: true,
      handler(val) {
        var content = this.groupsSvg.html();
        this.rootSvgf.html(content)
        this.drawFigureAnnotation();
      }
    },
    SelectStudentList: {
      deep: true,
      handler(val) {
        let entG = this.entG;
        this.updataScatter();
        this.drawContour(entG);
      }
    },
    selectGroup(val) {
      const _this = this;
      d3.selectAll(".stuGroup").remove();
      let num = val.length;
      let backG = _this.rootSvgf;
      let colorList = _this.stuColorList;
      for (let i = 0; i < num; i++) {
        let cx = 20 + i * 40;
        let cy = 500;
        let r = 12;
        let fill = colorList[i];
        let opacity = 1;
        let circle = _this.drawCircle(backG, cx, cy, r, "white", opacity, fill, 3, 'stuGroup', `stuGroup_${i}`);
        circle.on("click", function () {
          d3.selectAll(`.stuGroup`).attr("opacity", 0.1);
          d3.select(this).attr("opacity", 1);
          let id = d3.select(this).attr("id").split("_")[1];
          _this.selectGroupId = id;

          d3.select(".close").classed("hidden", false);
        }).on("mouseover", function () {
          d3.selectAll(`.stuGroup`).attr("opacity", 0.1);
          d3.select(this).attr("opacity", 1);
          _this.$refs.listen.removeEventListener("mouseup", _this.mouseUp);
          _this.$refs.listen.removeEventListener("mousedown", _this.mouseDown);
          _this.jgDrag = false;
        })
      }
    },
    type(val) {
    },
  },
  methods: {

    addGroupClk() {
      const _this = this;
      let selectStuGroup = _this.selectGroup;
      // if (selectStuGroup.length < 5)
      //   selectStuGroup.push([]);
      selectStuGroup = [[],[],[]]
      _this.selectGroup = selectStuGroup;
      // d3.select(`#addGroupDiv`)
      // .attr("style", function(){
      //   return `right:${450-(selectStuGroup.length)*40}px`
      // });
    },
    delGroupClk() {
      const _this = this;
      let selectStuGroup = _this.selectGroup;
      if (selectStuGroup.length > 0)
        selectStuGroup.pop();
      _this.selectGroup = selectStuGroup;
      // d3.select(`#addGroupDiv`)
      // .attr("style", function(){
      //   return `right:${450-(selectStuGroup.length)*40}px`
      // });
    },
    confirmGroupClk() {
      const _this = this;
      let selectStuGroup = _this.selectGroup;

      this.$bus.$emit("SelectedStu", _this.SelectStudentList);
      // d3.select(`#addGroupDiv`)
      // .attr("style", function(){
      //   return `right:${450-(selectStuGroup.length)*40}px`
      // });
    },

    drawMain(svg) {
      let _this = this;
      let data = _this.data;
      let margin = _this.margin;

      let width = _this.width - margin.left - margin.right;
      let height = _this.height - margin.top - margin.bottom;

      let scatterGTransformX = _this.scatterGTransformX;
      let scatterGTransformY = _this.scatterGTransformY;
      let scatterGTransformK = _this.scatterGTransformK;

      let groups = svg.append("g").attr("id", "ggroups").attr("class", "groups").attr("width", width).attr("height", height)
        .attr("transform", "translate(" + scatterGTransformX + ',' + scatterGTransformY + ") scale(" + scatterGTransformK + ")");
      this.groupsSvg = groups;

      let backG = groups.append("g").attr("id", "gbackG").attr("class", "groups").attr("width", width).attr("height", height);
      let arcG = groups.append("g").attr("id", "garcG").attr("class", "groups").attr("width", width).attr("height", height);
      let relG = groups.append("g").attr("id", "grelG").attr("class", "groups").attr("width", width).attr("height", height);
      let entSetG = groups.append("g").attr("id", "gentSetG").attr("class", "groups").attr("width", width).attr("height", height);
      let entbySetG = groups.append("g").attr("id", "gentbySetG").attr("class", "groups").attr("width", width).attr("height", height);
      let entG = groups.append("g").attr("id", "gentG").attr("class", "groups").attr("width", width).attr("height", height);
      let frontG = groups.append("g").attr("id", "gfrontG").attr("class", "groups").attr("width", width).attr("height", height);

      let MaxMinX = _this.MaxMinX;
      let MaxMinY = _this.MaxMinY;

      let xSize_linear = d3.scaleLinear().domain([MaxMinX[1], MaxMinX[0]]).range([30, width - 30]);
      let ySize_linear = d3.scaleLinear().domain([MaxMinY[1], MaxMinY[0]]).range([30, height - 30]);

      _this.arcG = arcG;
      _this.entG = entG;
      _this.entSetG = entSetG;
      _this.entbySetG = entbySetG;
      _this.relG = relG;
      _this.backG = backG;
      _this.scatterZoom = scatterZoom;
      let copyg = _this.rootSvgf.select("#ggroups");
      let interval = _this.circleInterval;



      let scalePre = _this.scatterSvgScale;
      let stx = 0;
      let sty = 0;
      let stk = 1;
      var scatterZoom = d3.zoom()
        .scaleExtent([0, 100])
        .on("start", (e) => {
          if (_this.jgDrag) {
            sty = e.transform.y;
            stx = e.transform.x;
            stk = e.transform.k;
          }
        })
        .on('zoom', (e) => {
          if (_this.jgDrag) {
            scatterGTransformX = _this.scatterGTransformX + e.transform.x - stx;
            scatterGTransformY = _this.scatterGTransformY + e.transform.y - sty;
            scatterGTransformK = _this.scatterGTransformK + e.transform.k - stk;
            groups.attr('transform', 'translate(' + (scatterGTransformX) + ',' + (scatterGTransformY) + ') scale(' + (scatterGTransformK) + ')')
            _this.rootSvgf.selectAll(".groups").attr('transform', 'translate(' + (scatterGTransformX) + ',' + (scatterGTransformY) + ') scale(' + (scatterGTransformK) + ')')
          }
        })
        .on('end', (e) => {
          if (_this.jgDrag) {
            _this.scatterGTransformX = scatterGTransformX;
            _this.scatterGTransformY = scatterGTransformY;
            _this.scatterGTransformK = scatterGTransformK;
            groups.attr('transform', 'translate(' + (scatterGTransformX) + ',' + (scatterGTransformY) + ') scale(' + (scatterGTransformK) + ')')
            _this.groupsSvg = groups;
          }
        });

      svg.call(scatterZoom);
      d3.select(".close").classed("hidden", true);
      d3.select(".scatterTooltip").classed("hidden", true);
      // svg.call(d3.zoom().on('start', null).on('zoom',null).on('end', null))

      let attrList = _this.stuAttrList;
      let stuAttrMaxMinList = _this.stuAttrMaxMinList;

      let rSize_linear = d3.scaleLinear().domain([stuAttrMaxMinList[1][1], stuAttrMaxMinList[1][0]]).range([3, 8]);

      let stuMaxColor = _this.stuMaxColor;
      let stuMinColor = _this.stuMinColor;
      let stuColor_linear = d3.scaleLinear().domain([stuAttrMaxMinList[1][1], stuAttrMaxMinList[1][0]]).range([0, 1]);
      let stuCompute_color = d3.interpolate(stuMinColor, stuMaxColor);

      let groupData = tools.deepClone(_this.groupData);
      let colorList = _this.mcolor;
      for (let i = 0; i < groupData.length; i++) {
        let cx = xSize_linear(groupData[i]['x']);
        let cy = ySize_linear(groupData[i]['y']);
        let sId = groupData[i]['id']
        groupData[i]['cx'] = cx;
        groupData[i]['cy'] = cy;
        groupData[i]['r'] = rSize_linear(groupData[i][attrList[1]]);
        groupData[i]['fill'] = stuCompute_color(stuColor_linear(groupData[i][attrList[1]])) //'grey'//colorList[parseInt(groupData[i]['kmeansC'])];
      }
      _this.groupData = groupData;
      _this.updataScatter();
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
    drawFigureAnnotation() {
      const _this = this;
      let frontG = _this.rootSvgf;

      let stuMaxColor = _this.stuMaxColor;
      let stuMinColor = _this.stuMinColor;

      let len = 6;

      let Color_linear = d3.scaleLinear().domain([0, len]).range([0, 1]);
      let Rsize_linear = d3.scaleLinear().domain([0, len]).range([1, 6]);
      let Compute_color = d3.interpolate(stuMinColor, stuMaxColor);

      let textsr = _this.drawTxt(frontG, 6, 15, "BestScoreingRate:", "black", 10, `FigScater_con`);
      let textat = _this.drawTxt(frontG, 6, 45, "Attempts:", "black", 10, `FigScater_con`);
      let textbs = _this.drawTxt(frontG, 6, 75, "ScoreingRate:", "black", 10, `FigScater_con`);
      let prex = 0;
      let prerx = 0;
      let colorSR = _this.attrColorList[0];
      let colorBestS = _this.attrColorList[1];
      let colorAttempts = _this.attrColorList[2];

      _this.drawRect(frontG, 10, 58, 40, 5, 0, "rgb(230,230,230)", "1", "grey", "1", `FigScater_conRectColorB`, 'FigScater');
      _this.drawRect(frontG, 10, 58, 30, 5, 0, colorAttempts, "1", "grey", "1", `FigScater_conRectColor`, 'FigScater');

      _this.drawRect(frontG, 10, 88, 40, 5, 0, "rgb(230,230,230)", "1", "grey", "1", `FigScater_conRectB`, 'FigScater');
      _this.drawRect(frontG, 10, 88, 30, 5, 0, colorSR, "1", "grey", "1", `FigScater_conRect`, 'FigScater');

      let path1 = d3.path();
      let points = [[10, 50], [10, 54], [14, 50], [10, 54], [14, 58], [10, 54], [10, 58], [10, 54], [40, 54], [40, 54], [36, 50], [40, 54], [36, 58], [40, 54], [40, 50], [40, 58]]
      let points2 = [[10, 80], [10, 84], [14, 80], [10, 84], [14, 88], [10, 84], [10, 88], [10, 84], [40, 84], [40, 84], [36, 80], [40, 84], [36, 88], [40, 84], [40, 80], [40, 88]]
      let curve_generator = d3.line()
        .x((d) => d[0])
        .y((d) => d[1])
      // .curve(d3.curveBasisClosed)
      _this.drawLine(frontG, curve_generator(points), "black", 1, '0', '1', `line1`, 'FigScater_line1', "rgb(230,230,230)");
      _this.drawLine(frontG, curve_generator(points2), "black", 1, '0', '1', `line2`, 'FigScater_line1', "rgb(230,230,230)");
      for (let i = 0; i < len * 3; i++) {
      }
      for (let i = 0; i < len; i++) {
        let color = Compute_color(Color_linear(i));
        let circle = _this.drawCircle(frontG, 15 + prex, 23, Rsize_linear(i), color, 1, "none", "1", 'FigScater', `FigScater_conColor${i}`);
        prex += Rsize_linear(i) * 2 + 4;
        prerx += i * 4 + 2;
      }

    },
    drawContour(svg) {
      const _this = this;
      d3.selectAll(".counter").remove();
      let groupData = tools.deepClone(_this.groupData);
      let SelectStudentList = _this.SelectStudentList;
      let nodesList = [
        [], [], [], [], []
      ]
      for (let i = 0; i < SelectStudentList.length; i++) {
        for (let j = 0; j < SelectStudentList[i].length; j++) {
          let stuD = groupData.find(function (s) { return s['id'] == SelectStudentList[i][j] });
          let stuTemp = {
            x: stuD['cx'],
            y: stuD['cy'],
            r: stuD['r'] + 6 * 3 - 3
          }
          nodesList[i].push(stuTemp);
        }
      }
      let colorList = _this.stuColorList;
      // for(let i=0;i<groupData.length;i++){
      //   let sId = groupData[i]['id']
      //     nodesList[parseInt(groupData[i]['kmeansC'])].push({
      //       x:groupData[i]['cx'],
      //       y:groupData[i]['cy'],
      //       r:groupData[i]['r']
      //     })
      // }
      let k = 0;
      nodesList.forEach(nodeList => {
        let path = contour(nodeList, 80);
        let contourData = _this.arcsToPaths(path)
        contourData.forEach(contourD => {
          svg.append("path")
            .attr("class", "counter")
            .attr("d", function () { return contourD.d; })
            .style("stroke", colorList[parseInt(k)])
            .style("stroke-width", 3)
            .style("opacity", 1)
            // .attr("stroke-dasharray", "3")
            // .attr("stroke-dashoffset", "30")
            .attr("transform", function () { return contourD.transform; });
        })
        k++;
      })

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
    arcsToPaths(arcs) {
      let paths = [];
      let arcGen = d3.arc();

      arcs.forEach(function (arc) {
        let startAngleTemp = arc.startAngle;

        if (startAngleTemp > arc.endAngle) {
          startAngleTemp -= 2 * Math.PI;
        }

        paths.push({
          d: arcGen({
            innerRadius: arc.radius,
            outerRadius: arc.radius,
            startAngle: startAngleTemp,
            endAngle: arc.endAngle
          }),
          transform: "translate(" + arc.center.x + "," + arc.center.y + ")"
        });
      });

      return paths;
    },
    drawCircle(svg, x, y, r, fill, opacity, stroke, width, className = 'entCircle', idName) {
      const _this = this;

      d3.select(`#${idName}`).remove();
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
    getMaxMin(data, attrname) {
      return [
        Math.max.apply(Math, data.map(function (d) { return d[attrname]; })),
        Math.min.apply(Math, data.map(function (d) { return d[attrname]; }))
      ]
    },
    mouseDown(event) {
      const _this = this;
      _this.jgDrag = false;
      let entG = _this.entG
      let sx = event.layerX - _this.scatterGTransformX;
      let sy = event.layerY - _this.scatterGTransformY;
      _this.selectStartX = sx;
      _this.selectStartY = sy;
      // _this.drawRect(entG, sx, sy, 100, 100, 10, "grey", "5", "none","0.1", `SelectRect`, 'SelectRect');
      this.$refs.listen.addEventListener("mousemove", _this.mouseMove);
    },
    mouseMove(event) {
      const _this = this;
      let entG = _this.entG
      let tx = event.layerX - _this.scatterGTransformX;
      let ty = event.layerY - _this.scatterGTransformY;

      _this.selectEndX = tx;
      _this.selectEndY = ty;
      let sx = _this.selectStartX;
      let sy = _this.selectStartY;


      let minx = sx < tx ? sx : tx;
      let miny = sy < ty ? sy : ty;
      let maxx = sx > tx ? sx : tx;
      let maxy = sy > ty ? sy : ty;
      _this.drawRect(entG, minx, miny, maxx - minx, maxy - miny, 10, "grey", "5", "none", "0.1", `SelectRect`, 'SelectRect');
      this.$refs.listen.addEventListener("mouseup", _this.mouseUp);
      // this.$refs.scatterC.addEventListener("mousedown", _this.mouseDown);
    },
    mouseUp(event) {
      const _this = this;
      this.$refs.listen.removeEventListener("mousemove", _this.mouseMove);
      _this.jgDrag = true;

      d3.select(".close").classed("hidden", true);
      this.getSelectStudentList();
      // this.$refs.scatterCantain.removeEventL("mouseup", _this.mouseUp);
      // this.$refs.scatterC.addEventListener("mousedown", _this.mouseDown);
    },
    getSelectStudentList() {
      const _this = this;
      let temp = tools.deepClone(_this.SelectStudentList);
      let groupData = _this.groupData;
      let sx = _this.selectStartX;
      let sy = _this.selectStartY;
      let tx = _this.selectEndX;
      let ty = _this.selectEndY;
      _this.selectStartX = 0;
      _this.selectStartY = 0;
      _this.selectEndX = 0;
      _this.selectEndY = 0;
      let minx = sx < tx ? sx : tx;
      let miny = sy < ty ? sy : ty;
      let maxx = sx > tx ? sx : tx;
      let maxy = sy > ty ? sy : ty;
      let SelectStudentList = [];
      let BuSelectStudentList = [];
      for (let i = 0; i < groupData.length; i++) {
        let cx = groupData[i]['cx'];
        let cy = groupData[i]['cy'];
        let sId = groupData[i]['id'];
        if (((cx > minx) && (cx < maxx)) && ((cy > miny) && (cy < maxy))) {
          let jg = 0;
          temp.forEach(t => {
            t.forEach(s => {
              if (s == sId)
                jg = 1;
            })
          })
          if (jg == 0)
            SelectStudentList.push(sId);
          
        }
        else{
          let jg = 0;
          temp.forEach(t => {
            t.forEach(s => {
              if (s == sId)
                jg = 1;
            })
          })
          if (jg == 0)
            BuSelectStudentList.push(sId);
        }
      }
      let selectGroupId = _this.selectGroupId;
      temp[selectGroupId] = SelectStudentList;
      if((selectGroupId == 1)){
        temp[2] = BuSelectStudentList;
      }
      _this.SelectStudentList = temp;
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
    updataScatter() {
      const _this = this;
      let entG = _this.entG;
      let groupData = _this.groupData;
      let SelectStudentList = _this.SelectStudentList;
      for (let i = 0; i < groupData.length; i++) {
        let cx = groupData[i]['cx'];
        let cy = groupData[i]['cy'];
        let r = groupData[i]['r']
        let sId = groupData[i]['id']
        let fill = groupData[i]['fill'];
        let opacity = 1;
        // if(SelectStudentList.indexOf(sId)!=-1){
        //   opacity = 1;
        // }
        _this.drawCircle(entG, cx, cy, r, fill, opacity, "grey", "0", 'entStu', `entStu_${sId}`);
        let stuAttrList = _this.stuAttrList;
        let stuAttrMaxMinList = _this.stuAttrMaxMinList;
        let attrLen = stuAttrList.length;
        let colorList = _this.attrColorList;
        let starR = 0;//-Math.PI/2;
        let stepH = 7;
        let perh = r;
        for (let j = 0; j < attrLen; j++) {
          if (stuAttrList[j] == 'bestScore') {

          }
          else if (stuAttrList[j] == 'acceptedNum') {

          }
          else {
            let Angle_linear = d3.scaleLinear().domain([0, stuAttrMaxMinList[j][0]]).range([0, Math.PI * 2]);
            let h = perh + stepH;
            var dataset = { startAngle: starR, endAngle: starR + Angle_linear(groupData[i][stuAttrList[j]]) }; //创建一个弧生成器
            var datasetB = { startAngle: starR, endAngle: starR + Math.PI * 2 }; //创建一个弧生成器
            var arcPath = d3.arc()
              .innerRadius(perh)
              .outerRadius(h - 1);
            var arcPathBack = d3.arc()
              .innerRadius(1)
              .outerRadius(h + 2);
            perh = h;
            var pathArc = arcPath(dataset);
            var pathArcB = arcPath(datasetB);
            let entColor = colorList[j];//importanceCompute_color(importanceColor_linear(curEnt['scoringRate']));
            // _this.drawArc(entG, 0, 0, arcPathBack(dataset), "#000", "#000", 'type', 0, 3);
            _this.drawArc(entG, cx, cy, pathArcB, fill, "rgb(230,230,230)", 'typeB', `stuAttrB_${sId}_${j}`, 0, 0);
            _this.drawArc(entG, cx, cy, pathArc, entColor, entColor, 'type', `stuAttr_${sId}_${j}`, 0, 0);
          }
        }

        let circle = _this.drawCircle(entG, cx, cy, 25, fill, 0, "grey", "0", 'entStuF', `entStuF_${sId}_${i}`);
        circle.on("mousemove", function (d) {
          let ts = d3.select(this);
          let id = ts.attr("id").split("_")[1];
          _this.overScatterStuId = id;

          _this.$bus.$emit("SelectingStu", _this.overScatterStuId);

          let idod = ts.attr("id").split("_")[2];
          let clasN = ts.attr("class");
          let nametext = '';
          let ent = groupData.find(function (c) { return c['id'] == id });
          var yPosition = d.clientY + 20;
          var xPosition = d.clientX + 20;
          
          if(d.clientX>2100){
            xPosition = d.clientX - 210;
          }
          let srtext = ent['scoringRate'];
          let totalAttemptsTxt = ent['totalAttempts'];
          let bestScore = ent['bestScore']
          var scatterTooltip = d3
            .select(".scatterTooltip")
            .style("left", xPosition + "px")
            .style("top", yPosition + "px");
          // 更新浮层内容
          let attr = ['scoringRate', 'totalAttempts','bestScore'];
          let attrN = ['Scoring Rate', 'Attempts', 'bestScoreRate', 'Rel Count'];
          // 更新浮层内容
          for (let a = 0; a < attr.length; a++) {

            scatterTooltip.select(`.attr${a}`).text(`${attrN[a]} : ${ent[attr[a]]}`)
            if(attrN[a] == 'Scoring Rate')
              scatterTooltip.select(`.attr${a}`).text(`${attrN[a]} : ${ent[attr[a]].toFixed(2)}`)
          }
          scatterTooltip.select(".name").text(`Student${i+1}`);
          // 移除浮层hidden样式，展示浮层
          scatterTooltip.classed("hidden", false);
        }).on("mouseleave", function (d) {
          _this.$bus.$emit("SelectingStu", "");
          d3.select(".scatterTooltip").classed("hidden", true);
        })
      }
    },

    drawArc(svg, x, y, arcPath, stroke, fill, className, idN, stroke_dasharray = "0", width = 3) {
      d3.select(`#${idN}`).remove();
      svg.append("path")
        .attr("d", arcPath)
        .attr("class", className)
        .attr("id", idN)
        .attr("transform", "translate(" + x + "," + y + ")")
        .attr("stroke", stroke)
        .attr('stroke-width', width)
        .attr("stroke-dasharray", stroke_dasharray)
        .attr("stroke-linejoin", "round")
        .attr("fill", fill)
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
        .attr("width", width - 0)
        .attr("height", height - 50)
        .attr('transform', 'translate(0,0)')
        .style("position", "absolute");

      var svgf = d3.select("#scatterCantain").append("svg")
        .attr("width", width)
        .attr("height", height)
      _this.rootSvg = svg;
      _this.rootSvgf = svgf;

      _this.rootSvgFig = svg;
      let data = _this.groupData;
      let MaxMinX = _this.getMaxMin(data, 'x');
      let MaxMinY = _this.getMaxMin(data, 'y');

      let stuAttrList = ['scoringRate', 'bestScore', 'totalAttempts', 'acceptedNum']//,'time']
      _this.stuAttrList = stuAttrList;
      let stuAttrMaxMinList = [];

      for (let i = 0; i < stuAttrList.length; i++) {
        stuAttrMaxMinList.push(_this.getMaxMin(data, stuAttrList[i]));
      }
      _this.stuAttrMaxMinList = stuAttrMaxMinList;

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

    d3.select(".scatterTooltip").classed("hidden", true);
    this.$bus.$on('groupData', (val) => {
      _this.groupData = val;
      this.updataAll();
    });

    // this.$bus.$on('attrColorList', (val) => {_this.attrColorList = val;});
    this.$bus.$on('stuColorList', (val) => { _this.stuColorList = val; });
    // this.$refs.scatterCantain.addEventListener("mousedown", _this.mouseDown); // 监听点击事件
    // this.$refs.movescatterRight.addEventListener("mousemove", _this.movescatterRight); // 监听点击事件
    // this.$refs.movescatterLeft.addEventListener("mouseleave", _this.leavescatterMove); // 监听点击事件
    // this.$refs.movescatterRight.addEventListener("mouseleave", _this.leavescatterMove); // 监听点击事件

  },
  beforeDestroy() {
    clearInterval(this.moveTimer);
  },
} 
</script>

<style>@import './index.css';</style>
