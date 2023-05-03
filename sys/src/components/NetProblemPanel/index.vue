<!-- eslint-disable no-unused-vars -->
<!-- eslint-disable no-unused-vars -->

<template>
  <div class="netPPanel">
    <div class="panelHead"></div>
    <!-- //SupportPanel</div> -->
    <div id="netPPanelDiv" class="panelBody" ref="netPPanelDiv">
      <div id="topicLine" ref="topicLine"></div>
      <div id="netPData" ref="netPData"></div>
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
      problemsData: [],
      problemConceptData: [],
      problemRelByConcept: [],
      problemListByConcept: [],
      submissionsData: [],
      studentsData: [],
      conceptsData: [],
      netData: [],
      calcNetDataRady: 0,
      nameinput: "Fundamental Graphs",
      curEntId: "",
      insertEntId: "",
      insertSourceEntId: "-1",
      insertTargetEntId: "-1",
      sonList: [],


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
      let width = this.$refs.netPData.offsetWidth - margin.left - margin.right - 60;
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
      _this.drawQuestionSurface(entG);
    },
    drawQuestionSurface(svg) {
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

      let proData = _this.problemsData;
      let netData = _this.netData;
      let problemConceptData = _this.problemConceptData;
      let proRel = tools.deepClone(_this.problemRelByConcept);
      let proInList = tools.deepClone(_this.problemListByConcept);
      let ent_node = [];
      let ent_edge = [];

      let proId = _this.curEntId;
      if (proId == "") { return; }
      let proList = proInList[proId]
      for (let r = 0; r < problemConceptData.length; r++) {
        let curRel = problemConceptData[r];
        let pId = curRel['problem'];
        let cId = curRel['conceptId'];
        if (1) {
          if (proList.indexOf(pId) != -1) {
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
        }
      }
      // Object.keys(netData).forEach((r)=>{
      //   let s = r.split("_")[0];
      //   let t = r.split("_")[1];

      //   if((s == proId)||(t==proId)){
      //   ent_edge.push({
      //     source: s,
      //     target: t
      //   })
      //   if (ent_node.find(function (d) { return d['id'] == s }) == undefined) {
      //     ent_node.push({ "id": s,})
      //   }
      //   if (ent_node.find(function (d) { return d['id'] == t }) == undefined) {
      //     ent_node.push({ "id": t,})
      //   }
      // }
      // })
      // for (let r = 0; r < proRel.length; r++) {
      //   let curRel = proRel[r];
      //   let s = curRel['source'];
      //   let t = curRel['target'];
      //   if((s == proId)||(t==proId)){
      //     ent_edge.push(proRel[r])
      //     if (ent_node.find(function (d) { return d['id'] == s }) == undefined) {
      //       ent_node.push({ "id": s,})
      //     }
      //     if (ent_node.find(function (d) { return d['id'] == t }) == undefined) {
      //       ent_node.push({ "id": t,})
      //   }}
      // }
      var forceSimulation = d3.forceSimulation()
        .force("link", d3.forceLink().id((d) => { return d.id }))
        .force("charge", d3.forceManyBody().strength(-250))
        .force("center", d3.forceCenter(width / 2, height / 2));
      forceSimulation.nodes(ent_node)
        .on("tick");

      forceSimulation.force("link")
        .links(ent_edge)
        .distance(2);

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
            _this.drawEntityProblem(entG, d.x, d.y, `astPro_${d.id}`);
          else if (d.type == "concept")
            _this.drawEntityConcept(entG, d.x, d.y, `astCon_${d.id}`);
          return d.x;
        })
        .attr("cy", function (d) { return d.y })
        .attr("r", 5)
        .attr("opacity", "0")
        .call(drags());

      var path = relG.selectAll('.path')
        .data(ent_edge)
        .enter()
        .append('path')
        .attr("class", function (d) { return "s-" + d.source.id + "-t-" + d.target.id })
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
            _this.updateEntity(entG, esx, esy, `astPro_${d.id}`)
          //   _this.drawEntityProblem(entG, esx, esy, `entPro_${d.id}`);
          else if (d.type == "concept")
            _this.updateEntity(entG, esx, esy, `astCon_${d.id}`)
            // _this.updateEntity(entG,esx,esy,`astCon_${d.id}`)

            if (d.x < rSize) return rSize;
          return d.x > svgWidth - rSize ? svgWidth - rSize : d.x
        })
          .attr("cy", (d) => {
            if (d.y < rSize) return rSize
            return d.y > svgHeight - rSize ? svgHeight - rSize : d.y
          });

        let width_linear = d3.scaleLinear().domain([0, 1]).range([0, 10]);

        ent_node.forEach(n => {
          if (n['type'] == "problem") {
            let sourceId = n['id']; 
            ent_node.forEach(en => {
              if (en['type'] == "problem") {
                let targetId = en['id'];
                if (netData[`${sourceId}_${targetId}`] != undefined) {
                  d3.select(`.pros_${sourceId}_prot_${targetId}`).remove()
                  relG.append('path')
                    .attr("class", function (d) { return `pros_${sourceId}_prot_${targetId}` })
                    .attr('d', function (d) {
                      let startA = [n.x, n.y]
                      let endA = [en.x, en.y]
                      let path = d3.path();
                      path.moveTo(startA[0], startA[1]);
                      let conP = _this.getControlPoints(startA,endA);
                      path.quadraticCurveTo(conP[0], conP[1], endA[0], endA[1]);
                      return path.toString()
                    })
                    .style('stroke', "grey")
                    .style('fill', "none")
                    .style("stroke-opacity", "0.3")
                    .style('stroke-width', width_linear(netData[`${sourceId}_${targetId}`]))
                }
              }
            })
          }
        })

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

      let rSize = 10;//rSize_linear(curEnt['conCount']);

      let points = _this.calcRegularPolygonPoints(3, 0, 0, rSize);
      let r = 20; let g = 190; let b = 200;
      _this.drawPolygon(entG, points, `astpro_${idn}`, '1px', `rgb(${r},${g},${b})`, `rgba(${r},${g},${b},1)`);

    },
    getControlPoints(startP,endP){
      let conP = [];
      // return [(startP[0]+endP[0])/2,(startP[1]+endP[1])/2]
      return [(startP[0]),(endP[1])]
    },
    calcRegularPolygonPoints(num, x, y, r) {
      let arcStep = Math.PI * 2 / num;
      let points = [];
      for (let i = 0; i < num; i++) {
        points.push([x - Math.sin(arcStep * i) * r, y + Math.cos(arcStep * i) * r])
      }
      return points
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
      let rSize = 10;//rSize_linear(curEnt['conCount']);

      let points = _this.calcRegularPolygonPoints(10, 0, 0, rSize);
      let r = 120; let g = 190; let b = 200;
      _this.drawPolygon(entG, points, `astcon_${idn}`, '1px', `rgb(${r},${g},${b})`, `rgba(${r},${g},${b},1)`);



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
    getProRel() {
      const _this = this;
      let conceptsData = _this.conceptsData;
      let problemsData = _this.problemsData;
      let problemConceptData = _this.problemConceptData;
      let ProRel = [];
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
      console.log(proLis)
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
      _this.problemRelByConcept = ProRel;
      _this.problemListByConcept = proLis;
    },
    updata() {
      const _this = this;

      _this.getProRel();
      // _this.calcNetData();
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
      // _this.updata();

    });
  },
  mounted() {
    const _this = this
    // _this.tableData.find(function (d) { return d['key'] == 'name' })['value'] = 'Computer Network';
    this.$bus.$on('selectEnt', (val) => {
      _this.curEntId = val;
      console.log(val)
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
