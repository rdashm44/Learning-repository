"""
Helper to access models from blueprints
"""
from flask import current_app

def get_models():
    """Get db and models from the app context"""
    # Import here to avoid circular imports
    import app as app_module
    return (
        app_module.db,
        app_module.User,
        app_module.HuntingStand,
        app_module.StandCheckIn,
        app_module.Harvest
    )
