import * as THREE from 'three'

let renderer, scene, camera, animId
let objects = []
let wireframeMode = false
let autoRotate = false
let isMouseDown = false
let lastMouse = { x: 0, y: 0 }
let cameraSpherical = { radius: 10, theta: Math.PI / 4, phi: Math.PI / 3 }
let selectedMesh = null
let onSelectCallback = null
let canvas_ref = null

function createTexture(pattern = {}) {
  const size = 512
  const canvas = document.createElement('canvas')
  canvas.width = size; canvas.height = size
  const ctx = canvas.getContext('2d')
  const type = pattern.type || 'solid'
  const c1 = pattern.colors?.[0] || '#888888'
  const c2 = pattern.colors?.[1] || '#666666'
  ctx.fillStyle = c1; ctx.fillRect(0, 0, size, size)

  switch (type) {
    case 'football': {
      ctx.fillStyle = '#ffffff'; ctx.fillRect(0, 0, size, size)
      const pentagons = [[256,256],[256,100],[400,156],[370,340],[142,340],[112,156],[256,412],[450,290],[450,120],[62,120],[62,290]]
      ctx.fillStyle = '#111111'
      pentagons.forEach(([cx,cy]) => {
        ctx.beginPath()
        for (let i=0;i<5;i++){const a=(Math.PI*2/5)*i-Math.PI/2,r=46;i===0?ctx.moveTo(cx+r*Math.cos(a),cy+r*Math.sin(a)):ctx.lineTo(cx+r*Math.cos(a),cy+r*Math.sin(a))}
        ctx.closePath(); ctx.fill(); ctx.strokeStyle='#333333'; ctx.lineWidth=4; ctx.stroke()
      })
      break
    }
    case 'basketball': {
      ctx.fillStyle=c1||'#e8671b'; ctx.fillRect(0,0,size,size)
      ctx.strokeStyle=c2||'#000000'; ctx.lineWidth=8
      ctx.beginPath();ctx.moveTo(256,0);ctx.lineTo(256,512);ctx.stroke()
      ctx.beginPath();ctx.moveTo(0,256);ctx.lineTo(512,256);ctx.stroke()
      ctx.beginPath();ctx.arc(256,256,160,0,Math.PI*2);ctx.stroke()
      ctx.beginPath();ctx.ellipse(256,256,80,240,0,0,Math.PI*2);ctx.stroke()
      break
    }
    case 'tennis': {
      ctx.fillStyle=c1||'#ccff00';ctx.fillRect(0,0,size,size)
      ctx.strokeStyle=c2||'#ffffff';ctx.lineWidth=20
      ctx.beginPath();ctx.arc(0,256,200,-0.6,0.6);ctx.stroke()
      ctx.beginPath();ctx.arc(512,256,200,Math.PI-0.6,Math.PI+0.6);ctx.stroke()
      break
    }
    case 'wood': {
      ctx.fillStyle=c1||'#8B4513';ctx.fillRect(0,0,size,size)
      for(let i=0;i<20;i++){const y=(i/20)*size;ctx.strokeStyle=i%2===0?(c2||'#6B3410'):(c1||'#8B4513');ctx.lineWidth=Math.random()*6+2;ctx.beginPath();ctx.moveTo(0,y+Math.random()*10);ctx.bezierCurveTo(128,y+Math.random()*15,384,y+Math.random()*15,512,y+Math.random()*10);ctx.stroke()}
      break
    }
    case 'fur': {
      ctx.fillStyle=c1||'#d4a96a';ctx.fillRect(0,0,size,size)
      ctx.strokeStyle=c2||'#a07040';ctx.lineWidth=1.5
      for(let i=0;i<300;i++){const x=Math.random()*size,y=Math.random()*size,len=Math.random()*20+5,a=Math.random()*Math.PI*2;ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x+Math.cos(a)*len,y+Math.sin(a)*len);ctx.stroke()}
      break
    }
    case 'fabric': {
      ctx.fillStyle=c1||'#888888';ctx.fillRect(0,0,size,size)
      const step=12;ctx.strokeStyle=c2||'#666666';ctx.lineWidth=1
      for(let x=0;x<size;x+=step){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,size);ctx.stroke()}
      for(let y=0;y<size;y+=step){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(size,y);ctx.stroke()}
      break
    }
    case 'glass': {
      ctx.fillStyle='#0d1b2a';ctx.fillRect(0,0,size,size)
      const g=ctx.createLinearGradient(0,0,size,size)
      g.addColorStop(0,'rgba(255,255,255,0.15)');g.addColorStop(0.5,'rgba(255,255,255,0.02)');g.addColorStop(1,'rgba(255,255,255,0.08)')
      ctx.fillStyle=g;ctx.fillRect(0,0,size,size)
      break
    }
    case 'wheel': {
      ctx.fillStyle=c1||'#111111';ctx.fillRect(0,0,size,size)
      ctx.beginPath();ctx.arc(256,256,160,0,Math.PI*2);ctx.fillStyle=c2||'#888888';ctx.fill()
      ctx.beginPath();ctx.arc(256,256,50,0,Math.PI*2);ctx.fillStyle='#aaaaaa';ctx.fill()
      ctx.strokeStyle=c2||'#888888';ctx.lineWidth=12
      for(let i=0;i<5;i++){const a=(i/5)*Math.PI*2;ctx.beginPath();ctx.moveTo(256+Math.cos(a)*55,256+Math.sin(a)*55);ctx.lineTo(256+Math.cos(a)*155,256+Math.sin(a)*155);ctx.stroke()}
      break
    }
    case 'windows': {
      ctx.fillStyle=c1||'#4488aa';ctx.fillRect(0,0,size,size)
      const cols=6,rows=10,pw=size/cols,ph=size/rows
      for(let r=0;r<rows;r++)for(let c=0;c<cols;c++){ctx.fillStyle=Math.random()>0.3?(c2||'#87CEEB'):'#1a2a3a';ctx.fillRect(c*pw+6,r*ph+6,pw-12,ph-12)}
      break
    }
    case 'ridged': {
      const sh=size/16
      for(let i=0;i<16;i++){ctx.fillStyle=i%2===0?c1:c2;ctx.fillRect(0,i*sh,size,sh)}
      break
    }
    case 'metal': {
      const gm=ctx.createLinearGradient(0,0,size,size)
      gm.addColorStop(0,c2||'#aaaaaa');gm.addColorStop(0.4,c1||'#dddddd');gm.addColorStop(0.6,c1||'#dddddd');gm.addColorStop(1,c2||'#888888')
      ctx.fillStyle=gm;ctx.fillRect(0,0,size,size)
      ctx.strokeStyle='rgba(255,255,255,0.1)';ctx.lineWidth=1
      for(let i=0;i<40;i++){const y=(i/40)*size;ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(size,y);ctx.stroke()}
      break
    }
    case 'brick': {
      ctx.fillStyle=c1||'#8B3A2A';ctx.fillRect(0,0,size,size)
      const bw=80,bh=36;ctx.fillStyle=c2||'#555555'
      for(let row=0;row<size/bh+1;row++){const off=(row%2)*(bw/2);for(let col=-1;col<size/bw+1;col++){ctx.fillRect(col*bw+off,row*bh,4,bh);ctx.fillRect(col*bw+off,row*bh,bw,4)}}
      break
    }
    case 'stripes': {
      const sw=size/12
      for(let i=0;i<12;i++){ctx.fillStyle=i%2===0?c1:c2;ctx.fillRect(i*sw,0,sw,size)}
      break
    }
    case 'dots': {
      ctx.fillStyle=c1;ctx.fillRect(0,0,size,size);ctx.fillStyle=c2;const sp=48
      for(let x=sp/2;x<size;x+=sp)for(let y=sp/2;y<size;y+=sp){ctx.beginPath();ctx.arc(x,y,14,0,Math.PI*2);ctx.fill()}
      break
    }
    case 'checker': {
      const cs=size/8
      for(let r=0;r<8;r++)for(let c=0;c<8;c++){ctx.fillStyle=(r+c)%2===0?c1:c2;ctx.fillRect(c*cs,r*cs,cs,cs)}
      break
    }
    case 'label': {
      ctx.fillStyle=c1||'#ffffff';ctx.fillRect(0,0,size,size)
      ctx.strokeStyle=c2||'#cccccc';ctx.lineWidth=8;ctx.strokeRect(20,20,size-40,size-40)
      ctx.fillStyle=c2||'#cccccc';ctx.fillRect(40,80,size-80,12);ctx.fillRect(40,120,size-120,12);ctx.fillRect(40,160,size-100,12)
      break
    }
  }
  const tex = new THREE.CanvasTexture(canvas); tex.needsUpdate = true; return tex
}

