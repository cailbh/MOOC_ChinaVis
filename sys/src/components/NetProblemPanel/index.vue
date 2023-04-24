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
      problemsData:[],
      submissionsData:[],
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
    drawQuestionSurface(svg){
      const _this = this;
      let psvg =svg
      let w = psvg.attr("width");
      let h = psvg.attr("height");
      psvg.select("#netPG").remove();
      let prog = psvg.append("g").attr("id", "netPG").attr("width", w).attr("height", h);
      let proData = _this.problemsData;
      let proId = _this.curEntId;
      if(proId == ""){return;}
      let curPro = proData.find(function(p){return (p['id']).toString() == (proId).toString()})
      let title = curPro['title'];
      let tx=10;
      let ty = 20;
      // ty = _this.drawTxt(prog,tx,ty,w,`Title:${title}`,"black",22,'title');
      let content = curPro['content'];

      _this.tableData.find(function(t){return t['key'] == 'Title'})['value'] = title;
      _this.tableData.find(function(t){return t['key'] == 'Content'})['value'] = content;
      console.log(_this.tableData)
      // _this.drawTxt(prog,tx,ty+25,w,`Title:${content}`,"black",16,'title');
    },
    calcNetData(){
      const _this = this;
      let problemData = _this.problemsData;
      let submissionsData  = _this.submissionsData;
      for(let i=0;i<problemData.length-1;i++){
        let problemIId=problemData[i]['id'];
        for(let j=0;j<problemData.length;j++){
          let problemJId=problemData[j]['id'];
        }
      }
    },
    updata() {
    const _this = this;
      _this.drawnetPData();
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
    });
    this.$bus.$on('Submission', (val) => {
      console.log(val)
     _this.submissionsData = val;
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
