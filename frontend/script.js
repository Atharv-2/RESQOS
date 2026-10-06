/* ---------- Icons (inline SVG paths) ---------- */
const ICONS = {
  shield:'<path d="M12 3l8 3v6c0 4.5-3.4 8-8 9-4.6-1-8-4.5-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
  menu:'<path d="M4 7h16M4 12h16M4 17h16"/>',
  alert:'<path d="M12 3l10 18H2z"/><path d="M12 10v5M12 18h.01"/>',
  risk:'<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4.5"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3"/>',
  pin:'<path d="M12 21s-6-5.4-6-10a6 6 0 0 1 12 0c0 4.6-6 10-6 10z"/><circle cx="12" cy="11" r="2"/>',
  plan:'<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4V3h6v1M9 11l2 2 4-4M9 17h6"/>',
  rain:'<path d="M7 15a4 4 0 1 1 1-7.9A5 5 0 0 1 17.5 9 3.5 3.5 0 0 1 17 16H7z"/><path d="M8 19l-1 2M12 19l-1 2M16 19l-1 2"/>',
  spark:'<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M19 16v4M17 18h4"/>',
  hospital:'<rect x="4" y="4" width="16" height="16" rx="3"/><path d="M12 8v8M8 12h8"/>',
  building:'<path d="M4 21V8l8-5 8 5v13M9 21v-6h6v6"/>',
  rescue:'<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3.5"/><path d="M5.6 5.6l3.9 3.9M14.5 14.5l3.9 3.9M18.4 5.6l-3.9 3.9M9.5 14.5l-3.9 3.9"/>',
  collect:'<path d="M12 4v11M7 10l5 5 5-5M5 20h14"/>',
  display:'<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>'
};
const icon = n => `<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">${ICONS[n]}</svg>`;

/* ---------- Content (static/mock; swap for real data later) ---------- */
const FLOW = [
  {icon:'alert',  title:'Weather Alert',      text:'A heavy-rain warning is received.'},
  {icon:'risk',   title:'Risk Assessment',    text:'Risk is assessed for the location.'},
  {icon:'hospital',title:'Nearby Resources',  text:'Emergency resources are identified.'},
  {icon:'plan',   title:'Preparedness Plan',  text:'Recommended actions are prepared.'}
];
const FEATURES = [
  {icon:'rain',    title:'Heavy Rain Monitoring', text:'Monitor rainfall and weather conditions.'},
  {icon:'risk',    title:'Location-Specific Risk Assessment', text:'Assess risk using rainfall and geographical factors.'},
  {icon:'hospital',title:'Emergency Resource Identification', text:'Identify nearby hospitals, police stations, shelters and roads.'},
  {icon:'spark',   title:'AI Preparedness Recommendations', text:'Generate location-specific preparedness recommendations for authorities.'}
];
const STEPS = [
  {title:'Collect', text:'Gather weather information'},
  {title:'Detect',  text:'Identify heavy-rain conditions'},
  {title:'Assess',  text:'Evaluate location risk'},
  {title:'Locate',  text:'Find nearby resources'},
  {title:'Plan',    text:'Prepare recommendations'},
  {title:'Display', text:'Show results to authorities'}
];
const USERS = [
  {icon:'shield',  title:'Disaster Management Authorities'},
  {icon:'pin',     title:'Police & Emergency Teams'},
  {icon:'hospital',title:'Hospitals'},
  {icon:'building',title:'Local Administration'},
  {icon:'rescue',  title:'Rescue Teams'}
];

/* ---------- Small render "components" ---------- */
const IconBox = n => `<div class="ico">${icon(n)}</div>`;
const FlowItem = i => `<div class="flow-item">${IconBox(i.icon)}<h3>${i.title}</h3><p>${i.text}</p></div>`;
const FeatureCard = i => `<article class="card">${IconBox(i.icon)}<h3>${i.title}</h3><p>${i.text}</p></article>`;
const Step = (s,k) => `<li><div class="dot">${k+1}</div><div><h3>${s.title}</h3><p>${s.text}</p></div></li>`;
const UserCard = i => `<div class="user">${IconBox(i.icon)}<h3>${i.title}</h3></div>`;
const mount = (id, items, fn) => document.getElementById(id).innerHTML = items.map(fn).join('');

mount('flow', FLOW, FlowItem);
mount('features-grid', FEATURES, FeatureCard);
mount('timeline', STEPS, Step);
mount('users-grid', USERS, UserCard);

document.querySelectorAll('[data-icon]').forEach(el => el.innerHTML = icon(el.dataset.icon));
document.querySelectorAll('.logo-mark svg').forEach(s => { s.style.cssText = 'width:20px;height:20px'; });
document.querySelectorAll('.menu svg').forEach(s => { s.style.cssText = 'width:22px;height:22px'; });

/* Mobile menu */
const menu = document.getElementById('menu'), links = document.getElementById('links');
menu.addEventListener('click', () => menu.setAttribute('aria-expanded', links.classList.toggle('open')));
links.addEventListener('click', () => { links.classList.remove('open'); menu.setAttribute('aria-expanded', false); });
