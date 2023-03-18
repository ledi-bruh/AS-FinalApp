import sys, os
from pathlib import Path

if (dir := str(Path(os.getcwd()).parent)) not in sys.path:
    sys.path.append(dir)

from app import app
from routes import render_page_content
from layout.sidebar.sidebar_callbacks import toggle_collapse, toggle_classname

from src.core.settings import settings


if __name__ == "__main__":
    app.run_server(
        host=settings.host,
        port=settings.port,
        debug=settings.debug,
    )
