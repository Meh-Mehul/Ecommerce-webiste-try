from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileAllowed, FileField
from website.models import User, Item
from flask_login import current_user
class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    def validate_username(self, uname):
        user = User.query.filter_by(uname = uname.data).first()
        if user:
            raise ValidationError('Username Taken Please choose a newer one')
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('Email Taken Please choose a newer one')
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Update')
    pic = FileField('Update PFP', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    def validate_username(self, uname):
        if uname.data != current_user.uname: 
            user = User.query.filter_by(uname = uname.data).first()
            if user:
                raise ValidationError('Username Taken Please choose a newer one')
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('Email Taken Please choose a newer one')


class SellItemForm(FlaskForm):
    name = StringField('Item Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    price = IntegerField('Price',
                        validators=[DataRequired()])
    desc = TextAreaField('Short Description of The Product', validators=[DataRequired()])
    class_ = SelectField('Choose Type of Product', choices=[('PHONE', 'SmartPhone'), ('LAPPY', 'Laptop'), ('ACC', 'Accessories')])
    pic = FileField('Pic for Item', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Sell Product')
    def validate_name(self, name):
        item = Item.query.filter_by(name = name.data).first()
        if item:
            raise ValidationError('Item name Taken Please choose a newer one')


class UpdateItemForm(FlaskForm):
    name = StringField('Item Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    price = IntegerField('Price',
                        validators=[DataRequired()])
    desc = TextAreaField('Short Description of The Product', validators=[DataRequired()])
    class_ = SelectField('Choose Type of Product', choices=[('PHONE', 'SmartPhone'), ('LAPPY', 'Laptop'), ('ACC', 'Accessories')])
    pic = FileField('Pic for Item', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Sell Product')
    def validate_name(self, name):
        item = Item.query.filter_by(name = name.data).first()
        if item:
            raise ValidationError('Item name Taken Please choose a newer one')