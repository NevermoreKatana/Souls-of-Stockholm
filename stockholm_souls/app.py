import os
import dotenv
from stockholm_souls.database.validator import password_checker
from stockholm_souls.database.db import (verification,
                                         take_user_id,
                                         take_user_info,
                                         take_additional_user_info,
                                         create_new_user,
                                         create_session_data,
                                         check_user,
                                         check_valid_api_key,
                                         take_user_secret_key,
                                         take_all_users,
                                         take_all_posts,
                                         take_one_post,
                                         take_posts_api,
                                         take_comments,
                                         add_comments)
from flask import (Flask,
                   render_template,
                   request,
                   flash,
                   redirect,
                   jsonify,
                   flash,
                   session)
from flask_jwt_extended import (JWTManager,
                                create_access_token,
                                jwt_required,
                                get_jwt_identity)
dotenv.load_dotenv()

app = Flask(__name__, static_folder='templates')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
jwt = JWTManager(app)

@app.route('/', methods=['GET'])
def index():
    posts_data = take_all_posts()
    current_user = session.get('user')
    if current_user:
        return render_template('index.html', cu = current_user, posts=posts_data)
    return render_template('index.html',posts=posts_data)


@app.route('/login', methods=['GET'])
def login_form():
    return render_template('/user/login.html')


@app.route('/login/', methods=['POST'])
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

@app.route('/register', methods=['GET'])
def reg_form():
    return render_template('/user/register.html')


@app.route('/register/', methods=['POST'])
def register_user():
    name = request.form['uname']
    passwd = request.form['passwd']
    confirm_passwd = request.form['confirm_passwd']
    country = request.form['country']
    gender = request.form['gender']
    age = request.form['age']
    errors = password_checker(passwd, confirm_passwd)
    if check_user(name):
        flash({'exist':'A user with this name exists'})
        return redirect('/register')
    elif errors:
        flash(errors)
        return redirect('/register')
    secret = create_access_token(identity=name)
    create_new_user(name, passwd, country,gender,age, secret)
    id = take_user_id(name)
    user_data = create_session_data(id)
    session['user'] = user_data
    return redirect(f'/profile/{id}')

@app.route('/profile/<id>', methods=['GET'])
def show_profile(id):
    current_user = session.get('user')
    user_info = take_user_info(id)
    if user_info:
        additional_info = take_additional_user_info(id)
        return render_template('/user/profile.html', info = user_info, a_inf=additional_info, cu = current_user)
    else:
        return render_template('error/index.html')


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/')



@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    jwt_key = data['API_Key']
    tg_id = data['user_id']
    check = check_valid_api_key(jwt_key, tg_id)
    return jsonify(check)

@app.route('/profiles', methods=['GET'])
def show_profiles():
    data = take_all_users()
    current_user = session.get('user')
    return render_template('user/profiles.html', users=data, cu=current_user)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('/error/index.html')

@app.route('/post/<id>', methods=['GET'])
def show_post(id):
    post_info = take_one_post(id)
    comments_data = take_comments(id)
    current_user = session.get('user')
    if post_info:
        return render_template('post.html', post=post_info[0], cu=current_user, comments = comments_data)
    return render_template('/error/index.html')


@app.route('/<jwt>/posts', methods=['POST'])
def api_posts(jwt):
    data = take_posts_api(jwt)
    if data:
        return jsonify(data)
    return jsonify({'denied': 'Отказано в доступе'})


@app.route('/post/<post_id>/comment', methods=['POST'])
def add_comment(post_id):
    content = request.form['comment']
    user = session.get('user')
    if user:
        add_comments(post_id, content, user)
        return redirect(f'/post/{post_id}')
    flash('Войдите в аккаунт')
    return redirect(f'/post/{post_id}')