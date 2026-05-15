import { generateScene, editScene } from './api.js'
import {
  initViewer, buildScene, toggleWireframe, toggleAutoRotate, resetCamera,
  exportGLB, exportOBJ, exportSTL, exportJSON,
  setOnSelect, updateSelectedMaterial, updateSelectedTransform, deselectAll
} from './viewer3d.js'

// Elements
const fileInput      = document.getElementById('file-input')
const dropZone       = document.getElementById('drop-zone')
const previewImg     = document.getElementById('preview-img')
const btnGenerate    = document.getElementById('btn-generate')
const statusBox      = document.getElementById('status-box')
const sceneInfo      = document.getElementById('scene-info')
const spinner        = document.getElementById('spinner')
const placeholder    = document.getElementById('placeholder-text')
const viewerControls = document.getElementById('viewer-controls')
const hint           = document.getElementById('hint')
const selectHint     = document.getElementById('select-hint')
const detailTabs     = document.querySelectorAll('.detail-tab')
const canvas         = document.getElementById('three-canvas')
const promptInput    = document.getElementById('prompt-input')
const btnPrompt      = document.getElementById('btn-prompt')
const btnSnapshot    = document.getElementById('btn-snapshot')
const historyList    = document.getElementById('history-list')

// Editor
const editorEmpty    = document.getElementById('editor-empty')
const editorControls = document.getElementById('editor-controls')
const selectedLabel  = document.getElementById('selected-label')
const propColor      = document.getElementById('prop-color')
const propMaterial   = document.getElementById('prop-material')
const propMetalness  = document.getElementById('prop-metalness')
const propRoughness  = document.getElementById('prop-roughness')
const propOpacity    = document.getElementById('prop-opacity')
const valMetalness   = document.getElementById('val-metalness')
const valRoughness   = document.getElementById('val-roughness')
const valOpacity     = document.getElementById('val-opacity')
const posX = document.getElementById('pos-x')
const posY = document.getElementById('pos-y')
const posZ = document.getElementById('pos-z')
const scaleX = document.getElementById('scale-x')
const scaleY = document.getElementById('scale-y')
const scaleZ = document.getElementById('scale-z')
const rotX = document.getElementById('rot-x')
const rotY = document.getElementById('rot-y')
const rotZ = document.getElementById('rot-z')

// Export buttons
const btnExportGlb    = document.getElementById('btn-export-glb')
const btnExportGlbTop = document.getElementById('btn-export-glb-top')
const btnExportObj    = document.getElementById('btn-export-obj')
const btnExportStl    = document.getElementById('btn-export-stl')
const btnExportJson   = document.getElementById('btn-export-json')

let selectedFile  = null
let detailLevel   = 'medium'
let currentScene  = null
let versionHistory = []

// ── Material presets ──────────────────────────────────────────
const MATERIAL_PRESETS = {
  matte:   { metalness: 0.0, roughness: 0.9 },
  metal:   { metalness: 0.9, roughness: 0.1 },
  glass:   { metalness: 0.0, roughness: 0.0, opacity: 0.4 },
  plastic: { metalness: 0.0, roughness: 0.5 },
  wood:    { metalness: 0.0, roughness: 0.8 },
  rubber:  { metalness: 0.0, roughness: 1.0 },
}

initViewer(canvas)

// ── Selection callback ────────────────────────────────────────
setOnSelect((props) => {
  if (!props) {
    editorEmpty.style.display = 'block'
    editorControls.style.display = 'none'
    return
  }
  editorEmpty.style.display = 'none'
  editorControls.style.display = 'block'
  selectedLabel.textContent = `Selected: ${props.label}`
  propColor.value = props.color
  propMetalness.value = props.metalness
  propRoughness.value = props.roughness
  propOpacity.value = props.opacity
  valMetalness.textContent = Number(props.metalness).toFixed(2)
  valRoughness.textContent = Number(props.roughness).toFixed(2)
  valOpacity.textContent   = Number(props.opacity).toFixed(2)
  propMaterial.value = 'custom'
  // Transform
  posX.value = props.position[0]; posY.value = props.position[1]; posZ.value = props.position[2]
  scaleX.value = props.scale[0];  scaleY.value = props.scale[1];  scaleZ.value = props.scale[2]
  rotX.value = props.rotation[0]; rotY.value = props.rotation[1]; rotZ.value = props.rotation[2]
})

