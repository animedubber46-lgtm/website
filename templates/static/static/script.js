const player = document.getElementById("player");
const uploadInput = document.getElementById("videoUpload");
const shareLink = document.getElementById("shareLink");

function uploadVideo(){
    const file = uploadInput.files[0];
    if(!file) return alert("Select video");
    if(file.size > 10*1024*1024*1024) return alert("Max 10GB");

    const formData = new FormData();
    formData.append('video', file);

    fetch('/upload',{method:'POST',body:formData})
    .then(res=>res.text())
    .then(data=>{
        shareLink.innerHTML=data;
    })
    .catch(err=>alert("Upload failed"));
}

// Block dev tools & common shortcuts
document.addEventListener('keydown', e=>{
    if(e.ctrlKey && ["s","u","c","x","i","j"].includes(e.key.toLowerCase())){
        e.preventDefault();
        alert("Action blocked!");
    }
});

// Snowfall Animation
const canvas=document.getElementById("snowCanvas");
const ctx=canvas.getContext("2d");
canvas.width=window.innerWidth;
canvas.height=window.innerHeight;
let snow=[];
for(let i=0;i<200;i++){
    snow.push({x:Math.random()*canvas.width,y:Math.random()*canvas.height,r:Math.random()*4+1,d:Math.random()*1});
}
function drawSnow(){
    ctx.clearRect(0,0,canvas.width,canvas.height);
    ctx.fillStyle="white";
    ctx.beginPath();
    for(let f of snow){ctx.moveTo(f.x,f.y);ctx.arc(f.x,f.y,f.r,0,Math.PI*2);}
    ctx.fill();
    updateSnow();
}
function updateSnow(){for(let f of snow){f.y+=Math.pow(f.d+1,0.5);f.x+=Math.sin(f.d);if(f.y>canvas.height){f.y=0;f.x=Math.random()*canvas.width;}}}
setInterval(drawSnow,30);
window.addEventListener("resize",()=>{canvas.width=window.innerWidth;canvas.height=window.innerHeight;});
