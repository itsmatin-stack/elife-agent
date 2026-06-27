const CACHE = 'elife-v1';
const ASSETS = [
  '/',
  '/index.html',
  '/assets/core.css',
  '/assets/core.js',
  '/manifest.json',
  '/pages/dashboard.html',
  '/pages/tasks.html',
  '/pages/notes.html',
  '/pages/customers.html',
  '/pages/orders.html',
  '/pages/analytics.html',
  '/pages/invoices.html',
  '/pages/calendar.html',
  '/pages/reminders.html',
  '/pages/files.html',
  '/pages/research.html',
  '/pages/code.html',
  '/pages/translate.html',
  '/pages/profile.html',
  '/pages/history.html',
  '/pages/vault.html',
  '/pages/notifications.html',
  '/pages/saved.html',
  '/pages/emails.html',
  '/pages/settings.html',
  '/pages/apikeys.html',
  '/pages/about.html',
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  // API calls — always network
  if(e.request.url.includes('/api/') || e.request.url.includes('groq.com')) {
    return e.respondWith(fetch(e.request).catch(() => new Response('{"error":"offline"}', {headers:{'Content-Type':'application/json'}})));
  }
  // Assets — cache first
  e.respondWith(
    caches.match(e.request).then(cached => cached || fetch(e.request).then(res => {
      const clone = res.clone();
      caches.open(CACHE).then(c => c.put(e.request, clone));
      return res;
    }))
  );
});
