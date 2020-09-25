# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['four_in_a_row.py'],
             pathex=['/Users/omerhagage/Desktop/מדמ״ח/year1/סמסטר-א/מבוא למדעי המחשב 67101/ex12'],
             binaries=[('/System/Library/Frameworks/Tk.framework/Tk', 'tk'), ('/System/Library/Frameworks/Tcl.framework/Tcl', 'tcl')],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='four_in_a_row',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )
app = BUNDLE(exe,
             name='four_in_a_row.app',
             icon=None,
             bundle_identifier=None)
