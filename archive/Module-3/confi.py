# config.py
import os
import logging

# Get the base directory path where this config file is located
base_directory = os.path.abspath(os.path.dirname(__file__))
# Define and create the logs directory if needed
logs_directory = os.path.join(base_directory, 'logs')
os.makedirs(logs_directory, exist_ok=True)

class Config:
    """Core application configuration settings with environment variable fallbacks"""
    
    # JWT Authentication Secret Key
    # Note: Should use environment variables in production environments
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'IHopeIPassThisCourseIHopeIPassThisCourse'
    
    # Group identification number
    GROUP_ID = int(os.environ.get('GROUP_ID', 7))
    
    # Database connection parameters
    DB_HOST = os.environ.get('DB_HOST') or '10.0.116.125'
    DB_USER = os.environ.get('DB_USER') or 'cs432g7'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'qY5TzNmJ'
    DB_NAME_CIMS = os.environ.get('DB_NAME_CIMS') or 'cs432cims'
    DB_NAME_PROJECT = os.environ.get('DB_NAME_PROJECT') or 'cs432g7'
    
    # Default credentials for new user accounts
    DEFAULT_PASSWORD = 'default123'
    
    # Application logging configuration
    LOGGING_FILENAME = os.path.join(logs_directory, 'app.log')
    LOGGING_LEVEL = logging.INFO
    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Additional configuration classes could be implemented here
# for different environments (development, production, testing)
# by inheriting from this base Config class