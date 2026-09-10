import mysql.connector
from mysql.connector import Error
from flask import current_app
import logging

def get_cims_db_connection():
    """
    Creates and returns a connection to the central CIMS database.
    Returns None if connection fails.
    """
    try:
        # Establish connection using application configuration
        db_conn = mysql.connector.connect(
            host=current_app.config['DB_HOST'],
            database=current_app.config['DB_NAME_CIMS'],
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASSWORD'],
            connect_timeout=5
        )
        
        current_app.logger.info("Successfully connected to CIMS database")
        return db_conn

    except Error as db_error:
        current_app.logger.error(
            f"CIMS database connection failed: {str(db_error)}"
        )
        return None
    except Exception as unexpected_error:
        logging.error(
            f"Unexpected error connecting to CIMS database: {str(unexpected_error)}"
        )
        return None


def get_project_db_connection():
    """
    Creates and returns a connection to the project-specific database.
    Returns None if connection fails.
    """
    try:
        db_conn = mysql.connector.connect(
            host=current_app.config['DB_HOST'],
            database=current_app.config['DB_NAME_PROJECT'],
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASSWORD'],
            port=current_app.config.get('DB_PORT', 3306),
            connect_timeout=5
        )
        
        current_app.logger.debug(
            f"Established connection to project database: {current_app.config['DB_NAME_PROJECT']}"
        )
        return db_conn

    except Error as db_error:
        current_app.logger.error(
            f"Project database connection error: {str(db_error)}"
        )
        return None
    except Exception as unexpected_error:
        logging.critical(
            f"Critical error connecting to project database: {str(unexpected_error)}"
        )
        return None
