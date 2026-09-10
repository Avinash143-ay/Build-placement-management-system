# app/members/routes.py
from flask import request, jsonify, current_app, Blueprint
import mysql.connector
from database import get_cims_db_connection
from decorator import token_required

members_bp = Blueprint('members', __name__)

@members_bp.route('/profile/me', methods=['GET'])
@token_required
def get_my_profile(current_user_id, current_user_role):
    """Endpoint for authenticated users to access their own profile data"""
    current_app.logger.debug(f"Profile request from user {current_user_id}")
    
    try:
        with get_cims_db_connection() as conn:
            if not conn:
                return jsonify({"status": "error", "message": "Database unavailable"}), 500
                
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(
                    "SELECT ID, UserName, emailID, DoB FROM members WHERE ID = %s", 
                    (current_user_id,)
                )
                user_profile = cursor.fetchone()
                
                if not user_profile:
                    return jsonify({
                        "status": "error",
                        "message": "Profile not found"
                    }), 404
                    
                return jsonify(user_profile), 200
                
    except mysql.connector.Error as db_error:
        current_app.logger.error(f"Database error: {str(db_error)}")
        return jsonify({
            "status": "error",
            "message": "Database operation failed"
        }), 500
    except Exception as e:
        current_app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500

@members_bp.route('/admin/profile/<int:target_member_id>', methods=['GET'])
@token_required
def get_any_profile(current_user_id, current_user_role, target_member_id):
    """Admin-only endpoint to retrieve any member's profile"""
    if current_user_role != 'admin':
        return jsonify({
            "status": "error",
            "message": "Administrator access required"
        }), 403

    try:
        with get_cims_db_connection() as conn:
            if not conn:
                return jsonify({
                    "status": "error", 
                    "message": "Database unavailable"
                }), 500
                
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(
                    "SELECT ID, UserName, emailID, DoB FROM members WHERE ID = %s",
                    (target_member_id,)
                )
                member_data = cursor.fetchone()
                
                if not member_data:
                    return jsonify({
                        "status": "error",
                        "message": "Member not found"
                    }), 404
                    
                return jsonify(member_data), 200
                
    except mysql.connector.Error as db_error:
        current_app.logger.error(f"Database error: {str(db_error)}")
        return jsonify({
            "status": "error",
            "message": "Database operation failed"
        }), 500
    except Exception as e:
        current_app.logger.error(f"Unexpected error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Internal server error"
            }),500
