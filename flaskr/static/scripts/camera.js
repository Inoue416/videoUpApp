let promise = null
let sound_on = null
let sound_off = null
let width = 350
let height = 480
let streaming = false
let video = null
let constrains = { video: {
    width: 480,
    height: 360,
    frameRate: 30,
    facingMode: 'user',
  },
  audio: true
}
let headerArea = null
let footerArea = null
let recorder = null
let record_data = null
let cameraOnButton = null
let cameraOffButton = null
let reRecordButton = null
let cameraButtonArea = null
let confirmVideo = null
let backButtonArea = null
let downloadButton = null
let attrtibuteArray = ['noActive','cameraOn']
let dataMessage = null
let mimeType = null
let attentionMessage = null
let cameraArea = null
let uploadingArea = null;
let uploadForm = null;
let base64_video_url = null
let base64_reader = null

function successCallback(stream){
  video.srcObject = stream;
  if(MediaRecorder.isTypeSupported("video/mp4")){
    mimeType = "video/mp4"
    //ext = "mp4"
  }
  else{
    mimeType = "video/webm\;codecs=vp9"
    //ext = "webm"
  }
  recorder = new MediaRecorder(stream, { mimeType : mimeType })
  recorder.ondataavailable = function (e) {
    var confirm = document.getElementById('confirm')
    confirm.setAttribute('controls', '')
    confirm.setAttribute('width', width)
    confirm.setAttribute('height', height)
    var outputdata = window.URL.createObjectURL(e.data)
    record_data=e.data
    let blob = new Blob([e.data], { type: mimeType })
    base64_reader = new FileReader()
    base64_reader.readAsDataURL(blob)
    confirm.src = outputdata
  }
  console.log('Start recordr.')
};

function errorCallback(err){
  console.log(err);
};

//カメラの起動
function startup() {
  video = document.getElementById('camera')
  promise = navigator.mediaDevices.getUserMedia(constrains)
  promise.then(successCallback).then(errorCallback);
}

//サウンドを再生する関数
function sound(element){
  element.play();
}

//ヘッダー・フッターの削除
function removeHeaderFooter(){
  headerArea.setAttribute('class', attrtibuteArray[0])
  /*s = footerArea.getAttribute('class')
  s += (' '+attrtibuteArray[0])
  footerArea.setAttribute('class', s)*/
}
//ヘッダー・フッターの追加
function addHeaderFooter(){
  headerArea.removeAttribute('class')
  /*s = footerArea.getAttribute('class')
  s = s.replace((' '+attrtibuteArray[0]), '')
  footerArea.setAttribute('class', s)*/
}

// 録画開始の関数
function setRecordOn(){
  s = cameraArea.getAttribute('class')
  s = s.replace(' cameraAreaOff', '')
  s += (' cameraAreaOn')
  cameraArea.setAttribute('class', s)
  camera.removeAttribute('class')
  //ヘッダー・フッターの非表示化
  removeHeaderFooter();
  //確認画面と投稿フォームの非表示化
  s = confirmVideo.getAttribute('class')
  s += (' '+attrtibuteArray[0])
  confirmVideo.setAttribute('class', s)
  s = uploadreRecordButton.getAttribute('class')
  s += (' '+attrtibuteArray[0])
  uploadreRecordButton.setAttribute('class', s)
  backButtonArea.removeAttribute('class')
  //カメラ画面と録画ボタン、読み上げ文章の表示
  s = cameraButtonArea.getAttribute('class')
  s = s.replace((' '+attrtibuteArray[0]), '')
  cameraButtonArea.setAttribute('class', s)
  dataMessage.removeAttribute('class')
  attentionMessage.removeAttribute('class')
  //録画開始ボタンを表示、停止ボタンを非表示
  s = cameraOnButton.getAttribute('class')
  s = s.replace((' '+attrtibuteArray[0]), '')
  cameraOnButton.setAttribute('class', s)
  s = cameraOffButton.getAttribute('class')
  s += (' '+attrtibuteArray[0])
  cameraOffButton.setAttribute('class', s)
}

// 録画停止の関数
function setRecordOff(){
  s = cameraOnButton.getAttribute('class')
  s += (' '+attrtibuteArray[0])
  cameraOnButton.setAttribute('class', s)
  s = cameraOffButton.getAttribute('class')
  s = s.replace((' '+attrtibuteArray[0]), '')
  cameraOffButton.setAttribute('class', s)
}
// 再録画の関数
function setReRecord(){
  s = cameraArea.getAttribute('class')
  s = s.replace(' cameraAreaOn', '')
  s += (' cameraAreaOff')
  cameraArea.setAttribute('class', s)
  addHeaderFooter(); //ヘッダー・フッターの表示
  //録画ボタンを非表示に
  s = cameraButtonArea.getAttribute('class')
  s += (' '+attrtibuteArray[0])
  cameraButtonArea.setAttribute('class', s)
  backButtonArea.setAttribute('class', attrtibuteArray[0])
  //カメラと読み上げ文章を非表示に
  dataMessage.setAttribute('class', attrtibuteArray[0])
  attentionMessage.setAttribute('class', attrtibuteArray[0])
  //カメラゾーンを非表示に
  camera.setAttribute('class', attrtibuteArray[0])
  // 録画内容と動画の投稿フォームを表示
  s = confirmVideo.getAttribute('class')
  s = s.replace((' '+attrtibuteArray[0]), '')
  confirmVideo.setAttribute('class', s)
  s = uploadreRecordButton.getAttribute('class')
  s = s.replace((' '+attrtibuteArray[0]), '')
  uploadreRecordButton.setAttribute('class', s)
  //ストリームのoff
  video.srcObject = null
}

