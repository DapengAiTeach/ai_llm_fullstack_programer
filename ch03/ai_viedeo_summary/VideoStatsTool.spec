# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = ['PyQt6.sip', 'PyQt6.QtCore', 'PyQt6.QtGui', 'PyQt6.QtWidgets', 'cv2', 'loguru', 'config', 'config.constants', 'config.loguru', 'entity', 'entity.video_info', 'services', 'services.video_service', 'ui', 'ui.main_window', 'utils', 'utils.format', 'utils.resource']
hiddenimports += collect_submodules('config')
hiddenimports += collect_submodules('entity')
hiddenimports += collect_submodules('services')
hiddenimports += collect_submodules('ui')
hiddenimports += collect_submodules('utils')


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('config', 'config'), ('entity', 'entity'), ('services', 'services'), ('ui', 'ui'), ('utils', 'utils')],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['pytest', 'unittest', 'tkinter', 'matplotlib', 'scipy', 'pandas'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='VideoStatsTool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='VideoStatsTool',
)
