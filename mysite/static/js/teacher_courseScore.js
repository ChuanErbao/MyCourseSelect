// $('#submit').on('click', function() {
//     submit();
// });

var btns = Array.from(document.getElementsByTagName('button'))
btns.forEach(ele => {

    ele.onclick = e => {

        var formData = new FormData();
        formData.append("file", $('#' + ele.id + "stu_score")[0].files[0]);
        formData.append("course_no", $('#' + ele.id + 'course_no').val());
        // alert($('#' + ele.id + 'course_no').val());
        var filename = $('#' + ele.id + "stu_score")[0].files[0].name;
        var fileType = filename.substring(filename.lastIndexOf(".") + 1).toLowerCase();
        if (fileType != "xls" && fileType != "xlsx") {
            alert("请选择.xls的文件");
            return
        }
        var token = $.cookie('csrftoken');
        $.ajax({
            type: "post",

            headers:{
                 "X-CSRFToken": token
            },
            url: $('#url').val(),
            dataType: "json",
            data: formData,
            processData: false,
            contentType: false, //必须
            success: function(response) {
                alert(response.msg);
                return;
            }
        });

    }

})

// 登录
// function submit() {
//     var formData = new FormData();
//     formData.append("file", $("#stu_score")[0].files[0]);
//     formData.append("course_no", $('#course_no').val());
//     var filename = $("#stu_score")[0].files[0].name;
//     var fileType = filename.substring(filename.lastIndexOf(".") + 1).toLowerCase();
//     if (fileType != "xls" && fileType != "xlsx") {
//         alert("请选择.xls的文件");
//         return
//     }
//     $.ajax({
//         type: "post",
//         url: $('#url').val(),
//         dataType: "json",
//         // data: {
//         //     'stu_score': formData,
//         //     'course_no': $('#course_no').val()
//         // },
//         data: formData,
//         processData: false,
//         contentType: false, //必须
//         success: function(response) {
//             alert(response.msg);
//             return;
//         }
//     });
// }