play1=document.getElementById("music_play1");
play2=document.getElementById("music_play2");
play3=document.getElementById("music_play3");
play4=document.getElementById("music_play4");
play5=document.getElementById("music_play5");
play6=document.getElementById("music_play6");
musicList = [play1, play2, play3, play4, play5, play6];
musicListName = ["G_D_N_A-yoyoyoyo", "國蛋GorDoN-紐約鄰居", "國蛋GorDoN-Diary Freestyle pt.2", "The Marias-Ruthless", "Clairo-Sofia", "PUZZLEMAN LIVE-香草奶昔"];
var index =0; 

function start() {
    var player = musicList[index];
    var song = musicListName[index];
   
    var dur = player.duration;
    var s1 = parseInt(dur % 60);
    var m1 = parseInt((dur/ 60) % 60);
    document.getElementById("dur_time").innerHTML = "<font color='blue' size='5'>" + m1 + "分" + s1 + "秒"+"</font>";
 
    setInterval("calTime()", 1000);
    // 跑馬燈顯示正播放的歌曲名稱
    info.innerHTML = "現在正在播放" + song;player.play();
}

function pause() {
    var player = musicList[index];
    player.pause();
    info.innerHTML = "你按到暫停啦!!"
}

function next() {
    var player = musicList[index];
    player.pause();
    index += 1;
    if(index >= musicList.length) {
        index=0;
    }
    var player = musicList[index];
    start();
}
function previous() {
    var player = musicList[index];
    player.pause();
    index -= 1;
    if(index < 0) {index= musicList.length -1;
    }
    var player = musicList[index];
    start();
}

function upVolume() {
    var player = musicList[index];
    var volume = player.volume    + 0.1;
    if(volume >=1 ){
        volume = 1 ;
    }
    player.volume = volume;
    start();
}
function downVolume() {
    var player = musicList[index];
    var volume = player.volume   -0.1;
    if(volume <= 0 ){
        volume = 0 ;
    }
    player.volume =    volume;
    start();
}
function calTime(){
    var player = musicList[index];
     var cur = player.currentTime;
     var s2 = parseInt(cur % 60);
     var m2 = parseInt((cur / 60) % 60);
     document.getElementById("cur_time").innerHTML = "<font color='red' size='5'>" + m2 + "分" + s2 + "秒"+"</font>";
    }       