// ── Material controls ─────────────────────────────────────────
propColor.addEventListener('input', () => updateSelectedMaterial({ color: propColor.value }))

propMaterial.addEventListener('change', () => {
  const preset = MATERIAL_PRESETS[propMaterial.value]
  if (!preset) return
  propMetalness.value = preset.metalness
  propRoughness.value = preset.roughness
  if (preset.opacity !== undefined) propOpacity.value = preset.opacity
  valMetalness.textContent = preset.metalness.toFixed(2)
  valRoughness.textContent = preset.roughness.toFixed(2)
  if (preset.opacity !== undefined) valOpacity.textContent = preset.opacity.toFixed(2)
  updateSelectedMaterial({
    metalness: preset.metalness,
    roughness: preset.roughness,
    ...(preset.opacity !== undefined ? { opacity: preset.opacity } : {})
  })
})

propMetalness.addEventListener('input', () => {
  valMetalness.textContent = Number(propMetalness.value).toFixed(2)
  updateSelectedMaterial({ metalness: parseFloat(propMetalness.value) })
  propMaterial.value = 'custom'
})
propRoughness.addEventListener('input', () => {
  valRoughness.textContent = Number(propRoughness.value).toFixed(2)
  updateSelectedMaterial({ roughness: parseFloat(propRoughness.value) })
  propMaterial.value = 'custom'
})
propOpacity.addEventListener('input', () => {
  valOpacity.textContent = Number(propOpacity.value).toFixed(2)
  updateSelectedMaterial({ opacity: parseFloat(propOpacity.value) })
})
const scaleLock = document.getElementById('scale-lock')

// Override scale inputs to support lock
function applyScale(axis, value) {
  if (scaleLock.checked && axis !== 'all') {
    // proportional: find ratio
    const oldVal = parseFloat(
      axis === 'x' ? scaleX.value :
      axis === 'y' ? scaleY.value : scaleZ.value
    ) || 1
    const ratio = value / oldVal
    const nx = parseFloat(scaleX.value) * ratio
    const ny = parseFloat(scaleY.value) * ratio
    const nz = parseFloat(scaleZ.value) * ratio
    scaleX.value = nx.toFixed(2)
    scaleY.value = ny.toFixed(2)
    scaleZ.value = nz.toFixed(2)
    updateSelectedTransform({ sx: nx, sy: ny, sz: nz })
  } else if (axis === 'all') {
    // handled by buttons
  } else {
    updateSelectedTransform({
      sx: axis === 'x' ? value : undefined,
      sy: axis === 'y' ? value : undefined,
      sz: axis === 'z' ? value : undefined,
    })
  }
}


// Scale buttons (+X -X +Y -Y +Z -Z +All -All)
document.querySelectorAll('.scale-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const axis = btn.dataset.axis
    const dir  = parseFloat(btn.dataset.dir)
    const step = 0.2

    if (axis === 'all') {
      const nx = Math.max(0.01, parseFloat(scaleX.value) + dir * step)
      const ny = Math.max(0.01, parseFloat(scaleY.value) + dir * step)
      const nz = Math.max(0.01, parseFloat(scaleZ.value) + dir * step)
      scaleX.value = nx.toFixed(2)
      scaleY.value = ny.toFixed(2)
      scaleZ.value = nz.toFixed(2)
      updateSelectedTransform({ sx: nx, sy: ny, sz: nz })
    } else if (scaleLock.checked) {
      const oldVal = parseFloat(
        axis === 'x' ? scaleX.value :
        axis === 'y' ? scaleY.value : scaleZ.value
      ) || 1
      const newVal = Math.max(0.01, oldVal + dir * step)
      const ratio = newVal / oldVal
      const nx = Math.max(0.01, parseFloat(scaleX.value) * ratio)
      const ny = Math.max(0.01, parseFloat(scaleY.value) * ratio)
      const nz = Math.max(0.01, parseFloat(scaleZ.value) * ratio)
      scaleX.value = nx.toFixed(2)
      scaleY.value = ny.toFixed(2)
      scaleZ.value = nz.toFixed(2)
      updateSelectedTransform({ sx: nx, sy: ny, sz: nz })
    } else {
      // free axis only
      const input = axis === 'x' ? scaleX : axis === 'y' ? scaleY : scaleZ
      const newVal = Math.max(0.01, parseFloat(input.value) + dir * step)
      input.value = newVal.toFixed(2)
      updateSelectedTransform({
        sx: axis === 'x' ? newVal : undefined,
        sy: axis === 'y' ? newVal : undefined,
        sz: axis === 'z' ? newVal : undefined,
      })
    }
  })
})

