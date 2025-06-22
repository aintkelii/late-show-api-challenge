from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from server.app import db
from server.models.appearance import Appearance
from server.models.guest import Guest
from server.models.episode import Episode

appearance_bp = Blueprint('appearances', __name__)

@appearance_bp.route('/appearances', methods=['POST'])
@jwt_required()
def create_appearance():
    data = request.get_json()
    if not data or not all(k in data for k in ['rating', 'guest_id', 'episode_id']):
        return jsonify({"message": "Missing required fields"}), 400

    if not (1 <= data['rating'] <= 5):
        return jsonify({"message": "Rating must be between 1 and 5"}), 400

    if not Guest.query.get(data['guest_id']):
        return jsonify({"message": "Guest not found"}), 404
    if not Episode.query.get(data['episode_id']):
        return jsonify({"message": "Episode not found"}), 404

    appearance = Appearance(
        rating=data['rating'],
        guest_id=data['guest_id'],
        episode_id=data['episode_id']
    )
    db.session.add(appearance)
    db.session.commit()
    return jsonify({"message": "Appearance created successfully"}), 201