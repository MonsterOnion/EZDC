# -*- mode: python ; coding: utf-8 -*-
import glob
import os

# Get all language files under /assets/languages/ and /assets/themes/
languages_files = glob.glob(os.path.join('assets', 'languages', '**', '*'), recursive=True)
themes_files = glob.glob(os.path.join('assets', 'themes', '**', '*'), recursive=True)

# Get specific config files (excluding settings.json)
config_files = [
    # Include preset files with their directory structure
    ('config/preset/download/preset.json', 'config/preset/download'),
    ('config/preset/conversion/preset.json', 'config/preset/conversion'),
    # Include languages.json and themes.json files
    ('config/languages.json', 'config'),
    ('config/themes.json', 'config'),
]

# Now include them in the datas list
a = Analysis(
    ['main.py'],  # Your main entry point
    pathex=[],
    binaries=[  # Include ffmpeg.exe and ffprobe.exe in the root directory
        ('ffmpeg.exe', '.'),
        ('ffprobe.exe', '.')
    ],
    datas=[  # Use glob to gather all files and include them
        # Include all language and theme files while keeping the folder structure
        *( (f, 'assets/languages') for f in languages_files),
        *( (f, 'assets/themes') for f in themes_files),
        # Include only the specific config files, keeping their folder structure
        *( (src, dst) for src, dst in config_files),
    ],
    hiddenimports=[
        'yt-dlp',
        'yt_dlp.extractor.common',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

# Create the PYZ (compiled Python code)
pyz = PYZ(a.pure)

# Build the executable
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ezdc',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Set to True if you want a console window
    disable_windowed_traceback=True,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# Collect everything (binaries and assets) into the final executable
coll = COLLECT(
    exe,
    a.binaries,  # Include binaries like ffmpeg.exe and ffprobe.exe
    a.datas,     # Include all asset and config files, preserving their structure
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ezdc',
)
