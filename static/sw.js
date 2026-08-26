const CACHE_NAME = "rekap-kp-v1";
const ASSETS = [
    "/",
    "/static/css/style.css",
    "/static/js/app.js",
    "/static/js/auth.js",
    "/static/js/admin.js",
    "/static/manifest.json"
];

self.addEventListener("install", event => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => {
            return cache.addAll(ASSETS);
        })
    );
});

self.addEventListener("fetch", event => {
    event.respondWith(
        fetch(event.request).catch(() => caches.match(event.request))
    );
});