// ── Exports ───────────────────────────────────────────────────
export async function exportGLB() {
  if (!scene) return
  const { GLTFExporter } = await import('three/addons/exporters/GLTFExporter.js')
  const exporter = new GLTFExporter()
  const exportScene = new THREE.Scene()
  objects.forEach(m => exportScene.add(m.clone()))
  exporter.parse(exportScene, (gltf) => {
    const blob = new Blob([gltf], { type:'application/octet-stream' })
    download(blob, 'model.glb')
  }, (e) => console.error(e), { binary: true })
}

export async function exportOBJ() {
  if (!scene) return
  const { OBJExporter } = await import('three/addons/exporters/OBJExporter.js')
  const exporter = new OBJExporter()
  const exportScene = new THREE.Scene()
  objects.forEach(m => exportScene.add(m.clone()))
  const result = exporter.parse(exportScene)
  download(new Blob([result], { type:'text/plain' }), 'model.obj')
}

export async function exportSTL() {
  if (!scene) return
  const { STLExporter } = await import('three/addons/exporters/STLExporter.js')
  const exporter = new STLExporter()
  const exportScene = new THREE.Scene()
  objects.forEach(m => exportScene.add(m.clone()))
  const result = exporter.parse(exportScene, { binary: true })
  download(new Blob([result], { type:'application/octet-stream' }), 'model.stl')
}

