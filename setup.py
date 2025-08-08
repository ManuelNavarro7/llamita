#!/usr/bin/env python3
"""
Setup script for packaging Llamita as a macOS app
"""

from setuptools import setup

APP = ['src/voice_assistant.py']
DATA_FILES = [
    ('src', ['src/config.py']),
    ('assets/icons', ['assets/icons/llamita_icon.png']),
    ('assets/icons', ['assets/icons/llamita_icon.icns']),
]

OPTIONS = {
    'argv_emulation': False,
    'iconfile': './assets/icons/llamita_icon.png',
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
        'LSApplicationCategoryType': 'public.app-category.productivity',
        'NSPrincipalClass': 'NSApplication',
    },
    'packages': ['tkinter', 'requests', 'PIL', 'PIL._tkinter_finder'],
    'includes': ['config', 'document_processor', 'google_docs_processor'],
    'excludes': ['PyAudio', 'speech_recognition'],
    'optimize': 1,  # Reduced optimization for better compatibility
    'semi_standalone': False,
    'site_packages': True,
}

setup(
    name='Llamita',
    version='1.0.0',
    description='Intelligent AI Assistant',
    author='Llamita Team',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
