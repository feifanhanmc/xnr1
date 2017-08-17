var task_id='WXNR0001',phone='13192883429',uid='1897879843';
var name1,name2,password;
$('#go_bind').on('click',function () {
    name1=$('#username1').val();
    name2=$('#username2').val();
    password=$('#passwords').val();
    if ((name1==''||name2=='')&&password==''){
        $('#_bind_per #information').text('账号名密码不能为空。');
    }else {
        $('#_bind_per #information').text('是否将该微博用户绑定为虚拟人？');
    }
    $('#_bind_per').modal('show');
});
function bindSF(data) {
    var txt='';
    if (data){
        txt='绑定成功';
        var listURL='/weibo_xnr_create/recommend_follows/?monitor_keywords='+basicData_1.monitorKeywords+
            '&daily_interests='+basicData_1.daily;
        public_ajax.call_request('get',listURL,list);
    }else {
        txt='抱歉，系统网络原因，绑定失败';
        $('.backTWO').show();
        $('.notBind').hide();
        $('.sureBind').hide();
    }
    $('#success_fail #fs').text(txt);
    $('#success_fail').modal('show');
}
function userLIST() {
    var bind_url='/weibo_xnr_create/save_step_three_1/?nick_name='+basicData_2.nick_name+'&weibo_mail_account='+name1 +
        '&weibo_phone_account='+name2+'&password='+password;
    public_ajax.call_request('get',bind_url,bindSF);
}
function list(person) {
    var str1='',str2='';
    if (isEmptyObject(person.daily_interests)){
        str1='暂无数据';
        $('#success_fail .personlist1').css({textAlign:'center'});
    }else {
        for (var y in person.daily_interests){
            str1+=
                '<label class="demo-label" title="'+person.daily_interests[y]+'">'+
                '   <input class="demo-radio" type="checkbox" name="someone" value="'+y+'">'+
                '   <span class="demo-checkbox demo-radioInput"></span> '+person.daily_interests[y]+
                ' </label>';
        }
    };

    if (isEmptyObject(person.monitor_keywords)){
        str2='暂无数据';
        $('#success_fail .personlist2').css({textAlign:'center'});
    }else {
        for (var p in person.monitor_keywords){
            str2+=
                '<label class="demo-label" title="'+person.monitor_keywords[p]+'">'+
                '   <input class="demo-radio" type="checkbox" name="someone" value="'+p+'">'+
                '   <span class="demo-checkbox demo-radioInput"></span> '+person.monitor_keywords[p]+
                ' </label>';
        }
    };
    $('#success_fail .personlist1').html(str1);
    $('#success_fail .personlist2').html(str2);
}
$('#back').on('click',function () {
    window.open('/personalCenter/individual/');
});
$('.backTWO').on('click',function () {
    window.location.href='/registered/virtualCreated/';
})
$('#release').on('click',function () {
    window.open('/registered/posting/');
});
function surefocus() {
    let people=[];
    $("[name=someone]:checkbox:checked").each(function (index,item) {
        people.push($(this).val());
    });
    let focus_url='/weibo_xnr_create/save_step_three_2/?nick_name='+basicData_2.nick_name+'&followers_uids='+people.join(',');
    console.log(focus_url)
    public_ajax.call_request('get',focus_url,focusSF);
}
function focusSF(data) {
    var txt='';
    if (data){
        txt='关注人物成功';
        $('.lastGO').show();
    }else {
        txt='抱歉，系统网络原因，关注人物失败';
    }
    $('#letGo p').text(txt);
    $('#letGo').modal('show');
}