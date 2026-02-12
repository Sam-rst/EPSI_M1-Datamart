#!/usr/bin/env python3
"""
Exporte le schéma architecture en image PNG.
Dimensions autour + Stats centrales
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MERMAID_FILE = PROJECT_ROOT / "docs" / "schema_final.mmd"
OUTPUT_PNG = PROJECT_ROOT / "docs" / "schema_final.png"

def export_with_playwright():
    """Exporte le diagramme avec Playwright."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("❌ Playwright n'est pas installé.")
        return False
    
    print("🔧 Export du schéma architecture avec Playwright...")
    
    with open(MERMAID_FILE, "r", encoding="utf-8") as f:
        mermaid_code = f.read()
    
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
    </script>
    <style>
        body {{ 
            margin: 20px; 
            background: white; 
            font-family: 'Arial', sans-serif;
        }}
    </style>
</head>
<body>
    <div class="mermaid">
{mermaid_code}
    </div>
</body>
</html>
"""
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 2400, 'height': 2000})
        page.set_content(html_content)
        page.wait_for_timeout(3000)
        
        page.screenshot(path=str(OUTPUT_PNG), full_page=True)
        print(f"✅ PNG exporté: {OUTPUT_PNG}")
        
        browser.close()
    
    return True

def main():
    print("🚀 Export du schéma ARCHITECTURE\n")
    
    if not MERMAID_FILE.exists():
        print(f"❌ Fichier Mermaid introuvable: {MERMAID_FILE}")
        return 1
    
    print(f"📄 Fichier source: {MERMAID_FILE}\n")
    
    if export_with_playwright():
        print("\n✅ Export réussi!")
        print(f"📁 Fichier: {OUTPUT_PNG}")
        return 0
    else:
        print("❌ Échec de l'export")
        return 1

if __name__ == "__main__":
    sys.exit(main())
