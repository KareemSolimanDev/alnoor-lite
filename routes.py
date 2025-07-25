from run import app
from flask import render_template,request,flash,redirect,url_for,abort
from run import db
from models import User,Lesson
from flask_login import login_user,logout_user,login_required,current_user
from helpers import save_picture

@app.route('/')
@app.route('/home')
def home():
    lessons=Lesson.query.all()[::-1][:3]
    return render_template('home.html',title='Home',lessons=lessons)


@app.route('/about')
def about():
    return render_template('about.html',title='About')

@app.route('/listen')
def listen():
    flash('يتوقف تحميل الايه علي سرعه الانترنت ','info')
    return render_template('listen.html',title='listen')

@app.route('/read')
def read():
    return render_template('read.html',title='Read')

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
        flash("سيتم حذف حسابك ان كانت المعلومات غير صحيحه",category='info')
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
        if imgFile:
            image=save_picture(imgFile)
            lesson=Lesson(image=image,title=title,content=content,author=current_user)
        else:
            lesson=Lesson(title=title,content=content,author=current_user)
        db.session.add(lesson)
        try:
            db.session.commit()
        except:
            flash('يرجي التاكد من صحه البيانات وان العنوان مستحدم للمره الاولي',category='danger')
            return redirect(url_for('create'))
        flash('تم اضافه الدرس بنجاح',category='success')
        return redirect(url_for('home'))
    if (current_user.role=='user'):
        return abort(403)
    else:
        return render_template('create.html',title='Create')

@app.route('/lesson/<int:id>')
@login_required
def lesson(id):
    lesson=Lesson.query.get_or_404(id)
    return render_template('lesson_data.html',lesson=lesson,title='Lesson')


@app.route('/lessons')
@login_required
def lessons():
    page=request.args.get('page',1,type=int)
    lessons=Lesson.query.paginate(page=page,per_page=6)
    return render_template('all_lessons.html',lessons=lessons,title='Lesson')


@app.route('/blog')
@login_required
def blog():
    lessons_1=Lesson.query.all()[::-1][:4]
    lessons_2=Lesson.query.all()[::-1][4:8]
    return render_template('blog.html',lessons_1=lessons_1,lessons_2=lessons_2,title='Blog')

@app.route('/user/<uname>')
@login_required
def user(uname):
    guser=User.query.filter_by(uname=uname).first()
    if guser:
        user=guser
    else:
        return abort(404)
    return render_template('user.html',title='User',user=user)

@app.route('/user/<uname>/lessons')
@login_required
def user_lessons(uname):
    guser=User.query.filter_by(uname=uname).first()
    if guser:
        user=guser
    else:
        return abort(404)
    page=request.args.get('page',1,type=int)
    lessons=Lesson.query.filter_by(user_id=user.id).paginate(page=page,per_page=6)
    return render_template('user_lessons.html',title='User',user=user,page=page,lessons=lessons)

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html',title='Error'), 404

@app.errorhandler(403)
def not_allowed(e):
    return render_template('304.html',title='Error'), 403