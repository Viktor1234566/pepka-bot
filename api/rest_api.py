"""REST API for Pepka Bot"""
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from database.db_init import User
from payments.stripe_integration import StripePayment
from config import API_BASE_URL, API_PORT, API_VERSION
from loguru import logger
import json
from functools import wraps
from datetime import datetime

app = Flask(__name__)
api = Api(app)

# Middleware for logging
@app.before_request
def log_request():
    logger.info(f"{request.method} {request.path} - {request.remote_addr}")

@app.after_request
def log_response(response):
    logger.info(f"Response: {response.status_code}")
    return response

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(error):
    logger.error(f"Server error: {error}")
    return jsonify({"error": "Internal server error"}), 500

# API Resources

class UserProfile(Resource):
    """User profile endpoint."""
    
    def get(self, user_id):
        """Get user profile."""
        user_data = User.get(user_id)
        if not user_data:
            return {"error": "User not found"}, 404
        
        user_id, username, first_name, last_name, language, tokens, level, experience, hp, max_hp = user_data[:10]
        
        return {
            "user_id": user_id,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "language": language,
            "tokens": tokens,
            "level": level,
            "experience": experience,
            "hp": hp,
            "max_hp": max_hp
        }, 200

class UserStats(Resource):
    """User statistics endpoint."""
    
    def get(self, user_id):
        """Get user statistics."""
        user_data = User.get(user_id)
        if not user_data:
            return {"error": "User not found"}, 404
        
        # Placeholder stats
        return {
            "user_id": user_id,
            "total_clicks": 1234,
            "combats_won": 45,
            "combats_lost": 12,
            "quests_completed": 23,
            "current_streak": 7
        }, 200

class Leaderboard(Resource):
    """Leaderboard endpoint."""
    
    def get(self):
        """Get top 100 players."""
        limit = request.args.get('limit', 100, type=int)
        leaderboard = User.get_leaderboard(min(limit, 100))
        
        return {
            "leaderboard": [
                {
                    "rank": idx + 1,
                    "user_id": uid,
                    "username": username,
                    "tokens": tokens,
                    "level": level
                }
                for idx, (uid, username, tokens, level) in enumerate(leaderboard)
            ]
        }, 200

class PaymentStatus(Resource):
    """Payment status endpoint."""
    
    def get(self, intent_id):
        """Get payment status."""
        status = StripePayment.get_payment_status(intent_id)
        if not status:
            return {"error": "Payment not found"}, 404
        
        return {
            "intent_id": intent_id,
            "status": status
        }, 200

class HealthCheck(Resource):
    """Health check endpoint."""
    
    def get(self):
        """Check API health."""
        return {
            "status": "healthy",
            "version": API_VERSION,
            "timestamp": datetime.now().isoformat()
        }, 200

# Register resources
api.add_resource(HealthCheck, f'/{API_VERSION}/health')
api.add_resource(UserProfile, f'/{API_VERSION}/users/<int:user_id>')
api.add_resource(UserStats, f'/{API_VERSION}/users/<int:user_id>/stats')
api.add_resource(Leaderboard, f'/{API_VERSION}/leaderboard')
api.add_resource(PaymentStatus, f'/{API_VERSION}/payments/<intent_id>')

if __name__ == '__main__':
    logger.info(f"🚀 Starting Pepka API on {API_BASE_URL}:{API_PORT}")
    app.run(host='0.0.0.0', port=API_PORT, debug=False)
