from website import db, datetime, Login_manager
from flask_login import UserMixin

@Login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    sellitem = db.relationship('Item', backref='seller', lazy=True)
    
    def __repr__(self):
        return f'{self.uname}, {self.email}'

class Item(db.Model):
    __tablename__ = 'item'
    
    item_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    item_class = db.Column(db.String(20), nullable=False, default='PHONE')
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'{self.item_id}'

class ManyMany(db.Model):
    __tablename__ = 'manymany'
    
    id = db.Column(db.Integer, primary_key=True)
    items = db.Column(db.Integer, nullable=False)
    users = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f'{self.items} added to cart by {self.users}'
