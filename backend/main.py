"""
Módulo principal
"""

from backend.api.app import app


def main():
    """Ponto de entrada"""
    app.run(host="0.0.0.0", port=8000, debug=True)


if __name__ == "__main__":
    main()
