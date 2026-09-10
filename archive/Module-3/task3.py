# app/members/routes.py
from flask import request, jsonify, current_app, Blueprint
import mysql.connector
from database import get_cims_db_connection
from decorator import token_required

members_bp = Blueprint('members', __name__)

@members_bp.route('/admin/delete_member/<int:member_id_to_delete>', methods=['DELETE'])
@token_required
def delete_member_task3(current_user_id, current_user_role, member_id_to_delete):
    """
    Handles conditional deletion of members based on group associations
    - Full deletion if member has no group mappings
    - Only removes group mapping if member belongs to other groups
    Requires admin privileges
    """
    
    # Log the deletion attempt
    current_app.logger.info(
        f"Delete member request initiated by {current_user_id} "
        f"for member {member_id_to_delete}"
    )

    # 1. Verify admin privileges
    if current_user_role != 'admin':
        current_app.logger.warning(
            f"Unauthorized deletion attempt by user {current_user_id}"
        )
        return jsonify({
            "status": "error",
            "message": "Administrator privileges required"
        }), 403

    db_connection = None
    try:
        # 2. Establish database connection
        db_connection = get_cims_db_connection()
        if not db_connection:
            return jsonify({
                "status": "error",
                "message": "Database connection failed"
            }), 500

        with db_connection.cursor(dictionary=True) as cursor:
            # 3. Verify member exists
            cursor.execute(
                "SELECT ID FROM members WHERE ID = %s",
                (member_id_to_delete,)
            )
            if not cursor.fetchone():
                return jsonify({
                    "status": "error",
                    "message": f"Member {member_id_to_delete} not found"
                }), 404

            # 4. Check group associations
            cursor.execute(
                "SELECT COUNT(*) AS group_count FROM MemberGroupMapping "
                "WHERE MemberID = %s",
                (member_id_to_delete,)
            )
            group_count = cursor.fetchone()['group_count']

            # Prepare response data
            response_data = {
                "deleted_from_login": 0,
                "deleted_from_members": 0,
                "deleted_from_mapping": 0,
                "message": ""
            }

            # 5. Conditional deletion logic
            if group_count == 0:
                # Full deletion - no group associations
                cursor.execute(
                    "DELETE FROM Login WHERE MemberID = %s",
                    (member_id_to_delete,)
                )
                response_data["deleted_from_login"] = cursor.rowcount

                cursor.execute(
                    "DELETE FROM members WHERE ID = %s",
                    (member_id_to_delete,)
                )
                response_data["deleted_from_members"] = cursor.rowcount

                response_data["message"] = (
                    f"Member {member_id_to_delete} and their login "
                    "credentials were successfully deleted"
                )
            else:
                # Partial deletion - remove only our group association
                group_id = current_app.config.get('GROUP_ID', 'cs432g7')
                cursor.execute(
                    "DELETE FROM MemberGroupMapping "
                    "WHERE MemberID = %s AND GroupID = %s",
                    (member_id_to_delete, group_id)
                )
                response_data["deleted_from_mapping"] = cursor.rowcount

                response_data["message"] = (
                    f"Removed member {member_id_to_delete} from group {group_id}"
                    if response_data["deleted_from_mapping"] > 0
                    else f"No existing mapping for group {group_id}"
                )

            # Commit transaction
            db_connection.commit()
            current_app.logger.info(
                f"Successfully processed deletion for member {member_id_to_delete}"
            )
            return jsonify(response_data), 200

    except mysql.connector.Error as db_error:
        # Handle database errors
        if db_connection:
            db_connection.rollback()
        current_app.logger.error(
            f"Database error during member deletion: {str(db_error)}"
        )
        return jsonify({
            "status": "error",
            "message": "Database operation failed",
            "details": str(db_error)
        }), 500

    except Exception as unexpected_error:
        # Handle unexpected errors
        if db_connection:
            db_connection.rollback()
        current_app.logger.error(
            f"Unexpected error during member deletion: {str(unexpected_error)}"
        )
        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500

    finally:
        # Ensure connection is closed
        if db_connection and db_connection.is_connected():
            db_connection.close()
