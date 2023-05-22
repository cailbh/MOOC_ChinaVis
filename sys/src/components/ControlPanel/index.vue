<!-- eslint-disable no-unused-vars -->
<!-- eslint-disable no-unused-vars -->

<template>
  <div class="controlPanel">
    <div class="panelHead">Control View</div>
    <div id="controlPanelDiv" class="panelBody" ref="controlPanelDiv">
      <div id="upLoadVideo">
        <el-upload class="uploadVideoel" action="https://jsonplaceholder.typicode.com/posts/"
          :on-change="handleVideoChange" :file-list="fileVideoList">
          <el-button ref="videoBut" size="middle" type="primary">Upload</el-button>
        </el-upload>
      </div>
      <div id="baseInformation">
        <label class="T1">>Information</label>
        <el-button size="primary" type="primary" >Upload</el-button>
        <el-divider class="divider"></el-divider>
        <el-table stripe :data="tableData" style="width: 100%" height="250px"  
        :row-style="iRowStyle"
        :cell-style="iCellStyle"
        :header-row-style="iHeaderRowStyle"
        :header-cell-style="iHeaderCellStyle">
          <el-table-column prop="key" label="" width="321">

          </el-table-column>
          <el-table-column prop="value" label="" width="260">
            <template slot-scope="scope" style="float: left;font-size:10px">
              <div v-if="scope.row.key != 'Coursename'">
                <div style="text-align:center">
                  {{ scope.row.value }}</div>
   
              </div>
              <!-- <div :class="scope.row.name" :id="scope.row.name" :height="scope.row.value === '' ? '10' : '0'" disable-transitions>
                {{ scope.row.value }}
              </div> -->
            </template>
          </el-table-column>
        </el-table>

        <div id="iconUploadVideoel" @click="videoUpClk">
          <img class="iconUpload" :src="upLoadUrl">
        </div>
      </div>
      <div id = "controlLineChart" ref="controlLineDiv"></div>
      <div id="topicControl">
        <label class="T1">>Relationship</label>
        <!-- <el-button size="primary" type="primary" >Upload</el-button> -->
        <el-divider class="divider"></el-divider>
        <el-table :data="toolsData" style="width;: 100%"
        :row-style="icRowStyle"
        :cell-style="icCellStyle"
        :header-row-style="icHeaderRowStyle"
        :header-cell-style="icHeaderCellStyle">
          <el-table-column prop="key" label="" width="320">
          </el-table-column>
          <el-table-column prop="value" label="" width="360">
            <template slot-scope="scope">
              <div v-if="scope.row.key == 'Option :'" style='float: left;'>
                <el-radio-group size="mini" v-model="addRels">
                <el-radio-button label="Del"></el-radio-button>
                <el-radio-button label="Add"></el-radio-button>
                <el-radio-button label="Main"></el-radio-button>
                <el-radio-button label="None"></el-radio-button>
                </el-radio-group>
                <!-- <el-switch size="middle" v-model="switchL[1]" active-text="" inactive-text="1">
                </el-switch>
                <el-switch size="middle" v-model="switchL[2]" active-text="" inactive-text="2">
                </el-switch>
                <el-switch size="middle" v-model="switchL[3]" active-text="" inactive-text="3">
                </el-switch> -->
              </div>
              <div v-if="scope.row.key == 'Threshold :'" class="Level" style="float: left;" >
                <el-slider v-model="TopicCount" :step="1" :min="0" :max="10" style="width: 180px; margin-left:15px ;"></el-slider>
                <!-- <el-slider v-model="layoutSelect" :step="1" :min="0" :max="3" show-stops>
                </el-slider> -->
              </div>
              <div v-if="scope.row.key == 'Perplexity :'" class="Level" style="float: left;" >
                <el-slider v-model="TopicCount1" :step="1" :min="0" :max="10" style="width: 180px; margin-left:15px ;"></el-slider>
                <!-- <el-slider v-model="layoutSelect" :step="1" :min="0" :max="3" show-stops>
                </el-slider> -->
              </div>
              <!-- <el-tag :type="scope.row.value === '' ? 'primary' : 'success'" disable-transitions>{{ scope.row.tag -->
              <!-- // }}</el-tag> -->
              <!-- <div :class="scope.row.name" :height="scope.row.value === '' ? '10' : '0'" disable-transitions>
                {{ scope.row.value }}
              </div> -->
            </template>
          </el-table-column>
        </el-table>
        <!-- <el-table :data="topicControl" style="color:rgb(114, 114, 114);width;: 100%">
          <el-table-column prop="key" label="" width="340">

            <template slot-scope="scope">
              <div v-if="scope.row.key == 'Topic Count Control'">
                {{ scope.row.key }}
              </div>
              <div v-if="scope.row.key == 'count'" class="Level">
                node:&nbsp&nbsp&nbsp{{ nodeCount }}
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="value" label="" width="260">
            <template slot-scope="scope">
              <div v-if="scope.row.key == 'Topic Count Control'">

                <el-slider v-model="TopicCount" :step="1" :min="0" :max="10"></el-slider>

              </div>
              <div v-if="scope.row.key == 'count'" class="Level">
                relationships:{{ relCount }}
              </div>
            </template>
          </el-table-column>
        </el-table>
        <el-table :data="topicControl1" style="transform: translate(0,-27px); color:rgb(114, 114, 114);width;: 100%">
          <el-table-column prop="key" label="" width="240">

            <template slot-scope="scope">
              <div v-if="scope.row.key == 'Topic Count Control'">
                {{ scope.row.key }}
              </div>
              <div v-if="scope.row.key == 'count'" class="Level">
                node:&nbsp&nbsp&nbsp{{ nodeCount }}
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="value" label="" width="300">
            <template slot-scope="scope">
              <div v-if="scope.row.key == 'Topic Count Control'">

                <el-slider v-model="TopicCount" :step="1" :min="0" :max="10"></el-slider>

              </div>
              <div v-if="scope.row.key == 'count'" class="Level">
                r:&nbsp&nbsp&nbsp{{ relCount }}
              </div>
            </template>
          </el-table-column>
        </el-table> -->
      </div>
      <div id="tools">
        <el-button type="primary" style="height: 30px;width: 140px;padding: 0; margin: 10px 20px;" @click="confirmClk">Apply</el-button>
        <el-button type="primary" style="height: 30px;width: 140px;" >ReSet</el-button>
      </div>

      <!-- <div id="confirmButDiv" @click="confirmClk" ref="addBtn">
        <img class="icons" :src="confirmUrl">
      </div> -->

    </div>
    <!-- <div id="lectureStyleIconDiv">
        <img class="icons" :src="lectureStyleIconUrl">
      </div>
      <div id="banshuDiv">
        <img class="icons banshu" :src="banshuUrl">
      </div>
      <div id="kousuDiv">
        <img class="icons kousu" :src="kousuUrl">
      </div>
      <div id="pptDiv">
        <img class="icons ppt" :src="pptUrl">
      </div> -->
  </div>
</template>
  
<script>
import * as d3 from 'd3'
import { onMounted, ref } from 'vue';
import filenames from "@/utils/fileName";
import domtoimage from 'dom-to-image';
import tools from "@/utils/tools.js";
import { select } from 'd3';

export default {
  props: ["videoTime"],
  data() {
    return {
      selectSession: "3.3",
      TopicCount: 3,
      TopicCount1: 5,
      nodeCount: "23",
      relCount: "12",
      conceptTree:'',
      // nodeCount:"5",
      // relCount:"10",
      // nodeCount:"5",
      // relCount:"10",
      fileVideoList: [],
      fileSlidesList: [],
      fileScriptList: [],

      confirmUrl: require("@/assets/img/confirmGroup.png"),
      upSliderUrl: require('@/assets/img/Slider.png'),
      upScriptUrl: require('@/assets/img/Script.png'),
      // require('@/assets/videos/index.mp4'),
      upLoadUrl: require('@/assets/img/openFile.png'),
      videoUploadIcon: '@/',
      tableData: [{
        key: 'Course : ',
        // nameinput: "Random Variables",
        // nameinput: "Fundamental controlLines",
        // nameinput: "Trees",
        // value: 'Random Variables   ',
        // value: 'Fundamental controlLines   ',
        // value: 'C语言程序设计',
        value: 'C Language'// Programming'
      },{
        key: 'Questions ：',
        value: '236',
      },{
        key: 'Concepts ：',
        value: '59',
      },{
        key: 'Relationships ：',
        value: '1011',
      },{
        key: 'Students ：',
        value: '40',
      }
      ],
      addRels:"none",
      switchL: {
        "1": false,
        "2": false,
        "3": false
      },
      curToolState: {
        "addRel": false,
        "addRelMain": false,
        "delRel": false,
      },
      renew: false,
      lectureStyleIconUrl: require("@/assets/img/lecture style.png"),
      banshuUrl: require("@/assets/img/lecture style banshu.png"),
      kousuUrl: require("@/assets/img/lecture style kousu.png"),
      pptUrl: require("@/assets/img/lecture style ppt.png"),
      layoutSelect: "3",
      
      toolsData: [{
        key: 'Option :',
        value: '1',
      }, {
        key: 'Perplexity :',
        value: '2',
      }, {
        key: 'Threshold :',
        value: '3',
      }
      ],
      topicControl: [{
        key: 'Topic Count Control',
        value: '1',
      }
      ],
      topicControl1: [{
        key: 'count',
        value: '2',
      }
      ]
    };
  },
  watch: {
    type(val) {
    },
    conceptTree(val){
      console.log(val)
      this.drawOverView();
    },
    addRels(val){
        this.curToolState['addRel'] = false;
        this.curToolState['addRelMain'] = false;
        this.curToolState['delRel'] = false
      if(val =="None" ){
      }
      else if(val =="Add" ){
        this.curToolState['addRel'] = true;
      }
      else if(val =="Del" ){
        this.curToolState['delRel'] = true;
      }
      else if(val =="Main" ){
        this.curToolState['addRel'] = true;
        this.curToolState['addRelMain'] = true;
      }
        this.$emit("getToolState", this.curToolState);
    },
    switchL: {
      deep: true,
      handler(val) {
        this.curToolState['addRel'] = val['1'];
        this.curToolState['addRelMain'] = val['2'];
        this.curToolState['delRel'] = val['3'];
        this.$emit("getToolState", this.curToolState);
      }
    }
  },
  methods: {
    drawOverView(){
      var _this = this;
      // let margin = _this.margin
      let width = _this.$refs.controlLineDiv.offsetWidth ;
      let height = document.getElementById("controlLineChart").clientHeight ;
      _this.width = width;
      _this.height = height;
      d3.select("#controlLineChart").select("svg").remove()
      var svg = d3.select("#controlLineChart").append("svg")
        .attr("width", width)
        .attr("height", height);
      let data = _this.conceptTree;
      console.log(data);
      const pathAxisY = d3.path();
      pathAxisY.moveTo(20, 20);
      pathAxisY.lineTo(20, 90);
      _this.drawTxt(svg, 17, 28, "1", "black", 12, `control_`,'end');
      _this.drawTxt(svg, 17, 88, "0", "black", 12, `control_`,'end');
      _this.drawTxt(svg, 17, 58, "0.5", "black", 12, `control_`,'end');
      _this.drawTxt(svg, 5, 10, "Scoring Rate", "grey", 13, `control_`,"start");
      _this.drawTxt(svg, width-30, 115, "Chapter", "grey", 13, `control_`,"end");
      
      _this.drawPathLine(svg, pathAxisY, `black`, 1, "0", `controlLine1`, ""); 
      width-=10;
      const pathAxisX = d3.path();
      pathAxisX.moveTo(20, 90);
      pathAxisX.lineTo(width-10, 90);
      _this.drawPathLine(svg, pathAxisX, `black`, 1, "0", `controlLine2`, ""); 

      let xSize_linear = d3.scaleLinear().domain([0,1]).range([0,70]);
      let i = 0
      let stepx = width/8;
      let points = []

      let curve_generator = d3.line()
        .x((d) => d[0])
        .y((d) => d[1])
        .curve(d3.curveLinear)

      data.forEach(rev =>{
        if(rev['id'].length == 1)
        {
          let cx = 20 + stepx*i;
        let cy = 100-xSize_linear(rev['scoringRate']);
        
        points.push([cx,cy]);
        let pointss = [[cx,90],[cx,20]];
         _this.drawLine(svg, curve_generator(pointss), "grey", 0.5, '0', '1', `controlLineValueBacky${i}`, 'controlLineValue', "rgba(253, 195, 190,0.3)");

        _this.drawTxt(svg, cx+1, 103, `${i+1}`, "black", 12, `control_`,'middle');
        i++;
      }
      });

      // let curve_generatorb = d3.line()
      //   .x((d) => d[0])
      //   .y((d) => d[1])
      //   .curve(d3.curveBasis)
      // .c
      let linepoly = _this.drawLine(svg, curve_generator(points), "rgb(64, 158, 255)", 2, '0', '1', `controlLineValue`, 'controlLineValue', "rgba(253, 195, 190,0)");

      for(let i=0;i<5;i++){
        
        let points = [[20,20+70/5*i],[width-10,20+70/5*i]];
         _this.drawLine(svg, curve_generator(points), "grey", 0.5, '0', '1', `controlLineValueBack${i}`, 'controlLineValue', "rgba(253, 195, 190,0.3)");

      }
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
    iRowStyle:function ({row, rowIndex}) {
        return 'height:25px ;font-size:10px';
    },
    iHeaderRowStyle:function ({row, rowIndex}) {
        return 'height:10px';
    },
    iCellStyle:function ({row, column, rowIndex, columnIndex}) {
        return 'padding:0px;font-size:18px;'
    },
    iHeaderCellStyle:function ({row, column, rowIndex, columnIndex}) {
        return 'padding:0px'
    },

    icRowStyle:function ({row, rowIndex}) {
        return 'height:23px ;font-size:10px';
    },
    icHeaderRowStyle:function ({row, rowIndex}) {
        return 'height:23px';
    },
    icCellStyle:function ({row, column, rowIndex, columnIndex}) {
        return 'padding:0px;font-size:18px;'
    },
    icHeaderCellStyle:function ({row, column, rowIndex, columnIndex}) {
        return 'padding:0px'
    },
    handleCommand(command) {
      this.selectSession = command;
    },
    
    confirmClk() {

      this.renew = true;
      this.$bus.$emit("renew", this.renew);
      // this.curToolState['addRel']=false;
      // this.curToolState['addRelMain']=false;
      // this.curToolState['delRel']=false;
      this.$emit("getToolState", this.curToolState);
      this.renew = false;
    },
    click_Ent(time) {
      this.$emit("timeDur", time);
    },
    videoUpClk() {
      this.$refs.videoBut.$el.click()
    },
    sliderUpClk() {
      this.$refs.sliderBut.$el.click()
    },
    scriptUpClk() {
      this.$refs.scriptBut.$el.click()
    },
    handleVideoChange(file, fileList) {
      this.fileList = fileList.slice(-3);
    },
    handleSlidesChange(file, fileList) {
      this.fileList = fileList.slice(-3);
    },
    handleScriptChange(file, fileList) {
      this.fileList = fileList.slice(-3);
    }
  },
  created() {



    const _this = this;

    this.$nextTick(() => {

    });
  },
  mounted() {
    const _this = this


    this.$bus.$on('ConceptTree', (val) => {
      _this.conceptTree = val;
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
