document.getElementById('menu')?.addEventListener('click',()=>document.body.classList.toggle('nav-open'));
document.querySelectorAll('.journey-nav a').forEach(link=>{
  if(new URL(link.href,window.location.href).pathname===window.location.pathname){
    link.classList.add('active');
    link.setAttribute('aria-current','page');
  }
});
const input=document.getElementById('evidence');
input?.addEventListener('change',()=>document.getElementById('filename').textContent=input.files[0]?.name||'No file selected');
document.querySelectorAll('.spark').forEach(el=>{
  const values=JSON.parse(el.dataset.values||'[]'); if(values.length<2)return;
  const w=260,h=62,min=Math.min(...values),max=Math.max(...values),span=max-min||1;
  const pts=values.map((v,i)=>`${(i/(values.length-1))*w},${h-((v-min)/span)*(h-10)-5}`).join(' ');
  el.innerHTML=`<svg viewBox="0 0 ${w} ${h}" preserveAspectRatio="none"><polyline points="${pts}"/></svg>`;
});

const operator=document.querySelector('.operator');
async function refreshPlatformStatus(){
  if(!operator||!window.AQUAVIGIL_STATUS_URL)return;
  try{
    const response=await fetch(window.AQUAVIGIL_STATUS_URL,{headers:{Accept:'application/json'},cache:'no-store'});
    if(!response.ok)throw new Error('status unavailable');
    const data=await response.json();
    operator.innerHTML=`<span class="pulse"></span>${data.latest?`${data.latest.status} · ${data.latest.alert_count} alert${data.latest.alert_count===1?'':'s'} · analysis #${data.latest.id}`:'Fresh workspace · awaiting evidence'}`;
    operator.classList.remove('offline');
  }catch(_error){
    operator.innerHTML='<span class="pulse"></span>Platform connection unavailable';
    operator.classList.add('offline');
  }
}
refreshPlatformStatus();
setInterval(refreshPlatformStatus,30000);
