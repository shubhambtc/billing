(this["webpackJsonpgull-react"]=this["webpackJsonpgull-react"]||[]).push([[68],{2234:function(a,e,t){"use strict";t.r(e);var n=t(8),c=t(9),r=t(15),s=t(16),o=t(0),l=t.n(o),m=t(103),i=t(548),b=t(537),u=t(593),f=t.n(u);function h(a,e,t){for(var n=0,c=[];n<e;){var r=Math.floor(750*Math.random())+1,s=Math.floor(Math.random()*(t.max-t.min+1))+t.min,o=Math.floor(61*Math.random())+15;c.push([r,s,o]),864e5,n++}return c}var p={chart:{height:350,type:"bubble",toolbar:{show:!1}},dataLabels:{enabled:!1},series:[{name:"Bubble1",data:h(new Date("11 Feb 2017 GMT").getTime(),20,{min:10,max:60})},{name:"Bubble2",data:h(new Date("11 Feb 2017 GMT").getTime(),20,{min:10,max:60})},{name:"Bubble3",data:h(new Date("11 Feb 2017 GMT").getTime(),20,{min:10,max:60})},{name:"Bubble4",data:h(new Date("11 Feb 2017 GMT").getTime(),20,{min:10,max:60})}],fill:{opacity:.8},xaxis:{tickAmount:12,type:"category"},yaxis:{max:70}};function d(a,e,t){for(var n=0,c=[];n<e;){var r=Math.floor(Math.random()*(t.max-t.min+1))+t.min,s=Math.floor(61*Math.random())+15;c.push([a,r,s]),a+=864e5,n++}return c}var x={chart:{height:350,type:"bubble"},dataLabels:{enabled:!1},series:[{name:"Product1",data:d(new Date("11 Feb 2017 GMT").getTime(),20,{min:10,max:60})},{name:"Product2",data:d(new Date("11 Feb 2017 GMT").getTime(),20,{min:10,max:60})},{name:"Product3",data:d(new Date("11 Feb 2017 GMT").getTime(),20,{min:10,max:60})},{name:"Product4",data:d(new Date("11 Feb 2017 GMT").getTime(),20,{min:10,max:60})}],fill:{type:"gradient"},xaxis:{tickAmount:12,type:"datetime",labels:{rotate:0}},yaxis:{max:70},theme:{palette:"palette2"}},v=function(a){Object(r.a)(t,a);var e=Object(s.a)(t);function t(){var a;Object(n.a)(this,t);for(var c=arguments.length,r=new Array(c),s=0;s<c;s++)r[s]=arguments[s];return(a=e.call.apply(e,[this].concat(r))).state={},a}return Object(c.a)(t,[{key:"render",value:function(){return l.a.createElement("div",null,l.a.createElement(m.a,{routeSegments:[{name:"Charts",path:"/charts"},{name:"Apex",path:"/apex"},{name:"Bubble"}]}),l.a.createElement(i.a,null,l.a.createElement(b.a,{lg:6,md:6,sm:12,xs:12,className:"mb-4"},l.a.createElement(m.h,{className:"h-100",title:"Simple Bubble"},l.a.createElement(f.a,{options:p,series:p.series,type:p.chart.type}))),l.a.createElement(b.a,{lg:6,md:6,sm:12,xs:12,className:"mb-4"},l.a.createElement(m.h,{className:"h-100",title:"3D Bubble Chart"},l.a.createElement(f.a,{options:x,series:x.series,type:x.chart.type})))))}}]),t}(o.Component);e.default=v},537:function(a,e,t){"use strict";var n=t(11),c=t(1),r=t(10),s=t(12),o=t.n(s),l=t(0),m=t(18),i=t(5),b=["as","bsPrefix","className"],u=["className"];var f=l.forwardRef((function(a,e){var t=function(a){var e=a.as,t=a.bsPrefix,n=a.className,s=Object(r.a)(a,b);t=Object(m.b)(t,"col");var l=Object(m.a)(),i=[],u=[];return l.forEach((function(a){var e,n,c,r=s[a];delete s[a],"object"===typeof r&&null!=r?(e=r.span,n=r.offset,c=r.order):e=r;var o="xs"!==a?"-".concat(a):"";e&&i.push(!0===e?"".concat(t).concat(o):"".concat(t).concat(o,"-").concat(e)),null!=c&&u.push("order".concat(o,"-").concat(c)),null!=n&&u.push("offset".concat(o,"-").concat(n))})),[Object(c.a)(Object(c.a)({},s),{},{className:o.a.apply(void 0,[n].concat(i,u))}),{as:e,bsPrefix:t,spans:i}]}(a),s=Object(n.a)(t,2),l=s[0],f=l.className,h=Object(r.a)(l,u),p=s[1],d=p.as,x=void 0===d?"div":d,v=p.bsPrefix,j=p.spans;return Object(i.jsx)(x,Object(c.a)(Object(c.a)({},h),{},{ref:e,className:o()(f,!j.length&&v)}))}));f.displayName="Col",e.a=f},548:function(a,e,t){"use strict";var n=t(1),c=t(10),r=t(12),s=t.n(r),o=t(0),l=t(18),m=t(5),i=["bsPrefix","className","as"],b=o.forwardRef((function(a,e){var t=a.bsPrefix,r=a.className,o=a.as,b=void 0===o?"div":o,u=Object(c.a)(a,i),f=Object(l.b)(t,"row"),h=Object(l.a)(),p="".concat(f,"-cols"),d=[];return h.forEach((function(a){var e,t=u[a];delete u[a],e=null!=t&&"object"===typeof t?t.cols:t;var n="xs"!==a?"-".concat(a):"";null!=e&&d.push("".concat(p).concat(n,"-").concat(e))})),Object(m.jsx)(b,Object(n.a)(Object(n.a)({ref:e},u),{},{className:s.a.apply(void 0,[r,f].concat(d))}))}));b.displayName="Row",e.a=b}}]);
//# sourceMappingURL=68.da50f2bc.chunk.js.map