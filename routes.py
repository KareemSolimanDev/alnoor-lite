from run import app
from flask import render_template,request,flash,redirect,url_for
from run import db
from models import User,Lesson
from flask_login import login_user,logout_user,login_required,current_user
from helpers import save_picture

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html',title='Home')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        finame=request.form.get('fname')
        laname=request.form.get('lname')
        fname=finame+' '+laname
        email=request.form.get('email')
        username=request.form.get('username')
        password=request.form.get('password')
        check=request.form.get('check')
        user=User(fname=fname,email=email,uname=username,password=password)
        db.session.add(user)
        try:
            db.session.commit()
        except:
            flash('تحقق من ايميلك اوحاول تغيير اسم المستخدم','danger')
            return redirect(url_for('register'))
        login_user(user, remember=check)
        flash('تم انشاء الحساب بنجاح',category='success')
        return redirect(url_for('home'))
    else:
        return render_template('register.html',title='Register')


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        check=request.form.get('check')
        user=User.query.filter_by(email=email).first()
        if user and user.password==password:
            login_user(user, remember=check)
            flash('تم تسجيل الدخول',category='success')
            return redirect(url_for('home'))
        else:
            flash('يرجي التحقق من صحه البيانات',category='danger')
            return redirect(url_for('login'))
    else:
        return render_template('login.html',title='Login')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/create',methods=['GET','POST'])
@login_required
def create():
    if request.method=='POST':
        imgFile=request.files['imgFile']
        title=request.form.get('title')
        content=request.form.get('ckeditor')
        image=save_picture(imgFile)
        lesson=Lesson(image=image,title=title,content=content,author=current_user)
        db.session.add(lesson)
        try:
            db.session.commit()
        except:
            flash('يرجي التاكد من صحه البيانات وان العنوان مستحدم للمره الاولي',category='danger')
            return redirect(url_for('create'))
        flash('تم اضافه الدرس بنجاح',category='success')
        return redirect(url_for('home'))
    if current_user.role=='admin':
        return render_template('create.html',title='Create')
    else:
        return '404'

@app.route('/lesson/<int:id>')
def lesson(id):
    lesson=Lesson.query.get_or_404(id)
    return render_template('lesson_data.html',lesson=lesson,title='Lesson')