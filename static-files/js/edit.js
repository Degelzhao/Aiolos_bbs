console.log('edit starting...');

$(function($) {
    $('#btn-edit-question').click(function() {
        // let user = $('#question-user');
        // console.log(user.text());
        if($(this).text() == '编辑'){
            $(this).text('更新');
            let input_text = $('#question-text').text();
            let input = '<input id="question-text-input" class="mb-0  lh-100" type="text" value="' + input_text + ' ">';
            let input_desc = $('#question-desc').text();
            let textarea = '<textarea id="question-desc-input" class="p-3 text-dark-50 bg-light rounded box-shadow form-control">' + input_desc + '</textarea>';
            
            // <div class="p-3 text-white-50 bg-success rounded box-shadow" id="question-desc">
            // {{ question.question_desc }}
            // </div>
            // let input = '<input id="question-text-input" class="mb-0 lh-100" type="text" value="{{ question.question_text }}">'
            console.log(input_desc, textarea)
            $('#question-text').replaceWith(input);
            $('#question-desc').replaceWith(textarea);
        } else { // btn 更新
            $(this).text('编辑');
            console.log('更新数据...');
            // ajax post data
            // $.post("/topic", {
            $.post("/topic-update/", {
                'pk': $('#question-id').text(),
                'question_text': $('#question-text-input').val(),
                'question_desc': $('#question-desc-input').val(),
                'csrfmiddlewaretoken': $('[name="csrfmiddlewaretoken"]').val()
            }, function(data){
                console.log('修改成功1');
                let h6 = '<h6  id="question-text" class="mb-0 text-white lh-100">' + $('#question-text-input').val() + '</h6>'
                let div = '<div class="p-3 text-white-50 bg-success rounded box-shadow" id="question-desc">'
                + $('#question-desc-input').val()
             '</div>'
                $('#question-text-input').replaceWith(h6);
                $('#question-desc-input').replaceWith(div);
                $(this).text('编辑');
            })
            // 修改页面
            console.log('修改成功2');

        }
    })
    
    // 把对象转为url
    function getObjectURL(file) {
        var url = null; 
        if (window.createObjectURL != undefined) { // basic
            url = window.createObjectURL(file);
        } else if (window.URL != undefined) { // mozilla(firefox)
            url = window.URL.createObjectURL(file);
        } else if (window.webkitURL != undefined) { // webkit or chrome
            url = window.webkitURL.createObjectURL(file);
        }
        return url;
    };
    
    // 预览图片
    $("#user_picture").change(function(){
        var objUrl = getObjectURL(this.files[0]);
        console.log("objUrl = "+ objUrl);
        if (objUrl) {
            $("#user_picture_img").attr("src", objUrl);
        }
    });

});