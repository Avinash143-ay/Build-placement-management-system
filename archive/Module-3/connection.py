# app/auth/routes.py
from flask import request, jsonify, current_app, Blueprint
import jwt
from datetime import datetime, timezone, timedelta
import hashlib
import mysql.connector
from database import get_cims_db_connection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def local_login():
    """Authenticates users against CIMS database and issues JWT tokens"""
    current_app.logger.debug("Processing login request")
    
    # Validate request data
    try:
        credentials = request.get_json()
        if not credentials or 'user' not in credentials or 'password' not in credentials:
            current_app.logger.warning("Incomplete login credentials received")
            return jsonify({"message": "Username and password required"}), 400
            
        user_id = credentials['user']
        password_attempt = credentials['password']
        
    except Exception as parse_error:
        current_app.logger.error(f"Request parsing failed: {str(parse_error)}")
        return jsonify({"message": "Invalid request format"}), 400

    db_connection = None
    try:
        # Establish database connection
        db_connection = get_cims_db_connection()
        if not db_connection:
            return jsonify({"message": "Database unavailable"}), 503
            
        with db_connection.cursor(dictionary=True) as db_cursor:
            # Retrieve user credentials
            db_cursor.execute(
                "SELECT Password, Role FROM Login WHERE MemberID = %s",
                (user_id,)
            )
            user_record = db_cursor.fetchone()
            
            if not user_record:
                current_app.logger.warning(f"Login attempt for unknown user: {user_id}")
                return jsonify({"message": "Authentication failed"}), 401
                
            # Verify password against stored hash
            stored_hash = user_record['Password']
            is_authenticated = False
            
            # BCrypt verification
            if stored_hash.startswith(('$2a$', '$2b$', '$2y$')):
                try:
                    import bcrypt
                    is_authenticated = bcrypt.checkpw(
                        password_attempt.encode(),
                        stored_hash.encode()
                    )
                except Exception as bcrypt_error:
                    current_app.logger.error(f"BCrypt error: {str(bcrypt_error)}")
            
            # MD5 fallback
            if not is_authenticated and len(stored_hash) == 32:
                try:
                    attempt_hash = hashlib.md5(password_attempt.encode()).hexdigest()
                    is_authenticated = (attempt_hash == stored_hash)
                except Exception as md5_error:
                    current_app.logger.error(f"MD5 error: {str(md5_error)}")
            
            # Plain text fallback (not recommended)
            if not is_authenticated:
                is_authenticated = (password_attempt == stored_hash)
                
            if not is_authenticated:
                current_app.logger.warning(f"Failed login attempt for user: {user_id}")
                return jsonify({"message": "Authentication failed"}), 401
                
            # Generate JWT token
            token_expiry = datetime.now(timezone.utc) + timedelta(hours=1)
            auth_token = jwt.encode(
                {
                    'sub': user_id,
                    'role': user_record['Role'],
                    'iat': datetime.now(timezone.utc),
                    'exp': token_expiry
                },
                current_app.config['SECRET_KEY'],
                algorithm="HS256"
            )
            
            current_app.logger.info(f"Successful login for user: {user_id}")
            return jsonify({
                "status": "success",
                "token": auth_token,
                "expires": token_expiry.isoformat()
            }), 200
            
    except mysql.connector.Error as db_error:
        current_app.logger.error(f"Database error during login: {str(db_error)}")
        return jsonify({"message": "Service unavailable"}), 503
    except Exception as unexpected_error:
        current_app.logger.error(f"Unexpected error: {str(unexpected_error)}")
        return jsonify({"message": "Internal server error"}), 500
    finally:
        if db_connection and db_connection.is_connected():
            db_connection.close()
