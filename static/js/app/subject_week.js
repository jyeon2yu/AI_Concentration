
document.getElementById('subject-week-tab').onclick = function () {
    $.ajax({

        url: '../subject_data_week/',
        success: function (res) {
            let emotions = res;
            console.log('1주 과목 ajax 성공', res)

            const subject_frame = document.getElementById('subject_frame2')
            subject_frame2.innerHTML = `
              <div class='row'>
                <div class='col-lg-6 col-sm-6'>
                  <div class='card'>

                    <div class='card-body'>
                      <span class='text-font' style='margin-left : 20px; display : block;'>국어</span>

                      <div style='display: flex; justify-content: center;'>
                        <div class='image-box' style='text-align: center;'>
                            <img style='max-width : 100%; height : auto; vertical-align:middle;' src="../../static/img/grade_` + res['conc'][1] + `.png" alt="grade_korean.png">
                        </div>

                        <div class='image-box'>
                          <img style='max-width : 100%; height : auto; vertical-align:middle;' src="../../static/img/` + res['emotions'][1] + `.png" alt="emotion_korean.png">
                        </div>
                      </div>
                      
                    </div> <!-- card-body -->

                  </div>
                </div> <!-- column -->

                <div class='col-lg-6 col-sm-6'>
                  <div class='card'>

                    <div class='card-body'>
                      <span class='text-font' style='margin-left : 20px; display : block;'>수학</span>

                      <div style='display: flex; justify-content: center;'>
                        <div class='image-box' style='text-align: center;'>
                            <img style='max-width : 100%; height : auto; vertical-align:middle;' src="../../static/img/grade_` + res['conc'][2] + `.png" alt="grade_math.png">
                        </div>

                        <div class='image-box'>
                          <img style='max-width : 100%; height : auto; vertical-align:middle;' src="../../static/img/` + res['emotions'][2] + `.png" alt="emotion_math.png">
                        </div>
                      </div>
                      
                    </div> <!-- card-body -->

                  </div>
                </div> <!-- column -->

              </div> <!-- row -->

              <div class='row' >
                <div class='col-lg-6 col-sm-6'>
                  <div class='card'>

                    <div class='card-body'>
                      <span class='text-font' style='margin-left : 20px; display : block;'>영어</span>

                      <div style='display: flex; justify-content: center;'>
                        <div class='image-box' style='text-align: center;'>
                            <img style='max-width : 100%; height : auto; vertical-align:middle;' src="../../static/img/grade_` + res['conc'][0] + `.png" alt="grade_english.png">
                        </div>

                        <div class='image-box'>
                          <img style='max-width : 100%; height : auto; vertical-align:middle;' src="../../static/img/` + res['emotions'][0] + `.png" alt="emotion_english.png">
                        </div>
                      </div>
                      
                    </div> <!-- card-body -->

                  </div>
                </div> <!-- column -->

                <div class='col-lg-6 col-sm-6'>
                  <div class='card'>

                    <div class='card-body'>
                      <span class='text-font' style='margin-left : 20px; display : block;'>과학</span>

                      <div style='display: flex; justify-content: center;'>
                        <div class='image-box' style='text-align: center;'>
                            <img style='max-width : 100%; height : auto; vertical-align:middle;' src="../../static/img/grade_` + res['conc'][3] + `.png" alt="grade_science.png">
                        </div>

                        <div class='image-box'>
                          <img style='max-width : 100%; height : auto; vertical-align:middle;' src="../../static/img/` + res['emotions'][3] + `.png" alt="emotion_science.png">
                        </div>
                      </div>
                      
                    </div> <!-- card-body -->

                  </div>
                </div> <!-- column -->

              </div> <!-- row -->
              `;
        }

    }); //ajax
}// function