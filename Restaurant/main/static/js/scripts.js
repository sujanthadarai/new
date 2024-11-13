let tabcontents=document.getElementsByClassName('tab-content');
let tablinks =document.getElementsByClassName('tab-links');

function openlink(arg){
    for(let tabcontent of  tabcontents){
        tabcontent.classList.remove("active-tab");
    }
    for(let tablink of tablinks){
        tablink.classList.remove('active');
    }
    document.getElementById(arg).classList.add('active-tab');
    event.currentTarget.classList.add("active")

}
