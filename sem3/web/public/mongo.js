var array = []
var count = -1
var ro=0;
var po=0;
var kp=0;
var ra=0;

function rock(){
    if(ro==0)
    {
        document.getElementsByClassName("rock")[0].style.backgroundColor="green"
        count = count + 1
        array[count] = "rock"
        ro = 1;
    }
    else
    {
        document.getElementsByClassName("rock")[0].style.backgroundColor="#2ad767"
        count = count -1
        ro = 0;
    }
    //array[count] = "rock"
    //count = count+1
    //document.getElementsByClassName("rock")
    console.log(count)
    console.log(array)
}
function pop(){
    if(po==0)
    {
        document.getElementsByClassName("pop")[0].style.backgroundColor="green"
        count = count + 1
        array[count] = "pop"
        po = 1;
    }
    else
    {
        document.getElementsByClassName("pop")[0].style.backgroundColor="#2ad767"
        count = count -1
        po = 0;
    }
    //array[count] = "rock"
    //count = count+1
    //document.getElementsByClassName("rock")
    console.log(count)
    console.log(array)
}
function kpop(){
    if(kp==0)
    {
        document.getElementsByClassName("kpop")[0].style.backgroundColor="green"
        count = count + 1
        array[count] = "kpop"
        kp = 1;
    }
    else
    {
        document.getElementsByClassName("kpop")[0].style.backgroundColor="#2ad767"
        count = count -1
        kp = 0;
    }
    //array[count] = "rock"
    //count = count+1
    //document.getElementsByClassName("rock")
    console.log(count)
    console.log(array)
}
function rap(){
    if(ra==0)
    {
        document.getElementsByClassName("rap")[0].style.backgroundColor="green"
        count = count + 1
        array[count] = "rap"
        ra = 1;
    }
    else
    {
        document.getElementsByClassName("rap")[0].style.backgroundColor="#2ad767"
        count = count -1
        array[count] = NULL
        ra = 0;
    }
    //array[count] = "rock"
    //count = count+1
    //document.getElementsByClassName("rock")
    console.log(count)
    console.log(array)
}



