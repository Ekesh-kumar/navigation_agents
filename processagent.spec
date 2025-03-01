# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['processagent.py'],
    pathex=[],
    binaries=[],
    datas=[('D:\\ThoughtfocusR&D\\Navigator_agent\\Automate_agents\\.', 'Automate_agents')],
    hiddenimports=['numpy', 'pydantic', 'pydantic.deprecated.decorator', 'langchain', 'dotenv', 'json', 'sys'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='processagent',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
