import os
import json
from flask import Flask, request, jsonify, session, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_folder='static')
app.secret_key = 'rahasia_super_aman_sekali'
DB_FILE = 'db.json'

def load_db():
    if not os.path.exists(DB_FILE):
        return {"users": {}}
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Serve Static HTML pages
@app.route('/')
def serve_index():
    if 'username' in session:
        return send_from_directory('templates', 'dashboard.html')
    return send_from_directory('.', 'index.html')

@app.route('/dashboard')
def serve_dashboard():
    if 'username' not in session:
        return send_from_directory('.', 'index.html')
    return send_from_directory('templates', 'dashboard.html')

@app.route('/admin')
def serve_admin():
    if 'username' not in session:
        return send_from_directory('.', 'index.html')
    return send_from_directory('templates', 'admin.html')

@app.route('/<path:path>')
def serve_static_files(path):
    if os.path.exists(path):
        return send_from_directory('.', path)
    return "File not found", 404

# API Routes
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    db = load_db()
    user = db['users'].get(username)
    
    if user and check_password_hash(user['password'], password):
        session['username'] = username
        role = user.get('role', 'user')
        return jsonify({"success": True, "role": role})
    
    return jsonify({"success": False, "message": "Username atau password salah!"}), 401

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if len(password) < 6:
        return jsonify({"success": False, "message": "Password minimal 6 karakter!"})
        
    db = load_db()
    if username in db['users']:
        return jsonify({"success": False, "message": "Username sudah terdaftar!"})
        
    db['users'][username] = {
        "password": generate_password_hash(password),
        "role": "user",
        "profil": {},
        "kegiatan": []
    }
    save_db(db)
    return jsonify({"success": True, "message": "Berhasil mendaftar! Silakan login."})

@app.route('/api/data', methods=['GET', 'POST'])
def api_data():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401
        
    username = session['username']
    db = load_db()
    
    if request.method == 'GET':
        user_data = db['users'].get(username, {})
        return jsonify({
            "profil": user_data.get('profil', {}),
            "kegiatan": user_data.get('kegiatan', [])
        })
        
    if request.method == 'POST':
        new_data = request.json
        if username in db['users']:
            db['users'][username]['profil'] = new_data.get('profil', {})
            db['users'][username]['kegiatan'] = new_data.get('kegiatan', [])
            save_db(db)
            return jsonify({"success": True})
        return jsonify({"error": "User not found"}), 404

@app.route('/api/change_password', methods=['POST'])
def api_change_password():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401
        
    data = request.json
    old_pwd = data.get('old_pwd', '')
    new_pwd = data.get('new_pwd', '')
    
    username = session['username']
    db = load_db()
    user = db['users'].get(username)
    
    if user and check_password_hash(user['password'], old_pwd):
        if len(new_pwd) < 6:
            return jsonify({"success": False, "message": "Password baru minimal 6 karakter!"})
        db['users'][username]['password'] = generate_password_hash(new_pwd)
        save_db(db)
        return jsonify({"success": True, "message": "Password berhasil diubah!"})
        
    return jsonify({"success": False, "message": "Password lama salah!"})

if __name__ == '__main__':
    # Listen on all interfaces (0.0.0.0) so it's accessible from mobile/LAN
    app.run(host='0.0.0.0', port=8000, debug=True)
