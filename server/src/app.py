from flask import Flask

from routes.refactor_routes import refactor_bp
from utils.config import Route


def create_app():
    app = Flask(__name__)

    app.register_blueprint(refactor_bp)

    @app.route("/health", methods=["GET"])
    def health_check():
        return {"status": "ok"}, 200

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host=Route.HOST, port=Route.PORT)
