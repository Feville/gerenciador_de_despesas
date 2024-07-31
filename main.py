"""
Módulo principal
"""

from backend.api.app import app
from backend.core.logs.logger import setup_logger

logger = setup_logger(__name__)


def main():
    """Ponto de entrada"""
    logger.info("Iniciando aplicação")
    app.run(host="0.0.0.0", port=8000, debug=True)


if __name__ == "__main__":
    main()
