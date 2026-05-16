#!/usr/bin/env python3
"""Verificar se todos os imports estão funcionando corretamente"""

import sys

print("🔍 Verificando imports...\n")

tests = [
    ("flet", "UI Framework"),
    ("yt_dlp", "YouTube Downloader"),
    ("threading", "Threading"),
    ("time", "Time"),
    ("os", "OS"),
]

failed = []

for module, description in tests:
    try:
        __import__(module)
        print(f"✅ {module:15} - {description}")
    except ImportError as e:
        print(f"❌ {module:15} - {description}")
        failed.append((module, str(e)))

print("\n" + "="*50)

if failed:
    print(f"❌ {len(failed)} dependência(s) faltando:")
    for mod, err in failed:
        print(f"   - {mod}: {err}")
    print("\n📦 Instale com: pip install -r requirements.txt")
    sys.exit(1)
else:
    print("✅ Todas as dependências estão OK!")
    print("\n🚀 Você pode executar: python src/main.py")
    sys.exit(0)
