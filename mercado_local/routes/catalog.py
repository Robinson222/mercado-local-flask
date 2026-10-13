"""JSON endpoints for the product catalog and service status."""
from flask import Blueprint, current_app, jsonify

from mercado_local.store.database import list_products

catalog_blueprint = Blueprint("catalog", __name__, url_prefix="/api")


@catalog_blueprint.get("/products")
def products():
    """Return catalog products as JSON for the browser client."""
    return jsonify(list_products(current_app.config["DATABASE"]))


@catalog_blueprint.get("/health")
def health():
    """Expose a small health endpoint for local smoke checks and monitoring."""
    return jsonify(status="ok")
