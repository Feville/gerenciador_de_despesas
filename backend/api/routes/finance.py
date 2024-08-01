"""
Rotas de finanças do usuário
"""

from flask import Blueprint
from core.logs.logger import setup_logger
from core.services.controllers.finance import FinanceController
from core.services.database.access import (
    AccessDB,
)

logger = setup_logger(__name__)
access_blueprint = Blueprint("access", __name__)


dao = AccessDB()
finance_controller = FinanceController(dao)
