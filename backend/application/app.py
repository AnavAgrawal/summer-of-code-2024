from flask import Flask
import dotenv
import os
from database import login_manager, bcrypt, db, Staff
from blueprints.products.products import products_bp
from blueprints.login.login import login_bp
from blueprints.customers.customers import customers_bp
from blueprints.staff.staff import staff_bp
from blueprints.transactions.transactions import transactions_bp

def create_app():
    app = Flask(__name__)
    
    # get url from .env file
    dotenv.load_dotenv()
    url = os.getenv('DATABASE_URL')
    # url ='postgresql://postgres.thqxcgupvxmnnrmovubd:QTBqlDHX1Ih9ICoC@aws-0-ap-south-1.pooler.supabase.com:6543/postgres'

    app.config['SQLALCHEMY_DATABASE_URI'] = url
    app.config['SECRET_KEY'] = 'secret'
    app.config['EXPLAIN_TEMPLATE_LOADING'] = True

    db.init_app(app)
    bcrypt.init_app(app)

    login_manager.init_app(app)
        
    @login_manager.user_loader
    def load_user(user_id):
        return Staff.query.get(int(user_id))

    app.register_blueprint(login_bp)
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(staff_bp, url_prefix='/staff')
    app.register_blueprint(transactions_bp, url_prefix='/transactions')
    
    return app

def setup_db(app):
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    app = create_app()
    setup_db(app)
    app.run(debug=True)