from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Definir la clase User que extiende UserMixin
class User(UserMixin):
    def __init__(self, username):
        self.id = username

# Usuario ficticio para demostración (en producción, usarías una base de datos)
users = {"username": "paco", "password": "123"}

@login_manager.user_loader
def load_user(user_id):
    # En un escenario real, buscarías el usuario en la base de datos
    if user_id == users['username']:
        return User(user_id)
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == users['username'] and password == users['password']:
            user = User(username)
            login_user(user)
            # flash('Te has logueado correctamente.')
            return redirect(url_for('home'))
        else:
            flash('Credenciales inválidas. Por favor, inténtalo de nuevo.')
            return redirect(url_for('index'))
    return render_template('index.html')    

@app.route('/home')
@login_required
def home():
    return render_template('home.html')    

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
