// create javasecript object
const user_id = '1234';
const param = {
  'user_id': user_id
}

$('#conc-daily-tab').click(function(){
  const conc_daily_labels = ['집중', '이석', '졸음'];
  const colors =['red','skyblue','yellowgreen'];

  console.log('conc-daily, 클릭 이벤트 성공!');

  $('#conc_title').text("오늘의 집중도 분석 결과");
  console.log(document.getElementById('conc_title'));

  $.ajax({
    url : "../conc_daily/",
    type: "GET",
    success: function(data) {
      console.log("conc-daily Ajax Success!");
      console.log(data);

      let data1 = [data.today_conc.eye_close, data.today_conc.not_seat, data.today_conc.conc_time]

      console.log(data1)        


    },
    error: function(){
      console.log("conc-daily Ajax fail!");
    }
  })
});