# app/members/routes.py
from flask import request, jsonify, current_app, Blueprint
import mysql.connector
import hashlib
from database import get_cims_db_connection
from decorator import token_required

members_bp = Blueprint('members', __name__)

@members_bp.route('/admin/add_member', methods=['POST'])
@token_required
def add_member_task1(current_user_id, current_user_role):
    """Endpoint for admin to register new members with system credentials"""
    current_app.logger.debug(f"Admin member registration initiated by {current_user_id}")

    # Verify admin privileges
    if current_user_role != 'admin':
        current_app.logger.warning(f"Unauthorized access attempt by {current_user_id}")
        return jsonify({"status": "error", "message": "Administrator access required"}), 403

    # Validate request data
    try:
        member_data = request.get_json()
        if not member_data or 'name' not in member_data or 'email' not in member_data:
            current_app.logger.warning("Incomplete member registration data")
            return jsonify({"status": "error", "message": "Name and email are required"}), 400
            
        member_name = member_data['name']
        member_email = member_data['email']
        
    except Exception as parse_error:
        current_app.logger.error(f"Request parsing failed: {str(parse_error)}")
        return jsonify({"status": "error", "message": "Invalid request data"}), 400

    db_conn = None
    try:
        # Establish database connection
        db_conn = get_cims_db_connection()
        if not db_conn:
            return jsonify({"status": "error", "message": "Database connection failed"}), 500
            
        with db_conn.cursor() as cursor:
            # Register new member
            cursor.execute(
                "INSERT INTO members (UserName, emailID) VALUES (%s, %s)",
                (member_name, member_email)
            )
            new_member_id = cursor.lastrowid
            
            # Create login credentials
            password_hash = hashlib.md5(
                current_app.config['DEFAULT_PASSWORD'].encode()
            ).hexdigest()
            
            cursor.execute(
                "INSERT INTO Login (MemberID, Password, Role) VALUES (%s, %s, %s)",
                (new_member_id, password_hash, 'user')
            )
            
            db_conn.commit()
            
            current_app.logger.info(f"New member registered: ID {new_member_id}")
            return jsonify({
                "status": "success",
                "message": "Member registration complete",
                "member_id": new_member_id
            }), 201
            
    except mysql.connector.Error as db_error:
        db_conn.rollback()
        if db_error.errno == 1062:  # Duplicate entry
            return jsonify({
                "status": "error",
                "message": "Member already exists",
                "details": str(db_error)
            }), 409
        current_app.logger.error(f"Database error: {str(db_error)}")
        return jsonify({
            "status": "error", 
            "message": "Database operation failed"
        }), 500
    except Exception as unexpected_error:
        db_conn.rollback()
        current_app.logger.error(f"Unexpected error: {str(unexpected_error)}")
        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500
    finally:
        if db_conn and db_conn.is_connected():
            db_conn.close()
