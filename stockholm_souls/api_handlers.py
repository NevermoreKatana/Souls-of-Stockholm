from stockholm_souls.database.api_handler import add_new_comment, check_valid_jwt_key, take_posts_api, take_one_post_api
from stockholm_souls.database.db import (verification,
                                         take_jwt,
                                         )
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


@api_blueprint.route('/<jwt>/post/<post_id>/comment', methods=['POST'])
def add_comment_api(post_id, jwt):
    data = request.get_json()
    content = data['content']
    errors = add_new_comment(jwt, post_id, content)
    if errors:
        return jsonify(errors)
    return jsonify({'denied': 'Ошибка'})