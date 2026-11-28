import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',   // a new deploy takes over on the next visit
      injectRegister: 'auto',
      manifest: false,              // we ship public/manifest.webmanifest ourselves
      workbox: {
        globPatterns: ['**/*.{js,css,html,svg,png,ico,webmanifest}', 'site/*.webp'],
        // source collages dropped into cases/*/images/ before cutting are never part of the app shell
        globIgnores: ['cases/**/*.png'],
        navigateFallback: '/index.html',
        navigateFallbackDenylist: [/^\/cases\//, /^\/sw\.js$/],
        cleanupOutdatedCaches: true,
        runtimeCaching: [
          {
            // case files: always try the network first so edits show up, fall back offline
            urlPattern: ({ url, sameOrigin }) => sameOrigin && url.pathname.startsWith('/cases/') && url.pathname.endsWith('.json'),
            handler: 'NetworkFirst',
            options: { cacheName: 'case-data', networkTimeoutSeconds: 4, expiration: { maxEntries: 80 } },
          },
          {
            urlPattern: ({ request, sameOrigin }) => sameOrigin && request.destination === 'image',
            handler: 'CacheFirst',
            options: { cacheName: 'images', expiration: { maxEntries: 400, maxAgeSeconds: 60 * 60 * 24 * 30 } },
          },
          {
            // sound effects and case audio (ambience, narration): fetched by the board, kept for offline play
            urlPattern: ({ url, sameOrigin }) => sameOrigin && url.pathname.endsWith('.mp3') && (url.pathname.startsWith('/sfx/') || url.pathname.startsWith('/cases/')),
            handler: 'CacheFirst',
            options: { cacheName: 'audio', expiration: { maxEntries: 200, maxAgeSeconds: 60 * 60 * 24 * 30 } },
          },
          {
            urlPattern: ({ url }) => url.origin === 'https://fonts.googleapis.com' || url.origin === 'https://fonts.gstatic.com',
            handler: 'StaleWhileRevalidate',
            options: { cacheName: 'fonts', expiration: { maxEntries: 30 } },
          },
          {
            // ONNX Runtime WebAssembly (~22 MB) for the on-device voice: cached after first use
            urlPattern: ({ url, sameOrigin }) => sameOrigin && url.pathname.endsWith('.wasm'),
            handler: 'CacheFirst',
            options: { cacheName: 'tts-runtime', expiration: { maxEntries: 4 } },
          },
          // the voice model itself (~400 MB) lives in its own Cache Storage, filled only after consent
          // Supabase (auth, database, realtime) is never cached: multiplayer must stay live
        ],
      },
    }),
  ],
  worker: { format: 'es' },
  optimizeDeps: { exclude: ['onnxruntime-web'] }, // keeps its .wasm URLs intact and avoids a dev reload on first use // on-device TTS worker (src/lib/supertonic/worker.ts) uses ES module imports
  // cross-origin isolation: lets onnxruntime-web use several WebAssembly threads for the on-device voice
  server: { port: 5173, headers: { 'Cross-Origin-Opener-Policy': 'same-origin', 'Cross-Origin-Embedder-Policy': 'require-corp' } },
  preview: { headers: { 'Cross-Origin-Opener-Policy': 'same-origin', 'Cross-Origin-Embedder-Policy': 'require-corp' } },
  test: { environment: 'node', include: ['src/**/*.test.ts', 'supabase/functions/**/*.test.ts'] },
} as any);
