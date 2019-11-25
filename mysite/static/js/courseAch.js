// 判断是否有cookie
$(function(){
  $.getJSON('../cookies',function(data){
    if(data.res == '0'){
      alert(data.msg);
      window.location.href='../login.html';
      return;
    }
    if (data.data[0].typeId != '1') {
      $.getJSON('../deleteCookies',function(res){
      })
      window.location.href='../login.html';
      return;
    }
    console.log(data);
    $('header span').attr('data',data.data[0].typeId);
    $('header span label').html(data.data[0].username);
    $('header span label').attr('data',data.data[0].userId);
    findChoosed();
  });
});
//查找已选课程
function findChoosed(){
   $.ajax({
    type:'get',
    url:'../ChooseCourse.jsp',
    data:{
      'api':'courseChoosedbyStudent',
      // 'typeId':typeId,
      'stuNum':$('header span label').attr('data')
    },
    success:function(res){
     if (res.res == '0') {
      return;
     }
    console.log(res);
    var openCourseValid = [];
    var openCourseNoValid = [];
    var labCourse = [];
    var dirCourse = [];
    for(var i = 0; i < res.data.length; i++){
      if (res.data[i].type_id == 'openCourse') {
        if (res.data[i].valid == '1') {
          openCourseValid.push(res.data[i]);
        }
        if (res.data[i].valid == '0') {
          openCourseNoValid.push(res.data[i]);
        }
      }
      if (res.data[i].type_id == 'labCourse') {
        labCourse.push(res.data[i]);
      }
      if (res.data[i].type_id == 'dirCourse') {
        dirCourse.push(res.data[i]);
      }
    }
    if (openCourseValid.length > 0 || openCourseNoValid.length > 0) {
      var data1 = {
        isAdmin: true,
        list:openCourseValid
      }
      var html1 = template('openValidTemplate',data1);
      document.getElementById('openValidTable').innerHTML = html1;
      $('#collapseOne').collapse('show');
      if (openCourseNoValid.length > 0) {
        var data2 = {
          isAdmin: true,
          list:openCourseNoValid
        }
        var html2 = template('openNoValidTemplate',data2);
        document.getElementById('openNoValidTable').innerHTML = html2;
      }
    }
    if (labCourse.length > 0) {
    var data3 = {
        isAdmin: true,
        list:labCourse
      }
      var html3 = template('labTemplate',data3);
      document.getElementById('labTable').innerHTML = html3;
      $('#collapseTwo').collapse('show');
    }
    if (dirCourse.length > 0) {
      var data4 = {
        isAdmin: true,
        list:dirCourse
      }
      var html4 = template('dirTemplate',data4);
      document.getElementById('dirTable').innerHTML = html4;
      $('#collapseThree').collapse('show');
    }
  }
  });
}
  // $(function () { $('#collapseTwo').collapse('show')});
  // $(function () { $('#collapseThree').collapse('show')});
  // $(function () { $('#collapseOne').collapse('show')});