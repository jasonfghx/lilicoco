var seqImg = new Array(6);
var seqImg_length = seqImg.length; 

for (var i = 1; i <= seqImg_length; i++) {
    seqImg[i-1]="photos/work" + i + ".jpg";
}

setInterval("sequentialImg()", 1500);   
var i=0;           
function sequentialImg(){   
    document.getElementById("seq_div").innerHTML = "<img src='"+seqImg[i]+"' class='mt-4 mb-4 d-block mx-auto'>";
    i++;
    if(i >= seqImg_length) {
        i=0;
    }
}

var ranImg = new Array(6);
for (var j = 1; j <= ranImg.length; j++) {
    ranImg[j-1]="photos/work" + j + ".jpg";
}

setInterval("randomImg()", 1500);

function randomImg(){
         var imgIndex = Math.floor(Math.random()*ranImg.length);     
         document.getElementById("ran_div").innerHTML    = "<img src='"+ranImg[imgIndex]+"' class='mt-4 mb-4 d-block mx-auto' >";
}