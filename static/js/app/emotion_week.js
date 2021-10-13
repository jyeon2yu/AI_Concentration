$('#emotion-week-tab').click(function () {
    console.log('emotion-week, 클릭 이벤트 성공!')
    $.ajax({
        url: "../emotion_week/",
        type: "GET",
        // data: JSON.stringify(param),
        success: function (data) {
            console.log('emotion-week Ajax Success!');

            // change a image
            let week_emotion = document.getElementsByClassName('emotion_week');
            let week_ko_emotion = document.getElementsByClassName('week_ko_emotion');
            let week_ma_emotion = document.getElementsByClassName('week_ma_emotion');
            let week_en_emotion = document.getElementsByClassName('week_en_emotion');
            let week_sc_emotion = document.getElementsByClassName('week_sc_emotion');

            // change a text
            let week_rank_title = document.getElementsByClassName('emotion-week-rank');
            let week_rank_ko_title = document.getElementsByClassName('emotion-week-ko-rank');
            let week_rank_ma_title = document.getElementsByClassName('emotion-week-ma-rank');
            let week_rank_en_title = document.getElementsByClassName('emotion-week-en-rank');
            let week_rank_sc_title = document.getElementsByClassName('emotion-week-sc-rank');


            for (let i = 0; i < week_emotion.length; i++) {
                week_emotion[i].src = data['week_emo'][i][2]; //daily emotion top3
                week_ko_emotion[i].src = data['korean'][i][2]; //korean emotion top3
                week_ma_emotion[i].src = data['math'][i][2];   //math emotion top3
                week_en_emotion[i].src = data['english'][i][2];//english emotion top3
                week_sc_emotion[i].src = data['science'][i][2];//science emotion top3

                week_rank_title[i].innerText = data['week_emo'][i][1];
                week_rank_ko_title[i].innerText = data['korean'][i][1];
                week_rank_ma_title[i].innerText = data['math'][i][1];
                week_rank_en_title[i].innerText = data['english'][i][1];
                week_rank_sc_title[i].innerText = data['science'][i][1];
            }


        },
        error: function () {
            console.log("emotion-week Ajax fail!");
        }
    })
});