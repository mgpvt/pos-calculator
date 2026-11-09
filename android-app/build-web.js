// Copies the web app (one level up) into ./www so Capacitor can bundle it.
// The service worker is left out on purpose: the native app already ships its files.
const fs = require("fs"), path = require("path");
const src = path.resolve(__dirname, "..");
const dst = path.join(__dirname, "www");
fs.rmSync(dst, { recursive: true, force: true });
fs.mkdirSync(dst, { recursive: true });
for (const f of ["index.html", "manifest.webmanifest", "guide.html"]) fs.copyFileSync(path.join(src, f), path.join(dst, f));
for (const d of ["icons", "vendor", "guide-img"]) fs.cpSync(path.join(src, d), path.join(dst, d), { recursive: true });
fs.rmSync(path.join(dst, "icons", "store-icon-1024.png"), { force: true });
console.log("www ready:", fs.readdirSync(dst).join(", "));
