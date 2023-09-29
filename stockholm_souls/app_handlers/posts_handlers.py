from flask import (render_template,
                   request,
                   redirect,
                   flash,
                   session,
                   Blueprint)
from stockholm_souls.database.db_posts_handlers import (take_one_post,
                                                        take_comments,
                                                        add_comments,
                                                        add_new_post)

posts_blueprint = Blueprint('posts', __name__)


@posts_blueprint.route('/post/<id>', methods=['GET'])
def show_post(id):
    post_info = take_one_post(id)
    comments_data = take_comments(id)
    current_user = session.get('user')
    if post_info:
        return render_template('posts/post.html',
                               post=post_info[0],
                               cu=current_user,
                               comments=comments_data)
    return render_template('/error/index.html')


@posts_blueprint.route('/post/<post_id>/comment', methods=['POST'])
def add_comment(post_id):
    content = request.form['comment']
    user = session.get('user')
    if user:
        add_comments(post_id, content, user)
        return redirect(f'/post/{post_id}')
    flash('Войдите в аккаунт')
    return redirect(f'/post/{post_id}')


@posts_blueprint.route('/post/create', methods=['GET'])
def create_post_form():
    current_user = session.get('user')
    return render_template('posts/create_post.html', cu=current_user)


@posts_blueprint.route('/post/create/', methods=['POST'])
def create_post():
    current_user = session.get('user')
    if current_user:
        post_name = request.form['name']
        contet = request.form['content']
        user_id = current_user['id']
        user_name = current_user['name']
        add_new_post(user_id, user_name, post_name, contet)
        return redirect('/')
    flash('Сначала войдите в аккаунт')
    return redirect('/post/create')
