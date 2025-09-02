from flask import Blueprint, jsonify, request

from services.script_refactor import run_refactor


refactor_bp = Blueprint("refactor", __name__)


@refactor_bp.route("/refactor", methods=["POST"])
def refactor():
    data = request.get_json()
    folder_map = data.get("folder_map", {})
    dry_run = data.get("dry_run", True)

    try:
        result = run_refactor(folder_map, dry_run)
        return jsonify({"status": "success", "log": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
