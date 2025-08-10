from pathlib import Path
import sys
import threading
import time

from flaskwebgui import FlaskUI

from vitae.features.researchers.app import main

def close_splash(delay=5):
    def delayed_close():
        time.sleep(delay)
        try:
            import pyi_splash
            pyi_splash.close()
        except:
            pass

    threading.Thread(target=delayed_close, daemon=True).start()


def redirect_console_to_logfile(logfile: Path):
    log_file = logfile.open("+a", encoding="utf-8")
    sys.stdout = log_file
    sys.stderr = log_file

def start_app():
    FlaskUI(app=main(), server="fastapi").run()


if __name__ == "__main__":
    redirect_console_to_logfile(Path("vitae.log"))
    close_splash()
    start_app()
