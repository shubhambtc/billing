(this["webpackJsonpgull-react"]=this["webpackJsonpgull-react"]||[]).push([[86],{2039:function(e,a){},2208:function(e,a,t){"use strict";t.r(a);var n=t(50),l=t(8),i=t(9),s=t(15),c=t(16),r=t(0),m=t.n(r),o=t(26),d=t(11),u=t(2196),p=t(585),b=t(643),E=t(630),v=t(547),h=t(103),g=t(597),N=t(592),f=function(e){Object(s.a)(t,e);var a=Object(c.a)(t);function t(){var e;Object(l.a)(this,t);for(var n=arguments.length,i=new Array(n),s=0;s<n;s++)i[s]=arguments[s];return(e=a.call.apply(a,[this].concat(i))).state={to:"",subject:"",content:"",attachment:null},e.handleSubmit=function(e,a){a.setSubmitting;console.log(e)},e.handleContentChange=function(a){e.setState({content:a})},e}return Object(i.a)(t,[{key:"render",value:function(){var e=this.props,a=e.open,t=e.handleClose;return m.a.createElement(u.a,{show:a,onHide:t,size:"lg",centered:!0},m.a.createElement(g.b,{initialValues:this.state,validationSchema:S,onSubmit:this.handleSubmit,enableReinitialize:!0},(function(e){var a=e.values,n=e.errors,l=e.touched,i=e.handleChange,s=e.handleBlur,c=e.handleSubmit,r=(e.isSubmitting,e.setSubmitting,e.setFieldValue);return m.a.createElement("form",{onSubmit:c,className:"inbox-form p-4"},m.a.createElement(p.a,{className:"mb-2"},m.a.createElement(b.a,null,"To"),m.a.createElement(E.a,{type:"email",name:"to",placeholder:"uilib@xmail.com",onChange:i,onBlur:s,isInvalid:n.to&&l.to,value:a.to})),m.a.createElement(p.a,{className:"mb-2"},m.a.createElement(b.a,null,"Subject"),m.a.createElement(E.a,{type:"text",name:"subject",placeholder:"uilib@xmail.com",onChange:i,onBlur:s,isInvalid:n.subject&&l.subject,value:a.subject})),m.a.createElement(h.g,{content:a.content,handleContentChange:function(e){return r("content",e)},placeholder:"insert text here..."}),m.a.createElement("div",{className:"mt-3 d-flex flex-wrap justify-content-between"},m.a.createElement(v.a,{type:"button",onClick:t,variant:"secondary"},"Cancel"),m.a.createElement("div",{className:"d-flex align-items-center"},a.attachment&&m.a.createElement("p",{className:"me-4"},a.attachment.name),m.a.createElement("label",{htmlFor:"attachment",className:"mb-0"},m.a.createElement(v.a,{type:"button",className:"me-2 ",as:"span",variant:"secondary"},m.a.createElement("i",{className:"i-Mail-Attachement"}))),m.a.createElement("input",{onChange:function(e){return r("attachment",e.target.files[0])},className:"d-none",id:"attachment",type:"file"}),m.a.createElement(v.a,{className:"btn-rounded",variant:"primary",type:"submit"},m.a.createElement("i",{className:"i-Paper-Plane"})))))})))}}]),t}(r.Component),S=N.object().shape({to:N.string().email("Invalid email").required("email is required"),subject:N.string().required("subject is required"),content:N.string().required("content required")}),x=f,y=function(e){var a=e.open,t=e.toggleSidenav,n=Object(r.useState)(!1),l=Object(d.a)(n,2),i=l[0],s=l[1];return m.a.createElement("div",{className:"inbox-main-sidebar sidebar",style:{left:a?0:"-180px"}},m.a.createElement("div",{className:"pt-3 pe-3 pb-3"},m.a.createElement("i",{className:"sidebar-close i-Close cursor-pointer",onClick:function(){return t("mainSidenavOpen")}}),m.a.createElement("button",{onClick:function(){return s(!0)},className:"btn btn-rounded btn-primary w-100 mb-4"},"Compose"),m.a.createElement("div",{className:"ps-3"},m.a.createElement("p",{className:"text-muted mb-2"},"Browse"),m.a.createElement("ul",{className:"inbox-main-nav"},m.a.createElement("li",null,m.a.createElement("span",{className:"active"},m.a.createElement("i",{className:"icon-regular i-Mail-2"})," Inbox (2)")),m.a.createElement("li",null,m.a.createElement("span",null,m.a.createElement("i",{className:"icon-regular i-Mail-Outbox"})," Sent")),m.a.createElement("li",null,m.a.createElement("span",null,m.a.createElement("i",{className:"icon-regular i-Mail-Favorite"})," Starred")),m.a.createElement("li",null,m.a.createElement("span",null,m.a.createElement("i",{className:"icon-regular i-Folder-Trash"})," Trash")),m.a.createElement("li",null,m.a.createElement("span",null,m.a.createElement("i",{className:"icon-regular i-Spam-Mail"})," Spam"))))),m.a.createElement(x,{open:i,handleClose:function(){s(!1)}}))},O=t(6),j=t.n(O),w=t(110),C=t.n(w),M=t(2015),k=t.n(M),L=t(952),R=function(e){e.mainSidenavOpen;var a=e.secSidenavOpen,t=e.isMobile,n=e.messageList,l=void 0===n?[]:n,i=e.toggleSidenav,s=Object(r.useState)(null),c=Object(d.a)(s,2),o=c[0],u=c[1];return Object(r.useEffect)((function(){l.length>0&&u(l[0])}),[l]),m.a.createElement("div",{className:"inbox-main-content sidebar-content",style:{marginLeft:t?0:"180px"}},m.a.createElement("div",{className:"inbox-secondary-sidebar-container box-shadow-1 sidebar-container"},m.a.createElement("div",{className:"sidebar-content",style:{marginLeft:t?0:"360px"}},m.a.createElement("div",{className:"inbox-secondary-sidebar-content position-relative",style:{minHeight:"500px"}},m.a.createElement("div",{className:"inbox-topbar box-shadow-1 perfect-scrollbar rtl-ps-none ps-3","data-suppress-scroll-y":"true"},m.a.createElement("span",{"data-sidebar-toggle":"main",className:"link-icon d-md-none",onClick:function(){return i("mainSidenavOpen")}},m.a.createElement("i",{className:"icon-regular i-Arrow-Turn-Left"})),m.a.createElement("span",{className:"link-icon me-3 d-md-none",onClick:function(){return i("secSidenavOpen")}},m.a.createElement("i",{className:"icon-regular me-1 i-Left-3"})," Inbox"),m.a.createElement("div",{className:"d-flex"},m.a.createElement("span",{href:"",className:"link-icon me-3"},m.a.createElement("i",{className:"icon-regular i-Mail-Reply"}),"Reply"),m.a.createElement("span",{href:"",className:"link-icon me-3"},m.a.createElement("i",{className:"icon-regular i-Mail-Reply-All"}),"Forward"),m.a.createElement("span",{href:"",className:"link-icon me-3"},m.a.createElement("i",{className:"icon-regular i-Mail-Reply-All"}),"Delete"))),o?m.a.createElement(C.a,{className:"inbox-details perfect-scrollbar rtl-ps-none","data-suppress-scroll-x":"true"},m.a.createElement("div",{className:"d-flex no-gutters"},m.a.createElement("div",{className:"me-2",style:{width:"36px"}},m.a.createElement("img",{className:"rounded-circle",src:o.sender.photo,alt:o.sender.name})),m.a.createElement("div",{className:"col-xs-12"},m.a.createElement("p",{className:"m-0"},o.sender.name),m.a.createElement("p",{className:"text-12 text-muted"},Object(L.default)(new Date(o.date).getTime(),"dd MMM, yyyy")))),m.a.createElement("h4",{className:"mb-3"},o.subject),m.a.createElement("div",null,k()(o.message))):m.a.createElement("div",{className:"w-100 text-center"},"No message available"))),m.a.createElement(C.a,{className:"inbox-secondary-sidebar sidebar",style:{left:t?a?0:"-280px":0}},m.a.createElement("i",{className:"sidebar-close i-Close cursor-pointer",onClick:function(){return i("secSidenavOpen")}}),l.map((function(e){return m.a.createElement("div",{className:"mail-item",key:e.id,onClick:function(){return function(e){u(e),t&&i("secSidenavOpen")}(e)}},m.a.createElement("div",{className:"avatar"},m.a.createElement("img",{src:e.sender.photo,alt:e.sender.name})),m.a.createElement("div",{className:"col-xs-6 details"},m.a.createElement("span",{className:"name text-muted"},e.sender.name),m.a.createElement("p",{className:"m-0"},e.subject)),m.a.createElement("div",{className:"col-xs-3 date"},m.a.createElement("span",{className:"text-muted"},Object(L.default)(new Date(e.date).getTime(),"dd MMM, yyyy"))))})))))},q=function(e){Object(s.a)(t,e);var a=Object(c.a)(t);function t(){var e;Object(l.a)(this,t);for(var i=arguments.length,s=new Array(i),c=0;c<i;c++)s[c]=arguments[c];return(e=a.call.apply(a,[this].concat(s))).container=m.a.createRef(),e.state={mainSidenavOpen:!0,secSidenavOpen:!0,masterCheckbox:!1,isMobile:!1,messageList:[]},e.toggleSidenav=function(a){e.setState(Object(n.a)({},a,!e.state[a]))},e}return Object(i.a)(t,[{key:"componentDidMount",value:function(){var e=this;Object(o.d)()&&this.setState({mainSidenavOpen:!1,secSidenavOpen:!1,isMobile:!0}),window&&(this.windowResizeListener=window.addEventListener("resize",(function(a){Object(o.d)()?e.setState({mainSidenavOpen:!1,secSidenavOpen:!1,isMobile:!0}):e.setState({mainSidenavOpen:!0,secSidenavOpen:!0,isMobile:!1})}))),j.a.get("/api/inbox/all").then((function(a){e.setState({messageList:a.data})}))}},{key:"componentWillUnmount",value:function(){window&&window.removeEventListener("resize",this.windowResizeListener)}},{key:"render",value:function(){var e=this.state,a=e.mainSidenavOpen,t=e.secSidenavOpen,n=e.messageList,l=e.isMobile;return m.a.createElement("div",{className:"inbox-main-sidebar-container sidebar-container"},m.a.createElement(R,{secSidenavOpen:t,mainSidenavOpen:a,isMobile:l,messageList:n,toggleSidenav:this.toggleSidenav}),m.a.createElement(y,{open:a,toggleSidenav:this.toggleSidenav}))}}]),t}(r.Component);a.default=q}}]);
//# sourceMappingURL=86.f81ad6c7.chunk.js.map