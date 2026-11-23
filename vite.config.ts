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
            urlPattern: ({ url }) => url.origin === 'https://fonts.googleapis.com' || url.origin === 'https://fonts.gstatic.com',
            handler: 'StaleWhileRevalidate',
            options: { cacheName: 'fonts', expiration: { maxEntries: 30 } },
          },
          // Supabase (auth, database, realtime) is never cached: multiplayer must stay live
        ],
      },
    }),
  ],
  server: { port: 5173 },
  test: { environment: 'node', include: ['src/**/*.test.ts'] },
} as any);
