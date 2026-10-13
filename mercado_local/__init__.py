"""Flask application factory for Mercado Local."""
from pathlib import Path

from flask import Flask, jsonify
from werkzeug.exceptions import RequestEntityTooLarge

from mercado_local.store.database import initialize
from mercado_local.routes.catalog import catalog_blueprint
from mercado_local.routes.orders import orders_blueprint
from mercado_local.routes.pages import pages_blueprint


def create_app(test_config=None):
    """Build an application instance with replaceable configuration for each environment."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=str(Path(app.instance_path) / "tienda.db"),
        MAX_CONTENT_LENGTH=16_384,
    )

    # Tests can provide a temporary DB path without touching the development database.
    if test_config:
        app.config.update(test_config)

    Path(app.config["DATABASE"]).parent.mkdir(parents=True, exist_ok=True)
    initialize(app.config["DATABASE"])

    app.register_blueprint(pages_blueprint)
    app.register_blueprint(catalog_blueprint)
    app.register_blueprint(orders_blueprint)

    @app.after_request
    def add_security_headers(response):
        """Send baseline browser protections with every Flask response."""
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; style-src 'self'; script-src 'self'; "
            "connect-src 'self'; img-src 'self' data:"
        )
        return response

    @app.errorhandler(RequestEntityTooLarge)
    def request_too_large(_error):
        """Return JSON for requests rejected by MAX_CONTENT_LENGTH."""
        return jsonify(error="La solicitud supera el tamaño permitido."), 413

    return app
