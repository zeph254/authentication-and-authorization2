from datetime import datetime, timezone
from flask import Blueprint,jsonify,request
from models import TokenBlocklist, User,db
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, jwt_required

auth_bp = Blueprint('auth_bp',__name__)


@auth_bp.route("/login",methods = ["POST"])
def login():
    data = request.get_json()
    email = data["email"]
    password = data["password"]

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity = user.id)
        
        return jsonify({"access token":access_token})
    else:
        return jsonify[{"error":"User doesn't exist/cridentials are wrong "}], 200
    

#get current user
@auth_bp.route("/current_user" )
@jwt_required()
def current_user():
    current_user_id = get_jwt_identity()

    user = User.query.get(current_user_id)
    user_data = {
        "id":user.id,
        "email":user.email,
        "username":user.username,
        "is_approved":user.is_approved,
        "is_admin":user.is_admin
    }

    return jsonify(user_data), 200


@auth_bp.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    now = datetime.now(timezone.utc)
    db.session.add(TokenBlocklist(jti=jti, created_at=now))
    db.session.commit()
    return jsonify({"success":"loged out successfully"}), 200
