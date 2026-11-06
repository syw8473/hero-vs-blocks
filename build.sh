#!/bin/sh
# tile-kiln.html is the page published as a Claude artifact (the host adds the <html>/<head> wrapper).
# index.html is the same page wrapped in a full HTML document for GitHub Pages, plus the PWA bits
# (install manifest, home-screen icons, offline service worker) that only work on a real website.
cd "$(dirname "$0")"
{
  printf '<!doctype html>\n<html lang="zh-Hant">\n<head>\n<meta charset="utf-8">\n'
  printf '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
  printf '<link rel="manifest" href="manifest.webmanifest">\n'
  printf '<meta name="theme-color" content="#0e2a2d">\n'
  printf '<link rel="icon" type="image/png" sizes="192x192" href="icons/icon-192.png">\n'
  printf '<link rel="apple-touch-icon" href="icons/apple-touch-icon.png">\n'
  printf '<meta name="apple-mobile-web-app-capable" content="yes">\n<meta name="mobile-web-app-capable" content="yes">\n'
  printf '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">\n'
  printf '<meta name="apple-mobile-web-app-title" content="勇者鬥磚塊">\n'
  printf '<style>[hidden]{display:none!important}:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px);box-sizing:border-box}</style>\n'
  cat tile-kiln.html
  printf '\n<script>if ("serviceWorker" in navigator) addEventListener("load", () => navigator.serviceWorker.register("sw.js").catch(() => {}));</script>\n'
  printf '</html>\n'
} > index.html
