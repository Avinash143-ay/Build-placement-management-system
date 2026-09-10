# app/_init_.py
import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask, jsonify, render_template

# Import configuration object
from confi import Config

def create_app(config_class=Config):
    """Application Factory Function"""
    app = Flask(__name__, instance_relative_config=True)

    # Load configuration from config.py
    app.config.from_object(config_class)

    # Optional: Load instance config if it exists (e.g., for secrets)
    # app.config.from_pyfile('config.py', silent=True) # Looks in instance/config.py

    # Configure Logging
    # Ensure logs directory exists (handled in config.py now, but good practice)
    log_dir = os.path.dirname(app.config['LOGGING_FILENAME'])
    os.makedirs(log_dir, exist_ok=True)

    # Use RotatingFileHandler for better log management
    file_handler = RotatingFileHandler(
        app.config['LOGGING_FILENAME'],
        maxBytes=10240,  # Max 10KB per file
        backupCount=10   # Keep 10 backup files
    )
    file_handler.setFormatter(logging.Formatter(app.config['LOGGING_FORMAT']))
    file_handler.setLevel(app.config['LOGGING_LEVEL'])

    # Add handler to Flask's logger
    app.logger.addHandler(file_handler)
    app.logger.setLevel(app.config['LOGGING_LEVEL'])

    # Also configure root logger if needed (for libraries logging)
    logging.basicConfig(level=app.config['LOGGING_LEVEL'], format=app.config['LOGGING_FORMAT'])


    app.logger.info('CS432 API Startup') # Log app start

    # Register Blueprints
    from connection import auth_bp
    try:
        from task import members_bp
    except ImportError:
        from task1 import members_bp
    from routes import teams_bp
    # from .events.routes import events_bp 
    # from .matches.routes import matches_bp 
    # from .venues.routes import venues_bp 
    # from .equipment.routes import equipment_bp 

    app.register_blueprint(auth_bp) # No URL prefix, routes like /login
    app.register_blueprint(members_bp) # No URL prefix, routes like /profile/me, /admin/add_member
    app.register_blueprint(teams_bp, url_prefix='/teams')  # Register with a URL prefix
    # app.register_blueprint(events_bp, url_prefix='/events') # Register new
    # app.register_blueprint(matches_bp, url_prefix='/matches') # Register new
    # app.register_blueprint(venues_bp, url_prefix='/venues') # Register new
    # app.register_blueprint(equipment_bp, url_prefix='/equipment') # Register new

    portal_overview = {
        "title": "Placement Management Portal",
        "subtitle": "A demo-ready college placement system for students, recruiters, and admins.",
        "highlights": [
            "Student registration and job applications",
            "Company job posting and shortlist tracking",
            "Admin oversight, interviews, and placement statistics",
            "JWT-secured APIs with role-based access control",
        ],
    }

    @app.route('/')
    def index():
         return render_template(
             'portal.html',
             portal=portal_overview,
             active_section='home',
         )

    @app.route('/portal')
    def portal_home():
         return render_template(
             'portal.html',
             portal=portal_overview,
             active_section='home',
         )

    @app.route('/portal/student')
    def portal_student():
         return render_template(
             'portal.html',
             portal={
                 **portal_overview,
                 'title': 'Student Portal',
                 'subtitle': 'View openings, apply for jobs, and track interview status.',
             },
             active_section='student',
         )

    @app.route('/portal/company')
    def portal_company():
         return render_template(
             'portal.html',
             portal={
                 **portal_overview,
                 'title': 'Company Portal',
                 'subtitle': 'Post openings, review applications, and manage hiring workflows.',
             },
             active_section='company',
         )

    @app.route('/portal/admin')
    def portal_admin():
         return render_template(
             'portal.html',
             portal={
                 **portal_overview,
                 'title': 'Admin Portal',
                 'subtitle': 'Monitor placement progress, manage records, and oversee the system.',
             },
             active_section='admin',
         )

    @app.route('/api')
    def api_home():
         return jsonify({"message": "Welcome to the CS432 Group 7 API"})

    return app