#!/usr/bin/env python3
import sys
import py_compile

files_to_check = [
    'src/modules/downloader/engine.py',
    'src/ui/views/downloader_view.py'
]

errors = []
for file in files_to_check:
    try:
        py_compile.compile(file, doraise=True)
        print(f"✅ {file} - OK")
    except py_compile.PyCompileError as e:
        print(f"❌ {file} - ERRO")
        errors.append(str(e))

if errors:
    print("\n=== ERROS ENCONTRADOS ===")
    for error in errors:
        print(error)
    sys.exit(1)
else:
    print("\n✅ Todos os arquivos estão OK!")
    sys.exit(0)
