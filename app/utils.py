from functools import wraps
from flask import session, redirect, url_for

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('auth.login'))
        
        from app.models import User
        user = User.query.get(session.get('user_id'))
        if not user or not user.is_admin:
            # Return JSON if API, redirect if page? 
            # Original code returned JSON error for both. Let's keep it simple.
            # But wait, admin dashboard is a page. Returning JSON 403 might be weird for a browser visit.
            # The original code returned JSON: jsonify({'error': 'Acesso negado...'}), 403
            # Let's stick to original behavior or improve it later.
            from flask import jsonify
            return jsonify({'error': 'Acesso negado. Apenas administradores.'}), 403
        
        return f(*args, **kwargs)
    return decorated_function
