#!/bin/sh
# tile-kiln.html is the page published as a Claude artifact (the host adds the <html>/<head> wrapper).
# index.html is the same page wrapped in a full HTML document, for GitHub Pages or opening the file directly.
cd "$(dirname "$0")"
{
  printf '<!doctype html>\n<html lang="zh-Hant">\n<head>\n<meta charset="utf-8">\n'
  printf '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
  printf '<style>[hidden]{display:none!important}:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px);box-sizing:border-box}</style>\n'
  cat tile-kiln.html
  printf '\n</html>\n'
} > index.html
