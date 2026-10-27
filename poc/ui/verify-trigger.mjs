/** Exercise the real Trigger DOM through the isolated stored-response service. */
import fs from 'node:fs/promises';
await import('./verify-navigation.mjs');
const source = await fs.readFile(new URL('./dist/navigation-check.html', import.meta.url), 'utf8');
const checks = `<script>
const triggerButton=document.createElement('button');triggerButton.id='check-trigger';triggerButton.textContent='Run Trigger checks';document.querySelector('#navigation-checks').prepend(triggerButton);
const triggerInput=()=>navRoot().querySelector('.trigger__threshold input');
const triggerNode=()=>navRoot().querySelector('.card--trigger');
const triggerSlider=()=>navRoot().querySelector('.trigger__slider');
const triggerStatus=()=>triggerNode().querySelector('.trigger__status').textContent;
const triggerNumber=value=>{const input=triggerInput();input.value=String(value);input.dispatchEvent(new Event('input',{bubbles:true}));};
const triggerChoose=label=>{triggerNode().querySelector('.trigger__operator button').click();triggerNode().querySelector('[role="option"][aria-label="'+label+'"]').click();};
const triggerWheel=(input,deltaY)=>input.dispatchEvent(new WheelEvent('wheel',{deltaY,bubbles:true,cancelable:true}));
function checkTriggerConnector(){
 const line=navRoot().querySelector('.edge--trigger'),normal=[...navRoot().querySelectorAll('.edge:not(.edge--trigger)')];
 navAssert(line&&normal.length>0,'Connector check needs a Trigger line and thesis arrows');
 navAssert(getComputedStyle(line).markerEnd==='none','Trigger connector has a directional arrowhead');
 navAssert(normal.every(path=>getComputedStyle(path).markerEnd!=='none'),'A thesis connector lost its arrowhead');
}
triggerButton.onclick=async()=>{
 const result=document.querySelector('#navigation-result');result.textContent='Running Trigger checks';
 try{
  navClick('show-idea');navSubmit(fixtureCard.idea.text);await navUntil(()=>!!fixtureRequest);
  navAssert(!triggerNode(),'Pending request displayed the Trigger early');
  navClick('fixture-finish');
  await navUntil(()=>navRoot().querySelectorAll('.card').length===6);navRoot().querySelector('[data-zoom="2"]').click();
  navAssert(triggerInput().value==='70'&&triggerStatus()==='Not met','Completed Trigger default is incorrect');
  const metric=triggerNode().querySelector('.trigger__metric'),metricButton=metric.querySelector('button');
  metricButton.click();
  const metricOptions=[...metric.querySelectorAll('[role="option"]')];
  navAssert(metricButton.getAttribute('aria-expanded')==='true'&&metricOptions.length===1&&metricOptions[0].textContent==='AI confidence','Trigger metric is not the requested single-option select');
  metricOptions[0].click();navAssert(metricButton.getAttribute('aria-expanded')==='false'&&triggerInput().value==='70','Selecting the metric changed the condition');
  navAssert([metricButton,triggerNode().querySelector('.trigger__operator button'),triggerNode().querySelector('.trigger__threshold')].every(n=>n.offsetHeight===30),'Trigger controls have different heights');
  navAssert(metricButton.scrollWidth<=metricButton.clientWidth,'Trigger metric text is clipped');
  navAssert(getComputedStyle(triggerNode().querySelector('.trigger__operator button>svg')).display!=='none','Comparison dropdown indicator was not restored');
  checkTriggerConnector();
  navRoot().querySelector('.card--idea').dispatchEvent(new Event('mouseenter'));checkTriggerConnector();
  navRoot().querySelector('.card--idea').dispatchEvent(new Event('mouseleave'));checkTriggerConnector();
  const idea=navRoot().querySelector('.card--idea'),trigger=triggerNode();
  navAssert(idea.offsetLeft-trigger.offsetLeft-trigger.offsetWidth===180,'Trigger is not to the left of its Idea');
  navAssert(trigger.offsetTop+trigger.offsetHeight/2===idea.offsetTop+idea.offsetHeight/2,'Trigger and Idea are not vertically centred');
  triggerNumber(60);navAssert(triggerStatus()==='Met','Edited condition was not applied');
  const confidence=triggerNode().querySelector('.trigger__confidence').textContent;
  navAssert(confidence===navRoot().querySelector('.card--idea .plot-badge').textContent.trim(),'Trigger and Idea confidence disagree');
  navAssert(triggerNode().querySelector('.trigger__current').textContent.startsWith('Current value:'),'Metric value label is incorrect');
  const marker=()=>triggerNode().querySelector('.trigger__current-marker').getBoundingClientRect();
  const initialMarker=marker().left,label=triggerNode().querySelector('.trigger__current').getBoundingClientRect();
  navAssert(label.top>=marker().bottom&&Math.abs(label.left+label.width/2-marker().left-marker().width/2)<1,'Current value is not labelled directly below its marker');
  triggerChoose('Less than or equal to');navAssert(triggerStatus()==='Not met','Selected comparison was not applied');
  triggerNumber(parseInt(confidence));triggerChoose('Equal to');navAssert(triggerStatus()==='Met','Equality did not use displayed confidence');
  const camera=navRoot().querySelector('.world').style.transform;
  triggerWheel(triggerInput(),-100);navAssert(triggerInput().value===String(parseInt(confidence)+1)&&triggerStatus()==='Not met','Scrolling did not adjust the threshold');
  navAssert(navRoot().querySelector('.world').style.transform===camera,'Threshold scroll panned the canvas');
  triggerNumber(100);triggerWheel(triggerInput(),-100);navAssert(triggerInput().value==='100','Threshold exceeded 100');
  navAssert(triggerNode().querySelector('.trigger__confidence').textContent===confidence,'Threshold editing replaced the current metric value');
  navAssert(Math.abs(marker().left-initialMarker)<1,'Threshold editing moved the current-value marker');
  triggerNumber(0);triggerWheel(triggerSlider(),100);navAssert(triggerInput().value==='0','Threshold fell below 0');
  triggerSlider().value='55';triggerSlider().dispatchEvent(new Event('input',{bubbles:true}));
  navAssert(triggerInput().value==='55','Slider and number disagree');triggerChoose('Greater than');
  const replay=navRoot().querySelector('.replay input');replay.value='0';replay.dispatchEvent(new Event('input',{bubbles:true}));
  navAssert(triggerNode().querySelector('.trigger__confidence').textContent===navRoot().querySelector('.card--idea .plot-badge').textContent.trim(),'Replay did not update Trigger confidence');
  navAssert(Math.abs(marker().left-initialMarker)>1,'Replay did not move the current-value marker');
  navRoot().querySelector('[data-range="30d"]').click();navAssert(triggerInput().value==='55','Range redraw lost the condition');
  const saved=navSnapshot();navClick('show-library');navClick('show-idea');navAssert(navSnapshot()===saved,'Navigation changed the Trigger');
  navSubmit('A different idea');await navUntil(()=>!!fixtureRequest);navAssert(!triggerNode(),'New query retained the old Trigger');
  navClick('fixture-finish');await navUntil(()=>navRoot().querySelectorAll('.card').length===6);navRoot().querySelector('[data-zoom="2"]').click();
  navAssert(triggerInput().value==='70','New query did not reset the Trigger threshold');
  checkTriggerConnector();
  for(const path of navRoot().querySelectorAll('.edge')){
   const source=navRoot().querySelector('.card[data-id="'+path.dataset.source+'"]'),target=navRoot().querySelector('.card[data-id="'+path.dataset.target+'"]');
   const start=path.getPointAtLength(0),end=path.getPointAtLength(path.getTotalLength());
   navAssert(Math.abs(start.x-source.offsetLeft-source.offsetWidth)<1&&Math.abs(end.x-target.offsetLeft)<1,'Trigger graph has a detached connector');
  }
  let changes=0;const standalone=Hivemind.createTriggerCard({confidence:61,onChange:()=>changes++});
  document.body.append(standalone.element);
  for(const value of [0,100]){standalone.setConfidence(value);const cardBox=standalone.element.getBoundingClientRect(),labelBox=standalone.element.querySelector('.trigger__current').getBoundingClientRect();navAssert(labelBox.left>=cardBox.left&&labelBox.right<=cardBox.right,'Current value label escaped the card at an endpoint');}
  const detachedInput=standalone.element.querySelector('input');standalone.destroy();detachedInput.value='80';detachedInput.dispatchEvent(new Event('input',{bubbles:true}));
  navAssert(changes===0&&!standalone.element.isConnected,'Destroyed Trigger retained active listeners');
  navAssert(fixturePosts===2&&fixtureAborts===0,'Trigger edits made or cancelled a service request');
  result.textContent='Passed: Trigger controls, replay, navigation, reset and teardown; 2 queries, 0 aborts';
 }catch(error){result.textContent='FAILED: '+error.message;throw error;}
};
</script>`;
await fs.writeFile(
  new URL('./dist/trigger-check.html', import.meta.url),
  source.replace('</body>', () => checks + '</body>'),
);
console.log('Wrote poc/ui/dist/trigger-check.html');
