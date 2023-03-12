import sys, os
from pathlib import Path

if (dir := str(Path(os.getcwd()).parent)) not in sys.path:
    sys.path.append(dir)

from src.app import app
from src.core.settings import settings


if __name__ == '__main__':
    app.run_server(
        host=settings.host,
        port=settings.port,
        debug=True,
    )
