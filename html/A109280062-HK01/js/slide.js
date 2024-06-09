
var imgFile = [];
var fileNum = 5;
var main = document.querySelector('.main');
var thumb = document.querySelector('.thumb');


var startNum = 0; // first image
var pageBox = document.querySelector('.page');

var timer = null;

//------------------------------
// create image filename
//------------------------------
for (let i=0; i<fileNum; i++){
	let name = `work${i+1}`;
	imgFile.push(name);
}
//------------------------------
// create page button
//------------------------------
// for (let i=0; i<fileNum; i++){
// 	let page = document.createElement('span');
// 	page.num = i;
// 	page.innerHTML = i+1;
// 	pageBox.appendChild(page);
// }
// let pages = pageBox.getElementsByTagName('span');
// function active(page_num){
// 	Array.from(pages).forEach(function(item){
// 		item.className = '';
// 	})
// 	pages[page_num].className = 'active'; 
// }
// active(startNum);
//-----------------------
// page button
//-----------------------
// Array.from(pages).forEach(function(item){
// 	item.onclick = function(){
// 		startNum = this.num;
// 		stopPlay();
// 		imgShow(this.num);
// 		active(this.num);
// 		startPlay();
// 	}
// 	if (screen.width > 768){
// 		item.onmouseover = function(){
// 			thumb.classList.add('show');
// 			thumb.src = `photos/${imgFile[this.num]}.jpeg`;
// 		}
// 		item.onmouseout = function(){
// 			thumb.classList.remove('show');
// 		}
// 	}
// })
//-------------------------
// dynamic image
//-------------------------
function imgShow(img_num){
	main.src = `photos/${imgFile[img_num]}.jpg`;
}
imgShow(startNum);
//-------------------------
// arrow button
//-------------------------
// prev.addEventListener('click',function(){arrow('prev')});
// next.addEventListener('click',function(){arrow('next')});

function arrow(dir){
	let first = dir=='next'? 0 : fileNum-1;
	let end = dir=='next'? fileNum-1 : 0;
	if (startNum == end){
		startNum = first
	} else{
		dir=='next'? startNum += 1 : startNum -= 1
	}
	stopPlay();
	imgShow(startNum);
	active(startNum);
	startPlay();
}
//-------------------------
// keyboard
//-------------------------
// document.onkeydown = function(e) {
// 	if (e.keyCode === 37){
// 		prev.click();
// 	} else if (e.keyCode === 39){
// 		next.click();
// 	}
// }
//-------------------------
// autoplay
//-------------------------
startPlay();

function startPlay(){
	if (timer == null){
		timer = setInterval(function(){
			startNum++;
			if (startNum >= fileNum){
				startNum = 0
			}
			imgShow(startNum);
			// active(startNum);
		}, 3000)
	}
}

function stopPlay(){
	clearInterval(timer);
	timer = null;
}