// 録画機能のセットアップ
function setup(){
  cameraArea = document.getElementById("cameraArea")
  s = cameraArea.getAttribute('class')
  s += ' cameraAreaOn'
  cameraArea.setAttribute('class', s)
  uploadingArea = document.getElementById("uploadingArea")
  uploadingArea.setAttribute('class', 'noActive')
  uploadForm = document.getElementById("uploadForm")
  uploadForm.addEventListener('submit', function(){
    var els = this.elements;
    for (var i=0; i < els.length; i++){
      if(els[i].type == "submit"){
        els[i].disabled = true
      }
      if (els[i].type == "button"){
        els[i].disabled = true
      }
    }
    uploadingArea.removeAttribute('class')
    s = cameraArea.getAttribute('class')
    s += (' uplaodingAreaOn')
    cameraArea.setAttribute('class', s)
  });
  //ヘッダー・フッターを非表示
  headerArea = document.getElementById('headerArea')
  footerArea = document.getElementById('footerArea')
  s = footerArea.getAttribute('class')
  s += (' '+attrtibuteArray[0])
  footerArea.setAttribute('class', s)
  removeHeaderFooter();
  //録画内容ダウンロードボタン
  downloadButton = document.getElementById("downloadButton")
  //カメラ起動・停止の合図の音声
  sound_on = document.getElementById('sound_on')
  sound_off = document.getElementById('sound_off')
  //録画開始のイベントの定義
  dataMessage = document.getElementById("dataMessage")
  attentionMessage = document.getElementById("attentionMessage")
  cameraButtonArea = document.getElementById("cameraButtonArea")
  cameraOnButton = document.getElementById("cameraOnButton")
  cameraOffButton = document.getElementById('cameraOffButton')
  s = cameraOffButton.getAttribute('class')
  s += (' '+attrtibuteArray[0])
  cameraOffButton.setAttribute('class', s)
  reRecordButton = document.getElementById("reRecordButton")
  //録画内容の確認画面の要素を獲得
  confirmVideo = document.getElementById('confirmArea')
  s = confirmVideo.getAttribute('class')
  s += (' '+attrtibuteArray[0])
  confirmVideo.setAttribute('class', s)
  uploadreRecordButton = document.getElementById('uploadreRecordButton')
  s = uploadreRecordButton.getAttribute('class')
  s += (' '+attrtibuteArray[0])
  uploadreRecordButton.setAttribute('class', s)
  backButtonArea = document.getElementById("backButtonArea")

  //録画開始ボタンのイベントの定義
  cameraOnButton.addEventListener('click', function (ev){
    //録画onボタンの挙動
    setRecordOff();
    //録画開始
    sound(sound_on);
    window.setTimeout(function(){console.log('stop camera')}, 1000);
    recorder.start()
    ev.preventDefault()
  }, false);

  //録画停止のイベント定義
  cameraOffButton.addEventListener('click', function (ev){
    //録画の停止
    recorder.stop()
    //stream.getTracks().forEach(track => track.stop());
    sound(sound_off)
    window.setTimeout(function(){console.log('stop camera')}, 500);
    setReRecord();
  })

  //再録画のイベント定義
  reRecordButton.addEventListener('click', function (ev){
    setRecordOn();
    startup();
  })

  //ダウンロードのイベント定義
  downloadButton.addEventListener('click', function (ev){
    var blob = new Blob([record_data], { type: mimeType })
    let base64_video_url = base64_reader.result
    
    window.URL = window.URL || window.webkitURL;
    var URL = window.URL || window.webkitURL;
    var createObjectURL = URL.createObjectURL || webkitURL.createObjectURL;
    var url = createObjectURL(blob)
    var a = document.createElement('a')
    document.body.appendChild(a)
    a.style = 'display:none'
    a.href = url;
    var time = Date.now();
    a.download = (time)
    a.click();
    window.URL.revokeObjectURL(url);
    // console.log(base64_reader)
    console.log('base64 url: ', base64_video_url)
    base64_reader = null
  })
  startup();
  console.log('Complete setup.')
}
setup();
