from flask import Blueprint, request, jsonify
from application.generators.cellular_automata import ProceduralGenerator

map_bp = Blueprint("map_bp", __name__)

@map_bp.route("/generate-map", methods=["POST"])
def generate_map():
    try:
        data = request.json or {}

        mapa = ProceduralGenerator.generar_mapa(data)

        return jsonify({
            "status": "success",
            "config": data,
            "map": mapa
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500