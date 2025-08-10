import shutil

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

# Move Files
shutil.copy("README.md", "dist/app/")
shutil.copy("GUIDE.md", "dist/app/")
shutil.copy("GUIA.md", "dist/app/")
shutil.copy("CONTRIBUTING.md", "dist/app/")
shutil.copy("vitae.example.toml", "dist/app/vitae.toml")

# Rename Files
shutil.move("dist/app/app.exe", "dist/app/vitae.exe")
shutil.move("dist/app", "dist/vitae")