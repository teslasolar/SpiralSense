// SpiralSense Nav — injected into all pages (flat + 3D)
(function () {
  'use strict';
  const NAV = window.NAV_CONFIG || {};
  const is3D = NAV.mode === '3d';
  const base = NAV.base || '';
  const current = NAV.current || 'root';

  const layers = [
    { id: 'root', label: 'Standard', flat: base + '/', three: base + '/3d.html' },
    { id: 'p2', label: 'p=2', flat: base + '/p2_identity/', three: base + '/p2_identity/3d.html' },
    { id: 'p3', label: 'p=3', flat: base + '/p3_storage/', three: base + '/p3_storage/3d.html' },
    { id: 'p5', label: 'p=5', flat: base + '/p5_content/', three: base + '/p5_content/3d.html' },
    { id: 'p7', label: 'p=7', flat: base + '/p7_connection/', three: base + '/p7_connection/3d.html' },
    { id: 'p11', label: 'p=11', flat: base + '/p11_assembly/', three: base + '/p11_assembly/3d.html' },
    { id: 'p13', label: 'p=13', flat: base + '/p13_chain/', three: base + '/p13_chain/3d.html' },
    { id: 'p17', label: 'p=17', flat: base + '/p17_observer/', three: base + '/p17_observer/3d.html' },
  ];

  const colors = {
    root: '#00ffaa', p2: '#ff4444', p3: '#ff8800', p5: '#ffdd00',
    p7: '#00cc44', p11: '#0088ff', p13: '#8844ff', p17: '#ff44cc'
  };

  // Build nav HTML
  const nav = document.createElement('nav');
  nav.id = 'spiralnav';
  const style = document.createElement('style');
  style.textContent = `
    #spiralnav {
      position: fixed; top: 0; left: 0; right: 0; z-index: 9999;
      background: rgba(10,10,15,0.95); border-bottom: 1px solid #222;
      display: flex; align-items: center; padding: 0 0.8rem;
      font-family: 'Courier New', monospace; font-size: 0.7rem;
      backdrop-filter: blur(8px); height: 36px;
    }
    #spiralnav .brand {
      color: #00ffaa; font-weight: bold; font-size: 0.75rem;
      text-decoration: none; margin-right: 1rem; white-space: nowrap;
    }
    #spiralnav .links { display: flex; gap: 0.1rem; flex: 1; flex-wrap: nowrap; overflow-x: auto; }
    #spiralnav .links a {
      color: #555; text-decoration: none; padding: 0.3rem 0.5rem;
      border-radius: 3px; white-space: nowrap; transition: all 0.15s;
    }
    #spiralnav .links a:hover { color: #e0e0e0; background: #1a1a28; }
    #spiralnav .links a.active { color: #e0e0e0; background: #1e1e2a; }
    #spiralnav .toggle {
      margin-left: 0.8rem; display: flex; gap: 0;
      border: 1px solid #333; border-radius: 4px; overflow: hidden;
    }
    #spiralnav .toggle a {
      padding: 0.25rem 0.6rem; text-decoration: none;
      color: #555; font-size: 0.65rem; transition: all 0.15s;
    }
    #spiralnav .toggle a.active { background: #00ffaa; color: #0a0a0f; }
    #spiralnav .toggle a:hover:not(.active) { color: #e0e0e0; }
    body { padding-top: 36px !important; }
  `;
  document.head.appendChild(style);

  // Brand
  const brand = document.createElement('a');
  brand.href = (NAV.home || '/');
  brand.className = 'brand';
  brand.textContent = '510,510';
  nav.appendChild(brand);

  // Layer links
  const linksDiv = document.createElement('div');
  linksDiv.className = 'links';
  layers.forEach(l => {
    const a = document.createElement('a');
    a.href = is3D ? l.three : l.flat;
    a.textContent = l.label;
    a.style.borderBottom = '2px solid ' + (colors[l.id] || '#555');
    if (l.id === current) a.className = 'active';
    linksDiv.appendChild(a);
  });
  nav.appendChild(linksDiv);

  // 2D/3D toggle
  const toggle = document.createElement('div');
  toggle.className = 'toggle';
  const cur = layers.find(l => l.id === current) || layers[0];
  const flatLink = document.createElement('a');
  flatLink.href = cur.flat;
  flatLink.textContent = '2D';
  if (!is3D) flatLink.className = 'active';
  const threeLink = document.createElement('a');
  threeLink.href = cur.three;
  threeLink.textContent = '3D';
  if (is3D) threeLink.className = 'active';
  toggle.appendChild(flatLink);
  toggle.appendChild(threeLink);
  nav.appendChild(toggle);

  document.body.prepend(nav);
})();
