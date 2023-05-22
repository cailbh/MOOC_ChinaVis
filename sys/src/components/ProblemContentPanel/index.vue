<!-- eslint-disable no-unused-vars -->
<!-- eslint-disable no-unused-vars -->

<template>
  <div class="procPanel">
    <div class="panelHead">Content View </div>
      <!-- //SupportPanel</div> -->
    <div id="procPanelDiv" class="panelBody" ref="procPanelDiv">
      <div id="questionSer" ref="questionSer"></div>
      
        <el-table stripe  :data="tableData" style="width: 100%;height:80%;overflow-y: scroll;scrollbar-width: none;"         
        :row-style="iRowStyle"
        :cell-style="iCellStyle"
        :header-row-style="iHeaderRowStyle"
        :header-cell-style="iHeaderCellStyle">
          <!-- <el-table-column prop="key" label="" width="190">
          </el-table-column> -->
          <!-- eslint-disable -->
          <el-table-column prop="value" label="" width="480">
            <template slot-scope="scope">
              <div v-if="scope.row.key == 'Title'">
                <div style="float: left;height: 40px;font-size: 24px;color: rgb(103, 103, 103);">
                {{ scope.row.value }}</div>

              </div>
              <div v-if="scope.row.key == 'Type'">
                <!-- <div style="float: left;height:15px;font-size: 17px;"> -->
                <div style="float: left;height: auto;;font-size: 20px;color: rgb(103, 103, 103);">
                  {{ `${scope.row.value}` }}</div>
              </div>
              <div v-if="scope.row.key == 'ContentT'">
                <div style="float: left;height: auto;;font-size: 22px;color: rgb(103, 103, 103);">
                {{ scope.row.value }}</div>
              </div>
              <div v-if="scope.row.key == 'Content'">
                <div style="float: left;height: auto;">
                  &nbsp;&nbsp;{{ `&nbsp;&nbsp;${scope.row.value}` }}</div>
              </div>
              <div v-if="scope.row.key == 'InputT'">
                <div style="float: left;height: auto;;font-size: 22px;color: rgb(103, 103, 103);">
                {{ scope.row.value }}</div>
              </div>
              <div v-if="scope.row.key == 'Input'">
                <div style="float: left;height: auto;">
                  &nbsp;&nbsp;{{ `&nbsp;&nbsp;${scope.row.value}` }}</div>
              </div>
              <div v-if="scope.row.key == 'OutT'">
                <div style="float: left;height: auto;;font-size: 22px;color: rgb(103, 103, 103);">
                {{ scope.row.value }}</div>
              </div>
              <div v-if="scope.row.key == 'Out'">
                <div style="float: left;height: auto;">
                  &nbsp;&nbsp;{{ `&nbsp;&nbsp;${scope.row.value}` }}</div>
              </div>
            </template>
          </el-table-column>
          <!-- eslint-enable -->
        </el-table>
      <!-- <div id="connectCon" ref="connectCon">
      </div> -->
      <div id="procData" ref="procData">

      </div>
    </div>
    </div>
</template>
  
<script>
import * as d3 from 'd3'
import tools from "@/utils/tools.js";

