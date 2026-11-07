/* Shop Calculator - offline cache. Bump CACHE when any listed file changes. */
var CACHE = "shop-calculator-v1";
var FILES = [
  "./", "index.html", "manifest.webmanifest",
  "icons/icon-192.png", "icons/icon-512.png", "icons/icon-maskable-512.png", "icons/apple-touch-icon.png",
  "vendor/fonts.css",
  "vendor/jspdf.umd.min.js", "vendor/jspdf.plugin.autotable.min.js",
  "vendor/fonts/Inter-400.woff2", "vendor/fonts/Inter-500.woff2", "vendor/fonts/Inter-600.woff2",
  "vendor/fonts/Inter-700.woff2", "vendor/fonts/Inter-800.woff2",
  "vendor/fonts/JetBrainsMono-400.woff2", "vendor/fonts/JetBrainsMono-500.woff2", "vendor/fonts/JetBrainsMono-700.woff2"
];

self.addEventListener("install", function (e) {
  e.waitUntil(caches.open(CACHE).then(function (c) { return c.addAll(FILES); }).then(function () { return self.skipWaiting(); }));
});

self.addEventListener("activate", function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.filter(function (k) { return k !== CACHE; }).map(function (k) { return caches.delete(k); }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener("fetch", function (e) {
  if (e.request.method !== "GET") return;
  e.respondWith(
    caches.match(e.request, { ignoreSearch: true }).then(function (hit) {
      return hit || fetch(e.request).catch(function () { return caches.match("index.html"); });
    })
  );
});