// ── Transform controls ────────────────────────────────────────
posX.addEventListener('input', () => updateSelectedTransform({ px: parseFloat(posX.value) }))
posY.addEventListener('input', () => updateSelectedTransform({ py: parseFloat(posY.value) }))
posZ.addEventListener('input', () => updateSelectedTransform({ pz: parseFloat(posZ.value) }))
scaleX.addEventListener('input', () => updateSelectedTransform({ sx: parseFloat(scaleX.value) }))
scaleY.addEventListener('input', () => updateSelectedTransform({ sy: parseFloat(scaleY.value) }))
scaleZ.addEventListener('input', () => updateSelectedTransform({ sz: parseFloat(scaleZ.value) }))
rotX.addEventListener('input', () => updateSelectedTransform({ rx: parseFloat(rotX.value) }))
rotY.addEventListener('input', () => updateSelectedTransform({ ry: parseFloat(rotY.value) }))
rotZ.addEventListener('input', () => updateSelectedTransform({ rz: parseFloat(rotZ.value) }))

// ── Detail tabs ───────────────────────────────────────────────
detailTabs.forEach(tab => {
  tab.addEventListener('click', () => {
    detailTabs.forEach(t => t.classList.remove('active'))
    tab.classList.add('active')
    detailLevel = tab.dataset.val
  })
})

// ── File handling ─────────────────────────────────────────────
fileInput.addEventListener('change', e => handleFile(e.target.files[0]))
dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('dragover') })
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'))
dropZone.addEventListener('drop', e => {
  e.preventDefault(); dropZone.classList.remove('dragover')
  handleFile(e.dataTransfer.files[0])
})

function handleFile(file) {
  if (!file || !file.type.startsWith('image/')) return
  selectedFile = file
  previewImg.src = URL.createObjectURL(file)
  previewImg.style.display = 'block'
  previewImg.style.marginTop = '0.5rem'
  btnGenerate.disabled = false
  setStatus('Image ready — click Generate!', '')
}

// ── Generate ──────────────────────────────────────────────────
btnGenerate.addEventListener('click', async () => {
  if (!selectedFile) return
  setGenerating(true)
  setStatus('Analyzing image with Groq Vision...', 'loading')
  try {
    const result = await generateScene(selectedFile, detailLevel)
    currentScene = result.scene
    showScene(currentScene)
  } catch (err) {
    setStatus(`✗ Error: ${err.message}`, 'error')
    placeholder.textContent = 'Generation failed. Try again.'
    placeholder.style.display = 'block'
  } finally {
    setGenerating(false)
  }
})

// ── AI Prompt Edit ────────────────────────────────────────────
btnPrompt.addEventListener('click', async () => {
  const prompt = promptInput.value.trim()
  if (!prompt || !currentScene) return
  btnPrompt.disabled = true
  setStatus(`Applying: "${prompt}"...`, 'loading')
  try {
    const result = await editScene(currentScene, prompt)
    currentScene = result.scene
    showScene(currentScene)
    promptInput.value = ''
    setStatus(`✓ Applied: "${prompt}"`, 'success')
  } catch (err) {
    setStatus(`✗ Edit failed: ${err.message}`, 'error')
  } finally {
    btnPrompt.disabled = false
  }
})
promptInput.addEventListener('keydown', e => { if (e.key==='Enter') btnPrompt.click() })

