document.getElementById('emotion-daily-tab').onclick = function() {
    console.log('emotion-daily, 클릭 이벤트 성공!')
    $.ajax({
        url: "../emotion_daily/",
        type: "GET",
        success: function (data) {
            console.log('emotion-daily Ajax Success!');

            // change a image
            let daily_emotion = document.getElementsByClassName('daily_emotion');
            let daily_ko_emotion = document.getElementsByClassName('daily_ko_emotion');
            let daily_ma_emotion = document.getElementsByClassName('daily_ma_emotion');
            let daily_en_emotion = document.getElementsByClassName('daily_en_emotion');
            let daily_sc_emotion = document.getElementsByClassName('daily_sc_emotion');

            // change a text
            let daily_rank_title = document.getElementsByClassName('emotion-daily-rank');
            let daily_rank_ko_title = document.getElementsByClassName('emotion-daily-ko-rank');
            let daily_rank_ma_title = document.getElementsByClassName('emotion-daily-ma-rank');
            let daily_rank_en_title = document.getElementsByClassName('emotion-daily-en-rank');
            let daily_rank_sc_title = document.getElementsByClassName('emotion-daily-sc-rank');

            for (let i = 0; i < daily_emotion.length; i++) {
                daily_emotion[i].src = data['today_emo'][i][2]; //daily emotion top3
                daily_ko_emotion[i].src = data['korean'][i][2]; //korean emotion top3
                daily_ma_emotion[i].src = data['math'][i][2];   //math emotion top3
                daily_en_emotion[i].src = data['english'][i][2];//english emotion top3
                daily_sc_emotion[i].src = data['science'][i][2];//science emotion top3

                daily_rank_title[i].innerText = data['today_emo'][i][0];
                daily_rank_ko_title[i].innerText = data['korean'][i][0];
                daily_rank_ma_title[i].innerText = data['math'][i][0];
                daily_rank_en_title[i].innerText = data['english'][i][0];
                daily_rank_sc_title[i].innerText = data['science'][i][0];
            }

            //$('#today_1').attr(src, "/static/img/emo_2.png");
            //document.getElementById('today_1').src=src_path(data['today_emo'][0]);
        },
        error: function () {
            console.log("emotion-daily Ajax fail!");
        }
    })
}

// $('#emotion-daily-tab').click(function () {
    

// });