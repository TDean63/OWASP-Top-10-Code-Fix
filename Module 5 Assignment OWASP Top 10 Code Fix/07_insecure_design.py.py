import secrets
import hashlib

from datetime import datetime, timedelta, timezone
from flask import request, jsonify
from argon2 import PasswordHasher

ph = PasswordHasher()

# request a password reset.
@app.route('/request-reset', methods=['POST'])
def request_reset():
    email = request.form['email']

    user = User.query.filter_by(email=email).first()

    if user:
        # create a cryptographically secure token.
        token = secrets.token_urlsafe(32)

        # store a hash not the actual token.
        token_hash = hashlib.sha256(
            token.encode()
        ).hexdigest()

        reset = PasswordResetToken(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=(
                datetime.now(timezone.utc)
                + timedelta(minutes=15)
            )
        )

        db.session.add(reset)
        db.session.commit()

        # email the token using a configured trusted password reset URL
        send_reset_email(user.email, token)

    # return the same message etiehr way
    return jsonify({
        "message":
        "If the account exists, a reset link will be sent."
    })

# verify the token and reset the password
@app.route('/reset-password', methods=['POST'])
def reset_password():
    token = request.form['token']
    new_password = request.form['new_password']

    # check the new password against the applications password policy
    if len(new_password) < 15:
        return jsonify({
            "error": "Password is too short"
        }), 400

    token_hash = hashlib.sha256(
        token.encode()
    ).hexdigest()

    reset = PasswordResetToken.query.filter_by(
        token_hash=token_hash
    ).first()

    if (
        reset is None
        or reset.expires_at.replace(
            tzinfo=timezone.utc
        ) <= datetime.now(timezone.utc)
    ):
        return jsonify({
            "error": "Invalid or expired reset token"
        }), 400

    user = db.session.get(User, reset.user_id)

    if user is None:
        return jsonify({
            "error": "Invalid reset token"
        }), 400

    # hash the new password before saving it
    user.password = ph.hash(new_password)

    # delete the token so it cannot be reused
    db.session.delete(reset)

    db.session.commit()

    return jsonify({
        "message": "Password reset successfully"
    })