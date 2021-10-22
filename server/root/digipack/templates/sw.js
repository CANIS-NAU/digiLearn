var staticCacheName = 'digipackpwa-v1';

self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(staticCacheName).then(function(cache) {
      return cache.addAll([
        '/'
      ]);
    })
  );
});

// this function caches the index page of the webapp
self.addEventListener('fetch', function(event) {
  var requestUrl = new URL(event.request.url);
    if (requestUrl.origin === location.origin) {
      if ((requestUrl.pathname === '/')) {
        event.respondWith(caches.match('/'));
        return;
      }
    }

    event.respondWith(
      
      // caches the main page
      caches.match(event.request).then(function(response) {
        return response || fetch(event.request);
      }),

      // dynamically caches 
      caches.open('mysite-dynamic').then(function(cache) {
        return fetch(event.request).then(function(response) {
          cache.put(event.request, response.clone());
          return response;
        });
      })

    );


});