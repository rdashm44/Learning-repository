from flask import Blueprint, request, jsonify
from api.utils import token_required
from datetime import datetime

harvest_bp = Blueprint('harvest_api', __name__, url_prefix='/api/harvest')

@harvest_bp.route('', methods=['GET'])
@token_required
def get_harvests(current_user):
    from app import Harvest
    user_id = request.args.get('user_id', type=int)
    if user_id:
        harvests = Harvest.query.filter_by(user_id=user_id).order_by(Harvest.harvest_date.desc()).all()
    else:
        harvests = Harvest.query.order_by(Harvest.harvest_date.desc()).all()
    return jsonify({
        'harvests': [{
            'id': h.id,
            'user_id': h.user_id,
            'username': h.hunter.username,
            'species': h.species,
            'weight': h.weight,
            'notes': h.notes,
            'harvest_date': h.harvest_date.isoformat()
        } for h in harvests]
    }), 200

@harvest_bp.route('/<int:harvest_id>', methods=['GET'])
@token_required
def get_harvest(current_user, harvest_id):
    from app import db, Harvest
    harvest = db.session.get(Harvest, harvest_id)
    if not harvest:
        return jsonify({'error': 'Harvest record not found'}), 404
    return jsonify({
        'harvest': {
            'id': harvest.id,
            'user_id': harvest.user_id,
            'username': harvest.hunter.username,
            'species': harvest.species,
            'weight': harvest.weight,
            'notes': harvest.notes,
            'harvest_date': harvest.harvest_date.isoformat()
        }
    }), 200

@harvest_bp.route('', methods=['POST'])
@token_required
def log_harvest(current_user):
    from app import db, Harvest
    data = request.get_json()
    if not data or not data.get('species'):
        return jsonify({'error': 'species is required'}), 400
    harvest = Harvest(
        user_id=current_user.id,
        species=data['species'],
        weight=data.get('weight'),
        notes=data.get('notes'),
        harvest_date=datetime.utcnow()
    )
    db.session.add(harvest)
    db.session.commit()
    return jsonify({
        'message': 'Harvest logged successfully',
        'harvest': {
            'id': harvest.id,
            'species': harvest.species,
            'weight': harvest.weight,
            'notes': harvest.notes,
            'harvest_date': harvest.harvest_date.isoformat()
        }
    }), 201

@harvest_bp.route('/<int:harvest_id>', methods=['PUT'])
@token_required
def update_harvest(current_user, harvest_id):
    from app import db, Harvest
    harvest = db.session.get(Harvest, harvest_id)
    if not harvest:
        return jsonify({'error': 'Harvest record not found'}), 404
    if harvest.user_id != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    data = request.get_json()
    if 'species' in data:
        harvest.species = data['species']
    if 'weight' in data:
        harvest.weight = data['weight']
    if 'notes' in data:
        harvest.notes = data['notes']
    db.session.commit()
    return jsonify({
        'message': 'Harvest updated successfully',
        'harvest': {
            'id': harvest.id,
            'species': harvest.species,
            'weight': harvest.weight,
            'notes': harvest.notes,
            'harvest_date': harvest.harvest_date.isoformat()
        }
    }), 200

@harvest_bp.route('/<int:harvest_id>', methods=['DELETE'])
@token_required
def delete_harvest(current_user, harvest_id):
    from app import db, Harvest
    harvest = db.session.get(Harvest, harvest_id)
    if not harvest:
        return jsonify({'error': 'Harvest record not found'}), 404
    if harvest.user_id != current_user.id and not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    db.session.delete(harvest)
    db.session.commit()
    return jsonify({
        'message': 'Harvest deleted successfully'
    }), 200

@harvest_bp.route('/my-harvests', methods=['GET'])
@token_required
def get_my_harvests(current_user):
    from app import Harvest
    harvests = Harvest.query.filter_by(user_id=current_user.id).order_by(Harvest.harvest_date.desc()).all()
    return jsonify({
        'harvests': [{
            'id': h.id,
            'species': h.species,
            'weight': h.weight,
            'notes': h.notes,
            'harvest_date': h.harvest_date.isoformat()
        } for h in harvests]
    }), 200

@harvest_bp.route('/stats', methods=['GET'])
@token_required
def get_harvest_stats(current_user):
    from app import Harvest
    all_harvests = Harvest.query.all()
    by_species = {}
    total_weight = 0
    for h in all_harvests:
        by_species[h.species] = by_species.get(h.species, 0) + 1
        if h.weight:
            total_weight += h.weight
    return jsonify({
        'total_harvests': len(all_harvests),
        'by_species': by_species,
        'total_weight': round(total_weight, 2)
    }), 200
