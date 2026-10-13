#!/usr/bin/env python3
"""
Script de montagem do protótipo GHC Gestão.
Junta HTML, CSS, Logo base64, Core, Seed e Módulos em um único arquivo HTML autônomo.
"""
import base64
import glob
import os
import sys

def main():
    root = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(root, "src")
    out_file = os.path.join(root, "ghc_gestao.html")

    # 1. Carregar logo em base64
    logo_path = os.path.join(root, "public", "logo-ghc.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_b64 = "data:image/png;base64," + base64.b64encode(f.read()).decode("ascii")
    else:
        logo_b64 = ""

    # 2. Carregar CSS
    with open(os.path.join(src, "styles.css"), "r", encoding="utf-8") as f:
        css = f.read()

    # 3. Carregar JavaScript na ordem correta
    js_parts = []
    
    with open(os.path.join(src, "core.js"), "r", encoding="utf-8") as f:
        js_parts.append(f.read())

    with open(os.path.join(src, "seed.js"), "r", encoding="utf-8") as f:
        js_parts.append(f.read())

    modules_dir = os.path.join(src, "modules")
    if os.path.isdir(modules_dir):
        mod_files = sorted(glob.glob(os.path.join(modules_dir, "*.js")))
        for mf in mod_files:
            with open(mf, "r", encoding="utf-8") as f:
                js_parts.append(f"/* Module: {os.path.basename(mf)} */\n" + f.read())

    # Inicialização do App no fim do script
    js_parts.append("\n/* Inicialização */\ndocument.addEventListener('DOMContentLoaded', () => { App.start(); });\n")

    full_js = "\n\n".join(js_parts)

    # 4. Injetar no index.html
    with open(os.path.join(src, "index.html"), "r", encoding="utf-8") as f:
        html = f.read()

    html = html.replace("__LOGO__", logo_b64)
    html = html.replace("/*@@CSS@@*/", css)
    html = html.replace("/*@@JS@@*/", full_js)

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(html)

    size_kb = os.path.getsize(out_file) / 1024
    print(f"Sucesso! Gerado {out_file} ({size_kb:.1f} KB)")

if __name__ == "__main__":
    main()
