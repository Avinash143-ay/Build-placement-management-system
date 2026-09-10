# app/auth/decorators.py
import jwt
from functools import wraps
from flask import request, jsonify, current_app

def token_required(f):
    """Authentication decorator that verifies JWT tokens from request headers"""
    @wraps(f)
    def decorated(*args, **kwargs):
        # Extract token from Authorization header
        auth_token = None
        authorization_header = request.headers.get('Authorization', '')
        
        if authorization_header.startswith('Bearer '):
            auth_token = authorization_header.split()[1]

        if not auth_token:
            current_app.logger.warning("Request missing authorization token")
            return jsonify({'message': 'Authentication token required'}), 401

        try:
            # Verify and decode the JWT token
            token_payload = jwt.decode(
                auth_token,
                current_app.config['SECRET_KEY'],
                algorithms=["HS256"]
            )
            
            # Log successful token validation
            current_app.logger.debug(
                f"Valid token for user {token_payload['sub']} with role {token_payload['role']}"
            )
            
            # Pass user credentials to the wrapped function
            return f(
                token_payload['sub'],  # current_user_id
                token_payload['role'], # current_user_role
                *args,
                **kwargs
            )

        except jwt.ExpiredSignatureError:
            current_app.logger.warning("Expired authentication token")
            return jsonify({'message': 'Session expired - please login again'}), 401
            
        except jwt.InvalidTokenError:
            current_app.logger.warning("Invalid authentication token provided")
            return jsonify({'message': 'Invalid authentication credentials'}), 401
            
        except Exception as unexpected_error:
            current_app.logger.error(
                f"Unexpected token validation error: {str(unexpected_error)}"
            )
            return jsonify({
                'message': 'Authentication system error',
                'details': str(unexpected_error)
            }), 401

    return decorated
