"""Page routes for the web user interface."""
from flask import Blueprint, render_template

pages_blueprint = Blueprint("pages", __name__)


@pages_blueprint.get("/")
def home():
    """Render the storefront shell; JavaScript loads the live catalog from the API."""
    return render_template("index.html")
