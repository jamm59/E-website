const swt_btn = document.querySelector('.switch');
const moon = document.querySelector('.switch i');
const section = document.querySelector('.section');
const section2 = document.querySelector('.section2');
const footer = document.querySelector('.main-footer');
const store = document.querySelector('.main-store');
console.log(moon);

swt_btn.addEventListener('click', ()=>{
    click();
});


let clicked = false;
function click(){
    clicked = !clicked;
    console.log(clicked)
    if (clicked){
        swt_btn.style.background = '#334756';
        swt_btn.style.color = 'white';
        moon.style.transform = 'rotate(270deg)';
        moon.style.marginBottom = '5px'; 
        document.body.style.backgroundColor= '#334756';
        section.style.background= '#334756';
        section2.style.background = '#334756';
        store.style.background = 'linear-gradient(#334756 5% ,#EEEEEE 80% ,#334756)';
        footer.style.background = '#EEEEEE';
        footer.style.color = 'black';
    }
    else {
        swt_btn.style.background = 'white';
        swt_btn.style.color = '#334756';
        moon.style.transform = 'rotate(-360deg)';
        moon.style.marginBottom = '0'; 
        document.body.style.backgroundColor= '#EEEEEE';
        document.querySelector('.main-store').style.background = 'linear-gradient(#EEEEEE 5% ,#FCD1D1 80% ,#EEEEEE)';
    }
}