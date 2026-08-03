# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all, collect_dynamic_libs

datas, binaries, hiddenimports = collect_all("silero_vad")
binaries += collect_dynamic_libs("mlx")
binaries += [(".venv/lib/python3.12/site-packages/mlx/lib/libjaccl.dylib", "mlx")]

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    exclude_binaries=True,
    name='Jarvis',
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    name='Jarvis',
)

app = BUNDLE(
    coll,
    name='Jarvis.app',
)
