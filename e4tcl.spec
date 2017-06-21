# -*- mode: python -*-

block_cipher = None


a = Analysis(['e4tcl.py'],
             pathex=['C:\\Users\\MilhausDesk\\PycharmProjects\\e4tcl'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='e4tcl',
          debug=False,
          strip=False,
          upx=False,
          console=False,
          icon=".\\icons\\e4tcl.ico")

