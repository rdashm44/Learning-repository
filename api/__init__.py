"""
Hunt Club Manager API
REST API for iOS app and third-party integrations
"""
from flask import Blueprint, jsonify

# Create main API blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/')
def api_info():
    """
    API information endpoint

    Response:
        {
            "name": "Hunt Club Manager API",
            "version": "1.0.0",
            "endpoints": {...}
        }
    """
    return jsonify({
        'name': 'Hunt Club Manager API',
        'version': '1.0.0',
        'description': 'REST API for Hunt Club Management',
        'endpoints': {
            'auth': {
                'POST /api/auth/login': 'Authenticate and get JWT token',
                'POST /api/auth/register': 'Register new user',
                'GET /api/auth/me': 'Get current user info',
                'GET /api/auth/verify': 'Verify token validity'
            },
            'stands': {
                'GET /api/stands': 'List all hunting stands',
                'GET /api/stands/<id>': 'Get stand details',
                'POST /api/stands/checkin': 'Check in to a stand',
                'POST /api/stands/checkout': 'Check out from stand',
                'GET /api/stands/my-checkin': 'Get your active check-in',
                'GET /api/stands/active': 'List all active check-ins'
            },
            'harvest': {
                'GET /api/harvest': 'List all harvest records',
                'GET /api/harvest/<id>': 'Get harvest details',
                'POST /api/harvest': 'Log a new harvest',
                'PUT /api/harvest/<id>': 'Update harvest record',
                'DELETE /api/harvest/<id>': 'Delete harvest record',
                'GET /api/harvest/my-harvests': 'Get your harvests',
                'GET /api/harvest/stats': 'Get harvest statistics'
            }
        },
        'authentication': 'Bearer token in Authorization header',
        'documentation': 'See README.md for detailed API documentation'
    }), 200

def register_api_blueprints(app):
    """
    Register all API blueprints with the Flask app

    Args:
        app: Flask application instance
    """
    from api.auth import auth_bp
    from api.stands import stands_bp
    from api.harvest import harvest_bp

    # Register individual API blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(stands_bp)
    app.register_blueprint(harvest_bp)

    # Register main API blueprint
    app.register_blueprint(api_bp)

    print("✅ API blueprints registered successfully")