// ── Version History ───────────────────────────────────────────
btnSnapshot.addEventListener('click', () => {
  if (!currentScene) return
  const snap = {
    scene: JSON.parse(JSON.stringify(currentScene)),
    label: currentScene.scene_title,
    time: new Date().toLocaleTimeString()
  }
  versionHistory.unshift(snap)
  renderHistory()
  setStatus(`✓ Version saved: "${snap.label}"`, 'success')
})

function renderHistory() {
  if (versionHistory.length === 0) {
    historyList.innerHTML = '<div style="font-size:0.65rem;color:var(--muted);font-family:\'Space Mono\',monospace">No versions saved yet</div>'
    return
  }
  historyList.innerHTML = versionHistory.map((v, i) => `
    <div class="history-item" data-idx="${i}">
      <span>${v.label} · ${v.time}</span>
      <span class="restore-btn">Restore</span>
    </div>
  `).join('')
  historyList.querySelectorAll('.history-item').forEach(el => {
    el.addEventListener('click', () => {
      const idx = parseInt(el.dataset.idx)
      currentScene = JSON.parse(JSON.stringify(versionHistory[idx].scene))
      showScene(currentScene)
      setStatus(`✓ Restored: "${versionHistory[idx].label}"`, 'success')
    })
  })
}

// ── Exports ───────────────────────────────────────────────────
btnExportGlb.addEventListener('click', () => exportGLB())
btnExportGlbTop.addEventListener('click', () => exportGLB())
btnExportObj.addEventListener('click', () => exportOBJ())
btnExportStl.addEventListener('click', () => exportSTL())
btnExportJson.addEventListener('click', () => exportJSON(currentScene))

// ── Show scene helper ─────────────────────────────────────────
function showScene(scene) {
  buildScene(scene)
  const count = scene.objects?.length || 0
  setStatus(`✓ ${count} object(s) · "${scene.scene_title}"`, 'success')
  document.getElementById('scene-title').textContent = scene.scene_title
  document.getElementById('scene-desc').textContent = scene.description
  const pillContainer = document.getElementById('scene-objects')
  pillContainer.innerHTML = (scene.objects||[]).map(o =>
    `<span class="obj-pill">${o.type}: ${o.label}</span>`
  ).join('')
  sceneInfo.style.display = 'block'
  viewerControls.style.display = 'flex'
  hint.style.display = 'block'
  selectHint.style.display = 'block'
  btnExportGlb.disabled = false
  btnExportGlbTop.disabled = false
  btnExportObj.disabled = false
  btnExportStl.disabled = false
  btnExportJson.disabled = false
  btnPrompt.disabled = false
  btnSnapshot.disabled = false
}

function setGenerating(on) {
  btnGenerate.disabled = on
  spinner.style.display = on ? 'block' : 'none'
  placeholder.style.display = on ? 'none' : (currentScene ? 'none' : 'block')
  if (on) {
    sceneInfo.style.display = 'none'
    viewerControls.style.display = 'none'
    hint.style.display = 'none'
    selectHint.style.display = 'none'
  }
}

function setStatus(msg, type) {
  statusBox.textContent = msg
  statusBox.className = 'status-box' + (type ? ` ${type}` : '')
}

// ── Viewer controls ───────────────────────────────────────────
document.getElementById('btn-reset-cam').addEventListener('click', resetCamera)
document.getElementById('btn-wireframe').addEventListener('click', function() {
  this.textContent = toggleWireframe() ? '◫ Solid' : '◫ Wireframe'
})
document.getElementById('btn-autorotate').addEventListener('click', function() {
  this.textContent = toggleAutoRotate() ? '↻ Stop' : '↻ Rotate'
})