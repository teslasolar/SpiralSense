// SpiralSense 3D Engine — Three.js powered
// Shared across all 3D pages. Each page sets window.LAYER_CONFIG before loading.
// Uses Three.js from CDN (loaded by each page).

(function () {
  'use strict';
  const CFG = window.LAYER_CONFIG || { layer: 'root', prime: 0, color: '#00ffaa' };
  const PRIMES = [
    { p: 2, color: '#ff4444', name: 'Identity' },
    { p: 3, color: '#ff8800', name: 'Storage' },
    { p: 5, color: '#ffdd00', name: 'Content' },
    { p: 7, color: '#00cc44', name: 'Connection' },
    { p: 11, color: '#0088ff', name: 'Assembly' },
    { p: 13, color: '#8844ff', name: 'Chain' },
    { p: 17, color: '#ff44cc', name: 'Observer' },
  ];

  const container = document.getElementById('scene');
  if (!container) return;

  // Scene setup
  const scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0a0a0f);
  scene.fog = new THREE.FogExp2(0x0a0a0f, 0.003);

  const W = container.clientWidth || window.innerWidth;
  const H = container.clientHeight || window.innerHeight;
  const camera = new THREE.PerspectiveCamera(60, W / H, 0.1, 2000);
  camera.position.set(0, 80, 200);
  camera.lookAt(0, 0, 0);

  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(W, H);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  container.appendChild(renderer.domElement);

  // Orbit-like mouse control
  let mouseX = 0, mouseY = 0, targetX = 0, targetY = 0;
  let isDragging = false, startX = 0, startY = 0, rotY = 0, rotX = 0.3;
  container.addEventListener('mousedown', e => { isDragging = true; startX = e.clientX; startY = e.clientY; });
  window.addEventListener('mouseup', () => { isDragging = false; });
  window.addEventListener('mousemove', e => {
    if (isDragging) {
      rotY += (e.clientX - startX) * 0.005;
      rotX += (e.clientY - startY) * 0.003;
      rotX = Math.max(-1.2, Math.min(1.2, rotX));
      startX = e.clientX; startY = e.clientY;
    }
  });
  // Touch
  container.addEventListener('touchstart', e => { isDragging = true; startX = e.touches[0].clientX; startY = e.touches[0].clientY; }, { passive: true });
  window.addEventListener('touchend', () => { isDragging = false; });
  window.addEventListener('touchmove', e => {
    if (isDragging && e.touches.length) {
      rotY += (e.touches[0].clientX - startX) * 0.005;
      rotX += (e.touches[0].clientY - startY) * 0.003;
      rotX = Math.max(-1.2, Math.min(1.2, rotX));
      startX = e.touches[0].clientX; startY = e.touches[0].clientY;
    }
  }, { passive: true });

  // Zoom
  container.addEventListener('wheel', e => {
    camera.position.z = Math.max(50, Math.min(500, camera.position.z + e.deltaY * 0.3));
    e.preventDefault();
  }, { passive: false });

  // Grid floor
  const gridHelper = new THREE.GridHelper(400, 40, 0x111122, 0x111122);
  gridHelper.position.y = -60;
  scene.add(gridHelper);

  // Build spirals based on layer
  function buildSpiral(p, color, offsetY, phaseOffset) {
    const pts = [];
    const colors = [];
    const segments = 600;
    const col = new THREE.Color(color);

    for (let i = 0; i < segments; i++) {
      const t = i / segments;
      const angle = t * Math.PI * 6 + phaseOffset;
      const radius = 20 + t * 80;
      const x = Math.cos(angle * (p / 7)) * radius;
      const z = Math.sin(angle * (p / 7)) * radius;
      const y = (t - 0.5) * 120 + offsetY;
      pts.push(x, y, z);
      const bright = 0.3 + 0.7 * (1 - t);
      colors.push(col.r * bright, col.g * bright, col.b * bright);
    }

    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.Float32BufferAttribute(pts, 3));
    geo.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
    const mat = new THREE.LineBasicMaterial({ vertexColors: true, linewidth: 2, transparent: true, opacity: 0.85 });
    return new THREE.Line(geo, mat);
  }

  // Particle field
  function buildParticles(count, spread, color) {
    const geo = new THREE.BufferGeometry();
    const pos = [];
    for (let i = 0; i < count; i++) {
      pos.push((Math.random() - 0.5) * spread, (Math.random() - 0.5) * spread, (Math.random() - 0.5) * spread);
    }
    geo.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    const mat = new THREE.PointsMaterial({ color: new THREE.Color(color), size: 1.5, transparent: true, opacity: 0.5 });
    return new THREE.Points(geo, mat);
  }

  // Glowing sphere for nodes
  function buildNode(x, y, z, color, size) {
    const geo = new THREE.SphereGeometry(size || 3, 16, 16);
    const mat = new THREE.MeshBasicMaterial({ color: new THREE.Color(color), transparent: true, opacity: 0.8 });
    const mesh = new THREE.Mesh(geo, mat);
    mesh.position.set(x, y, z);
    return mesh;
  }

  // Ring
  function buildRing(radius, color, y) {
    const geo = new THREE.RingGeometry(radius - 0.5, radius + 0.5, 64);
    const mat = new THREE.MeshBasicMaterial({ color: new THREE.Color(color), side: THREE.DoubleSide, transparent: true, opacity: 0.4 });
    const mesh = new THREE.Mesh(geo, mat);
    mesh.rotation.x = -Math.PI / 2;
    mesh.position.y = y || 0;
    return mesh;
  }

  // Text sprite
  function makeLabel(text, color, size) {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = 256; canvas.height = 64;
    ctx.font = 'bold 28px Courier New';
    ctx.fillStyle = color || '#00ffaa';
    ctx.textAlign = 'center';
    ctx.fillText(text, 128, 40);
    const tex = new THREE.CanvasTexture(canvas);
    const mat = new THREE.SpriteMaterial({ map: tex, transparent: true });
    const sprite = new THREE.Sprite(mat);
    sprite.scale.set(size || 30, (size || 30) * 0.25, 1);
    return sprite;
  }

  const group = new THREE.Group();
  scene.add(group);

  // Layer-specific builds
  if (CFG.layer === 'root' || CFG.layer === 'observer') {
    // All 7 spirals
    PRIMES.forEach((pr, i) => {
      const spiral = buildSpiral(pr.p, pr.color, 0, i * 0.9);
      group.add(spiral);
      const label = makeLabel('p=' + pr.p + ' ' + pr.name, pr.color, 20);
      label.position.set(0, 70 - i * 18, 0);
      group.add(label);
    });
    const center = makeLabel('510,510', '#00ffaa', 40);
    center.position.set(0, 85, 0);
    group.add(center);
    group.add(buildParticles(500, 300, '#00ffaa'));
  } else if (CFG.layer === 'identity') {
    // Keypair visualization — two intertwined spirals
    group.add(buildSpiral(2, '#ff4444', 0, 0));
    group.add(buildSpiral(2, '#ff6666', 0, Math.PI));
    group.add(buildNode(0, 0, 0, '#ff4444', 8));
    const label = makeLabel('Ed25519 Keypair', '#ff4444', 30);
    label.position.set(0, 80, 0);
    group.add(label);
    group.add(buildRing(50, '#ff4444', -50));
    group.add(buildRing(70, '#ff4444', -50));
    group.add(buildParticles(300, 200, '#ff4444'));
  } else if (CFG.layer === 'storage') {
    // DHT mesh — nodes connected
    const positions = [];
    for (let i = 0; i < 20; i++) {
      const a = (i / 20) * Math.PI * 2;
      const r = 40 + Math.random() * 40;
      const x = Math.cos(a) * r;
      const z = Math.sin(a) * r;
      const y = (Math.random() - 0.5) * 60;
      positions.push([x, y, z]);
      group.add(buildNode(x, y, z, '#ff8800', 2 + Math.random() * 2));
    }
    // Connect nodes
    const lineMat = new THREE.LineBasicMaterial({ color: 0xff8800, transparent: true, opacity: 0.2 });
    for (let i = 0; i < positions.length; i++) {
      for (let j = i + 1; j < positions.length; j++) {
        if (Math.random() > 0.7) {
          const geo = new THREE.BufferGeometry().setFromPoints([
            new THREE.Vector3(...positions[i]), new THREE.Vector3(...positions[j])
          ]);
          group.add(new THREE.Line(geo, lineMat));
        }
      }
    }
    const label = makeLabel('DHT Mesh Memory', '#ff8800', 30);
    label.position.set(0, 80, 0);
    group.add(label);
    group.add(buildParticles(200, 200, '#ff8800'));
  } else if (CFG.layer === 'content') {
    // FFT bars — Sacred Nine
    const verbs = ['sense', 'build', 'link', 'hold', 'release', 'pattern', 'resonate', 'emerge', 'remember'];
    verbs.forEach((v, i) => {
      const h = 10 + Math.random() * 50;
      const geo = new THREE.BoxGeometry(6, h, 6);
      const mat = new THREE.MeshBasicMaterial({ color: new THREE.Color('#ffdd00'), transparent: true, opacity: 0.6 + Math.random() * 0.3 });
      const mesh = new THREE.Mesh(geo, mat);
      const a = (i / 9) * Math.PI * 2;
      mesh.position.set(Math.cos(a) * 45, h / 2 - 30, Math.sin(a) * 45);
      group.add(mesh);
      const lbl = makeLabel(v, '#ffdd00', 12);
      lbl.position.set(Math.cos(a) * 45, h + -25, Math.sin(a) * 45);
      group.add(lbl);
    });
    group.add(buildSpiral(5, '#ffdd00', 0, 0));
    group.add(buildParticles(200, 200, '#ffdd00'));
  } else if (CFG.layer === 'connection') {
    // The main SpiralSense 3D spiral — 7 frequency bands
    const bands = [
      { lo: 20, hi: 50, color: '#FF0000', name: 'Sub-bass' },
      { lo: 50, hi: 160, color: '#FF8000', name: 'Bass' },
      { lo: 160, hi: 500, color: '#FFFF00', name: 'Warmth' },
      { lo: 500, hi: 1600, color: '#00FF00', name: 'Clarity' },
      { lo: 1600, hi: 5000, color: '#0000FF', name: 'Presence' },
      { lo: 5000, hi: 12000, color: '#4B0082', name: 'Air' },
      { lo: 12000, hi: 20000, color: '#8B00FF', name: 'Highs' },
    ];
    bands.forEach((band, i) => {
      const pts = [];
      const cols = [];
      const col = new THREE.Color(band.color);
      const n = 400;
      for (let j = 0; j < n; j++) {
        const t = j / n;
        const angle = t * Math.PI * 8;
        const r = 15 + t * 90;
        const amp = 0.5 + 0.5 * Math.sin(t * Math.PI * 4 + i * 1.3);
        pts.push(Math.cos(angle) * r, (t - 0.5) * 150 + amp * 15, Math.sin(angle) * r);
        cols.push(col.r * amp, col.g * amp, col.b * amp);
      }
      const geo = new THREE.BufferGeometry();
      geo.setAttribute('position', new THREE.Float32BufferAttribute(pts, 3));
      geo.setAttribute('color', new THREE.Float32BufferAttribute(cols, 3));
      group.add(new THREE.Line(geo, new THREE.LineBasicMaterial({ vertexColors: true, transparent: true, opacity: 0.8 })));
    });
    const label = makeLabel('Pitch as Light', '#00cc44', 30);
    label.position.set(0, 90, 0);
    group.add(label);
    // Baseline ring
    group.add(buildRing(80, '#00cc44', -70));
    group.add(buildParticles(400, 300, '#00cc44'));
  } else if (CFG.layer === 'assembly') {
    // CRDT convergence — multiple node clusters merging
    const clusters = [[-40, 0, -40], [40, 0, -40], [0, 0, 40]];
    clusters.forEach(([cx, cy, cz], ci) => {
      for (let i = 0; i < 8; i++) {
        const ox = cx + (Math.random() - 0.5) * 30;
        const oy = cy + (Math.random() - 0.5) * 30;
        const oz = cz + (Math.random() - 0.5) * 30;
        group.add(buildNode(ox, oy, oz, '#0088ff', 2));
      }
      group.add(buildRing(20, '#0088ff', cy));
    });
    // Convergence lines between clusters
    const convMat = new THREE.LineBasicMaterial({ color: 0x0088ff, transparent: true, opacity: 0.15 });
    for (let i = 0; i < clusters.length; i++) {
      for (let j = i + 1; j < clusters.length; j++) {
        const geo = new THREE.BufferGeometry().setFromPoints([
          new THREE.Vector3(...clusters[i]), new THREE.Vector3(...clusters[j])
        ]);
        group.add(new THREE.Line(geo, convMat));
      }
    }
    group.add(buildSpiral(11, '#0088ff', 0, 0));
    const label = makeLabel('CRDT Convergence', '#0088ff', 30);
    label.position.set(0, 80, 0);
    group.add(label);
    group.add(buildParticles(300, 200, '#0088ff'));
  } else if (CFG.layer === 'chain') {
    // Mersenne cascade — Lucas-Lehmer spiral with cascade frames
    const exps = [2, 3, 5, 7, 13, 17, 19];
    exps.forEach((exp, i) => {
      const a = (i / exps.length) * Math.PI * 2;
      const r = 50;
      const size = 3 + exp * 0.3;
      group.add(buildNode(Math.cos(a) * r, 0, Math.sin(a) * r, '#8844ff', size));
      const lbl = makeLabel('M' + exp, '#8844ff', 14);
      lbl.position.set(Math.cos(a) * r, size + 5, Math.sin(a) * r);
      group.add(lbl);
    });
    group.add(buildSpiral(13, '#8844ff', 0, 0));
    // L1/L2 chain rings
    group.add(buildRing(30, '#8844ff', -40));
    group.add(buildRing(60, '#aa66ff', -40));
    const l1 = makeLabel('L1 Authority', '#8844ff', 18);
    l1.position.set(30, -35, 0);
    group.add(l1);
    const l2 = makeLabel('L2 Operations', '#aa66ff', 18);
    l2.position.set(60, -35, 0);
    group.add(l2);
    group.add(buildParticles(300, 200, '#8844ff'));
  } else if (CFG.layer === 'guild_chain') {
    // Guild Chain — load chain data and render blocks in 3D vector space
    const LAYER_COLORS = {
      2: '#ff4444', 3: '#ff8800', 5: '#ffdd00', 7: '#00cc44',
      11: '#0088ff', 13: '#8844ff', 17: '#ff44cc',
    };
    const chainData = window.CHAIN_DATA || [];
    const prevPositions = [];

    chainData.forEach((block, idx) => {
      const v = block.vector || [0, 0, 0];
      const col = LAYER_COLORS[block.layer] || '#00ffaa';
      const size = block.index === 0 ? 6 : 3;

      // Block node
      group.add(buildNode(v[0], v[1], v[2], col, size));

      // Label
      const shortLabel = block.label.length > 20 ? block.label.substring(0, 20) : block.label;
      const lbl = makeLabel('[' + block.index + '] ' + shortLabel, col, 10);
      lbl.position.set(v[0], v[1] + size + 3, v[2]);
      group.add(lbl);

      // Chain link to previous block
      if (prevPositions.length > 0) {
        const prev = prevPositions[prevPositions.length - 1];
        const geo = new THREE.BufferGeometry().setFromPoints([
          new THREE.Vector3(prev[0], prev[1], prev[2]),
          new THREE.Vector3(v[0], v[1], v[2])
        ]);
        const linkMat = new THREE.LineBasicMaterial({
          color: new THREE.Color(col), transparent: true, opacity: 0.35
        });
        group.add(new THREE.Line(geo, linkMat));
      }
      prevPositions.push(v);
    });

    // Layer rings at each Y level
    [0, 25, 50, 75, 100, 125, 150].forEach((y, i) => {
      const primeColors = ['#ff4444', '#ff8800', '#ffdd00', '#00cc44', '#0088ff', '#8844ff', '#ff44cc'];
      group.add(buildRing(90, primeColors[i], y));
    });

    const title = makeLabel('Guild Chain — ' + chainData.length + ' blocks', '#00ffaa', 25);
    title.position.set(0, 170, 0);
    group.add(title);
    group.add(buildParticles(300, 250, '#8844ff'));
  }

  // Ambient light (for any mesh materials)
  scene.add(new THREE.AmbientLight(0xffffff, 0.5));

  // Resize
  window.addEventListener('resize', () => {
    const w = container.clientWidth || window.innerWidth;
    const h = container.clientHeight || window.innerHeight;
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    renderer.setSize(w, h);
  });

  // Animate
  let autoRot = 0;
  function animate() {
    requestAnimationFrame(animate);
    autoRot += 0.003;
    const finalRotY = rotY + (isDragging ? 0 : autoRot);
    group.rotation.y = finalRotY;
    group.rotation.x = rotX;
    renderer.render(scene, camera);
  }
  animate();
})();
