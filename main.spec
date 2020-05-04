# -*- mode: python -*-
from kivy.deps import sdl2, glew

block_cipher = None


a = Analysis(['path\\main.py'],
             pathex=['path\\build'],
             binaries=None,
             datas=None,
             hiddenimports=[
             'kivy.app',
             'kivy.uix.widget',
             'kivy.uix.label',
             'kivy.properties',
             'kivy.clock',
             'kivy.core.window',
             'kivy.uix.screenmanager',
             'kivy.uix.checkbox',
             'kivy.uix.textinput',
             'random',
             'logging',
             'select',
             'socket',
             'threading',
             'sys',
             'struct',
             ],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
             
from os.path import join
from fnmatch import fnmatch
exclusion_patterns = (
    join("kivy_install", "data", "images", "testpattern.png"),
    join("kivy_install", "data", "images", "image-loading.gif"),
    join("kivy_install", "data", "keyboards*"),
    join("kivy_install", "data", "settings_kivy.json"),
    join("kivy_install", "data", "logo*"),
    join("kivy_install", "data", "fonts", "DejaVuSans*"),
    join("kivy_install", "modules*"),
    join("Include*"),
    join("sdl2-config"),
    # Filter app directory
    join("personal*"),
    join("sign-apk*"),
    join(".idea*"),
)

def can_exclude(fn):
    for pat in exclusion_patterns:
        if fnmatch(fn, pat):
            return True

a.datas = [x for x in a.datas if not can_exclude(x[0])]
a.binaries = [x for x in a.binaries if not can_exclude(x[0])]
# Filter app directory
appfolder = [x for x in Tree('path\\', excludes=['*.py','*.pyc']) if not can_exclude(x[0])]  

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
             
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='your-exe-name',
          debug=False,
          strip=False,
          upx=True,
          console=True , icon='path\\data\\img\\program.ico')
          
coll = COLLECT(exe, appfolder,
               a.binaries,
               a.zipfiles,
               a.datas,
               Tree('path'),
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins )],
               strip=False,
               upx=True,
               name='your-exe-name')
