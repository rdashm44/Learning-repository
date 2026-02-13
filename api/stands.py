from flask import Blueprint, request, jsonify
from api.utils import token_required
from datetime import datetime

stands_bp = Blueprint('stands_api', __name__, url_prefix='/api/stands')

@stands_bp.route('', methods=['GET'])
@token_required
def get_stands(current_user):
    from app import HuntingStand
    stands = HuntingStand.query.all()
    return jsonify({
        'stands': [{
            'id': stand.id,
            'name': stand.name,
            'description': stand.description,
            'max_hunters': stand.max_hunters,
            'is_available': stand.is_available(),
            'active_hunters': len(stand.get_active_checkins())
        } for stand in stands]
    }), 200

@stands_bp.route('/<int:stand_id>', methods=['GET'])
@token_required
def get_stand(current_user, stand_id):
    from app import db, HuntingStand
    stand = db.session.get(HuntingStand, stand_id)
    if not stand:
        return jsonify({'error': 'Stand not found'}), 404
    active_checkins = stand.get_active_checkins()
    return jsonify({
        'stand': {
            'id': stand.id,
            'name': stand.name,
            'description': stand.description,
            'max_hunters': stand.max_hunters,
            'is_available': stand.is_available(),
            'active_checkins': [{
                'user_id': checkin.user_id,
                'username': checkin.hunter.username,
                'checkin_time': checkin.checkin_time.isoformat()
            } for checkin in active_checkins]
        }
    }), 200

@stands_bp.route('/checkin', methods=['POST'])
@token_required
def checkin(current_user):
    from app import db, HuntingStand, StandCheckIn
    data = request.get_json()
    if not data or not data.get('stand_id'):
        return jsonify({'error': 'stand_id required'}), 400
    existing_checkin = StandCheckIn.query.filter_by(
        user_id=current_user.id,
        checkout_time=None
    ).first()
    if existing_checkin:
        return jsonify({
            'error': 'Already checked in',
            'current_stand': existing_checkin.stand.name
        }), 400
    stand = db.session.get(HuntingStand, data['stand_id'])
    if not stand:
        return jsonify({'error': 'Stand not found'}), 404
    if not stand.is_available():
        return jsonify({'error': 'Stand is at capacity'}), 400
    checkin = StandCheckIn(
        user_id=current_user.id,
        stand_id=stand.id,
        checkin_time=datetime.utcnow()
    )
    db.session.add(checkin)
    db.session.commit()
    return jsonify({
        'message': 'Checked in successfully',
        'checkin': {
            'id': checkin.id,
            'stand_id': stand.id,
            'stand_name': stand.name,
            'checkin_time': checkin.checkin_time.isoformat()
        }
    }), 201

@stands_bp.route('/checkout', methods=['POST'])
@token_required
def checkout(current_user):
    from app import db, StandCheckIn
    checkin = StandCheckIn.query.filter_by(
        user_id=current_user.id,
        checkout_time=None
    ).first()
    if not checkin:
        return jsonify({'error': 'No active check-in found'}), 400
    checkin.checkout_time = datetime.utcnow()
    db.session.commit()
    duration = (checkin.checkout_time - checkin.checkin_time).total_seconds() / 3600
    return jsonify({
        'message': 'Checked out successfully',
        'checkin': {
            'id': checkin.id,
            'stand_name': checkin.stand.name,
            'checkin_time': checkin.checkin_time.isoformat(),
            'checkout_time': checkin.checkout_time.isoformat(),
            'duration_hours': round(duration, 2)
        }
    }), 200

@stands_bp.route('/my-checkin', methods=['GET'])
@token_required
def get_my_checkin(current_user):
    from app import StandCheckIn
    checkin = StandCheckIn.query.filter_by(
        user_id=current_user.id,
        checkout_time=None
    ).first()
    if not checkin:
        return jsonify({'checkin': None}), 200
    return jsonify({
        'checkin': {
            'id': checkin.id,
            'stand_id': checkin.stand_id,
            'stand_name': checkin.stand.name,
            'checkin_time': checkin.checkin_time.isoformat()
        }
    }), 200

@stands_bp.route('/active', methods=['GET'])
@token_required
def get_active_checkins(current_user):
    from app import StandCheckIn
    active_checkins = StandCheckIn.query.filter_by(checkout_time=None).all()
    return jsonify({
        'active_checkins': [{
            'user_id': checkin.user_id,
            'username': checkin.hunter.username,
            'stand_id': checkin.stand_id,
            'stand_name': checkin.stand.name,
            'checkin_time': checkin.checkin_time.isoformat()
        } for checkin in active_checkins]
    }), 200
