import PyInstaller.__main__

PyInstaller.__main__.run([
    "vitae/app.py",

    # Build Parameters
    "--noconfirm",
    "--clean",

    # Application Parameters
    "--windowed",
    "--splash", "splash.png",
    "--add-data", "vitae/features/researchers/templates;vitae/features/researchers/templates",
])