export function exportJSON(sceneData) {
  const blob = new Blob([JSON.stringify(sceneData, null, 2)], { type:'application/json' })
  download(blob, 'scene.json')
}

function download(blob, filename) {
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url; a.download = filename; a.click()
  URL.revokeObjectURL(url)
}

// ── Selection ─────────────────────────────────────────────────
export function setOnSelect(cb) { onSelectCallback = cb }

function handleClick(e) {
  if (!canvas_ref || !camera || !scene) return
  const rect = canvas_ref.getBoundingClientRect()
  const mouse = new THREE.Vector2(
    ((e.clientX-rect.left)/rect.width)*2-1,
    -((e.clientY-rect.top)/rect.height)*2+1
  )
  const raycaster = new THREE.Raycaster()
  raycaster.setFromCamera(mouse, camera)
  const hits = raycaster.intersectObjects(objects, false)
  if (hits.length > 0) selectObject(hits[0].object)
  else deselectAll()
}

function selectObject(mesh) {
  deselectAll()
  selectedMesh = mesh
  mesh.userData._origEmissive = mesh.material.emissive?.getHex?.() || 0
  mesh.material.emissive = new THREE.Color(0x553300)
  if (onSelectCallback) onSelectCallback({
    label:     mesh.userData.label || 'object',
    color:     '#' + mesh.material.color.getHexString(),
    metalness: mesh.material.metalness,
    roughness: mesh.material.roughness,
    opacity:   mesh.material.opacity,
    position:  [+mesh.position.x.toFixed(2), +mesh.position.y.toFixed(2), +mesh.position.z.toFixed(2)],
    scale:     [+mesh.scale.x.toFixed(2), +mesh.scale.y.toFixed(2), +mesh.scale.z.toFixed(2)],
    rotation:  [
      +(mesh.rotation.x * 180/Math.PI).toFixed(1),
      +(mesh.rotation.y * 180/Math.PI).toFixed(1),
      +(mesh.rotation.z * 180/Math.PI).toFixed(1)
    ]
  })
}

