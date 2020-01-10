//グローバル変数
var items = [];
var all = 'all';
var otherOne = 'yahoo';
var otherTow = 'buzzfeed';

//上限回数       
var setTimes = 100;
//チェック関数
function checkId(data){
         var id = '';
         id = data.id;
         //見つからない場合は-1
         if (items.indexOf(id) == -1){
            if (checkTimes(items)) {
              items.push(id);    
              addTags(data);
              console.log('通信成功');
              console.log(data);
              console.log('items');
              console.log(items);
              console.log('-------------------------------------------------------------');
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
function today(){
  /** 現在のDateオブジェクト作成 */
  var d = new Date();
 
  /** 日付を文字列にフォーマットする */
  var formatted = `${d.getFullYear()}-${(d.getMonth()+1).toString().padStart(2, '0')}-${d.getDate().toString().padStart(2, '0')}`;
  console.log(formatted);
  return formatted;

}

function addTags(data){
  $('ol').empty();
  $(function() {
    $('ul').empty();
    $('ul').append('['+data.dt+']'+'</br>'+'<a href='+data.url+' target="_blank"><h2>'+data.title+'</h2></a>');
  });
  $(function() {
    $('#iframe').empty();
    $('#iframe').append('<iframe src='+'"'+data.url+'"'+'width=1250 height=600>'+'</iframe>');
  });
  
}

function show(data){
  $(function() {
    $('ul').empty();
    $('ol').empty();
    $('#iframe').empty();
    for (var i = 0; i < data.length; i++) {
      $('ol').append('<li><a href='+data[i].url+' target="_blank">'+data[i].title+'</a></li>');
    }  
  });
}


function checkTimes(items){
    if (items.length >= (setTimes)){
        alert('上限回数を超えました。リロードされます。');
        window.location.reload();
        return false;
    } else {
        return true;
    }   
}

function random(){  
  $(function(){
    var targetUrl = 'http://localhost:8080/random';
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
          if (data == null) {
             
            alert('データがありません');
          } else {
            console.log(data);
            checkId(data); 
          }
        }).fail(function(data, XMLHttpRequest, textStatus){
          /* 通信失敗時 */
          alert('通信失敗');
          console.log('通信失敗');
          console.log(data);
          console.log("XMLHttpRequest : " + XMLHttpRequest.status);
          console.log("textStatus     : " + textStatus);
      });
  });
}

function other(other){

  var targetUrl = 'http://localhost:8080/other'
  var date = today();

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
  } else {
    console.log('NG');
  }

  $(function(){
      $.ajax({
          url: targetUrl,
          type: 'POST',
          contentType: 'application/JSON',
          dataType: 'JSON',
          data : JSON.stringify(request),
          scriptCharset: 'utf-8',
      }).done(function(data){ 
          /* 通信成功時 */
          if (data == null) {
            alert('データがありません');
          } else {
            show(data); 
          }
          console.log(data);        
        }).fail(function(data, XMLHttpRequest, textStatus){
          /* 通信失敗時 */
          alert('通信失敗');
          console.log('通信失敗');
          console.log(data);
          console.log("XMLHttpRequest : " + XMLHttpRequest.status);
          console.log("textStatus     : " + textStatus);
      });
  });
}


/*function setTimer(){
  var startRandom = function(){
    random();
  };
  var setStartInterval = setInterval(startRandom, 3000);
  return setStartInterval;
}

var setStartInterval;
window.onload = function(){
// ページ読み込み時に実行したい処理
  setStartInterval = setTimer()
}
*/

$(function(){ 
  $('#start').on('click',function(){
    random();
    console.log('start');
  });
});

$(function(){
  $('.other').on('click',function(){
    var id = $(this).attr('id');
    console.log(id);
    if (id == all) {
      other(all);
    } else if (id == otherOne) {
      other(otherOne);
    } else if (id == otherTow) {
      other(otherTow);
    }
  });
});

$(function(){
  $('.reset').on('click',function(){
    window.location.reload();
  });
});

$(function(){
  $('.reset').on('click',function(){
    window.location.reload();
  });
});

$('#area').change(function() {
    var r = $('option:selected').val();
    
    console.log(r);
})
