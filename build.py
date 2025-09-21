import os
import sys
import shutil

import PyInstaller.__main__


def _add_data_arg(src: str, dest: str) -> str:
    """Return a platform-correct --add-data argument for PyInstaller.

    PyInstaller expects the SOURCE and DEST to be separated by the OS path
    separator (os.pathsep). The CLI also accepts the --add-data=SRC:DEST
    style when passed as a single argv element, so we build that string here.
    """
    sep = os.pathsep
    return f"--add-data={src}{sep}{dest}"


PyInstaller.__main__.run([
    "vitae/app.py",

    # Build Parameters
    "--noconfirm",
    "--clean",

    # Application Parameters
    "--windowed",

    # Right now, macOS does not support pyi_splash / --splash
    *([] if sys.platform.startswith('darwin') else ["--splash", "splash.png"]),
    _add_data_arg("vitae/features/researchers/templates", "vitae/features/researchers/templates"),
])


# Move Files (assume PyInstaller produced dist/app)
if os.path.isdir("dist/app"):
    shutil.copy("README.md", "dist/app/")
    shutil.copy("GUIDE.md", "dist/app/")
    shutil.copy("GUIA.md", "dist/app/")
    shutil.copy("CONTRIBUTING.md", "dist/app/")
    shutil.copy("LICENSE", "dist/app/")
    shutil.copy("vitae.example.toml", "dist/app/vitae.toml")

    # Rename Files (only if they exist)
    exe_src = "dist/app/app.exe"
    exe_dst = "dist/app/vitae.exe"
    if os.path.isfile(exe_src):
        shutil.move(exe_src, exe_dst)

    # Move the final app folder to dist/vitae
    if os.path.isdir("dist/app"):
        # if destination exists, remove it first
        if os.path.exists("dist/vitae"):
            shutil.rmtree("dist/vitae")
        shutil.move("dist/app", "dist/vitae")
else:
    print("Warning: expected dist/app directory not found after PyInstaller run")