export function deselectAll() {
  if (selectedMesh) {
    selectedMesh.material.emissive = new THREE.Color(selectedMesh.userData._origEmissive || 0)
    selectedMesh = null
  }
  if (onSelectCallback) onSelectCallback(null)
}

export function updateSelectedMaterial({ color, metalness, roughness, opacity }) {
  if (!selectedMesh) return
  if (color !== undefined) {
    // Remove texture so color actually shows
    selectedMesh.material.map = null
    selectedMesh.material.color.set(color)
    selectedMesh.material.needsUpdate = true
  }
  if (metalness !== undefined) selectedMesh.material.metalness = metalness
  if (roughness !== undefined) selectedMesh.material.roughness = roughness
  if (opacity !== undefined) {
    selectedMesh.material.opacity = opacity
    selectedMesh.material.transparent = opacity < 1
  }
}

export function updateSelectedTransform({ px, py, pz, sx, sy, sz, rx, ry, rz }) {
  if (!selectedMesh) return
  if (px !== undefined) selectedMesh.position.x = px
  if (py !== undefined) selectedMesh.position.y = py
  if (pz !== undefined) selectedMesh.position.z = pz
  if (sx !== undefined) selectedMesh.scale.x = Math.max(0.01, sx)
  if (sy !== undefined) selectedMesh.scale.y = Math.max(0.01, sy)
  if (sz !== undefined) selectedMesh.scale.z = Math.max(0.01, sz)
  if (rx !== undefined) selectedMesh.rotation.x = rx * Math.PI / 180
  if (ry !== undefined) selectedMesh.rotation.y = ry * Math.PI / 180
  if (rz !== undefined) selectedMesh.rotation.z = rz * Math.PI / 180
}

// ── Viewer Core ───────────────────────────────────────────────
export function initViewer(canvas) {
  canvas_ref = canvas
  renderer = new THREE.WebGLRenderer({ canvas, antialias:true, alpha:true, preserveDrawingBuffer:true })
  renderer.setPixelRatio(window.devicePixelRatio)
  renderer.shadowMap.enabled = true
  renderer.shadowMap.type = THREE.PCFSoftShadowMap
  resize(canvas)
  window.addEventListener('resize', () => resize(canvas))

  let dragDist = 0
  canvas.addEventListener('mousedown', e => { isMouseDown=true; dragDist=0; lastMouse={x:e.clientX,y:e.clientY} })
  canvas.addEventListener('mouseup', e => { isMouseDown=false; if(dragDist<5) handleClick(e) })
  canvas.addEventListener('mousemove', e => {
    if (!isMouseDown) return
    const dx=e.clientX-lastMouse.x, dy=e.clientY-lastMouse.y
    dragDist+=Math.abs(dx)+Math.abs(dy); lastMouse={x:e.clientX,y:e.clientY}
    if (e.buttons===1) {
      cameraSpherical.theta-=dx*0.005
      cameraSpherical.phi=Math.max(0.1,Math.min(Math.PI-0.1,cameraSpherical.phi-dy*0.005))
    } else if (e.buttons===2) {
      camera.position.add(new THREE.Vector3(-dx*0.01,dy*0.01,0))
    }
    updateCamera()
  })
  canvas.addEventListener('contextmenu', e => e.preventDefault())
  canvas.addEventListener('wheel', e => {
    cameraSpherical.radius=Math.max(2,Math.min(50,cameraSpherical.radius+e.deltaY*0.01))
    updateCamera()
  })
}

function resize(canvas) {
  const w=canvas.clientWidth, h=canvas.clientHeight
  renderer.setSize(w,h,false)
  if (camera) { camera.aspect=w/h; camera.updateProjectionMatrix() }
}

function updateCamera() {
  if (!camera) return
  const {radius,theta,phi}=cameraSpherical
  camera.position.set(radius*Math.sin(phi)*Math.sin(theta),radius*Math.cos(phi),radius*Math.sin(phi)*Math.cos(theta))
  camera.lookAt(0,0,0)
}

