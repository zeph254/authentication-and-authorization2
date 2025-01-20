from operator import and_
from flask import Blueprint,jsonify,request
from werkzeug.security import generate_password_hash
from models import User,db
from flask_jwt_extended import jwt_required, get_jwt_identity


user_bp = Blueprint('user_bp',__name__)


@user_bp.route("/users", methods= ["POST"])
def register_user():
    data = request.get_json()
    username = data["username"]
    email = data["email"]
    password = generate_password_hash (data["password"])

    check_username = User.query.filter_by(username=username).first()
    check_email = User.query.filter_by(email=email).first()

    if check_username or check_email:
        return jsonify [{"error":"username/Email exist"}]
    

    else:
        new_user = User(username=username,email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message":"user saved succesfully"}),201
    
#update user
@user_bp.route("/users", methods=["PATCH"])
@jwt_required()
def update_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if user:
        data = request.get_json()

        username = data.get("username", user.username)
        email = data.get("email", user.email)
        password = generate_password_hash(data.get("password", user.password))

        # Check for duplicate username or email excluding the current user
        check_username = User.query.filter(
            and_(User.username == username, User.id != current_user_id)
        ).first()
        check_email = User.query.filter(
            and_(User.email == email, User.id != current_user_id)
        ).first()

        if check_username or check_email:
            return jsonify({"error": "Username or Email already exists"}), 409
        else:
            user.username = username
            user.email = email
            user.password = password

            db.session.commit()
            return jsonify({"success": "User updated successfully"}), 200
    else:
        return jsonify({"error": "User doesn't exist"}), 404

#delete user
@user_bp.route("/users", methods=["DELETE"])
@jwt_required()
def delete_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"success": "your account is deleted successfully"}), 200
    else:
        return jsonify({"error": "User doesn't exist"}), 404

