(function(e){function t(t){for(var i,r,s=t[0],l=t[1],c=t[2],f=0,d=[];f<s.length;f++)r=s[f],Object.prototype.hasOwnProperty.call(o,r)&&o[r]&&d.push(o[r][0]),o[r]=0;for(i in l)Object.prototype.hasOwnProperty.call(l,i)&&(e[i]=l[i]);u&&u(t);while(d.length)d.shift()();return a.push.apply(a,c||[]),n()}function n(){for(var e,t=0;t<a.length;t++){for(var n=a[t],i=!0,s=1;s<n.length;s++){var l=n[s];0!==o[l]&&(i=!1)}i&&(a.splice(t--,1),e=r(r.s=n[0]))}return e}var i={},o={main:0},a=[];function r(t){if(i[t])return i[t].exports;var n=i[t]={i:t,l:!1,exports:{}};return e[t].call(n.exports,n,n.exports,r),n.l=!0,n.exports}r.m=e,r.c=i,r.d=function(e,t,n){r.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:n})},r.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},r.t=function(e,t){if(1&t&&(e=r(e)),8&t)return e;if(4&t&&"object"===typeof e&&e&&e.__esModule)return e;var n=Object.create(null);if(r.r(n),Object.defineProperty(n,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var i in e)r.d(n,i,function(t){return e[t]}.bind(null,i));return n},r.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return r.d(t,"a",t),t},r.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},r.p="/front/";var s=window["webpackJsonp"]=window["webpackJsonp"]||[],l=s.push.bind(s);s.push=t,s=s.slice();for(var c=0;c<s.length;c++)t(s[c]);var u=l;a.push([0,"chunk-common"]),n()})({0:function(e,t,n){e.exports=n("56d7")},5025:function(e,t,n){"use strict";n("8a57")},"56d7":function(e,t,n){"use strict";n.r(t);n("e260"),n("e6cf"),n("cca6"),n("a79d");var i=n("a026"),o=function(){var e=this,t=e._self._c;return t("v-row",{staticClass:"d-flex flex-row"},[t("v-col",{staticClass:"d-flex flex-row flex-wrap"},e._l(e.wheels,(function(n,i){return t("fortune-wheel",{key:i,attrs:{color:e.showColor&&n===e.selectedRisk?"yellow":"",share:n,single:!1,label:!0,startingCover:!0},on:{animationOver:e.increaseDone}})})),1)],1)},a=[],r=n("2ef0"),s=n.n(r),l=n("6be1"),c={name:"App",components:{FortuneWheel:l["a"]},data:function(){var e=s.a.range(0,101,10);return{counterDone:0,wheels:s.a.shuffle(e),showColor:window.showColor,selectedRisk:window.selectedRisk}},watch:{counterDone:function(e){e===this.wheels.length&&$("#next").removeClass("d-none")}},mounted:function(){this.$vuetify.theme.dark=!1},methods:{increaseDone:function(){this.counterDone++,console.debug("ONE MORE DONE!",this.counterDone)}}},u=c,f=(n("5025"),n("2877")),d=Object(f["a"])(u,o,a,!1,null,null,null),h=d.exports,p=n("01e8"),v=n.n(p),m=n("be33"),g=n("ce5b"),y=n.n(g),b=(n("bf40"),n("ad3d")),w=n("11ca");i["default"].use(y.a);var _={};m["c"].add(w["b"],w["a"]),i["default"].component("font-awesome-icon",b["a"]),i["default"].use(v.a),i["default"].config.productionTip=!1,new i["default"]({vuetify:new y.a(_),render:function(e){return e(h)}}).$mount("#app")},"6be1":function(e,t,n){"use strict";var i=function(){var e=this,t=e._self._c;return t("v-card",{staticClass:"mx-1 px-3 my-1 py-3 d-flex flex-column justify-center align-center",staticStyle:{"align-items":"center!important","justify-content":"center"},style:{background:e.my_color},attrs:{color:e.my_color,outlined:"",rounded:"",elevation:10}},[t("div",{staticClass:"mb-1"},[t("font-awesome-icon",{attrs:{icon:"fa-solid fa-circle-arrow-down"}})],1),t("div",{staticStyle:{position:"relative",display:"flex","align-items":"center","justify-content":"center"}},[t("transition",{attrs:{"enter-active-class":"animate__animated animate__jello"}}),t("div",{ref:"circle1",staticStyle:{position:"relative",display:"flex","align-items":"center","justify-content":"center"}},[t("div",{staticClass:"seventyfive",style:{background:e.get_share}}),t("div",{staticClass:"backgroundfif",staticStyle:{position:"absolute"}})]),t("transition",{attrs:{"leave-active-class":"animate__animated animate__flipOutY"}},[e.cover?t("div",{ref:"cover",staticClass:"fif",staticStyle:{position:"absolute","z-index":"10"},on:{click:e.hideCover}},[e.label?t("div",[e._v("Click me!")]):e._e()]):e._e()])],1)])},o=[],a=n("5530"),r=(n("ac1f"),n("466d"),n("99af"),n("2ef0")),s=n.n(r);n("77ed");var l={name:"App",props:["share","single","color","startingCover","label","noAnim"],components:{},data:function(){return{cover:this.startingCover,result:!1,animation:null,isPlaying:!1,my_color:"",val:"ssss"}},mounted:function(){var e=this.$refs.circle1,t=this,n=s.a.random(0,359),i=720+n,o={rotate:window.lotteryOutcome,duration:0,delay:0,easing:"linear",loop:!1},r={rotate:360,duration:3600,loop:!0,easing:"linear",delay:0},l={targets:e,rotate:i,duration:3600,loop:!1,delay:500,easing:"easeOutSine",update:function(e){var n=e.animations[0].currentValue,i=/(.*?)deg/,o=n.match(i);t.val=o[1]%360,console.debug(parseInt(n))},complete:function(e){t.$emit("animationOver"),t.result=!0,t.my_color=t.color}};this.single&&(l=Object(a["a"])(Object(a["a"])({},l),r)),this.noAnim&&(l=Object(a["a"])(Object(a["a"])({},l),o)),this.animation=this.$anime(l),this.single||(this.animation.pause(),this.isPlaying=!1)},watch:{val:function(e){}},computed:{winningColor:function(){var e=this.val%360;return e>=this.losingangle?"green":"red"},weWin:function(){var e=this.val%360;return e>=this.losingangle?"win!":"lose!"},losingangle:function(){return 360-this.winningangle},winningangle:function(){return 360*this.share/100},get_share:function(){return"conic-gradient(green 0% ".concat(this.share,"%, red ").concat(this.share,"% 100%)")}},methods:{hideCover:function(){this.single||(this.cover=!1,this.startSpin())},startSpin:function(){!1===this.isPlaying?(this.isPlaying=!0,this.animation.play()):(this.isPlaying=!1,this.animation.pause())}}},c=l,u=(n("d8d7"),n("2877")),f=Object(u["a"])(c,i,o,!1,null,null,null);t["a"]=f.exports},"8a57":function(e,t,n){},d8d7:function(e,t,n){"use strict";n("ea56")},ea56:function(e,t,n){}});