export default {
  props: [],
  data() {
    return {
      typeRadio: "cell State",
      treeData: null,
      toolsState: '',
      problemsData:[],
      problemConceptData:[],
      conceptTree:[],
      // confirmUrl: require("@/assets/img/confirm.svg"),
      // cancelUrl: require("@/assets/img/cancel.svg"),
      // toolsButsUrl: require("@/assets/img/toolsButs.png"),
      // addNodeSonUrl: require("@/assets/img/addNode1.png"),
      // addNodePerUrl: require("@/assets/img/addNode2.png"),
      // addLinkBasicUrl: require("@/assets/img/addLink.png"),
      // nameinput: "Random Variables",
      nameinput: "Fundamental Graphs",
      // nameinput: "Trees",
      lectureStyleValue: [0, 80],
      tableData: [{
        key: 'Title',
        value: '',
      },{
        key: 'Type',
        value: '',
      }, {
        key: 'ContentT',
        value: '',
      }, {
        key: 'Content',
        value: '',
      }, {
        key: 'InputT',
        value: '',
      }, {
        key: 'Input',
        value: '',
      },{
        key: 'OutT',
        value: '',
      },{
        key: 'Out',
        value: '',
      }
      ],
      
      graphGTransformK: 1,
      graphGTransformX: 0,
      graphGTransformY: 10,
      curEntId: "",
      insertEntId: "",
      insertSourceEntId: "-1",
      insertTargetEntId: "-1",
      sonList: [],
      minDImportance: 0,
      maxDImportance: 0,
      minDRelevance: 0,
      maxDRelevance: 0,
      maxDDuration: 0,
      maxTotalDuration: 0,
      importanceMinColor: "rgb(203, 230, 209)",
      importanceMaxColor: "rgb(22, 144, 207)",
      totalDuration: 1000,
      importanceColor_linear: null,
      importanceCompute_color: null,
      relevanceScale_linear: null,
      totalDurationScale_linear: null,
      DivisionDataList: [],
      rootDivisionDataList: [],
      entDivisionDataList: [],
      colorMap: {},
      rootColorMap:{},
      videoDuration: 570,
      selectRectId: "",
      selectRectClass: "",
      topicLineWidth: 1000,
      topicLineHeight: 1000,
      moveLineWidth: 1000,
      entLineWidth: 1000,
      totalSonDuration: 0,
      treeGTransformK:1,
      treeGTransformX:10,
      treeGTransformY:100,
      margin: { top: 5, right: 5, bottom: 5, left: 5 },
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
      mLightcolor: [
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
    typeRadio(val) {
    },
    lectureStyleValue(val){
      console.log(val);
      let mid = (val[0]+val[1])/2;
      d3.select("#procData .el-slider__runway")
      .attr("style","background: linear-gradient(90deg, #ff9c9c "+mid+"%,#6f8be0 "+mid+"%) !important")
    },
    type(val) {
    },
    // selectEnt(val){
    //   console.log(val);
    // },
    curEntId(curEntId) {
    }
  },
  methods: {
    selectType(v) {
      // console.log(v)
    },
    

    iRowStyle:function ({row, rowIndex}) {
        return 'height:35px';
    },
    iHeaderRowStyle:function ({row, rowIndex}) {
        return 'height:35px';
    },
    iCellStyle:function ({row, column, rowIndex, columnIndex}) {
        return 'padding:2px'
    },
    iHeaderCellStyle:function ({row, column, rowIndex, columnIndex}) {
        return 'padding:0px'
    },
    drawprocData() {
      const _this = this;
      const margin = _this.margin;
      let width = this.$refs.procData.offsetWidth - margin.left - margin.right;
      let height = this.$refs.procData.offsetHeight - margin.top - margin.bottom;
      d3.select("#procData").select("svg").remove();
      var svg = d3.select("#procData").append("svg")
        .attr("id", "procEnt")
        .attr("width", width)
        .attr("height", height);

        let graphGTransformX = _this.graphGTransformX;
      let graphGTransformY = _this.graphGTransformY;
      let graphGTransformK = _this.graphGTransformK;
      
      let stx = 0;
      let sty = 0;
      let stk = 1;
      let entG = svg.append("g").attr("id", "entG").attr("width", width).attr("height", height);
      let sonG = svg.append("g").attr("id", "sonG").attr("width", width).attr("height", height).attr("transform", "translate(1,320)");
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
          entG.attr('transform', 'translate(' + (graphGTransformX) + ',' + (graphGTransformY) + ') scale(' + (graphGTransformK) + ')')
        })
        .on('end', (e) => {
          _this.graphGTransformX = graphGTransformX;
          _this.graphGTransformY = graphGTransformY;
          _this.graphGTransformK = graphGTransformK;
          entG.attr('transform', 'translate(' + (graphGTransformX) + ',' + (graphGTransformY) + ') scale(' + (graphGTransformK) + ')')
        });

      svg.call(graphZoom);
      // _this.entG = entG;
      // _this.sonG = sonG;
      _this.drawQuestionSurface(entG);
      // _this.drawSonLine(_this.data[1]);
    },
    drawSonLine(data) {
      const _this = this;
      let psvg = d3.select("#sonG");
      let w = psvg.attr("width") - 1;
      let h = 40;
      psvg.remove();
      let svg = d3.select("#procEnt").append("g").attr("id", "sonG").attr("width", w + 1).attr("height", h + 2).attr("transform", "translate(1,320)");
      let color_linear = _this.importanceColor_linear;
      let compute_color = _this.importanceCompute_color;
      let oData = _this.data;
      _this.entLineWidth = w;
      // if (sonList.length > 0) {
      svg.selectAll().remove();
      svg.append("line")
        .attr("x1", 0)
        .attr("y1", h / 2)
        .attr("x2", w)
        .attr("y2", h / 2)
        .attr("stroke", "rgb(200,200,200)")
        .attr("stroke-width", "5px");

      let totalSonDuration = 0;
      let dataIndex = oData.map(item => item.id).indexOf(data['id']);
      let startIndex = ((dataIndex - 2) > 0) ? (dataIndex - 2) : (0);
      let endIndex = ((dataIndex + 1) < oData.length) ? (dataIndex + 2) : (oData.length - 1);

      let dataLi = tools.deepClone(oData).splice(startIndex, endIndex - startIndex + 1);
      // let data = sonList;
      for (let i = 0; i < dataLi.length; i++) {
        let curEnt = oData.find(function (d) { return d['id'] == dataLi[i]['id'] });
        let time = tools.time2seconds(curEnt['time'][0]);
        let endTime = tools.time2seconds(curEnt['time'][1]);
        totalSonDuration += endTime - time;
      }
      _this.totalSonDuration = totalSonDuration;
      let cxLinear = d3.scaleLinear([0, totalSonDuration], [0, w]);
      let DivisionDataList = [];
      // let colorIndex = 0;
      let prex = 0;
      for (let i = 0; i < dataLi.length; i++) {
        let curEnt = oData.find(function (d) { return d['id'] == dataLi[i]['id'] });
        let temp = tools.deepClone(curEnt);
        if (DivisionDataList.length != 0) {
          DivisionDataList[DivisionDataList.length - 1]['nextId'] = temp['id'];
          temp['preId'] = DivisionDataList[DivisionDataList.length - 1]['id'];
        }
        else { temp['preId'] = "-1"; }
        DivisionDataList.push(temp);
        let time = tools.time2seconds(curEnt['time'][0]);
        let endTime = tools.time2seconds(curEnt['time'][1]);
        let curEntDur = endTime - time;
        let cx = prex;
        let endx = prex + cxLinear(curEntDur);
        let importanceValue = curEnt['attribute']['importance'];
        let entColor = compute_color(color_linear(importanceValue));
        if (i != 0) {
          _this.drawRect(svg, cx - 5, 0, 5, h, h / 2, "division_" + curEnt['id'], "entdivisionLine", "rgb(250,250,250)", 5, '', 0);
        }
        if (dataLi[i]['id'] == data['id']) _this.drawRect(svg, cx, 0, endx - cx, h, h / 2, "procEnt_" + curEnt['id'], "procEnt", entColor, 1, "black", 1)//color[_this.colorMap[son['id']]], 5, 0.1)
        else _this.drawRect(svg, cx, 0, endx - cx, h, h / 2, "procEnt_" + curEnt['id'], "procEnt", entColor, 1, "rgb(150,150,150)", 1)//color[_this.colorMap[son['id']]], 5, 0.1)
        prex = endx;
      }
      DivisionDataList[DivisionDataList.length - 1]['nextId'] = "-1";
      _this.entDivisionDataList = DivisionDataList;
    },
    drawEntityOri(data) {
      const _this = this;
      let psvg = d3.select("#entG");
      let w = psvg.attr("width");
      let h = psvg.attr("height");
      psvg.remove();
      let svg = d3.select("#procEnt").append("g").attr("id", "entG").attr("width", w).attr("height", h);
      let color_linear = _this.importanceColor_linear;
      let compute_color = _this.importanceCompute_color;
      let totalDurationValue = data['totalDuration'];
      let rScale = _this.totalDurationScale_linear;
      let r = rScale(totalDurationValue);
      let oData = _this.data;
      let x = svg.attr("width") / 2;
      let y = 120;
      let importanceValue = data['attribute']['importance'];
      let relevanceValue = data['attribute']['relevance'];
      svg.selectAll().remove();

      if (data['type'] == '1') {
        let area = tools.calcTriangle(x, y, r);
        _this.drawTriangle(svg, "rgb(250, 199, 88)", area, "rgb(250, 199, 88)");
      }
      else {

        let cy = y;
        let totalDuration = _this.totalDuration;
        let timeLineScale_linear = d3.scaleLinear([0, totalDuration], [x - r * Math.sqrt(3) / 2, x + r * Math.sqrt(3) / 2])
        let timeLineHighScale_linear = d3.scaleLinear([0, _this.maxDDuration], [0, r * (1 + Math.sqrt(3) / 2)])
        let circleColor = compute_color(color_linear(importanceValue));
        _this.drawCircle(svg, x, cy, r, circleColor, data, 1, "entCircle", "entCircle_" + data['id']);

        r = r * Math.sqrt(3) / 2;
        y += r / 2;
        let path = d3.path();


        path.moveTo(x - r, y);
        let lineLi = [data['time']];
        let linePoint = [{ 'id': data['id'], 'time': data['time'], 'x': 0, 'y': 0 }];
        for (let srel in data["similarityRel"]) {
          let cdata = oData.find(function (d) { return d['id'] == data["similarityRel"][srel] })
          lineLi.push(cdata['time'])
          linePoint.push({ 'id': cdata['id'], 'time': cdata['time'], 'x': 0, 'y': 0 })
        }
        const sortmt = (a, b) => {
          return tools.time2seconds(a[0]) - tools.time2seconds(b[0]);
        }
        const sortlp = (a, b) => {
          return tools.time2seconds(a['time'][0]) - tools.time2seconds(b['time'][0]);
        }
        lineLi = lineLi.sort(sortmt);
        linePoint = linePoint.sort(sortlp);
        let lineData = [[x - r, y]];
        for (let t = 0; t < lineLi.length; t++) {
          let startT = lineLi[t][0];
          let endT = lineLi[t][1];
          let startS = tools.time2seconds(startT);
          let endS = tools.time2seconds(endT);
          let duration = endS - startS;

          let startx = timeLineScale_linear((startS - duration * 10));
          let endx = timeLineScale_linear((endS + duration * 10));

          let startyf = y + timeLineHighScale_linear((duration)) / 8;
          let startyf1 = y + timeLineHighScale_linear((duration)) / 8;
          let endyf = y + timeLineHighScale_linear((duration)) / 8;
          let endyf1 = y + timeLineHighScale_linear((duration)) / 8;
          let yz = y - timeLineHighScale_linear((duration));
          let midx = timeLineScale_linear((endS + startS) / 2);
          linePoint[t]['x'] = midx;
          linePoint[t]['y'] = y - timeLineHighScale_linear(duration) / 1.7;
          let y1 = y;
          if (startx < (lineData[lineData.length - 1][0])) {
            if (t > 0) {
              lineData.splice(lineData.length - 3, 3);
              startx = (lineData[lineData.length - 1][0] + midx) / 2;
              y1 = lineData[lineData.length - 1][1] + timeLineHighScale_linear((duration)) / 2;
              startyf = lineData[lineData.length - 1][1] + timeLineHighScale_linear((duration)) / 2;
              startyf1 = lineData[lineData.length - 1][1] + timeLineHighScale_linear((duration)) / 2;
            }
          }
          let startx1 = startx + (timeLineScale_linear((startS + duration)) - timeLineScale_linear((startS)));
          let endx1 = endx - (timeLineScale_linear((startS + duration)) - timeLineScale_linear((startS)));
          let startx2 = startx1 + (timeLineScale_linear((startS + duration)) - timeLineScale_linear((startS)));
          let endx2 = endx1 - (timeLineScale_linear((startS + duration)) - timeLineScale_linear((startS)));
          if (endx > (r + x)) endx = r + x;
          if (startx1 < (lineData[lineData.length - 1][0])) startx1 = lineData[lineData.length - 1][0];
          if (endx1 > (r + x)) endx1 = r + x;
          if (startx2 < (lineData[lineData.length - 1][0])) startx2 = lineData[lineData.length - 1][0];
          if (endx2 > (r + x)) endx2 = r + x;
          lineData.push([startx, y1], [startx1, startyf1], [startx2, startyf], [midx, yz], [endx2, endyf], [endx1, endyf1], [endx, y])
        }
        lineData.push([x + r, y])
        let curve_generator = d3.line()
          .x((d) => d[0])
          .y((d) => {
            let h = Math.sqrt(Math.pow(r, 2) - Math.pow((d[0] - (x - r)), 2));
            if ((y - d[1]) > (h + r * Math.sqrt(3) / 2))
              return y - (h + r * Math.sqrt(3) / 2) + 2;
            return d[1];
          })
          .curve(d3.curveBasis)
        _this.drawTimeLine(svg, curve_generator(lineData), "white", 2, '0', 'sonLine ', 'sonLine ');


        for (let p = 0; p < linePoint.length; p++) {
          _this.drawCircle(svg, linePoint[p]['x'], linePoint[p]['y'], 5, "red", linePoint[p], 0, "linePoint", "linePoint_" + linePoint[p]['id']);
        }

        // "1": "rgb(145, 204, 117)",
        //   "2": "rgb(84, 112, 198)",
        //   "3": "rgb(238, 102, 102)",
        let typeColor = {
          "1": "#ff9c9c",
          "2": "#f4f4d0",
          "3": "#6f8be0",
        };
        let duration = tools.time2seconds(data['time'][0]) - tools.time2seconds(data['time'][1]);
        let typeData = data['attribute']['expressions'];
        let sonList = data['son'];
        let typeArcScale_linear = d3.scaleLinear([0, duration], [0, Math.PI * 2]);

        var typeStartR = 0//Math.PI/4;

        var typeStepR = Math.PI / 1;

        if (sonList.length > 0) {
          for (let i in typeData) {
            let color = typeColor[i];
            let typeDurition = typeData[i];
            let totalTypeSeconds = 0;
            for (let d in typeDurition) {
              totalTypeSeconds += (tools.time2seconds(typeDurition[d][1]) - tools.time2seconds(typeDurition[d][0]))
            }
            let typeStepR = typeArcScale_linear(totalTypeSeconds)//Math.PI/2;

            let endAnglet = typeStartR + 1 * typeStepR
            var dataset = { startAngle: typeStartR, endAngle: endAnglet }; //创建一个弧生成器
            typeStartR = endAnglet;
            var arcPath = d3.arc()
              .innerRadius(r + 10)
              .outerRadius(r + 25);
            var pathArc = arcPath(dataset);
            _this.drawArc(svg, x, y - r / 2, pathArc, color, color, 'type f' + data['id'] + " t" + i);
          }
          let sonTotal = 0;
          let sonNum = 0
          for (let s in sonList) {
            let sonData = oData.find(function (d) { return d['id'] == sonList[s] });
            let sonDur = sonData['totalDuration'];
            sonTotal += sonDur;
            sonNum += 1;
          }
          let skipArc = Math.PI / (sonNum + 2);
          let timeSonLinear = d3.scaleLinear([0, sonTotal], [0, Math.PI * 2 - skipArc * sonNum]);
          let timeSonHeighLinear = d3.scaleLinear([0, sonTotal], [40, 40]);

          let timeSonColor_linear = d3.scaleLinear().domain([0, sonTotal]).range([0, 1]);
          let timeSonCompute_color = d3.interpolate("white", circleColor);
          var sonStartR = 0;//-Math.PI/2;
          for (let s in sonList) {
            let sonData = oData.find(function (d) { return d['id'] == sonList[s] });
            let sonDur = sonData['totalDuration'];

            let sonStepR = timeSonLinear(sonDur)//Math.PI/2;

            let endAnglet = sonStartR + sonStepR;
            var dataset = { startAngle: sonStartR, endAngle: endAnglet }; //创建一个弧生成器
            sonStartR = endAnglet;
            let color = 'blue';
            var arcPath = d3.arc()
              .innerRadius(r + 28)
              .outerRadius(r + timeSonHeighLinear(sonDur));
            var arcMidPath = d3.arc()
              .innerRadius(0)
              .outerRadius(r + 32);
            var pathArc = arcPath(dataset);

            endAnglet = sonStartR + skipArc;
            var midDataset = { startAngle: sonStartR, endAngle: endAnglet }; //创建一个弧生成器

            let jiantouPath = d3.path();
            jiantouPath.arc(x, y - r / 2, r + 32, sonStartR - Math.PI / 2, endAnglet - Math.PI / 2);

            sonStartR += skipArc;
            var pathMidArc = arcMidPath(midDataset);
            let timeSonColor = compute_color(color_linear(sonData['attribute']['importance']));
            _this.drawArc(svg, x, y - r / 2, pathArc, timeSonColor, timeSonColor, 'son f' + data['id'] + " s" + sonList[s], '0');
            if (s != sonList.length - 1) {
              _this.drawTimeLine(svg, jiantouPath, "rgb(200,200,200)", 3, '9,5', 'midArc ', 'midArc ');
            }
          }

        }


      }
      let txts = _this.nameinput.split(" ")
      _this.drawTxt(svg, x - r - 32, y + r + 50, r * 2 + 64, txts, "grey");
    },
    drawEntity(data) {
      const _this = this;
      let psvg = d3.select("#entG");
      let w = psvg.attr("width");
      let h = psvg.attr("height");
      psvg.remove();
      let svg = d3.select("#procEnt").append("g").attr("id", "entG").attr("width", w).attr("height", h);
      let color_linear = _this.importanceColor_linear;
      let compute_color = _this.importanceCompute_color;
      let totalDurationValue = data['totalDuration'];
      let rScale = _this.totalDurationScale_linear;
      let r = rScale(totalDurationValue);
      let oData = _this.data;
      let x = svg.attr("width") / 2;
      let y = 120;
      let importanceValue = data['attribute']['importance'];
      let relevanceValue = data['attribute']['relevance'];
      svg.selectAll().remove();

      if (data['type'] == '1') {
        let area = tools.calcTriangle(x, y, r);
        _this.drawTriangle(svg, "rgb(250, 199, 88)", area, "rgb(250, 199, 88)");
      }
      else {

        let cy = y;
        let totalDuration = _this.totalDuration;
        let timeLineScale_linear = d3.scaleLinear([0, totalDuration], [x - r * Math.sqrt(3) / 2, x + r * Math.sqrt(3) / 2])
        let timeLineHighScale_linear = d3.scaleLinear([0, _this.maxDDuration], [0, r * (1 + Math.sqrt(3) / 2)])
        let circleColor = compute_color(color_linear(importanceValue));
        _this.drawCircle(svg, x, cy, r, circleColor, data, 1, "entCircle", "entCircle_" + data['id']);

        r = r * Math.sqrt(3) / 2;
        y += r / 2;
        let path = d3.path();


        path.moveTo(x - r, y);
        let lineLi = [data];
        let linePoint = [{ 'id': data['id'], 'time': data['time'], 'x': 0, 'y': 0 }];
        let jgidL = [data['id']];
        let similarityRelsli = [data["similarityRel"]];
        while(similarityRelsli.length>0){
          let similarityRels = similarityRelsli[0];
          similarityRelsli.splice(0,1);
          let jg = 0;
          for (let srel in similarityRels) {
            let cdata = oData.find(function (d) { return d['id'] == similarityRels[srel] });
            if(jgidL.indexOf(cdata['id'])==-1){
              similarityRelsli.push(cdata["similarityRel"])
              jg=1;
              lineLi.push(cdata)
              jgidL.push(cdata['id'])
              linePoint.push({ 'id': cdata['id'], 'time': cdata['time'], 'x': 0, 'y': 0 })
            }
          }
          // if(jg==0){
            // break;
          // }
        }
        
        const sortmt = (a, b) => {
          return tools.time2seconds(a[0]) - tools.time2seconds(b[0]);
        }
        const sortlp = (a, b) => {
          return tools.time2seconds(a['time'][0]) - tools.time2seconds(b['time'][0]);
        }
        console.log(lineLi);
        lineLi = lineLi.sort(sortlp);
        linePoint = linePoint.sort(sortlp);
        let lineData = [[x - r * Math.sqrt(3)/2-4 , y]];
        for (let t = 0; t < lineLi.length; t++) {
          let startT = lineLi[t]['time'][0];
          let duration =lineLi[t]['totalDuration']
          // let endT = lineLi[t]['time'][1];
          let startS = tools.time2seconds(startT);
          let endS = startS +duration;
          // let startx = timeLineScale_linear((startS - duration * 10));
          // let endx = timeLineScale_linear((endS + duration * 10));
          let limst = (x - r * Math.sqrt(3) / 2);
          let limed = (x + r * Math.sqrt(3) / 2);
          let startx = (limst<timeLineScale_linear((startS)))?(timeLineScale_linear((startS))):(limst);
          let endx = (limed>timeLineScale_linear((endS)))?(timeLineScale_linear((endS))):(limed);
          // let midx = timeLineScale_linear((endS + startS) / 2);
          let midx = (startx+endx) / 2;
          let ys = y;
          let yz = y - timeLineHighScale_linear((duration));
          linePoint[t]['x'] = midx;
          linePoint[t]['y'] = y - timeLineHighScale_linear(duration) / 1.7;
          // if (startx < (lineData[lineData.length - 1][0])) {
            if (t > 0) {
              lineData.splice(lineData.length - 1, 1);
              midx+=t*5;
              startx = midx-((midx-(lineData[lineData.length - 1][0] + midx) / 2))/2;
              endx+=t*5;
              ys = y+(y-lineData[lineData.length - 1][1])/3
            }
            console.log(ys)
          // }
          lineData.push([startx, ys],[midx, yz],[endx, y])}
        lineData.push([x + r, y])
        let curve_generator = d3.line()
          .x((d) => d[0])
          .y((d) => {
            let h = Math.sqrt(Math.pow(r, 2) - Math.pow((d[0] - (x - r)), 2));
            if ((y - d[1]) > (h + r * Math.sqrt(3) / 2))
              return y - (h + r * Math.sqrt(3) / 2) + 2;
            return d[1];
          })
          .curve(d3.curveBundle )
          // .curve(d3.curveCatmullRom  )
          // .curve(d3.curveBasis)
        _this.drawTimeLine(svg, curve_generator(lineData), "white", 2, '0', 'sonLine ', 'sonLine ');


        for (let p = 0; p < linePoint.length; p++) {
          _this.drawCircle(svg, linePoint[p]['x'], linePoint[p]['y'], 5, "red", linePoint[p], 0, "linePoint", "linePoint_" + linePoint[p]['id']);
        }

        // "1": "rgb(145, 204, 117)",
        //   "2": "rgb(84, 112, 198)",
        //   "3": "rgb(238, 102, 102)",
        let typeColor = {
          "1": "#ff9c9c",
          "2": "#f4f4d0",
          "3": "#6f8be0",
        };
        let duration = tools.time2seconds(data['time'][0]) - tools.time2seconds(data['time'][1]);
        let typeData = data['attribute']['expressions'];
        let sonList = data['son'];
        let sons = [sonList];
        while (sons.length > 0) {
          let curSonList = sons[0];
          sons.splice(0, 1);
          if (curSonList.length > 0) {
            for (let s in curSonList) {
              let sonData = oData.find(function (d) { return d['id'] == curSonList[s] });
              let sonTypeData = sonData['attribute']['expressions'];

              for (let t in sonTypeData) {
                let typeDurition = sonTypeData[t];
                for (let d in typeDurition) {
                   typeData[t].push(typeDurition[d])
                }
              }
              sons.push(sonData['son']);
            }
          }
        }
        var typeStartR = 0//Math.PI/4;

        var typeStepR = Math.PI / 1;

        if (sonList.length > 0) {
          let typeTotalDur = 0;
          for (let t in typeData) {
            let typeDurition = typeData[t];
            for (let d in typeDurition) {
              typeTotalDur += (tools.time2seconds(typeDurition[d][1]) - tools.time2seconds(typeDurition[d][0]))
            }
          }
          let typeArcScale_linear = d3.scaleLinear([0, typeTotalDur], [0, Math.PI * 2]);
          for (let i in typeData) {
            let color = typeColor[i];
            let typeDurition = typeData[i];
            let totalTypeSeconds = 0;
            for (let d in typeDurition) {
              totalTypeSeconds += (tools.time2seconds(typeDurition[d][1]) - tools.time2seconds(typeDurition[d][0]))
            }
            if(totalTypeSeconds>0)
            {let typeStepR = typeArcScale_linear(totalTypeSeconds)//Math.PI/2;

            let endAnglet = typeStartR + 1 * typeStepR
            var dataset = { startAngle: typeStartR, endAngle: endAnglet }; //创建一个弧生成器
            typeStartR = endAnglet;
            var arcPath = d3.arc()
              .innerRadius(r + 10)
              .outerRadius(r + 25);
            var pathArc = arcPath(dataset);
            _this.drawArc(svg, x, y - r / 2, pathArc, color, color, 'type f' + data['id'] + " t" + i);}
          }

          let sonTotal = 0;
          let sonNum = 0
          for (let s in sonList) {
            let sonData = oData.find(function (d) { return d['id'] == sonList[s] });
            let sonDur = sonData['totalDuration'];
            sonTotal += sonDur;
            sonNum += 1;
          }
          let skipArc = Math.PI / (sonNum + 2);
          let timeSonLinear = d3.scaleLinear([0, sonTotal], [0, Math.PI * 2 - skipArc * sonNum]);
          let timeSonHeighLinear = d3.scaleLinear([0, sonTotal], [40, 40]);

          let timeSonColor_linear = d3.scaleLinear().domain([0, sonTotal]).range([0, 1]);
          let timeSonCompute_color = d3.interpolate("white", circleColor);
          var sonStartR = 0;//-Math.PI/2;
          for (let s in sonList) {
            let sonData = oData.find(function (d) { return d['id'] == sonList[s] });
            let sonDur = sonData['totalDuration'];

            let sonStepR = timeSonLinear(sonDur)//Math.PI/2;

            let endAnglet = sonStartR + sonStepR;
            var dataset = { startAngle: sonStartR, endAngle: endAnglet }; //创建一个弧生成器
            sonStartR = endAnglet;
            let color = 'blue';
            var arcPath = d3.arc()
              .innerRadius(r + 28)
              .outerRadius(r + timeSonHeighLinear(sonDur));
            var arcMidPath = d3.arc()
              .innerRadius(0)
              .outerRadius(r + 32);
            var pathArc = arcPath(dataset);

            endAnglet = sonStartR + skipArc;
            var midDataset = { startAngle: sonStartR, endAngle: endAnglet }; //创建一个弧生成器

            let jiantouPath = d3.path();
            jiantouPath.arc(x, y - r / 2, r + 32, sonStartR - Math.PI / 2, endAnglet - Math.PI / 2);

            sonStartR += skipArc;
            var pathMidArc = arcMidPath(midDataset);
            let timeSonColor = compute_color(color_linear(sonData['attribute']['importance']));
            _this.drawArc(svg, x, y - r / 2, pathArc, timeSonColor, timeSonColor, 'son f' + data['id'] + " s" + sonList[s], '0');
            if (s != sonList.length - 1) {
              _this.drawTimeLine(svg, jiantouPath, "rgb(200,200,200)", 3, '9,5', 'midArc ', 'midArc ');
            }
          }

        }


      }
      let txts = data['name'].split(" ")
      let tx = x - r - 30;
      let ty = y + r +60;
      let tw = r*2;
      tx = x;
      if(data['son'].length==0){
        tx = x//-r-10;
        ty = y+r*2;
      }
      if(data['id']=="3"){
        tx = x-10;
        ty = y+r*2;
      }
      if(data['id']=="4"){
        tx = x+10;
        ty = y+r*2;
      }
      // if(data['type']=='1'){
      //   tx = x-r/2;
      //   ty = y+r*2;
      // }

      _this.drawTxt(svg, tx, ty,tw , txts, "grey",22, `text_${data['id']}`);
      // let txts = _this.nameinput.split(" ")
      // _this.drawTxt(svg, x - r - 32, y + r + 50, r * 2 + 64, txts, "grey");
    },
    drawQuestionSurface(svg){
      const _this = this;
      let psvg =svg
      let w = psvg.attr("width");
      let h = psvg.attr("height");
      psvg.select("#procG").remove();
      let backg = psvg.append("g").attr("id", "backG").attr("width", w).attr("height", h);
      let prog = psvg.append("g").attr("id", "procG").attr("width", w).attr("height", h);
      let proData = _this.problemsData;
      let problemConceptData = _this.problemConceptData;
      let conceptTree = _this.conceptTree;

      console.log(conceptTree,problemConceptData);
      let proId = _this.curEntId;
      if(proId == ""){return;}
      let curPro = proData.find(function(p){return (p['id']).toString() == (proId).toString()})
      let title = curPro['title'];
      let type = curPro['type'];
      let tx=10;
      let ty = 20;
      // ty = _this.drawTxt(prog,tx,ty,w,`Title:${title}`,"black",22,'title');
      let content = curPro['content'].split("###");

      let input =" ";
      let output ="";
      if(proId == '1568086661408161798'){
        title = "ASCII";
        content = ["已知字符 'a' 的ASCII码为 97，执行下列语句的输出是_______。 `printf ('%d, %c', 'b', 'b'+1 )` ;"];
        _this.tableData.find(function(t){return t['key'] == 'InputT'})['value'] = "";
        input = "A.98, b   B.错误 C. 98, 99   D. 98, c"
        _this.tableData.find(function(t){return t['key'] == 'OutT'})['value'] = "";
        // output = "C. 98, 99   D. 98, c"
      }
      else if(type == 'PROGRAMMING'){
        input =" "+ content[1].split("输入格式:")[1];
        output =""+ content[2].split("输出格式:")[1];
        title = `Title: ${' '} ${title}`;
        _this.tableData.find(function(t){return t['key'] == 'ContentT'})['value'] = "Description:";
        _this.tableData.find(function(t){return t['key'] == 'InputT'})['value'] = "Input Format:";
        _this.tableData.find(function(t){return t['key'] == 'OutT'})['value'] = "Output Format:";
      }
      else{
        title = "";

        _this.tableData.find(function(t){return t['key'] == 'InputT'})['value'] = "";
        _this.tableData.find(function(t){return t['key'] == 'OutT'})['value'] = "";
      }
      _this.tableData.find(function(t){return t['key'] == 'Title'})['value'] = `${' '} ${title}`;
      _this.tableData.find(function(t){return t['key'] == 'Type'})['value'] = `Type: ${type}`;
      _this.tableData.find(function(t){return t['key'] == 'Content'})['value'] = content[0];
      _this.tableData.find(function(t){return t['key'] == 'Input'})['value'] = ` ${input}`;
      _this.tableData.find(function(t){return t['key'] == 'Out'})['value'] = ` ${output}`;
      console.log(_this.tableData)
      let conMap = {}
      let conName = []
      for(let i=0;i<conceptTree.length;i++){
        conMap[conceptTree[i]['id']] = -1;
        conName.push(conceptTree[i]['id'])
      }
      // var compare = function (x, y) {//比较函数
      //   let lenx = x.length;
      //   let leny = y.length;
      //   if(lenx!=leny)return lenx>leny;
      //   return x["problemSetId"] > y["problemSetId"] 
      // };
      // conName.sort(compare)

      for (let i = 0; i < problemConceptData.length; i++) {
        let conceptId = problemConceptData[i]['conceptId'];
        let problemId = problemConceptData[i]['problem'];
        let type = problemConceptData[i]['type'];
        if(problemId == proId){
          conMap[conceptId] = type;
        }
      }
      let prex = 30;
      let prey = 60;
      let textWidth = _this.drawTxt(prog, 14, 20, "Related concepts：", "rgb(103, 103, 103)", 22, `kd`);
      conceptTree.forEach(con=>{
        let jg = conMap[con['id']];
        if(jg!=-1){
          let recColor = "rgb(218, 127, 136)";
          if(jg==0)
            recColor = "grey"
          let textWidth = _this.drawTxt(prog, prex, prey, con['name'], "white", 16, `ProSur_con${con['id']}`);
          _this.drawRect(backg, prex-4, prey-20, textWidth+8,28,  10, recColor, "1", "none", "1", `ProSur_coRect${con['id']}`, 'ProSur');
        // prey+=10;
          prex+=textWidth+20;
          if(prex>270){
            prex = 30;
            prey+=30
          }
        }
        // let textWidth = _this.drawTxt(prog, prex, prey, con['id']+''+conMap[con['id']], "black", 10, `FigNet_con`);

          // _this.drawTxt(prog,prex,prey,w,`Title:${content}`,"black",16,'title');
      })
      // _this.drawTxt(prog,tx,ty+25,w,`Title:${content}`,"black",16,'title');
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
    drawTxt(svg, x, y, text, fill, fontsize = 12, idN, an = 'start') {
      let txt = svg.append("text")
        .attr("y", y)
        .attr("x", x)
        .attr("id", idN)
        .attr("fill", fill)
        .attr("font-size", fontsize)
        .style("text-anchor", an)
        .text(text)
      
        let textWidth = document.getElementById(`${idN}`).getBBox().width;
      return textWidth;
    },
    drawTxtW(svg, x, y, width, txts, fill, fontsize = 12, idN) {
      let tx = x;
      let ty = y;
      let preWidth = 0;
      let preIdN = 0;
      let pretext = ''
      for (let t = 0; t < txts.length; t++) {
        pretext +=" "+ txts[t];
        let txt = svg.append("text")
          .attr("y", ty)
          .attr("x", tx)
          .attr("id", `${idN}_${t}`)
          .attr("fill", fill)
          .attr("font-size", fontsize)
          .style("text-anchor", "start")
          .text(pretext)
        let textWidth = document.getElementById(`${idN}_${t}`).getBBox().width;
        if((textWidth>width)||(t==txts.length -1)){
          pretext = '';
          tx = x;
          ty += 25;
        }
        else{
          txt.remove()
        }
        preWidth += textWidth;
      }
      return ty;
    },
    drawTxtOri1(svg, x, y, width, txts, fill,fontsize=12) {
      let tx = x;
      let ty = y;
      for (let t = 0; t < txts.length; t++) {

      let txt =   svg.append("text")
          .attr("y", ty)
          .attr("x", tx)
          .attr("fill", fill)
          .attr("font-size",fontsize)
          .style("text-anchor", "middle")
          .text(txts[t])
        tx += txts[t].length * 14;
        if (tx - x > width) {
          tx = x;
          ty += 25;
        }
      }
    },
    drawTxtOri(svg, x, y, width, txts, fill) {
      let tx = x;
      let ty = y;
      for (let t = 0; t < txts.length; t++) {

        svg.append("text")
          .attr("y", ty)
          .attr("x", tx)
          .attr("fill", fill)
          .text(txts[t])
        tx += txts[t].length * 10;
        if (tx - x > width) {
          tx = x;
          ty += 25;
        }
      }
    },
    drawTriangle(svg, color, points, stroke, opacity = 1) {
      svg.append("polygon")
        .attr("points", points)
        .attr("fill", color)
        .attr("stroke-linejoin", "round")
        .attr("opacity", opacity)
        .attr("stroke", stroke)
        .attr("stroke-width", "15px");
    },
    drawCircle(svg, x, y, r, fill, data, opacity, className = 'entCircle', idName) {
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
        .on("mouseover", function (d) {
          d3.select(this).attr("r", r * 1.1)
          let classN = d3.select(this).attr("class");
          if (classN == 'linePoint') {
            d3.select(this).attr("opacity", 1).attr("r", 5)
          }
          else {
            d3.selectAll(".f" + data['id'])
              .attr("transform", function (d) {
                let transformd = d3.select(this).attr("transform")
                return transformd.split(" ")[0] + " scale(1.1)"
              })

            d3.selectAll(".basicRel")
              .attr("class", function (d) {
                let classN = d3.select(this).attr("class");
                let classNList = classN.split(" ");
                let jg = 0;
                for (let i = 0; i < classNList.length - 1; i++) {
                  console.log('source' + data['id'], classNList[i])
                  if ('source' + data['id'] == classNList[i]) { jg = 1; }
                  if ('target' + data['id'] == classNList[i]) { jg = 1; }
                }
                if (jg == 1) {
                  classN += " activeS";
                }
                return classN;
              })
          }
        })
        .on("mouseleave", function (d) {
          d3.select(this).attr("r", r)
          let classN = d3.select(this).attr("class");
          if (classN == 'linePoint') {
            d3.select(this).attr("opacity", 0).attr("r", 5)
          }
          else {
            d3.selectAll(".f" + data['id'])
              .attr("transform", function (d) {
                let transformd = d3.select(this).attr("transform")
                return transformd.split(" ")[0] + " scale(1)"
              })
            d3.selectAll("path")
              .attr("class", function (d) {
                let thisSelect = d3.select(this)
                let classN = thisSelect.attr("class");
                let classNList = classN.split(" ")
                if (classNList[classNList.length - 1] == "activeS") {
                  classN = "";
                  for (let i = 0; i < classNList.length - 1; i++) {
                    classN += classNList[i] + " ";
                  }
                }
                return classN
              })
          }
        })
        .on("mousedown", function (d) {
          d3.select(this).attr("r", r);
          d3.selectAll(".f" + data['id'])
            .attr("transform", function (d) {
              let transformd = d3.select(this).attr("transform")
              return transformd.split(" ")[0] + " scale(1)"
            })
          let thisId = this.id.split("_")[1];
          let thisData = oData.find(function (a) { return a['id'] == thisId })
          let thisTime = thisData['time'];
          _this.click_Ent(thisTime);
          // console.log(thisTime,thisId,thisData)
        })
      // .on("")
    },
    drawTimeLine(svg, path, stroke, width, stroke_dasharray = "0", idName, className) {
      svg.append('path')
        .attr('d', path.toString())
        .attr('stroke', stroke)
        .attr('class', className)
        .attr('id', idName)
        .attr("stroke-dasharray", stroke_dasharray)
        .attr('stroke-width', width)
        .attr('fill', 'none')
        .on('mouseover', function (d) {
          let thisSelect = d3.select(this)
          let classN = thisSelect.attr("class");
          let idN = thisSelect.attr("id");
          if (classN.split(" ")[0] == "basicRel") {
            d3.select(this).attr("class", classN + " activeS");
          }
        })
        .on('mouseleave', function (d) {
          let thisSelect = d3.select(this)
          let classN = thisSelect.attr("class");
          let classNList = classN.split(" ")
          if (classNList[classNList.length - 1] == "activeS") {
            classN = "";
            for (let i = 0; i < classNList.length - 1; i++) {
              classN += classNList[i] + " ";
            }
            d3.select(this).attr("class", classN);
          }
        })
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
    updata() {
      
    const _this = this;
      _this.drawprocData();
    },
    click_Ent(time) {
      this.$emit("timeDur", time);
    },
  },
  created() {
    const _this = this;
    this.$nextTick(() => {
      _this.updata();

    });
  },
  mounted() {
    const _this = this
    // _this.tableData.find(function (d) { return d['key'] == 'name' })['value'] = 'Computer Network';
    this.$bus.$on('selectEnt', (val) => {
     _this.curEntId = val;
     _this.updata();
    });
    this.$bus.$on('allProblem', (val) => {
     _this.problemsData = val;
      // _this.updata();
    });
    
    this.$bus.$on('ConceptTree', (val) => {
      _this.conceptTree = val;
    });
    
    this.$bus.$on('Pro_Con', (val) => {
      _this.problemConceptData = val;
    });
  },
  // beforeDestroy() {
  //   clearInterval(this.moveTimer);
  // },
} 
</script>

<style>
@import './index.css';
</style>
