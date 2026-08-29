const nav=document.querySelector('nav');
document.querySelector('.menu-toggle').addEventListener('click',()=>nav.classList.toggle('open'));

function showPage(){
  const id=location.hash.slice(1)||'home';
  document.querySelectorAll('.page').forEach(page=>{
    const active=page.id===id;
    page.classList.toggle('active',active);
    page.style.display=active?'block':'none';
  });
  nav.classList.remove('open');
  window.scrollTo({top:0,behavior:'smooth'});
}

const serviceSwitches=document.querySelectorAll('.service-switch');
const servicePanels=document.querySelectorAll('.service-panel');
serviceSwitches.forEach(switchButton=>{
  switchButton.addEventListener('click',()=>{
    const service=switchButton.dataset.service;
    serviceSwitches.forEach(button=>{
      const selected=button===switchButton;
      button.classList.toggle('active',selected);
      button.setAttribute('aria-selected',selected);
    });
    servicePanels.forEach(panel=>{
      const active=panel.dataset.panel===service;
      panel.classList.toggle('active',active);
      panel.hidden=!active;
    });
  });
});

window.addEventListener('hashchange',showPage);
showPage();