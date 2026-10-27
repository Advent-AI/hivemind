/** Verify Action controls against real captured prices, with a local-only Idea fixture. */
import fs from 'node:fs/promises';
await import('./verify-navigation.mjs');
const source = await fs.readFile(new URL('./dist/navigation-check.html', import.meta.url), 'utf8');
const checks = `<script>
const actionButton=document.createElement('button');actionButton.id='check-action';actionButton.textContent='Run Action checks';document.querySelector('#navigation-checks').prepend(actionButton);
const actionNode=()=>navRoot().querySelector('.card--action');
const investment=()=>actionNode().querySelector('input');
actionButton.onclick=async()=>{
 const result=document.querySelector('#navigation-result');result.textContent='Running Action checks';
 try{
  navClick('show-idea');navSubmit(fixtureCard.idea.text);await navUntil(()=>!!fixtureRequest);
  navAssert(!actionNode(),'Pending request showed an Action');navClick('fixture-finish');
  await navUntil(()=>navRoot().querySelectorAll('.card').length===6);navRoot().querySelector('[data-zoom="2"]').click();
  const action=actionNode(),trigger=navRoot().querySelector('.card--trigger');
  navAssert(trigger.offsetLeft-action.offsetLeft-action.offsetWidth===180,'Action is not left of Trigger');
  navAssert(action.offsetTop+action.offsetHeight/2===trigger.offsetTop+trigger.offsetHeight/2,'Action is not centred on Trigger');
  navAssert(investment().value==='5.0','Investment default is incorrect');
  navAssert(action.querySelector('[data-market-range="1Y"]').getAttribute('aria-pressed')==='true','Default chart range is not one year');
  const dot=action.querySelector('.action__status-dot');
  navAssert(dot&&!action.querySelector('.action__status svg')&&action.querySelector('.action__status').textContent==='Monitoring','Monitoring dot or label is missing');
  navAssert(getComputedStyle(dot).backgroundColor==='rgb(0, 0, 0)','Monitoring dot is not black');
  if(!matchMedia('(prefers-reduced-motion: reduce)').matches){
   const samples=new Set();for(let frame=0;frame<12;frame++){samples.add(getComputedStyle(dot).transform);await navFrame();}
   navAssert(samples.size>1,'Monitoring dot is not pulsing');
  }else navAssert(getComputedStyle(dot).animationName==='none','Monitoring dot ignores reduced motion');
  navAssert(action.querySelector('.action__price').textContent==='$215.38','Chart does not display the real latest completed price');
  navAssert(!action.querySelector('.action__source'),'Removed price footer is still rendered');
  navAssert(action.querySelector('.action__instrument').textContent==='NVDA-USDC | Hyperliquid-Spot','Action instrument label is incorrect');
  navAssert(action.querySelector('.action__plot svg').getAttribute('aria-label').includes('stock-price reference in USD. TrueNorth, as of Oct 26, 2026'),'Chart lost its actual reference-data identity');
  navAssert([...action.querySelectorAll('.action__row:nth-child(2)>span')].map(n=>n.textContent).join(',')==='Invest,of','Trailing wallet word remains');
  navAssert(/^[-+−]?[0-9]+[.][0-9]{2}%$/.test(action.querySelector('.action__change').textContent),'Timeframe remains beside price change');
  navAssert(action.querySelector('.action__logo path'),'Hyperliquid logo missing');
  navAssert(action.querySelectorAll('button:not([role="option"])').length===8,'An unexpected execution control was added');
  const stage=navRoot().querySelector('.stage'),replayTop=stage.querySelector('.replay').getBoundingClientRect().top;
  action.querySelector('.action__plot svg').focus();await navFrame();
  navAssert(stage.scrollTop===0&&stage.scrollLeft===0&&stage.querySelector('.replay').getBoundingClientRect().top===replayTop,'Chart focus scrolled the canvas controls');
  const body=action.querySelector('.card__body');navAssert(body.scrollHeight<=body.clientHeight,'Action content overflows its card');
  for(const row of action.querySelectorAll('.action__row'))navAssert(row.scrollWidth<=row.clientWidth,'Action control row clips');
  for(const button of action.querySelectorAll('.type-filter__trigger')){
   button.click();navAssert(button.getAttribute('aria-expanded')==='true','Select did not open');
   const menu=document.getElementById(button.getAttribute('aria-controls'));
   navAssert(menu.querySelectorAll('[role="option"]').length===1,'Preview exposes an unsupported choice');
   menu.querySelector('[role="option"]').click();navAssert(button.getAttribute('aria-expanded')==='false','Select did not close');
  }
  const paths=new Set();for(const range of ['1D','1W','1M','1Y']){
   action.querySelector('[data-market-range="'+range+'"]').click();
   navAssert(action.querySelector('.action__price').textContent==='$215.38','Range lost its latest observation');
   paths.add(action.querySelector('.action__line').getAttribute('d'));
  }navAssert(paths.size===4,'Chart ranges do not change the data');
  const camera=navRoot().querySelector('.world').style.transform;
  const typeAllocation=value=>{investment().focus();investment().value=value;investment().dispatchEvent(new Event('input',{bubbles:true}));};
  const allocationKey=key=>investment().dispatchEvent(new KeyboardEvent('keydown',{key,bubbles:true,cancelable:true}));
  typeAllocation('9.2');allocationKey('Escape');navAssert(investment().value==='5.0'&&document.activeElement!==investment(),'Escape did not cancel the allocation draft');
  typeAllocation('8.5');allocationKey('Enter');navAssert(investment().value==='8.5'&&document.activeElement!==investment(),'Enter did not commit the allocation');
  typeAllocation('12.3');action.querySelector('[data-market-range="1Y"]').focus();navAssert(investment().value==='8.5','Outside focus did not cancel the allocation draft');
  typeAllocation('12.3');action.querySelector('.action__status').dispatchEvent(new PointerEvent('pointerdown',{bubbles:true}));window.dispatchEvent(new PointerEvent('pointerup'));navAssert(investment().value==='8.5'&&document.activeElement!==investment(),'Clicking canvas text did not cancel the allocation draft');
  typeAllocation('');allocationKey('Enter');navAssert(investment().value==='8.5','Empty input replaced the saved allocation');
  typeAllocation('9.4');investment().dispatchEvent(new WheelEvent('wheel',{deltaY:-100,bubbles:true,cancelable:true}));allocationKey('Escape');navAssert(investment().value==='8.5','Wheel draft could not be cancelled');
  investment().dispatchEvent(new WheelEvent('wheel',{deltaY:-100,bubbles:true,cancelable:true}));
  navAssert(investment().value==='8.6'&&navRoot().querySelector('.world').style.transform===camera,'Investment scroll changed the canvas');
  navRoot().querySelector('[data-range="30d"]').click();
  navAssert(investment().value==='8.6'&&actionNode().querySelector('[data-market-range="1Y"]').getAttribute('aria-pressed')==='true','Replay range lost Action settings');
  const saved=navSnapshot();navClick('show-library');navClick('show-idea');navAssert(navSnapshot()===saved,'Navigation lost Action state');
  navSubmit('Second Action idea');await navUntil(()=>!!fixtureRequest);navAssert(!actionNode(),'New query retained old Action');
  navClick('fixture-finish');await navUntil(()=>navRoot().querySelectorAll('.card').length===6);navRoot().querySelector('[data-zoom="2"]').click();
  navAssert(investment().value==='5.0'&&actionNode().querySelector('[data-market-range="1Y"]').getAttribute('aria-pressed')==='true','New query failed to reset Action to one year');
  let changes=0;const standalone=Hivemind.createActionCard({market:null,onChange:()=>changes++});document.body.append(standalone.element);
  navAssert(standalone.element.textContent.includes('Price data unavailable')&&!standalone.element.querySelector('.action__line'),'Unavailable prices invented a chart');
  const detached=standalone.element.querySelector('input');standalone.destroy();detached.value='20';detached.dispatchEvent(new Event('input',{bubbles:true}));navAssert(changes===0,'Destroyed Action retained listeners');
  const withChart=Hivemind.createActionCard({market:JSON.parse(document.querySelector('#market-data').textContent),onChange:()=>changes++});document.body.append(withChart.element);
  const oldRange=withChart.element.querySelector('[data-market-range="1D"]'),oldPlot=withChart.element.querySelector('.action__plot svg'),oldQuote=withChart.element.querySelector('.action__price'),lastPrice=oldQuote.textContent;
  withChart.destroy();oldRange.click();oldPlot.dispatchEvent(new KeyboardEvent('keydown',{key:'Home',bubbles:true,cancelable:true}));
  navAssert(changes===0&&oldQuote.textContent===lastPrice,'Destroyed price chart retained listeners');
  navAssert(fixturePosts===2&&fixtureAborts===0,'Action controls triggered an extra query');
  result.textContent='Passed: Action layout, real prices, 4 ranges, investment, retention, reset, unavailable and teardown; 2 queries, 0 aborts';
 }catch(error){result.textContent='FAILED: '+error.message;throw error;}
};
</script>`;
await fs.writeFile(
  new URL('./dist/action-check.html', import.meta.url),
  source.replace('</body>', () => checks + '</body>'),
);
console.log('Wrote poc/ui/dist/action-check.html');
