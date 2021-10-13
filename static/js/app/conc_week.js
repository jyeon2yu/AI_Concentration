$('#conc-week-tab').click(function () {
    console.log('conc-week, 클릭 이벤트 성공!')
    // Draw a Chart
    let labels = ['월요일', '화요일', '수요일', '목요일', '금요일'];
    /*
      Ajax
      - url : 통신할 url,
      - type : GET / POST,
      - data : 전송할 데이터, JSON.stringify : JavaScript 값이나 객체를 JSON 문자열로 변환해주는 메서드
      - success, error : 통신이 성공/실패했을 때 실행되는 함수
    */
    $.ajax({
        url: "../conc_week/",
        type: "GET",
        // data: JSON.stringify(param),
        success: function (data) {
            console.log('conc-week Ajax Success!');
            console.log(data);

            // set data
            //console.log(data['week'].length); //print
            let data_list1 = [];
            let data_list2 = [];
            let data_list3 = [];
            let data_list4 = [];
            let data_list5 = [];
            for (step = 0; step < data['week'].length; step++) {
                data_list1.push((data['result'][step] / data['time'][step] * 100).toFixed(2));
                data_list2.push((data['korean'][step][1] / data['korean'][step][0] * 100).toFixed(2));
                data_list3.push((data['math'][step][1] / data['math'][step][0] * 100).toFixed(2));
                data_list4.push((data['english'][step][1] / data['english'][step][0] * 100).toFixed(2));
                data_list5.push((data['science'][step][1] / data['science'][step][0] * 100).toFixed(2));
                //console.log(data_list[step]);
            }

            myChart_conc1.data = {
                labels: labels,
                datasets: [{
                    label: "집중도(%)",
                    data: data_list1,
                    backgroundColor: 'rgb(255, 99, 132)',
                    borderColor: 'rgb(255, 99, 132)',
                    fill: false,
                    tension: 0.5
                }]
            };

            myChart_conc2.data = {
                labels: labels,
                datasets: [{
                    label: "집중도(%)",
                    backgroundColor: 'rgb(255, 99, 132)',
                    borderColor: 'rgb(255, 99, 132)',
                    data: data_list2
                }]
            };

            myChart_conc3.data = {
                labels: labels,
                datasets: [{
                    label: "집중도(%)",
                    backgroundColor: 'rgb(255, 99, 132)',
                    borderColor: 'rgb(255, 99, 132)',
                    data: data_list3
                }]
            };

            myChart_conc4.data = {
                labels: labels,
                datasets: [{
                    label: "집중도(%)",
                    backgroundColor: 'rgb(255, 99, 132)',
                    borderColor: 'rgb(255, 99, 132)',
                    data: data_list4
                }]
            };

            myChart_conc5.data = {
                labels: labels,
                datasets: [{
                    label: "집중도(%)",
                    backgroundColor: 'rgb(255, 99, 132)',
                    borderColor: 'rgb(255, 99, 132)',
                    data: data_list5
                }]
            };

            myChart_conc1.update();
            myChart_conc2.update();
            myChart_conc3.update();
            myChart_conc4.update();
            myChart_conc5.update();
        },
        error: function () {
            console.log("conc-week Ajax fail!");
        }
    })
});