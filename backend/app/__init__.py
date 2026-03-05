import logging

from flask import Flask
from flask_cors import CORS

from app.config.settings import Config
from app.extensions import bcrypt, db, jwt, limiter, migrate
from app.routes.admin_routes import bp as admin_bp
from app.routes.auth_routes import bp as auth_bp
from app.routes.order_routes import bp as order_bp
from app.routes.product_routes import bp as product_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    limiter.init_app(app)
    CORS(app, origins=app.config["CORS_ORIGINS"], supports_credentials=True)

    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(admin_bp)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.errorhandler(Exception)
    def handle_exception(error):
        app.logger.exception("Unhandled error: %s", error)
        return {"message": "Internal server error"}, 500

    return app
