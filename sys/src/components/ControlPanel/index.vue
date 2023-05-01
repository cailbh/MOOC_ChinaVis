<!-- eslint-disable no-unused-vars -->
<!-- eslint-disable no-unused-vars -->

<template>
  <div class="controlPanel">
    <div class="panelHead">ControlPanel</div>
    <div id="controlPanelDiv" class="panelBody" ref="controlPanelDiv">
      <div id="upLoadVideo">
        <el-upload class="uploadVideoel" action="https://jsonplaceholder.typicode.com/posts/"
          :on-change="handleVideoChange" :file-list="fileVideoList">
          <el-button ref="videoBut" size="middle" type="primary">Upload</el-button>
        </el-upload>
      </div>
      <div id="baseInformation">
        <el-table :data="tableData" style="width: 100%">
          <el-table-column prop="key" label="" width="190">
          </el-table-column>
          <el-table-column prop="value" label="" width="260">
            <template slot-scope="scope">
              <div v-if="scope.row.key == 'Course name'">
                <div style="float: left;">
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
      <div id="topicControl">
        <el-table :data="topicControl" style="color:rgb(114, 114, 114);width;: 100%">
          <el-table-column prop="key" label="" width="340">
            
            <template slot-scope="scope">
              <div  v-if="scope.row.key == 'Topic Count Control'">
                {{scope.row.key}}
              </div>
              <div v-if="scope.row.key == 'count'" class="Level">
                node:&nbsp&nbsp&nbsp{{nodeCount}}
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="value" label="" width="260">
            <template slot-scope="scope">
              <div  v-if="scope.row.key == 'Topic Count Control'">
                
                <el-slider v-model="TopicCount" :step="1" :min="0" :max="10" ></el-slider>

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
              <div  v-if="scope.row.key == 'Topic Count Control'">
                {{scope.row.key}}
              </div>
              <div v-if="scope.row.key == 'count'" class="Level">
                node:&nbsp&nbsp&nbsp{{nodeCount}}
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="value" label="" width="300">
            <template slot-scope="scope">
              <div  v-if="scope.row.key == 'Topic Count Control'">
                
                <el-slider v-model="TopicCount" :step="1" :min="0" :max="10" ></el-slider>

              </div>
              <div v-if="scope.row.key == 'count'" class="Level">
                relationships:&nbsp&nbsp&nbsp{{ relCount }}  
              </div>
            </template>
          </el-table-column>
      </el-table>
    </div>
      <div id="tools">
        <el-table :data="toolsData" style="color:rgb(167, 167, 167);width;: 100%">
          <el-table-column prop="key" label="" width="260">
          </el-table-column>
          <el-table-column prop="value" label="" width="260">
            <template slot-scope="scope">
              <div v-if="scope.row.key != 'Layout Level'">
                <el-switch size="middle" v-model="switchL[scope.row.value]" active-text="" inactive-text="">
                </el-switch>

              </div>
              <div v-if="scope.row.key == 'Layout Level'" class="Level">
                <el-slider
                  v-model="layoutSelect"
                  :step="1"
                  :min="0"
                  :max="3"
                  show-stops>
                </el-slider>
              </div>
              <!-- <el-tag :type="scope.row.value === '' ? 'primary' : 'success'" disable-transitions>{{ scope.row.tag -->
              <!-- // }}</el-tag> -->
              <!-- <div :class="scope.row.name" :height="scope.row.value === '' ? '10' : '0'" disable-transitions>
                {{ scope.row.value }}
              </div> -->
            </template>
          </el-table-column>
      </el-table>
    </div>
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
      TopicCount:"4",
      nodeCount:"23",
      relCount:"12",
      // nodeCount:"5",
      // relCount:"10",
      // nodeCount:"5",
      // relCount:"10",
      fileVideoList: [],
      fileSlidesList: [],
      fileScriptList: [],
      upSliderUrl: require('@/assets/img/Slider.png'),
      upScriptUrl: require('@/assets/img/Script.png'),
      // require('@/assets/videos/index.mp4'),
      upLoadUrl: require('@/assets/img/openFile.png'),
      videoUploadIcon: '@/',
      tableData: [{
        key: 'Course name',
        // nameinput: "Random Variables",
      // nameinput: "Fundamental Graphs",
      // nameinput: "Trees",
        // value: 'Random Variables   ',
        // value: 'Fundamental Graphs   ',
        value: 'C语言程序设计',
      }
      ],
      switchL:{
        "1":false,
        "2":false,
        "3":false
      },
      curToolState:{
        "addRel":false
      },
      lectureStyleIconUrl: require("@/assets/img/lecture style.png"),
      banshuUrl: require("@/assets/img/lecture style banshu.png"),
      kousuUrl: require("@/assets/img/lecture style kousu.png"),
      pptUrl: require("@/assets/img/lecture style ppt.png"),
      layoutSelect:"3",
      toolsData: [{
        key: 'addRel',
        value: '1',
      }, {
        key: '2',
        value: '2',
      },  {
        key: '3',
        value: '',
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
    switchL:{
      deep:true,
      handler(val){
        console.log(val);
          this.curToolState['addRel']=val['1']
        this.$emit("getToolState", this.curToolState);
      }
    }
  },
  methods: {
    handleCommand(command) {
      this.selectSession = command;
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




  },
  // beforeDestroy() {
  //   clearInterval(this.moveTimer);
  // },
} 
</script>

<style>
@import './index.css';
</style>
