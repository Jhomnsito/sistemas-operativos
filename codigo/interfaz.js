'use strict';
const $=id=>document.getElementById(id), colors=['#80ebc3','#8eb6ff','#ffc88b','#c4a4ff','#ffaaa4','#e0e68b'];
let cases=[],current=null,lastTests=null,timer=null,colorMap=new Map();
const fmt=n=>Number(n).toLocaleString('es',{maximumFractionDigits:2});
/** Crea un elemento DOM mediante textContent, sin interpretar HTML recibido. */
function node(tag,text,cls){const e=document.createElement(tag);if(text!==undefined)e.textContent=text;if(cls)e.className=cls;return e;}
/** Asigna un color estable a cada PID y gris a los intervalos sin CPU. */
function color(pid){return pid===null?'#58677c':colorMap.get(pid)||colors[0];}
/** Solicita JSON al servidor local y convierte respuestas fallidas en errores visibles. */
async function api(path,payload){const response=await fetch(path,payload===undefined?{}:{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});const data=await response.json();if(!response.ok)throw Error(data.error||'No se pudo completar la solicitud.');return data;}
/** Activa la vista seleccionada y oculta la otra sin recalcular resultados. */
function tab(name){for(const k of ['comparison','tests']){$('view-'+k).classList.toggle('hidden',k!==name);$('tab-'+k).classList.toggle('active',k===name);}}
$('tab-comparison').onclick=()=>tab('comparison');$('tab-tests').onclick=()=>tab('tests');
/** Presenta la carga enviada y avisa si contiene bloqueos de entrada/salida. */
function updateInputs(rows){$('inputs').replaceChildren();for(const p of rows){const tr=node('tr');for(const v of ['P'+p.pid,p.arrival,p.cpu])tr.append(node('td',v));$('inputs').append(tr);}$('io-note').textContent=rows.some(p=>p.io?.length)?'Este caso incluye bloqueo y regreso por entrada/salida.':'Este caso no incluye entrada/salida.';}
/** Carga entradas y quantum del escenario elegido sin ejecutar todavía. */
function selectScenario(){const c=cases[$('scenario').value];$('quantum').value=c.quantum;$('editor').value=JSON.stringify(c.processes,null,2);updateInputs(c.processes);$('status').textContent='Configuración lista. Pulsa Ejecutar comparación.';}
$('scenario').onchange=selectScenario;
/** Construye una tabla de registros usando las claves y etiquetas indicadas. */
function table(rows,fields){const wrap=node('div',undefined,'table-scroll'),t=node('table'),head=node('thead'),tr=node('tr');fields.forEach(([key,title])=>tr.append(node('th',title)));head.append(tr);t.append(head);const body=node('tbody');for(const r of rows){const row=node('tr');fields.forEach(([key])=>row.append(node('td',key==='pid'?'P'+r[key]:r[key])));body.append(row);}t.append(body);wrap.append(t);return wrap;}
/** Detiene la reproducción y restablece su control visual. */
function stop(){clearInterval(timer);timer=null;$('play').textContent='▶ Reproducir';}
/** Presenta métricas y tramos recibidos del simulador; no calcula la planificación. */
function render(data){stop();current=data;colorMap=new Map(data.input.processes.map((p,i)=>[p.pid,colors[i%colors.length]]));$('results').replaceChildren();$('events').replaceChildren();const max=Math.max(...data.results.map(r=>r.metrics.end_time));$('clock').max=max;$('clock').value=0;$('clock').disabled=false;$('play').disabled=false;
const selected=cases[$('scenario').value];$('result-title').textContent=(JSON.stringify(selected.processes)===JSON.stringify(data.input.processes)?selected.id+' · '+selected.name:'Caso personalizado')+' · quantum '+data.input.quantum+' · resultados calculados ahora';
for(const [i,r] of data.results.entries()){
 const outer=node('div',undefined,'result'),card=node('article',undefined,'card');outer.append(card);card.append(node('h2',r.algorithm));card.append(node('p',i===0?'Atiende por orden de llegada, hasta terminar o bloquearse.':'Reparte la CPU en turnos de hasta '+data.input.quantum+' unidades.','policy'));
 const numbers=node('div',undefined,'numbers');for(const [key,label] of [['avg_waiting','Espera media'],['avg_response','Respuesta media'],['avg_turnaround','Retorno medio']]){const box=node('div',undefined,'number');box.append(node('strong',fmt(r.metrics[key])),node('span',label));numbers.append(box);}card.append(numbers);
 const track=node('div',undefined,'track');for(const s of r.timeline){const part=node('div',s.pid===null?'Libre':'P'+s.pid,'segment');part.style.width=((s.end-s.start)/max*100)+'%';part.style.background=color(s.pid);part.title=(s.pid===null?'CPU ociosa':'P'+s.pid)+': '+s.start+' a '+s.end;track.append(part);}const cursor=node('div',undefined,'cursor');cursor.id='cursor-'+i;track.append(cursor);card.append(track);const axis=node('div',undefined,'axis');axis.append(node('span','0'),node('span',String(max)));card.append(axis);card.append(node('p','Instante 0','detail'));card.lastChild.id='now-'+i;
 card.append(table(r.processes,[['pid','Proceso'],['arrival','Llega'],['cpu','CPU'],['waiting','Espera'],['response','Responde'],['turnaround','Retorno'],['finish','Fin']]));
 card.append(node('p',r.metrics.context_switches+' cambios de contexto · '+r.metrics.dispatches+' despachos · CPU '+fmt(r.metrics.utilization_percent)+'%','detail'));$('results').append(outer);

}
const a=data.results[0].metrics,b=data.results[1].metrics,reading=$('interpretation');reading.replaceChildren(node('h3','Lectura de esta ejecución'));reading.append(node('p','Espera media: FCFS '+fmt(a.avg_waiting)+'; Round Robin '+fmt(b.avg_waiting)+'. Respuesta media: FCFS '+fmt(a.avg_response)+'; Round Robin '+fmt(b.avg_response)+'.'));
const p2=data.results.map(r=>r.processes.find(p=>p.pid===2));if(p2.every(Boolean))reading.append(node('p','P2 llega en '+p2[0].arrival+'. Su primer turno comienza en '+(p2[0].arrival+p2[0].response)+' con FCFS y en '+(p2[1].arrival+p2[1].response)+' con Round Robin. La respuesta es inicio del primer turno menos llegada.'));
reading.append(node('p','Estos resultados corresponden a esta entrada. Un algoritmo puede mejorar la respuesta sin reducir la espera o el retorno en otros casos.'));reading.classList.remove('hidden');$('comparison-evidence').textContent='Evidencia guardada: '+data.evidence;$('download').classList.remove('hidden');if($('event-details').open)renderEvents();tick();
}
/** Muestra quién ocupa la CPU en el instante seleccionado de la traza existente. */
function tick(){if(!current)return;const t=Number($('clock').value),max=Number($('clock').max);$('clock-label').textContent='t = '+t;current.results.forEach((r,i)=>{$('cursor-'+i).style.left=Math.min(99.7,t/max*100)+'%';const s=r.timeline.find(s=>s.start<=t&&t<s.end);$('now-'+i).textContent=t>=r.metrics.end_time?'Todos los procesos finalizaron.':s?.pid!=null?'Ejecutando P'+s.pid+' · tramo '+s.start+'–'+s.end:'CPU ociosa en este instante.';});}
$('clock').oninput=()=>{stop();tick();};$('play').onclick=()=>{if(timer){stop();return;}if(Number($('clock').value)>=Number($('clock').max))$('clock').value=0;$('play').textContent='Ⅱ Pausar';tick();timer=setInterval(()=>{$('clock').value=Number($('clock').value)+1;tick();if(Number($('clock').value)>=Number($('clock').max))stop();},650);};
$('compare').onclick=async()=>{const btn=$('compare');btn.disabled=true;$('status').classList.remove('error');$('status').textContent='Calculando con el simulador…';try{const rows=JSON.parse($('editor').value);const result=await api('/api/compare',{processes:rows,quantum:Number($('quantum').value)});updateInputs(rows);render(result);tab('comparison');$('status').textContent='Comparación completada. Evidencia guardada.';}catch(e){$('status').textContent=e.message;$('status').classList.add('error');}finally{btn.disabled=false;}};
$('tests').onclick=async()=>{const btn=$('tests');btn.disabled=true;$('test-status').className='';$('test-status').textContent='Ejecutando la suite real de Python…';try{const r=await api('/api/tests',{});lastTests=r;$('test-output').textContent=r.output;$('test-status').textContent=r.success?'Pruebas aprobadas · ejecución nueva':'Las pruebas no aprobaron. Revisa la salida.';$('test-status').className=r.success?'pass':'error';$('test-evidence').textContent='Evidencia guardada: '+r.evidence;$('download-tests').classList.remove('hidden');}catch(e){$('test-status').textContent=e.message;$('test-status').className='error';}finally{btn.disabled=false;}};
/** Descarga una copia JSON del resultado; libera después la URL temporal. */
function download(data,name){const url=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));const a=node('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
$('download').onclick=()=>download(current,'comparacion_cpu.json');$('download-tests').onclick=()=>download(lastTests,'pruebas_cpu.json');
api('/api/scenarios').then(data=>{cases=data;data.forEach((s,i)=>{const o=node('option',s.id+' · '+s.name);o.value=i;$('scenario').append(o);});$('scenario').value=1;selectScenario();}).catch(e=>{$('status').textContent=e.message;$('status').classList.add('error');});

/** Construye las transiciones completas solo cuando se abre el panel de estados. */
function renderEvents(){
 if(!current)return;
 $('events').replaceChildren();
 for(const r of current.results){
  $('events').append(node('h3',r.algorithm),table(r.events,[['time','Instante'],['pid','Proceso'],['state','Estado'],['reason','Motivo']]));
 }
}
$('event-details').ontoggle=()=>{if($('event-details').open)renderEvents();};
