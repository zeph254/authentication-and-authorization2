from flask import Flask
from models import TokenBlocklist, db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from datetime import timedelta

app = Flask(__name__)

# Migration initialization
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
migrate = Migrate(app, db)

db.init_app(app)

# Configure JWT
jwt = JWTManager()  # Instantiate the JWTManager class
jwt.init_app(app)

# Correct app.config assignment
app.config["JWT_SECRET_KEY"] = "ixjcfxnijcefjjjjncn"  # Correct syntax
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)

# Import and register blueprints
from views import *
app.register_blueprint(user_bp)
app.register_blueprint(book_bp)
app.register_blueprint(auth_bp)


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()

    return token is not None
