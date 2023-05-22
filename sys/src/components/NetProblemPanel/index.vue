<!-- eslint-disable no-unused-vars -->
<!-- eslint-disable no-unused-vars -->

<template>
  <div class="netPPanel">
    <div class="panelHead">Correlation View</div>
    <!-- //SupportPanel</div> -->
    <div id="netPPanelDiv" class="panelBody" ref="netPPanelDiv">
      <div id="topicLine" ref="topicLine"></div>
      <div id="netPData" ref="netPData"></div>
      
      <div class="netTooltip toolTip">
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

    </div>
  </div>
</template>
  
<script>
import * as d3 from 'd3'
import { onMounted, ref } from 'vue';
import filenames from "@/utils/fileName";
import domtoimage from 'dom-to-image';
import tools from "@/utils/tools.js";
import { tree } from 'd3';
import { SourceNode } from 'source-list-map';

export default {
  props: [],
  data() {
    return {
      typeRadio: "cell State",
      treeData: null,
      toolsState: '',
      proAttrList: [],
      selectedPro: [],
      selectedCon: '',
      proAttrMaxMinList: [],
      conAttrList: [],
      conAttrMaxMinList: [],
      problemsData: [],
      problemConceptData: [],
      problemRelByConcept: [],
      problemListByConcept: [],
      submissionsData: [],
      studentsData: [],
      conceptsData: [],
      netData: [],
      attrColorList: [],
      calcNetDataRady: 0,
      nameinput: "Fundamental Graphs",
      curEntId: "",
      insertEntId: "",
      EntProData: {},
      insertSourceEntId: "-1",
      insertTargetEntId: "-1",
      sonList: [],

      entProMinColor: "rgb(255,255,255)",
      entProMaxColor: "rgb(255, 0, 0)",

      entConMinColor: "rgb(255,255,255)",
      entConMaxColor: "rgb(46, 117, 182)",

      margin: { top: 5, right: 5, bottom: 5, left: 5 },
    };
  },
  watch: {
    typeRadio(val) {
    },
    netData() {
    },
    studentsData() {
      this.calcNetDataRady++;
    },
    problemsData() {
      this.calcNetDataRady++;
    },
    submissionsData() {
      this.calcNetDataRady++;
    },
    calcNetDataRady(val) {
      if (val == 3) {
        // this.calcNetData();
        // this.getProRel();
      }
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

    drawnetPData() {
      const _this = this;
      const margin = _this.margin;
      let width = this.$refs.netPData.offsetWidth - margin.left - margin.right;
      let height = this.$refs.netPData.offsetHeight - margin.top - margin.bottom;
      d3.select("#netPData").select("svg").remove();
      var svg = d3.select("#netPData").append("svg")
        .attr("id", "netPEnt")
        .attr("width", width)
        .attr("height", height);

      let entG = svg.append("g").attr("id", "entG").attr("width", width).attr("height", height);
      let sonG = svg.append("g").attr("id", "sonG").attr("width", width).attr("height", height)
      //.attr("transform", "translate(1,320)");
      // _this.entG = entG;
      // _this.sonG = sonG;
      _this.drawProConNet(entG);
      _this.drawFigureAnnotation(svg);
    },
    drawProConNet(svg) {
      const _this = this;
      let psvg = svg
      let width = psvg.attr("width");
      let height = psvg.attr("height");
      psvg.select("#netPG").remove();
      // let prog = psvg.append("g").attr("id", "netPG").attr("width", width).attr("height", height);
      let groups = svg.append("g").attr("id", "groups").attr("width", width).attr("height", height)
      // .attr("transform", "translate(" + graphGTransformX + ',' + graphGTransformY + ") scale(" + graphGTransformK + ")");
      // this.groupsSvg = groups;

      let backG = groups.append("g").attr("id", "proRbackG").attr("width", width).attr("height", height);
      let arcG = groups.append("g").attr("id", "proRarcG").attr("width", width).attr("height", height);
      let relG = groups.append("g").attr("id", "proRrelG").attr("width", width).attr("height", height);
      let entG = groups.append("g").attr("id", "proRentG").attr("width", width).attr("height", height);
      let frontG = groups.append("g").attr("id", "proRfrontG").attr("width", width).attr("height", height);

      let conceptsData = _this.conceptsData;
      let problemsData = _this.problemsData;
      let netData = _this.netData;
      let problemConceptData = _this.problemConceptData;
      let proRel = tools.deepClone(_this.problemRelByConcept);
      let proInList = tools.deepClone(_this.problemListByConcept);
      let ent_edgeC = [];

      let ent_nodeC = [];
      let ent_nodeP = [];
      let ent_edgeP = [];
      let proId = _this.curEntId;
      // if (proId == "") { return; }
      // let proList = proInList[proId];
      let proList = proInList;
      console.log(111)
      console.log(proList,proRel);
      let addEgList = {'0_0':[],"0_1":[],"1_0":[],"1_1":[]};
      // let conList = proRel[proId];
      for (let r = 0; r < problemConceptData.length; r++) {
        let curRel = problemConceptData[r];
        let pId = curRel['problem'];
        let cId = curRel['conceptId'];
        let type = curRel['type'];
        if (pId != proId) {
        }            
        if(proId != ""){
          if (pId == proId) {
            ent_edgeP.push({
              source: pId,
              target: cId,
              type:type
            })
            if (ent_nodeP.find(function (d) { return d['id'] == pId }) == undefined) {
              ent_nodeP.push({ "id": pId, "type": "problem" })
            }
            if (ent_nodeP.find(function (d) { return d['id'] == cId }) == undefined) {
              ent_nodeP.push({ "id": cId, "type": "concept" })
            }
          }
          else{
            for(let g=0;g<proRel.length;g++){
              let arr = proRel[g];
              
              if ((proList.indexOf(pId) != -1)) {
                if(arr.indexOf(cId)!=-1){
                  let tp = `${g}_${type}`;
                  if(addEgList[tp].indexOf(pId)==-1)
                    addEgList[tp].push(pId);
                    ent_edgeP.push({
                      source: pId,
                      target: cId,
                      type:type
                    })
                  if (ent_nodeP.find(function (d) { return d['id'] == pId }) == undefined) {
                    ent_nodeP.push({ "id": pId, "type": "problem" })
                  }
              }}
            }
          }  
        }
        else {
          // if ((conList.indexOf(cId)!=-1)) {
          if ((proList.indexOf(pId) != -1)) {
            ent_edgeP.push({
              source: pId,
              target: cId,
              type:type
            })
            if (ent_nodeP.find(function (d) { return d['id'] == pId }) == undefined) {
              ent_nodeP.push({ "id": pId, "type": "problem" })
            }
            if (ent_nodeC.find(function (d) { return d['id'] == pId }) == undefined) {
              ent_nodeC.push({ "id": pId, "type": "problem" })
            }
            if (ent_nodeP.find(function (d) { return d['id'] == cId }) == undefined) {
              ent_nodeP.push({ "id": cId, "type": "concept" })
            }

          }
        }
      }
      if(proId!=''){
        Object.keys(addEgList).forEach(e=>{
          let preId = proId
          addEgList[e].forEach(sId=>{
            addEgList[e].forEach(tId=>{
                {ent_edgeP.push({
                  source: sId,
                  target: tId,
                  type:"3"
                })}
                // preId = sId
            })
          })
      })}
      
      console.log(ent_edgeP);

      let svgWidth = width;
      let svgHeight = height;

      var forceSimulationP = d3.forceSimulation()
        .force("link", d3.forceLink().id((d) => { return d.id }))
        .force("charge", d3.forceManyBody().strength(parseInt(-ent_nodeP.length-ent_edgeP.length*1.2) * 1.5))
        .force("center", d3.forceCenter(svgWidth / 2, svgHeight / 2));
      forceSimulationP.nodes(ent_nodeP)
        .on("tick");

      let disLinear = d3.scaleLinear().domain([0, 200]).range([svgWidth / 18, svgWidth / 50]);
      forceSimulationP.force("link")
        .links(ent_edgeP)
        .distance(disLinear(ent_nodeP.length+ent_edgeP.length));

      // var forceSimulationC = d3.forceSimulation()
      //   .force("link", d3.forceLink().id((d) => { return d.id }))
      //   .force("charge", d3.forceManyBody().strength(parseInt(-ent_nodeC.length)))
      //   .force("center", d3.forceCenter(svgWidth / 2, svgHeight / 2));
      // forceSimulationC.nodes(ent_nodeC)
      //   .on("tick");
      // forceSimulationC.force("link")
      //   .links(ent_edgeC)
      //   .distance(svgWidth/4);

      let rSize = 10;
      const drags = () => {

        function dragstarted(event, d) {
          if (!event.active) forceSimulationP.alphaTarget(0.3).restart();
          d.fx = d.x;
          d.fy = d.y;
        }
        function dragged(event, d) {
          d.fx = event.x;
          d.fy = event.y;
          d.rx = event.x;
          d.ry = event.y;
        }

        function dragended(event, d) {
          if (!event.active) forceSimulationP.alphaTarget(0);
          d.fx = null;
          d.fy = null;
          d.rx = event.x;
          d.ry = event.y;
        }
        return d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended);
      }

      var circle = frontG.selectAll('circle')
        .data(ent_nodeP)
        .enter()
        .append("circle")
        .attr("id", function (d) { return d.id })
        .attr("class", function (d) { return d.type })
        .attr("cx", function (d) {
          if (d.type == "problem")
            _this.drawEntityProblem(entG, d.x, d.y, `astPro_${d.id}`);
          else if (d.type == "concept")
            _this.drawEntityConcept(entG, d.x, d.y, `astCon_${d.id}`);
          return d.x;
        })
        .attr("cy", function (d) { return d.y })
        .attr("r", 5)
        .attr("opacity", "0")
        .call(drags())
        .on("click",function(d){
          let ts = d3.select(this);
          let id = ts.attr("id");
          let clasN = ts.attr("class");
          let nametext = '';
          let ent ='';
          if(clasN == 'concept'){
            console.log(id,conceptsData)
            ent = conceptsData.find(function(c){return c['id'] == id});
            nametext = ent.name;
          }
          if(clasN == 'problem'){
            console.log(id,problemsData)
            ent = problemsData.find(function(c){return c['id'] == id});
            nametext = ent.title;
          }
        })
        .on("mousemove",function(d){
          let ts = d3.select(this);
          let id = ts.attr("id");
          let clasN = ts.attr("class");
          let nametext = '';
          let ent ='';
          let attr = ['scoringRate', 'totalAttempts', 'acceptedRate', 'proCount'];
          let attrN = ['Scoring Rate', 'Attempts', 'Pass Rate', 'Rel Count'];
          if(clasN == 'concept'){
            
            _this.$bus.$emit("SelectingCon", id);

            ent = conceptsData.find(function(c){return c['id'] == id});
            nametext = ent.name;

          attr = ['scoringRate', 'totalAttempts', 'acceptedRate', 'proCount'];
          attrN = ['Scoring Rate', 'Attempts', 'Pass Rate', 'Problems'];
          }
          if(clasN == 'problem'){
            
            _this.$bus.$emit("SelectingPro", id);

            ent = problemsData.find(function(c){return c['id'] == id});
            nametext = ent.title
            attr = ['scoringRate', 'totalAttempts', 'acceptedRate', 'conCount'];
            attrN = ['Scoring Rate', 'Attempts', 'Pass Rate', 'Concepts'];
          }

          var yPosition = d.clientY + 20;
          var xPosition = d.clientX + 20;
          if(d.clientX>2100){
            xPosition = d.clientX - 210;
          }
          if(d.clientY>1000){
            yPosition = d.clientY + 100;
          }
          var netTooltip = d3
            .select(".netTooltip")
            .style("left", xPosition + "px")
            .style("top", yPosition + "px");
          for (let a = 0; a < attr.length; a++) {

            netTooltip.select(`.attr${a}`).text(`${attrN[a]} : ${ent[attr[a]]}`)
            if(attrN[a] == 'Pass Rate')
              netTooltip.select(`.attr${a}`).text(`${attrN[a]} : ${ent[attr[a]].toFixed(2)}`)
            if(attrN[a] == 'Scoring Rate')
              netTooltip.select(`.attr${a}`).text(`${attrN[a]} : ${ent[attr[a]].toFixed(2)}`)
          }
          // 更新浮层内容
          netTooltip.select(".name").text(clasN);
          netTooltip.select(".text").text(nametext);
          // 移除浮层hidden样式，展示浮层
          netTooltip.classed("hidden", false);
        })
        .on("mouseleave", function (d) {
          
            _this.$bus.$emit("SelectingCon", '');
            _this.$bus.$emit("SelectingPro", '');

          d3.select(".netTooltip").classed("hidden", true);
        })
      // .call(drags());

      var path = relG.selectAll('.path')
        .data(ent_edgeP)
        .enter()
        .append('path')
        .attr("class", function (d) { return `"net_${d.type}-s-${d.source.id}-t-${d.target.id}` })
        .attr('d', function (d) {
          let eSource = d.source
          let eTarget = d.target
          let eSourceId = eSource['id']
          let eTargetId = eTarget['id']
          let startA = [eSource.x, eSource.y]
          let endA = [eTarget.x, eTarget.y]
          let path = d3.path()
          path.moveTo(startA[0], startA[1])
          path.quadraticCurveTo(startA[0], startA[1], endA[0], endA[1]);
          return path.toString()
        })
        .style('stroke',function(d){
          if(d.type == 1){
            return 'blue';
          }
          return "grey";
        })
        .style("stroke-opacity", "0.3")
        .style('stroke-width', function(d){
          if((d.source['id'] == proId)||(d.target['id'] == proId)){
            return 4;
          }
          return 2;
        })

      forceSimulationP.on("tick", () => {
        circle.attr("cx", (d) => {
          if(d.rx!=undefined){
            d.x = d.rx;
            d.y = d.ry;
          }
          let esx = d.x;
          let esy = d.y;
          if (esx < rSize) esx = rSize;
          esx = esx > svgWidth - rSize ? svgWidth - rSize : esx;
          if (esy < rSize) esy = rSize;
          esy = esy > svgHeight - rSize ? svgHeight - rSize : esy;
          if (d.id == proId) {
            esx = width / 2;
            esy = height / 2;
            d.x = esx;
            d.y = esy;
            _this.updateEntity(entG, esx, esy, `astPro_${d.id}`)
          }
          else if (d.type == "problem") {
            _this.updateEntity(entG, esx, esy, `astPro_${d.id}`)
          }
          //   _this.drawEntityProblem(entG, esx, esy, `entPro_${d.id}`);
          else if (d.type == "concept") {
            _this.updateEntity(entG, esx, esy, `astCon_${d.id}`)
          }
          // _this.updateEntity(entG,esx,esy,`astCon_${d.id}`)

          if (d.x < rSize) return rSize;
          return d.x > svgWidth - rSize ? svgWidth - rSize : d.x
        })
          .attr("cy", (d) => {
            if (d.y < rSize) return rSize
            return d.y > svgHeight - rSize ? svgHeight - rSize : d.y
          });

        let width_linear = d3.scaleLinear().domain([0, 1]).range([0, 10]);

        let lineColor_linear = d3.scaleLinear().domain([0, 1]).range([0, 1]);
        let lineCompute_color = d3.interpolate("white", "rgb(247, 54, 104)");
        ent_nodeP.forEach(n => {
          if (n['type'] == "problem") {
            let sourceId = n['id'];
            ent_nodeP.forEach(en => {
              if (en['type'] == "problem") {
                let targetId = en['id'];
                if ((netData[`${sourceId}_${targetId}`] != undefined) && (netData[`${sourceId}_${targetId}`] > 0.1)) {
                  d3.select(`.pros_${sourceId}_prot_${targetId}`).remove();
                  relG.append('path')
                    .attr("class", function (d) { return `pros_${sourceId}_prot_${targetId}` })
                    .attr('d', function (d) {
                      let startA = [n.x, n.y]
                      let endA = [en.x, en.y]
                      let path = d3.path();
                      path.moveTo(startA[0], startA[1]);
                      let conP = _this.getControlPoints(startA, endA);
                      // path.quadraticCurveTo(conP[0], conP[1], endA[0], endA[1]);
                      path.quadraticCurveTo(endA[0], endA[1], endA[0], endA[1]);
                      return path.toString()
                    })
                    .style('stroke', lineCompute_color(lineColor_linear(netData[`${sourceId}_${targetId}`])))
                    .style('fill', "none")
                    .style("stroke-opacity", "0.3")
                    .style('stroke-width', 3)
                }
              }
            })
          }
        })

        path.attr("d", (d) => {
          // if (!((d.source.type == 'problem') && (d.target.type == 'problem'))) 
          if (!(d.type==3)) 
          {
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
          }
        })

      });

    },

    drawProConNet1(svg) {
      const _this = this;
      let psvg = svg
      let width = psvg.attr("width");
      let height = psvg.attr("height");
      psvg.select("#netPG").remove();
      // let prog = psvg.append("g").attr("id", "netPG").attr("width", width).attr("height", height);
      let groups = svg.append("g").attr("id", "netGroups").attr("width", width).attr("height", height)
      // .attr("transform", "translate(" + graphGTransformX + ',' + graphGTransformY + ") scale(" + graphGTransformK + ")");
      // this.groupsSvg = groups;

      let backG = groups.append("g").attr("id", "proRbackG").attr("width", width).attr("height", height);
      let arcG = groups.append("g").attr("id", "proRarcG").attr("width", width).attr("height", height);
      let relG = groups.append("g").attr("id", "proRrelG").attr("width", width).attr("height", height);
      let entG = groups.append("g").attr("id", "proRentG").attr("width", width).attr("height", height);
      let frontG = groups.append("g").attr("id", "proRfrontG").attr("width", width).attr("height", height);

      let proData = _this.problemsData;
      let netData = _this.netData;
      let problemConceptData = _this.problemConceptData;
      let proRel = tools.deepClone(_this.problemRelByConcept);
      let proInList = tools.deepClone(_this.problemListByConcept);
      let ent_node = [];
      let ent_edge = [];

      let proId = _this.curEntId;
      if (proId == "") { return; }
      _this.drawEntityProblem(entG, width / 2, height / 2, `netEntPro_${proId}`);
    },
    drawEntityProblem(svg, x, y, pId) {
      const _this = this;
      d3.select("#" + pId).remove();
      let entG = svg.append("g").attr("id", pId);
      entG.attr("transform", `translate(${x},${y})`);
      let EntProData = tools.deepClone(_this.selectedPro);
      let idn = pId.split("_")[1];

      let curEnt = EntProData.find(function (p) { return p['id'] == idn; })

      // let rSize = 10;//rSize_linear(curEnt['conCount']);

      // let points = _this.calcRegularPolygonPoints(3, 0, 0, rSize);
      // let r = 20; let g = 190; let b = 200;
      // _this.drawPolygon(entG, points, `astpro_${idn}`, '1px', `rgb(${r},${g},${b})`, `rgba(${r},${g},${b},1)`);

      let attrList = _this.proAttrList;

      let attrLen = attrList.length;

      let proAttrMaxMinList = _this.proAttrMaxMinList;
      let proMaxMinDR = proAttrMaxMinList[3];
      let proMaxMinDC = proAttrMaxMinList[0];

      let currentMaxColor = _this.entProMaxColor;
      let currentMinColor = _this.entProMinColor;

      let importanceColor_linear = d3.scaleLinear().domain([proMaxMinDC[1], proMaxMinDC[0]]).range([0, 1]);
      let importanceCompute_color = d3.interpolate(currentMinColor, currentMaxColor);

      let rSize_linear = d3.scaleLinear().domain([proMaxMinDR[1], proMaxMinDR[0]]).range([10, 20]);


      let rSize = rSize_linear(curEnt['conCount']);
      if (idn == _this.curEntId) { rSize += 20 }
      let points = _this.calcRegularPolygonPoints(attrLen-1, 0, 0, rSize);
      let pointsB = _this.calcRegularPolygonPoints(attrLen-1, 0, 0, rSize+15);
      let entColor = importanceCompute_color(importanceColor_linear(curEnt['scoringRate']));

      let entPolygonB = _this.drawPolygon(entG, pointsB, `pro_${idn}`, '0px', "rgb(230,230,230)", "rgb(230,230,230)");
      let entPolygon = _this.drawPolygon(entG, points, `pro_${idn}`, '0px', entColor, entColor);

      entPolygon.on("mouseover", function (d) {
      })
      // let pointsList = [];
      // const pathAxis = d3.path();
      // pathAxis.moveTo(0, 0);
      // for (let i = 0; i < points.length; i++) {
      //   pathAxis.lineTo(points[i][0], points[i][1]);
      //   pathAxis.moveTo(0, 0);
      //   pathAxis.lineTo(points[i][0], points[i][1]);
      // }
      // pathAxis.lineTo(points[0][0], points[0][1]);
      // let rgbValue = tools.getRgbValue(entColor);
      // let r = parseInt(rgbValue[0]) * 0.2;
      // let g = parseInt(rgbValue[1]) * 0.4;
      // let b = parseInt(rgbValue[2]) * 0.7;
      // _this.drawPathLine(entG, pathAxis, `rgb(${r},${g},${b})`, 0.2, "10,3", `proAxis_${idn}`, "");
      // -------------------------
      // const path = d3.path();
      // let startP = _this.calcattrPoint(attrLen, 0, proAttrMaxMinList[0], curEnt[attrList[0]], 0, 0, rSize)
      // path.moveTo(startP[0], startP[1]);
      // pointsList.push(startP)
      // let startP2 = _this.calcattrPoint(attrLen, 1, proAttrMaxMinList[1], curEnt[attrList[1]], 0, 0, rSize)
      // path.bezierCurveTo(startP2[0], startP2[1], startP2[0], startP2[1], startP2[0], startP2[1]);
      // pointsList.push(startP2)
      // for (let i = 2; i < attrLen; i++) {
      //   let curP = _this.calcattrPoint(attrLen, i, proAttrMaxMinList[i], curEnt[attrList[i]], 0, 0, rSize)
      //   // path.lineTo(curP[0],curP[1]);
      //   pointsList.push(curP);
      //   path.bezierCurveTo(curP[0], curP[1], curP[0], curP[1], curP[0], curP[1])
      // }
      // path.bezierCurveTo(startP[0], startP[1], startP[0], startP[1], startP[0], startP[1])

      // pointsList.push(startP)
      // path.bezierCurveTo(startP2[0], startP2[1], startP2[0], startP2[1], startP2[0], startP2[1])
      // pointsList.push(startP2)
      // ----------------
      let StartR = 0//Math.PI/4;
      let StepInterR = Math.PI * 2 / 30;
      let StepR = (Math.PI * 2 - StepInterR * attrLen) / (attrLen-1);
      let perR = Math.PI*2/(attrLen-1);
      for (let i = 1; i < attrLen; i++) {
        let h = _this.calcRsize(proAttrMaxMinList[i], curEnt[attrList[i]],StepR);
        var datasetB = { startAngle: StartR + (i-1) * (StepR + StepInterR) + StepInterR, endAngle: StartR + (i) * (StepR + StepInterR) }; //创建一个弧生成器
        var dataset = { startAngle: StartR + (i-1) * (StepR + StepInterR) + StepInterR, endAngle: StartR + (i-1) * (StepR + StepInterR) +h }; //创建一个弧生成器
        var arcPath = d3.arc()
          .innerRadius(rSize)
          .outerRadius(rSize+10);
        var arcPathBack = d3.arc()
          .innerRadius(1)
          .outerRadius(h + 2);
        var pathArc = arcPath(dataset);
        var pathArcB = arcPath(datasetB);
        let entColor = _this.attrColorList[i];//importanceCompute_color(importanceColor_linear(curEnt['scoringRate']));
        // _this.drawArc(entG, 0, 0, pathArcB, "rgb(230, 230, 230)", "rgb(230, 230, 230)", 'typeB', 0, 0);
        // _this.drawArc(entG, 0, 0, pathArc, entColor, entColor, 'type', 0, 0);
      }

      for (let i = 1; i < attrLen; i++) {
        let points = [];
        let interNP = _this.calcattrPoint(attrLen-1, i-1, [0,1], 1, 0, 0, rSize+20);
        let outerNP = _this.calcattrPoint(attrLen-1, i-1, [0,1], 1, 0, 0, rSize+40);

        let interP = _this.calcattrPoint(attrLen-1, i, [0,1], 1, 0, 0, rSize+15);
        let outerP = _this.calcattrPoint(attrLen-1, i, [0,1], 1, 0, 0, rSize+30);

        let cinpx = _this.calclin([0,proAttrMaxMinList[i][0]], [interNP[0],interP[0]],curEnt[attrList[i]]);
        let cinpy = _this.calclin([0,proAttrMaxMinList[i][0]],[interNP[1],interP[1]], curEnt[attrList[i]]);

        let cotpx = _this.calclin([0,proAttrMaxMinList[i][0]],[outerNP[0],outerP[0]], curEnt[attrList[i]]);
        let cotpy = _this.calclin([0,proAttrMaxMinList[i][0]],[outerNP[1],outerP[1]], curEnt[attrList[i]]);

        let curP = _this.calcattrPoint(attrLen, i, proAttrMaxMinList[i], curEnt[attrList[i]], 0, 0, rSize)
        // path.lineTo(curP[0],curP[1]);
        points.push(interNP);
        points.push(outerNP);
        points.push([cotpx,cotpy]);
        points.push([cinpx,cinpy]);
        // if (i != attrLen - 1) {

        //   points.push(_this.calcattrPoint(attrLen, i + 1, proAttrMaxMinList[i], curEnt[attrList[i]], 0, 0, rSize));
        // }
        // else {
        //   points.push(_this.calcattrPoint(attrLen, 0, proAttrMaxMinList[i], curEnt[attrList[i]], 0, 0, rSize));
        // }
        // points.push([0, 0])
        let colorn = _this.attrColorList[i];
        _this.drawPolygon(entG, points, `proAttr_${idn}_${i}`, '1px', colorn, colorn);
      }
      let curve_generator = d3.line()
        .x((d) => d[0])
        .y((d) => {
          return d[1];
        })
        .curve(d3.curveCatmullRom)
      // .curve(d3.curveBundle)
      // _this.drawPolygon(entG, pointsList, `proAttr_${idn}`, '1px', `rgb(${r},${g},${b})`, `rgba(${r},${g},${b},0.3)`);
      // .attr("opacity","0.3")
      // _this.drawPathLine(entG, curve_generator(pointsList), "rgb(200,200,200)", 2, "0", "", "");

    },
    getControlPoints(startP, endP) {
      let conP = [];
      // return [(startP[0]+endP[0])/2,(startP[1]+endP[1])/2]
      return [(startP[0]), (endP[1])]
    },
    calcRegularPolygonPoints(num, x, y, r) {
      let arcStep = Math.PI * 2 / num;
      let points = [];
      for (let i = 0; i < num; i++) {
        points.push([x - Math.sin(arcStep * i) * r, y + Math.cos(arcStep * i) * r])
      }
      return points
    },
    calclin(domin,toDomin, value) {
      let point_linear = d3.scaleLinear().domain([domin[0], domin[1]]).range([toDomin[0], toDomin[1]]);
      let rarc = point_linear(value);
      return rarc;
    },

    calcRsize(domin, value, r) {
      let point_linear = d3.scaleLinear().domain([0, domin[0]]).range([0, r]);
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

      let conAttrMaxMinList = _this.conAttrMaxMinList;
      let conMaxMinDR = conAttrMaxMinList[3];
      let conMaxMinDC = conAttrMaxMinList[0];

      let currentMaxColor = _this.entConMaxColor;
      let currentMinColor = _this.entConMinColor;

      let Color_linear = d3.scaleLinear().domain([0, 1]).range([0, 1]);
      let Compute_color = d3.interpolate("white", currentMaxColor);

      let rSize_linear = d3.scaleLinear().domain([0, conMaxMinDR[0]]).range([5, 10]);

      let rSize = rSize_linear(curEnt['proCount']);
      // let points = _this.calcRegularPolygonPoints(10, 0, 0, rSize);
      let colorr = Compute_color(curEnt['scoringRate']);
      
      _this.drawCircle(entG, 0, 0, rSize, colorr, 1, "none", "1", `astcon_${idn}`, `astcon`);


      let StartR = 0//Math.PI/4;
      let StepInterR = Math.PI * 2 / 30;

      let StepR = (Math.PI * 2 - StepInterR * attrLen) / (attrLen-1);
      // --------------------------
      // for (let i = 0; i < attrLen; i++) {
      //   let curP = _this.calcattrPoint(attrLen, i, conAttrMaxMinList[i], curEnt[attrList[i]], 0, 0, rSize);
      //   let h = _this.calcRsize(conAttrMaxMinList[i], curEnt[attrList[i]], rSize)
      //   var dataset = { startAngle: StartR + i * (StepR + StepInterR) + StepInterR, endAngle: StartR + (i + 1) * (StepR + StepInterR) }; //创建一个弧生成器
      //   var arcPath = d3.arc()
      //     .innerRadius(1)
      //     .outerRadius(h);
      //   var arcPathBack = d3.arc()
      //     .innerRadius(1)
      //     .outerRadius(h + 2);
      //   var pathArc = arcPath(dataset);
      //   let entColor = _this.attrColorList[i];//importanceCompute_color(importanceColor_linear(curEnt['scoringRate']));
      //   _this.drawArc(entG, 0, 0, pathArc, entColor, entColor, 'type', 0, 3);
      // }
      // ---------------------------
      
      let perR = Math.PI*2/(attrLen-1);
      for (let i = 1; i < attrLen; i++) {
        let h = _this.calcRsize(conAttrMaxMinList[i], curEnt[attrList[i]],StepR);
        var datasetB = { startAngle: StartR + (i-1) * (StepR + StepInterR) + StepInterR, endAngle: StartR + (i) * (StepR + StepInterR) }; //创建一个弧生成器
        
        var dataset = { startAngle: StartR + (i-1) * (StepR + StepInterR) + StepInterR, endAngle: StartR + (i-1) * (StepR + StepInterR) +h }; //创建一个弧生成器
        var arcPath = d3.arc()
          .innerRadius(rSize)
          .outerRadius(rSize+10);
        var arcPathBack = d3.arc()
          .innerRadius(1)
          .outerRadius(h + 2);
        var pathArc = arcPath(dataset);
        var pathArcB = arcPath(datasetB);
        let entColor = _this.attrColorList[i];//importanceCompute_color(importanceColor_linear(curEnt['scoringRate']));
        _this.drawArc(entG, 0, 0, pathArcB, "rgb(230, 230, 230)", "rgb(230, 230, 230)", 'typeB', 0, 0);
        _this.drawArc(entG, 0, 0, pathArc, entColor, entColor, 'type', 0, 0);
      }


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
    getProRelO() {
      const _this = this;
      let conceptsData = _this.conceptsData;
      let problemsData = _this.problemsData;
      let problemConceptData = _this.problemConceptData;
      let selectedPro = _this.selectedPro;
      let proRel = {};
      let proLis = {}
      for (let p = 0; p < problemsData.length; p++) {
        let pId = problemsData[p]['id'];
        let proList = [];
        let conList = [];
        for (let c = 0; c < problemConceptData.length; c++) {
          let curPId = problemConceptData[c]['problem'];
          let curCId = problemConceptData[c]['conceptId'];
          if (curPId == pId) {
            conList.push(curCId);
          }
        }
        for (let r = 0; r < conList.length; r++) {
          let cId = conList[r];
          for (let c = 0; c < problemConceptData.length; c++) {
            let curPId = problemConceptData[c]['problem'];
            let curCId = problemConceptData[c]['conceptId'];
            if (curCId == cId) {
              proList.push(curPId);
            }
          }
        }
        proLis[pId] = proList;
        proRel[pId] = conList;
      }
      // for(let c = 0; c<conceptsData.length;c++){
      //   let conceptId = conceptsData[c]['id'];
      //   let proList = []
      //   problemConceptData.forEach(r=>{
      //     let curCId = r['conceptId']
      //     if(curCId == conceptId){
      //       proList.push(r['problem']);
      //     }
      //   })
      //   let listTemp = tools.deepClone(proList);
      //   console.log(conceptId,conceptsData[c]['concept_name'],proList)
      //   for(let p = 0; p<proList.length;p++){
      //     proLis[proList[p]] = listTemp;
      //   }
      // }
      // let proId = _this.curEntId;
      // for (let r = 0; r < ProRel.length; r++) {
      //   let curRel = ProRel[r];
      //   let s = curRel['source'];
      //   let t = curRel['target'];
      //   if((s == proId)||(t==proId)){
      //       if (proLis.find(function (d) { return d['id'] == s }) == undefined) {
      //           proLis.push({"id":s});
      //       }
      //       if (proLis.find(function (d) { return d['id'] == s }) == undefined) {
      //           proLis.push({"id":t});
      //       }
      // }
      // }
      _this.problemRelByConcept = proRel;
      _this.problemListByConcept = proLis;
    },
    getProRelO1() {
      const _this = this;
      let conceptsData = _this.conceptsData;
      let problemsData = _this.problemsData;
      let problemConceptData = _this.problemConceptData;
      let selectedPro = _this.selectedPro;
      let proRel = {};
      let proLis = []
      for (let p = 0; p < selectedPro.length; p++) {
        let pId = selectedPro[p]['id'];
        proLis.push(pId);
      }
      console.log(proLis)
      _this.problemRelByConcept = proRel;
      _this.problemListByConcept = proLis;
    },
    getProRel() {
      const _this = this;
      let conceptsData = _this.conceptsData;
      let problemsData = _this.problemsData;
      let problemConceptData = _this.problemConceptData;
      let selectedPro = _this.selectedPro;
      let proRel =[[],[]];
      let proLis = []
      for (let p = 0; p < selectedPro.length; p++) {
        let pId = selectedPro[p]['id'];
        proLis.push(pId);
      }
      let pId = _this.curEntId;
      for (let c = 0; c < problemConceptData.length; c++) {
        let curPId = problemConceptData[c]['problem'];
        let curCId = problemConceptData[c]['conceptId'];
        let type = problemConceptData[c]['type'];
        
        if (curPId == pId) {
          proRel[type].push(curCId);
        }
      }
      _this.problemRelByConcept = proRel;
      _this.problemListByConcept = proLis;
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
    drawFigureAnnotation(svg) {
      const _this = this;
      let frontG = svg;

      let stuMaxColor = _this.stuMaxColor;
      let stuMinColor = _this.stuMinColor;

      let len = 6;

      let Color_linear = d3.scaleLinear().domain([0, len]).range([0, 1]);
      let Rsize_linear = d3.scaleLinear().domain([0, len]).range([1, 6]);
      let Compute_color = d3.interpolate(stuMinColor, stuMaxColor);

      let textsr = _this.drawTxt(frontG, 16, 15, "AcceptedRate", "black", 10, `FigNet_con`);
      let textat = _this.drawTxt(frontG, 16, 35, "Attempts", "black", 10, `FigNet_con`);
      let textbs = _this.drawTxt(frontG, 16, 55, "Connection nums", "black", 10, `FigNet_con`);

      let texttm = _this.drawTxt(frontG, 136, 15, "Concepts", "black", 10, `FigNet_con`);
      let textgn = _this.drawTxt(frontG, 136, 35, "problems", "black", 10, `FigNet_con`);
      let prex = 0;
      let prerx = 0;
      let colorar = _this.attrColorList[0];
      let colorat = _this.attrColorList[1];
      let colorcn = _this.attrColorList[2];

      let colortm = _this.entProMaxColor;
      let colorgn = _this.entConMaxColor;

      _this.drawRect(frontG, 1, 2, 10, 15, 0, "rgb(230,230,230)", "1", "grey", "1", `FigNet_conRectColoraB`, 'FigNet');
      _this.drawRect(frontG, 1, 5, 10, 12, 0, colorar, "1", "grey", "1", `FigNet_conRectColora`, 'FigNet');

      _this.drawRect(frontG, 1, 22, 10, 15, 0, "rgb(230,230,230)", "1", "grey", "1", `FigNet_conRectColorB`, 'FigNet');
      _this.drawRect(frontG, 1, 25, 10, 12, 0, colorat, "1", "grey", "1", `FigNet_conRectColor`, 'FigNet');

      _this.drawRect(frontG, 1, 42, 10, 15, 0, "rgb(230,230,230)", "1", "grey", "1", `FigNet_conRectB`, 'FigNet');
      _this.drawRect(frontG, 1, 45, 10, 12, 0, colorcn, "1", "grey", "1", `FigNet_conRect`, 'FigNet');

      _this.drawCircle(frontG, 120, 12, 7, colorgn, 1, "grey", "1", 'FigNet', `FigNet_conColorc`);

      let points = _this.calcRegularPolygonPoints(3, 120, 31, 9);

      let entPolygon = _this.drawPolygon(frontG, points, `FigNet_Proc`, '1px', "grey", colortm);

      let path1 = d3.path();
      // let points0 = [[10, 20], [10, 24], [14, 20], [10, 24], [14, 28], [10, 24], [10, 28], [10, 24], [40, 24], [40, 24], [36, 20], [40, 24], [36, 28], [40, 24], [40, 20], [40, 28]]
      // let points1 = [[10, 50], [10, 54], [14, 50], [10, 54], [14, 58], [10, 54], [10, 58], [10, 54], [40, 54], [40, 54], [36, 50], [40, 54], [36, 58], [40, 54], [40, 50], [40, 58]]
      // let points2 = [[10, 80], [10, 84], [14, 80], [10, 84], [14, 88], [10, 84], [10, 88], [10, 84], [40, 84], [40, 84], [36, 80], [40, 84], [36, 88], [40, 84], [40, 80], [40, 88]]
      let curve_generator = d3.line()
        .x((d) => d[0])
        .y((d) => d[1])
      // .curve(d3.curveBasisClosed)
      // _this.drawLine(frontG, curve_generator(points0), "black", 1, '0', '1', `lineat`, 'FigNet_line1', "rgb(230,230,230)");
      // _this.drawLine(frontG, curve_generator(points1), "black", 1, '0', '1', `line2`, 'FigNet_line1', "rgb(230,230,230)");
      // _this.drawLine(frontG, curve_generator(points2), "black", 1, '0', '1', `line3`, 'FigNet_line1', "rgb(230,230,230)");
      for (let i = 0; i < len * 3; i++) {
      }
      for (let i = 0; i < len; i++) {
        // let color = Compute_color(Color_linear(i));
        // let circle = _this.drawCircle(frontG, 15 + prex, 23, Rsize_linear(i), color, 1, "red", "1", 'FigNet', `FigNet_conColor${i}`);
        // prex += Rsize_linear(i) * 2 + 4;
        // prerx += i * 4 + 2;
      }

    },

    updata() {
      const _this = this;
      _this.getProRel();
      _this.drawnetPData();
      
    },
    click_Ent(time) {
      this.$emit("timeDur", time);
    },
  },
  created() {
    const _this = this;
    this.$nextTick(() => {
      // _this.calcNetData();
      _this.updata();
      d3.select(".netTooltip").classed("hidden", true);
      _this.drawnetPData();
    });
  },
  mounted() {
    const _this = this
    this.$bus.$on('Domin', (val) => {
      _this.proAttrList = val[0];
      _this.proAttrMaxMinList = val[1];
      _this.conAttrList = val[2];
      _this.conAttrMaxMinList = val[3];
    });

    this.$bus.$on('attrColorList', (val) => {
      _this.attrColorList = val;
    });
    // _this.tableData.find(function (d) { return d['key'] == 'name' })['value'] = 'Computer Network';
    this.$bus.$on('selectEntData', (val) => {
      _this.curEntId = val[0];
      _this.EntProData = val[1];
      _this.updata();
    });

    this.$bus.$on('selectedPro', (val) => {
      _this.selectedPro = val;
      _this.updata();

    });

    this.$bus.$on('selectCon', (val) => {
      _this.selectedCon = val;
      _this.updata();
    });

    this.$bus.$on('allProblem', (val) => {
      _this.problemsData = val;
    });
    this.$bus.$on('Submission', (val) => {
      _this.submissionsData = val;
    });
    this.$bus.$on('Student', (val) => {
      _this.studentsData = val;
    });
    this.$bus.$on('Pro_Con', (val) => {
      _this.problemConceptData = val;
    });
    this.$bus.$on('ConceptTree', (val) => {
      _this.conceptsData = val;
    });
    this.$bus.$on('netData', (val) => {
      _this.netData = val;
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
