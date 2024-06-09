let staticCacheName = 'djangopwa-v1';

let crucialUrls = [
    "/offline-page/",
]

self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(staticCacheName).then(function(cache) {
      return cache.addAll([
        'offline/',
        ...crucialUrls,
      ]);
    })
  );
});
 
self.addEventListener('fetch', function(event) {
    event.respondWith(
      caches.match(event.request).then(function(response) {
        return response || fetch(event.request);
      }).catch(() => {
        return caches.match("/offline-page/");
      })
    );
});