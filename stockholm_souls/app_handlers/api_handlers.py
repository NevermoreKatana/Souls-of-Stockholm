from stockholm_souls.database.db_api_handlers import add_new_comment, check_valid_jwt_key, take_posts_api, take_one_post_api,create_new_post,check_valid_jwt
from stockholm_souls.database.db_user_nadlers import (verification,
                                                      take_user_info,
                                                      )
from stockholm_souls.database.db_api_handlers import take_jwt
from flask import (Flask,
                   render_template,
                   request,
                   flash,
                   redirect,
                   jsonify,
                   flash,
                   session, Blueprint)

api_blueprint = Blueprint('api', __name__)
@api_blueprint.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    jwt_key = data['API_Key']
    tg_id = data['user_id']
    check = check_valid_jwt_key(jwt_key, tg_id)
    return jsonify(check)


@api_blueprint.route('/a_api/login', methods=['POST'])
def a_api_login():
    data = request.get_json()
    user_name = data['login']
    passwd = data['password']
    errors = verification(user_name, passwd)
    if errors:
        return errors
    jwt = take_jwt(user_name)
    return {'login': 'success', "jwt": jwt}

@api_blueprint.route('/<jwt>/posts/<post_id>', methods=['GET'])
def show_post_api(jwt,post_id):
    post_data = take_one_post_api(post_id)
    if post_data:
        return jsonify(post_data)
    return jsonify({'denied': 'Такого поста нет'})

@api_blueprint.route('/<jwt>/posts', methods=['GET'])
def api_posts(jwt):
    data = take_posts_api(jwt)
    if data:
        return jsonify(data)
    return jsonify({'denied': 'Отказано в доступе'})


@api_blueprint.route('/<jwt>/post/<post_id>/comment/add', methods=['POST'])
def add_comment_api(post_id, jwt):
    data = request.get_json()
    content = data['content']
    if check_valid_jwt(jwt):
        add_new_comment(jwt, post_id, content)
        return jsonify({"success": "Успех"})
    return jsonify({'denied': 'Ошибка'})


@api_blueprint.route('/<jwt>/post/create', methods=['POST'])
def create_post(jwt):
    data = request.get_json()
    post_name = data['name']
    content = data['content']
    if check_valid_jwt(jwt):
        create_new_post(jwt, post_name, content)
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'denied'})


@api_blueprint.route('/<jwt>/profile/<id>', methods=['GET'])
def show_profile(jwt, id):
    if check_valid_jwt(jwt):
        data = take_user_info(id)
        return jsonify(data)
    return jsonify({'status': 'denied'})


