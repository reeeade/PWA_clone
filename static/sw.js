const STATIC_CACHE_V1 = 'pwa-cache-v1.2';
const cacheAssets = [
  '/',
  '/static/styles.css',
  '/static/app.js',
  '/static/manifest.json',
  '/static/icons/ico.png',
  '/static/icons/ico512.png',
  '/static/screenshots/jackpot_center.png',
  '/static/screenshots/jackpot_left.png',
  '/static/screenshots/jackpot_right.png',
];

// Установка Service Worker
self.addEventListener('install', (e) => {
  console.log('Service Worker: Installed');
  e.waitUntil(
    caches.open(STATIC_CACHE_V1).then((cache) => {
      console.log('Service Worker: Caching files');
      return cache.addAll(cacheAssets);
    })
  );
});

// Активация Service Worker
self.addEventListener('activate', (e) => {
  console.log('Service Worker: Activated');
  e.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cache) => {
          if (cache !== STATIC_CACHE_V1) {
            console.log('Service Worker: Clearing old cache');
            return caches.delete(cache);
          }
        })
      );
    })
  );
});

// Обработка запросов
self.addEventListener('fetch', (e) => {
  console.log('Service Worker: Fetching request');
  e.respondWith(
    caches.match(e.request).then((response) => {
      return response || fetch(e.request).catch(() => caches.match('/fallback.html'));
    })
  );
});
