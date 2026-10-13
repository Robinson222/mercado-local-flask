"""Order endpoint with payload, size, and same-origin checks."""
from flask import Blueprint, current_app, jsonify, request
from werkzeug.exceptions import BadRequest

from mercado_local.store.database import create_order

orders_blueprint = Blueprint("orders", __name__, url_prefix="/api")


@orders_blueprint.post("/orders")
def create_order_route():
    """Validate a JSON order and persist it through the existing data layer."""
    origin = request.headers.get("Origin")
    expected_origins = (f"http://{request.host}", f"https://{request.host}")
    if origin and origin not in expected_origins:
        return jsonify(error="Origen no permitido."), 403

    if not request.is_json:
        return jsonify(error="El contenido debe ser JSON."), 415

    try:
        payload = request.get_json()
    except BadRequest:
        return jsonify(error="El JSON enviado no es valido."), 400

    if not isinstance(payload, dict):
        return jsonify(error="La solicitud debe ser un objeto JSON."), 400

    try:
        result = create_order(
            current_app.config["DATABASE"],
            payload.get("customer"),
            payload.get("email"),
            payload.get("items"),
        )
    except ValueError as error:
        return jsonify(error=str(error)), 400

    return jsonify(result), 201
