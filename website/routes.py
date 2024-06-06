from website.models import User, Item, ManyMany
from flask import  render_template, url_for, flash, redirect, request
from website.forms import RegistrationForm, LoginForm, UpdateForm, SellItemForm, UpdateItemForm
from website import app, db, bcrypt
import secrets, os
from PIL import Image
from flask_login import login_user, current_user, logout_user, login_required
@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1 , type=int)
    items = Item.query.paginate(per_page=6)
    return render_template('home.html', title = 'sample', items = items, page  = page)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
         return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit(): 
            user = User.query.filter_by(email = form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
         return redirect(url_for('home'))
    form = RegistrationForm()
    print("Started")
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(uname = form.username.data, email = form.email.data, password = hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash(f'Your Account has been created, to access it, please Login', 'success')
        return redirect(url_for('login'))
    elif not form.validate_on_submit():
        print("Form was not validated")
    return render_template('register.html', title='Register', form=form)
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_pic(pic):
    random_hex = secrets.token_hex(8)
    _, ext = os.path.splitext(pic.filename)
    pic_fn = random_hex+ext
    path = os.path.join(app.root_path, 'static/userprofiles', pic_fn)
    output = (125, 125)
    i = Image.open(pic)
    i.thumbnail(output)
    i.save(path)
    return pic_fn
@app.route('/account', methods = ['GET', 'POST'])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.pic.data:
            pic_fn = save_pic(form.pic.data)
            current_user.image_file = pic_fn
        current_user.uname = form.username.data # Auto commands the SQLAlchemy
        current_user.email = form.email.data
        db.session.commit()
        flash('Your Account has been Updated', 'Success')
        return redirect(url_for('account'))
    elif request.method == 'GET': # If the user just loads the page we want him to see the details pre-filled on the form
        form.username.data = current_user.uname
        form.email.data = current_user.email
    profile = url_for('static', filename ='userprofiles/'+current_user.image_file)
    return render_template('account.html', title = 'Account', form= form, image = profile)

@app.route('/phone')
def phone():
    page = request.args.get('page', 1 , type=int)
    items = Item.query.filter_by(item_class = 'PHONE').paginate(per_page=6)
    if len(list(items)) == 0:
        items = None
    return render_template('phone.html', items = items, page = page)
@app.route('/laptops')
def laptops():
    page = request.args.get('page', 1 , type=int)
    items = Item.query.filter_by(item_class = 'LAPPY').paginate(per_page=6)
    if len(list(items)) == 0:
        items = None
    return render_template('laptops.html', items = items, page = page)
@app.route('/accessories')
def acc():
    page = request.args.get('page', 1 , type=int)
    items = Item.query.filter_by(item_class = 'ACC').paginate(per_page=6)
    if len(list(items)) == 0:
        items = None
    return render_template('acc.html', items = items, page = page)

def save_item_pic(pic):
    random_hex = secrets.token_hex(8)
    _, ext = os.path.splitext(pic.filename)
    pic_fn = random_hex+ext
    path = os.path.join(app.root_path, 'static/itempics', pic_fn)
    output = (250, 250)
    i = Image.open(pic)
    i.thumbnail(output)
    i.save(path)
    return pic_fn
@app.route('/sell', methods=['GET', 'POST'])
@login_required
def sellItem():
    form = SellItemForm()
    if form.validate_on_submit():
        if form.pic.data:
            pic_fn = save_item_pic(form.pic.data)
            item = Item(name = form.name.data, price = form.price.data, desc= form.desc.data, seller_id = current_user.id, item_class = form.class_.data, image_file = pic_fn)
        else:
            item = Item(name = form.name.data, price = form.price.data, desc= form.desc.data, seller_id = current_user.id, item_class = form.class_.data)
        db.session.add(item)
        db.session.commit()
        flash('Your Item has been Listed for selling', 'Success')
        return redirect(url_for('home'))
    items = Item.query.filter_by(seller = current_user).paginate(per_page=3)
    page = request.args.get('page', 1 , type=int)
    if len(list(items)) == 0:
        items = None
    return render_template('sell_item.html', form = form, items = items, page = page)

@app.route('/sell/update/<itemid>', methods=['GET', 'POST'])
@login_required
def updateitem(itemid):
    item = Item.query.get_or_404(itemid)
    if(item.seller.uname != current_user.uname):
        flash('Please Meddle With Your Products Only!', 'warning')
        return redirect(url_for('home'))
    form = UpdateItemForm()
    if form.validate_on_submit():
        item.name = form.name.data
        item.price = form.price.data
        item.desc = form.desc.data
        item.item_class = form.class_.data
        if form.pic.data:
            pic_fn = save_item_pic(form.pic.data)
            item.image_file = pic_fn
        db.session.commit()
        flash('Item Updated', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.name.data = item.name 
        form.price.data = item.price
        form.class_.data = item.item_class
        form.desc.data = item.desc
    return render_template('updateitem.html', form = form, item = item)

@app.route('/delete/<id>', methods=['GET', 'POST'])
@login_required
def deleteItem(id):
    item = Item.query.get_or_404(id)
    if(item.seller.uname != current_user.uname):
        flash('Please Meddle With Your Products Only!', 'warning')
        return redirect(url_for('home'))
    db.session.delete(item)
    db.session.commit()
    flash('Item Deleted Successfully', 'Success')
    return redirect(url_for('home'))
@app.route('/add/cart/<id>')
def addtocart(id):
    item = Item.query.get_or_404(id)
    rel = ManyMany(items = item.item_id, users = current_user.id)
    print(rel)
    db.session.add(rel)
    db.session.commit()
    flash('Item Added to Cart', 'Success')
    return redirect(url_for('cart'))

@app.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    added_items_id = ManyMany.query.filter_by(users = current_user.id).all()
    item_ids = []
    for ob in added_items_id:
        item_ids.append(ob.items)
    items = []
    price = 0
    freq = {}
    for id in item_ids:
        item = Item.query.get_or_404(id)
        price += item.price
        freq[item] = 1+freq.get(item, 0)
        items.append(item)
    print(price)
    return render_template('cart.html', items = items, freq = freq, total = price)
@app.route('/cart/remove/<id>', methods=['GET', 'POST'])
def removefromcart(id):
    item = Item.query.get_or_404(id)
    rel = ManyMany.query.filter_by(items = id, users = current_user.id).first_or_404()
    db.session.delete(rel)
    db.session.commit()
    flash(f'Item-{item.name} Successfully removed from cart')
    return redirect(url_for('cart'))