from flask import (render_template,
                   request,
                   redirect,
                   flash,
                   session, Blueprint)
from stockholm_souls.database.validator import password_checker
from stockholm_souls.database.db_user_nadlers import (verification,
                                                      take_user_id,
                                                      take_user_info,
                                                      take_additional_user_info,
                                                      create_new_user,
                                                      create_session_data,
                                                      check_user)
from flask_jwt_extended import create_access_token


users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/login', methods=['GET'])
def login_form():
    return render_template('/user/login.html')


@users_blueprint.route('/login/', methods=['POST'])
def login_user():
    name = request.form['uname']
    passwd = request.form['passwd']
    errors = verification(name, passwd)
    if errors:
        flash(errors)
        return redirect('/login')
    id = take_user_id(name)
    user_data = create_session_data(id)
    session['user'] = user_data
    flash('Успешный вход')
    return redirect(f'/profile/{id}')


@users_blueprint.route('/register', methods=['GET'])
def reg_form():
    return render_template('/user/register.html')


@users_blueprint.route('/register/', methods=['POST'])
def register_user():
    name = request.form['uname']
    passwd = request.form['passwd']
    confirm_passwd = request.form['confirm_passwd']
    country = request.form['country']
    gender = request.form['gender']
    age = request.form['age']
    errors = password_checker(passwd, confirm_passwd)
    if check_user(name):
        flash({'exist': 'A user with this name exists'})
        return redirect('/register')
    elif errors:
        flash(errors)
        return redirect('/register')
    secret = create_access_token(identity=name)
    create_new_user(name, passwd, country, gender, age, secret)
    id = take_user_id(name)
    user_data = create_session_data(id)
    session['user'] = user_data
    return redirect(f'/profile/{id}')


@users_blueprint.route('/profile/<id>', methods=['GET'])
def show_profile(id):
    current_user = session.get('user')
    user_info = take_user_info(id)
    if user_info:
        additional_info = take_additional_user_info(id)
        return render_template('/user/profile.html',
                               info=user_info,
                               a_inf=additional_info,
                               cu=current_user)
    else:
        return render_template('error/index.html')


@users_blueprint.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/')
