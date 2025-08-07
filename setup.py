#!/usr/bin/env python3
"""
Setup script for packaging Llamita as a macOS app
"""

from setuptools import setup

APP = ['voice_assistant.py']
DATA_FILES = [
    ('', ['config.py']),
    ('', ['requirements.txt']),
    ('', ['run_voice_assistant.sh']),
    ('', ['setup_complete.sh']),
    ('', ['SETUP_INSTRUCTIONS.md']),
    ('', ['PORTABLE_SETUP.md']),
    ('', ['llamita_icon.icns']),
    ('', ['llamita_icon.png'])
]

OPTIONS = {
    'argv_emulation': False,  # Disable argv emulation to prevent directory issues
    'iconfile': 'llamita_icon.icns',  # We'll create this
    'plist': {
        'CFBundleName': 'Llamita',
        'CFBundleDisplayName': '🦙 Llamita',
        'CFBundleGetInfoString': 'Llamita - Intelligent AI Assistant',
        'CFBundleIdentifier': 'com.llamita.assistant',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSHumanReadableCopyright': '© 2024 Llamita',
        'NSHighResolutionCapable': True,
        'LSMinimumSystemVersion': '10.13.0',
        'NSRequiresAquaSystemAppearance': False,
        'NSAppleScriptEnabled': False,
        'LSBackgroundOnly': False,
    },
    'packages': ['tkinter', 'requests', 'datetime'],
    'includes': ['config'],
    'excludes': ['PyAudio', 'speech_recognition'],  # Exclude voice features
    'optimize': 2,
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
