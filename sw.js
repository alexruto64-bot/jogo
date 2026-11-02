// Guarda os arquivos do jogo no navegador para ele abrir sem internet e poder ser instalado no PC.
// Sempre tenta a internet primeiro (assim cada atualização do jogo chega na hora) e, se não houver conexão, usa a cópia
// guardada. Só guarda os arquivos do próprio jogo e o Three.js do jsDelivr.
const CACHE = 'cavaleiro-do-teide';
const THREE_JS = 'https://cdn.jsdelivr.net/npm/three@0.147.0/';

self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', (e) => e.waitUntil(self.clients.claim()));

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  if (!req.url.startsWith(self.location.origin) && !req.url.startsWith(THREE_JS)) return;
  e.respondWith(
    fetch(req)
      .then((res) => {
        if (res.ok || res.type === 'opaque') {
          const copia = res.clone();
          caches.open(CACHE).then((c) => c.put(req, copia));
        }
        return res;
      })
      .catch(() => caches.match(req).then((guardada) => guardada || Response.error())),
  );
});