export function buildScene(sceneData) {
  if (animId) cancelAnimationFrame(animId)
  if (scene) scene.clear()
  deselectAll()

  scene = new THREE.Scene()
  scene.background = new THREE.Color('#0d0d1a')
  scene.fog = new THREE.FogExp2('#0d0d1a', 0.03)

  camera = new THREE.PerspectiveCamera(60, 16/9, 0.1, 1000)
  cameraSpherical = { radius:10, theta:Math.PI/4, phi:Math.PI/3 }
  updateCamera()

  scene.add(new THREE.AmbientLight(0xffffff, 1.2))
  const dirLight = new THREE.DirectionalLight(0xffffff, 2.5)
  dirLight.position.set(5,10,5); dirLight.castShadow=true; dirLight.shadow.mapSize.set(1024,1024)
  scene.add(dirLight)
  const fillLight = new THREE.DirectionalLight(0x8888ff, 0.8)
  fillLight.position.set(-5, 3, -5)
  scene.add(fillLight)
  const rimLight = new THREE.DirectionalLight(0xffffff, 0.5)
  rimLight.position.set(0, -5, -10)
  scene.add(rimLight)

  const grid = new THREE.GridHelper(20,20,'#2a2a4e','#1a1a2e')
  grid.position.y=-0.01; scene.add(grid)

  objects = []
  for (const obj of sceneData.objects||[]) {
    const geo = makeGeometry(obj.type, obj.scale)
    const pattern = obj.pattern||{type:'solid'}
    const tex = pattern.type==='solid' ? null : createTexture({...pattern, colors:pattern.colors||[obj.color||'#888888']})
    const isGlass = pattern.type==='glass'
    const mat = new THREE.MeshStandardMaterial({
      map: tex,
      color: tex ? '#ffffff' : (obj.color||'#888888'),
      metalness: pattern.type==='metal' ? 0.8 : (obj.metalness??0),
      roughness: pattern.type==='metal' ? 0.2 : (obj.roughness??0.6),
      transparent: isGlass||(obj.opacity??1)<1,
      opacity: isGlass ? 0.4 : (obj.opacity??1),
      emissive: new THREE.Color(0x000000)
    })
    const mesh = new THREE.Mesh(geo, mat)
    mesh.position.set(...(obj.position||[0,1,0]))
    mesh.rotation.set(...(obj.rotation||[0,0,0]))
    mesh.castShadow=true; mesh.receiveShadow=true
    mesh.userData = { label:obj.label, objData:obj }
    scene.add(mesh); objects.push(mesh)

    const edges = new THREE.EdgesGeometry(geo)
    mesh.add(new THREE.LineSegments(edges, new THREE.LineBasicMaterial({color:'#ffffff',transparent:true,opacity:0.08})))
  }

  const floor = new THREE.Mesh(new THREE.PlaneGeometry(30,30), new THREE.ShadowMaterial({opacity:0.3}))
  floor.rotation.x=-Math.PI/2; floor.position.y=-0.01; floor.receiveShadow=true; scene.add(floor)
  animate()
}

function makeGeometry(type, scale=[1,1,1]) {
  const [sx,sy,sz]=scale
  switch(type) {
    case 'sphere':   return new THREE.SphereGeometry(sx*0.5,64,64)
    case 'cylinder': return new THREE.CylinderGeometry(sx*0.5,sx*0.5,sy,32)
    case 'cone':     return new THREE.ConeGeometry(sx*0.5,sy,32)
    case 'torus':    return new THREE.TorusGeometry(sx*0.5,sx*0.15,16,64)
    case 'plane':    return new THREE.PlaneGeometry(sx,sz)
    default:         return new THREE.BoxGeometry(sx,sy,sz)
  }
}

export function toggleWireframe() {
  wireframeMode=!wireframeMode
  objects.forEach(m=>{if(m.material)m.material.wireframe=wireframeMode})
  return wireframeMode
}
export function toggleAutoRotate() { autoRotate=!autoRotate; return autoRotate }
export function resetCamera() { cameraSpherical={radius:10,theta:Math.PI/4,phi:Math.PI/3}; updateCamera() }

function animate() {
  animId=requestAnimationFrame(animate)
  if (autoRotate) { cameraSpherical.theta+=0.005; updateCamera() }
  renderer.render(scene,camera)
}