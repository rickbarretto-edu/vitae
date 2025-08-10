import io
import sys

from flaskwebgui import FlaskUI

from vitae.features.researchers.app import main


def suppress_console():
    sys.stdout = io.StringIO()
    sys.stderr = io.StringIO()

def start_app():
    FlaskUI(app=main(), server="fastapi").run()


if __name__ == "__main__":
    # suppress_console()
    start_app()
