console.log("WELCOME")

let songindex = 0
let audioElement = new Audio('songs/1.mp3')
let masterPlay = document.getElementById("masterPlay")
let myProgressBar = document.getElementById("myProgressBar")
let gif = document.getElementById("gif")
let songItem = Array.from( document.getElementsByClassName("songItem") )


let songs = [
    {songname:"glimpse",filePath:"songs/1.mp3",coverPath:"covers/1.jpg"},
    {songname:"faded",filePath:"songs/2.mp3",coverPath:"covers/2.jpg"},
    {songname:"idk",filePath:"songs/3.mp3",coverPath:"covers/3.jpg"},
    {songname:"random",filePath:"songs/4.mp3",coverPath:"covers/4.jpg"},
    {songname:"help",filePath:"songs/5.mp3",coverPath:"covers/5.jpg"}
]

songItem.forEach((element,i)=>{
    console.log(element+" "+i)
    element.getElementsByTagName('img')[0].src = songs[i].coverPath
})

//listen
//THE PLAY AND PAUSING OF THE SONG
masterPlay.addEventListener('click',()=>{
    if(audioElement.paused||audioElement.currentTime<=0){
        audioElement.play()
        masterPlay.classList.remove("fa-circle-play")
        masterPlay.classList.add("fa-circle-pause")
        gif.style.opacity = 1
    }
    else{
        audioElement.pause()
        masterPlay.classList.remove("fa-circle-pause")
        masterPlay.classList.add("fa-circle-play")
        gif.style.opacity = 0
    }
    
})


audioElement.addEventListener('timeupdate',()=>{
    //UPDATE THE SEEKBAR
    progress = parseInt((audioElement.currentTime/audioElement.duration)*100) //CONVERTS INTO INTERGER
    myProgressBar.value = progress
})

myProgressBar.addEventListener('change',()=>{
    audioElement.currentTime = myProgressBar.value * audioElement.duration/100
})
