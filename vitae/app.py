
from flaskwebgui import FlaskUI

from vitae.features.researchers.app import main

if __name__ == "__main__":
    FlaskUI(app=main(), server="fastapi").run()