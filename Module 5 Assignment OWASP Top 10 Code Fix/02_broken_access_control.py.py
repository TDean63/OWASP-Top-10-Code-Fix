from flask import jsonify, abort
from flask_login import login_required, current_user

@app.route('/account/<int:user_id')
@login_required
def get_account(user_id):

    # verify that the account belongs to the user.
    if current_user.id != user_id:
        abort(403)

    # retrieve the account.
    user = db.session.get(User, user_id)

    if user if None:
        abort(404)

    # return only premitted account information.
    return jsonify({
        "id": user.id,
        "username": user.username
    })