import sys, os
from pathlib import Path

if (dir := str(Path(os.getcwd()).parent)) not in sys.path:
    sys.path.append(dir)

from app import app
from src.core.settings import settings
from src.routes import render_page_content
from src.layout.sidebar.sidebar_callbacks import toggle_collapse, toggle_classname


if __name__ == "__main__":
    app.run_server(
        host=settings.host,
        port=settings.port,
        debug=settings.debug,
    )
