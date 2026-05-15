import { defineConfig } from 'vite'

export default defineConfig({
  server: {
    port: 5173,
    proxy: { '/api': 'http://localhost:8000' }
  },
  resolve: {
    alias: {
      'three/addons': 'three/examples/jsm'
    }
  }
})