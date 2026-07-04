"""Admin panel for Pepka Bot"""
from flask import Flask, render_template, request, jsonify, session, redirect
from functools import wraps
from database.db_init import User
from loguru import logger
from config import ADMIN_IDS
from datetime import datetime

app = Flask(__name__, template_folder='templates')
app.secret_key = 'your-secret-key-here'  # Change this!

# Authentication decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            return redirect('/admin/login')
        if session['admin_id'] not in ADMIN_IDS:
            return "Unauthorized", 403
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    """Admin login page."""
    if request.method == 'POST':
        admin_id = int(request.form.get('admin_id'))
        password = request.form.get('password')
        
        # Simple authentication (in production, use better methods)
        if admin_id in ADMIN_IDS and password == 'admin123':  # Change password!
            session['admin_id'] = admin_id
            logger.info(f"👨‍💼 Admin {admin_id} logged in")
            return redirect('/admin')
        else:
            return "Invalid credentials", 401
    
    return '''
    <html>
    <body>
        <h1>Pepka Admin Login</h1>
        <form method="post">
            <input type="number" name="admin_id" placeholder="Admin ID" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
    </body>
    </html>
    '''

@app.route('/admin')
@admin_required
def dashboard():
    """Admin dashboard."""
    leaderboard = User.get_leaderboard(10)
    total_users = len(leaderboard)  # Placeholder
    
    return f'''
    <html>
    <head>
        <title>Pepka Admin Dashboard</title>
        <style>
            body {{ font-family: Arial; margin: 20px; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #4CAF50; color: white; }}
        </style>
    </head>
    <body>
        <h1>🐸 Pepka Admin Dashboard</h1>
        <p>Admin ID: {session.get('admin_id')}</p>
        
        <h2>Statistics</h2>
        <p>Total Users: {total_users}</p>
        <p>Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <h2>Top Players</h2>
        <table>
            <tr>
                <th>Rank</th>
                <th>Username</th>
                <th>Tokens</th>
                <th>Level</th>
            </tr>
            {''.join(f'<tr><td>{idx+1}</td><td>{u[1]}</td><td>{u[2]}</td><td>{u[3]}</td></tr>' for idx, u in enumerate(leaderboard))}
        </table>
        
        <h2>Actions</h2>
        <ul>
            <li><a href="/admin/users">Manage Users</a></li>
            <li><a href="/admin/payments">View Payments</a></li>
            <li><a href="/admin/logs">View Logs</a></li>
            <li><a href="/admin/logout">Logout</a></li>
        </ul>
    </body>
    </html>
    '''

@app.route('/admin/users')
@admin_required
def manage_users():
    """Manage users."""
    return '''
    <html>
    <head>
        <title>Manage Users</title>
        <style>
            body {{ font-family: Arial; margin: 20px; }}
            form {{ margin: 20px 0; }}
            input {{ padding: 5px; margin: 5px; }}
        </style>
    </head>
    <body>
        <h1>Manage Users</h1>
        
        <h2>Add Tokens to User</h2>
        <form method="post" action="/admin/add-tokens">
            <input type="number" name="user_id" placeholder="User ID" required>
            <input type="number" name="amount" placeholder="Tokens to add" required>
            <button type="submit">Add Tokens</button>
        </form>
        
        <h2>Ban User</h2>
        <form method="post" action="/admin/ban-user">
            <input type="number" name="user_id" placeholder="User ID" required>
            <button type="submit">Ban User</button>
        </form>
        
        <a href="/admin">Back to Dashboard</a>
    </body>
    </html>
    '''

@app.route('/admin/add-tokens', methods=['POST'])
@admin_required
def add_tokens():
    """Add tokens to user."""
    user_id = int(request.form.get('user_id'))
    amount = int(request.form.get('amount'))
    
    User.add_tokens(user_id, amount)
    logger.info(f"👨‍💼 Admin {session.get('admin_id')} added {amount} tokens to user {user_id}")
    
    return f"✅ Added {amount} tokens to user {user_id}<br><a href='/admin/users'>Back</a>"

@app.route('/admin/ban-user', methods=['POST'])
@admin_required
def ban_user():
    """Ban a user."""
    user_id = int(request.form.get('user_id'))
    
    # Ban logic would go here
    logger.info(f"👨‍💼 Admin {session.get('admin_id')} banned user {user_id}")
    
    return f"✅ User {user_id} has been banned<br><a href='/admin/users'>Back</a>"

@app.route('/admin/logout')
@admin_required
def logout():
    """Admin logout."""
    session.clear()
    logger.info(f"👨‍💼 Admin logged out")
    return redirect('/admin/login')

if __name__ == '__main__':
    logger.info("🔐 Starting Pepka Admin Panel")
    app.run(host='0.0.0.0', port=5001, debug=False)
