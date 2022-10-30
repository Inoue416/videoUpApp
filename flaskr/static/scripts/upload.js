let uploadingArea = null;
let cameraArea = null;
let uploadForm = null;


function setUpUploadedEvent(){
  cameraArea = document.getElementById("cameraArea")
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
}
setUpUploadedEvent();
