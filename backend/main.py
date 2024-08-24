"""
Módulo principal
"""

from api.app import create_app
import api.router
from core.logs.logger import setup_logger
from core.services.database.database import DatabaseManager

logger = setup_logger(__name__)


def main():
    """Ponto de entrada"""
    logger.info("Iniciando aplicação")
    app = create_app()
    api.router.register_routes(app)
    app.run(host="0.0.0.0", port=8000, debug=True)


if __name__ == "__main__":
    create_app()
    DatabaseManager().migrate()
    main()
