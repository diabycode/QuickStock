let staticCacheName = 'djangopwa-v1';

let crucialUrls = [
    "/sales/",
    "/sales/create/",
    "/offline-page/",
    "/static/css/quickstockapp/form.css",
    "/static/css/quickstockapp/filter_form.css",
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
  let requestUrl = new URL(event.request.url);
    if (requestUrl.origin === location.origin) {
      if ((requestUrl.pathname === '/')) {
        event.respondWith(caches.match(''));
        return;
      }
    }
    event.respondWith(
      caches.match(event.request).then(function(response) {
        return response || fetch(event.request);
      }).catch(() => {
        return caches.match("/offline-page/");
      })
    );
});