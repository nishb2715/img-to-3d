// uploader.js - Image upload handling module
// This is a utility module; core upload logic lives in main.js
// Use this if you want to extract upload logic into a reusable class

export class ImageUploader {
  constructor({ dropZoneId, fileInputId, previewImgId, onFileReady }) {
    this.dropZone = document.getElementById(dropZoneId)
    this.fileInput = document.getElementById(fileInputId)
    this.previewImg = document.getElementById(previewImgId)
    this.onFileReady = onFileReady
    this.selectedFile = null

    this._bindEvents()
  }

  _bindEvents() {
    // File input change
    this.fileInput.addEventListener('change', (e) => {
      this._handleFile(e.target.files[0])
    })

    // Drag over
    this.dropZone.addEventListener('dragover', (e) => {
      e.preventDefault()
      this.dropZone.classList.add('dragover')
    })

    // Drag leave
    this.dropZone.addEventListener('dragleave', () => {
      this.dropZone.classList.remove('dragover')
    })

    // Drop
    this.dropZone.addEventListener('drop', (e) => {
      e.preventDefault()
      this.dropZone.classList.remove('dragover')
      const file = e.dataTransfer.files[0]
      this._handleFile(file)
    })
  }

  _handleFile(file) {
    if (!file) return

    // Validate type
    if (!file.type.startsWith('image/')) {
      console.warn('Unsupported file type:', file.type)
      this._showError('Please upload a valid image (JPG, PNG, WebP).')
      return
    }

    // Validate size (max 10MB)
    const MAX_SIZE = 10 * 1024 * 1024
    if (file.size > MAX_SIZE) {
      this._showError('Image too large. Max size is 10MB.')
      return
    }

    this.selectedFile = file
    this._showPreview(file)

    // Notify parent
    if (typeof this.onFileReady === 'function') {
      this.onFileReady(file)
    }
  }

  _showPreview(file) {
    const url = URL.createObjectURL(file)
    this.previewImg.src = url
    this.previewImg.style.display = 'block'
    this.previewImg.style.marginTop = '0.75rem'

    // Free memory when preview changes
    this.previewImg.onload = () => URL.revokeObjectURL(url)
  }

  _showError(msg) {
    // Briefly highlight drop zone in red
    this.dropZone.style.borderColor = 'var(--error)'
    this.dropZone.style.background = 'rgba(239,68,68,0.05)'
    setTimeout(() => {
      this.dropZone.style.borderColor = ''
      this.dropZone.style.background = ''
    }, 2000)
    console.error('[Uploader]', msg)
  }

  getFile() {
    return this.selectedFile
  }

  reset() {
    this.selectedFile = null
    this.fileInput.value = ''
    this.previewImg.src = ''
    this.previewImg.style.display = 'none'
  }
}