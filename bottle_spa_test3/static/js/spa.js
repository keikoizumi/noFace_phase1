//グローバル変数
var items = [];
//var tUrl = 'http://192.168.179.5:8080/';
//var tUrl = 'http://437b5552.ngrok.io/';
//var tUrl = 'http://noFace.com:8080/';
var tUrl = 'http://localhost:8080/';

var all = 'all';
var otherOne = 'yahoo';
var otherTow = 'buzzfeed';

//上限回数       
var setTimes = 200;
//チェック関数
function checkId(data) {
         var id = '';
         id = data.id;
         //見つからない場合は-1
         if (items.indexOf(id) == -1) {
            if (checkTimes(items)) {
              items.push(id);    
              addTags(data);
              console.log('通信成功');              
            }
         } else { 
          　if (checkTimes(items)) {
              items.push('NG');
              random();
            } else {
              items.push('NG');
            } 
         }  
}

function today() {
  /** 現在のDateオブジェクト作成 */
  var d = new Date();
 
  /** 日付を文字列にフォーマットする */
  var formatted = `${d.getFullYear()}-${(d.getMonth()+1).toString().padStart(2, '0')}-${d.getDate().toString().padStart(2, '0')}`;
  console.log(formatted);
  return formatted;

}

function checkTimes(items) {
    if (items.length >= (setTimes)) {
        //alert('上限回数を超えました。リロードされます。');
        window.location.reload();
        return false;
    } else {
        return true;
    }   
}

function random() {  
  $(function(){
    var targetUrl = tUrl+'random';
    var date = today();
    var request = {
        'date' : date
    };
      $.ajax({
          url: targetUrl,
          type: 'POST',
          contentType: 'application/JSON',
          dataType: 'JSON',
          data : JSON.stringify(request),
          scriptCharset: 'utf-8',
      }).done(function(data){ 
          /* 通信成功時 */
          if (data == null || data == '' || data[0] == '') {
            $('#table').empty();
            $('#iimg').empty();
            $('#table').append('<tr><td>1</td><td>データがありません</td></tr>');
          } else {
            checkId(data); 
          }
        }).fail(function(data, XMLHttpRequest, textStatus) {
          /* 通信失敗時 */
          alert('通信失敗');
          console.log('通信失敗');
          console.log(data);
          console.log("XMLHttpRequest : " + XMLHttpRequest.status);
          console.log("textStatus     : " + textStatus);
      });
  });
}

function other(other,pastDate) {

  var targetUrl = tUrl+'other';
  var date = null;

  if (pastDate == null || pastDate == '') {
    date = today();  
  } else {
    date = pastDate;
  }

  if (date != null) {
    if (other == all) {
      var request = {
          'date' : date,
          'other': all
      };
    } else if (other == otherOne) {
      var request = {
          'date' : date,
          'other': otherOne
      };
    } else if (other == otherTow) {
      var request = {
          'date' : date,
          'other': otherTow
      };  
    }
  } else {
    alert('不正な日付');
    var request = {
      'date' : today(),
      'other': all
    };
  }

  $(function() {
      $.ajax({
          url: targetUrl,
          type: 'POST',
          contentType: 'application/JSON',
          dataType: 'JSON',
          data : JSON.stringify(request),
          scriptCharset: 'utf-8',
      }).done(function(data) { 
          /* 通信成功時 */
          if (data == null || data == '' || data[0] == '') {
            $('#table').empty();
            $('#iimg').empty();
            $('#table').append('<tr><td>1</td><td>データがありません</td></tr>');
          } else {
            show(data); 
          }
          console.log(data);        
        }).fail(function(data, XMLHttpRequest, textStatus) {
          /* 通信失敗時 */
          alert('通信失敗');
          console.log('通信失敗');
          console.log(data);
          console.log("XMLHttpRequest : " + XMLHttpRequest.status);
          console.log("textStatus     : " + textStatus);
      });
  });
}

function getPastDay() {  
  $(function(){
    var targetUrl = tUrl+'getPastDay';
    
      $.ajax({
          url: targetUrl,
          type: 'POST',
          contentType: 'application/JSON',
          dataType: 'JSON',
          data : null,
          scriptCharset: 'utf-8',
      }).done(function(data) { 
          /* 通信成功時 */
          if (data == null || data == '' || data[0] == '') {
            $('#table').empty();
            $('#iimg').empty();
            $('#table').append('<tr><td>1</td><td>データがありません</td></tr>');
          } else {
            console.log(data[1]);
            console.log(data.length);
            for (var i = 0; i < data.length; i++) {
              $("#ddmenu").append('<option value="'+data[i].dt+'">'+data[i].dt+'</a>');
            }
          }
        }).fail(function(data, XMLHttpRequest, textStatus) {
          /* 通信失敗時 */
          alert('通信失敗');
          console.log('通信失敗');
          console.log(data);
          console.log("XMLHttpRequest : " + XMLHttpRequest.status);
          console.log("textStatus     : " + textStatus);
      });
  });
}


//初回アクセス時
window.onload = function() {
  //today;
  //other(all,pastDate);
  //プルダウンデータ取得
  getPastDay();
}

//noFace
$(function(){ 
  $('#start').on('click',function(){
    scraping();
  });
});

//TODAY(OTHER)
$(function() {
  $('.other').on('click',function() {
    var id = $(this).attr('id');
    var pastDate = null;
    if (timerID != null) {
      countStop();
    }
    if (id == all) {
      other(all,pastDate);
    } else if (id == otherOne) {
      other(otherOne,pastDate);
    } else if (id == otherTow) {
      other(otherTow,pastDate);
    }
  });
});

//プルダウン選択時
$(function() {
  $('#ddmenu').on('click',function() {
    if (timerID != null) {
      countStop();
    }
    var pastDate = $("#ddmenu").val();
    other(all,pastDate);
    console.log(pastDate);
  });
});

//リセット
$(function() {
  $('.reset').on('click',function() {
    //リロード
    window.location.reload();
  });
});

function addTags(data) {
  imgId = data.img_id;
  console.log('aaaaaaaaaaaaaaaaaaaaaaaaaaaa');
  $(function() {
    $('#table').empty();
    //$('#table').append('<tr><td>1</td><td><a href='+data.url+' target="_blank">'+data.title+'</a></td></tr>');
  });
  $(function() {
    $('#iimg').empty();
    //$('#iframe').append('<iframe style="border:none" src='+'"'+data.url+'"'+'width=111 height=70>'+'</iframe>');
    $('#iimg').append('<img src="./static/img/20200118/D142902.png" width="1000" height="500" alt="テスト">');
  });  
}

//その他
function show(data) {
  $(function() {
    var dirDay = today();
    var dirNaeme = dirDay.replace( /-/g , "" ) ;
    console.log(data);
    console.log(dirNaeme);
    $('#table').empty();
    $('#iimg').empty();
    for (var i = 0; i < data.length; i++) {
      var id = i+1;
      $('#table').append('<tr><td>'+id+'</td><td><a href='+data[i].url+' target="_blank">'+data[i].title+'</a><a href='+data[i].url+' target="_blank"><img src="./static/img/Selenium/'+dirNaeme+'/'+data[i].img_id+'.png" width="350" height="200" alt="no image"></a></td></tr>');
    }  
  });
}
