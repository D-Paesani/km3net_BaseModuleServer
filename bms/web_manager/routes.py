from bms.web_manager.forms import LoginForm
from bms.web_manager.dbmanager import Users, gen_random_psw
from bms.web_manager import bcrypt, db
from flask import Flask, request, render_template, redirect, url_for, flash, Blueprint
from bms.web_manager.forms import LoginForm
from flask_login import login_user, current_user, logout_user, login_required

routes_blueprint = Blueprint('user', __name__, template_folder="../../templates")#, static_folder="../static")

@routes_blueprint.route('/', methods = ['GET'])
@login_required
def base():
    return render_template('help.html')

@routes_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('base'))
    form = LoginForm()
    if request.method == "POST":
        ulogin = False
        if form.validate_on_submit():
            if Users.query.filter_by(username=form.username.data).first():
                ulogin = Users.query.filter_by(username=form.username.data).first()
            elif Users.query.filter_by(email=form.username.data).first():
                ulogin = Users.query.filter_by(email=form.username.data).first()
            if ulogin == False:
                flash('Username or Password not Found', 'danger-custom')
            elif ulogin and bcrypt.check_password_hash(ulogin.password, form.password.data):
                login_user(ulogin)
                flash(f'Login Successfully {current_user}', 'success-custom')
                return redirect(url_for('user.base'))
            else:
                flash("Wrong Password", 'danger-custom')
    return render_template('accounts/login.html', form=form)



@routes_blueprint.route('/logout')
@login_required
def logout():
    if current_user.source == 'google':
        Users.query.filter(Users.email == current_user.email).delete()
        db.session.commit()
    logout_user()
    return redirect(url_for('user.login'))

@routes_blueprint.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error=error)