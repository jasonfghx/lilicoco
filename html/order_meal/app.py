from flask import render_template,Flask,request,redirect,url_for ,flash,jsonify,json, send_file,session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import pandas as pd
app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key'  
app.config['SQLALCHEMY_BINDS'] ={
    "tool":"sqlite:///DB/meal.db",
    # "checklist":"sqlite:///DB/tool_checklist.db",
    # "BG_message":"sqlite:///DB/BG_message.db",
    # "ALC":"sqlite:///DB/ALC.db",
    # 'tool_improve':'sqlite:///DB/tool_improve.db',
    # 'd_p':'sqlite:///DB/d_p.db',
}

db = SQLAlchemy(app)
db.init_app(app)
db.create_all()
login_manager = LoginManager(app)  


@login_manager.user_loader
def user_loader(USR):
    if USR == None and USR == '':
        return
    user = User()
    user.id = USR
    return user
class User(UserMixin):  
    
    pass  

class mealDB(db.Model):
    __bind_key__ ='tool' 
    __tablename__ = 'meal'
    Id = db.Column(db.Integer, primary_key=True)
    meal = db.Column(db.String(256),nullable=False)
    address = db.Column(db.String(256))
    d = db.Column(db.String(256))
    def __init__(self , meal,address,d):
        self.meal = meal
        self.address = address
        self.d=d
class memberDB(db.Model):
    __bind_key__ ='tool' 
    __tablename__ = 'member'
    Id = db.Column(db.Integer, primary_key=True)
    TEL = db.Column(db.String(256),nullable=False)
    mail = db.Column(db.String(256))
    pa= db.Column(db.String(256))
    name1=db.Column(db.String(256))
    birth=db.Column(db.String(256))
    def __init__(self , TEL,mail,pa,name1,birth):
        self.TEL = TEL
        self.mail = mail
        self.pa=pa
        self.name1=name1
        self.birth=birth

@app.route('/member/', methods = ['GET', 'POST'])
def member():
    return render_template('member.html')
@app.route('/member_add/', methods = ['GET', 'POST'])
def mem_add():
    db.create_all()
    if request.method=='POST':
        TEL= request.values['TEL']
        mail= request.values['mail']
        pa= request.values['pa']
        name1= request.values['name1']
        birth= request.values['birth']
        add_data = memberDB(TEL=TEL,mail=mail,pa=pa,name1=name1,birth=birth)
        try:
            db.session.add(add_data)
            db.session.commit()
            db.session.close()
        except Exception as e:
            print(e)
    return render_template('member.html')
@app.route('/forget/', methods = ['GET', 'POST'])
def forget():
    
    return render_template('forget.html')
@app.route('/forget_update/', methods = ['GET', 'POST'])
def forget_update():
    if request.method=='POST':
        TEL= request.values['TEL']
        conn=sqlite3.connect("DB/meal.db")
        sql_select='''SELECT TEL,mail FROM member '''
        data2=pd.read_sql_query(sql_select,conn)  
        print(data2.values.tolist())
        if TEL in list(data2.values.ravel()):
            data2temp=data2[(data2['TEL']==TEL)|(data2['mail']==TEL)]
            print(data2temp)
            index=list(data2temp.index)[0]+1
            print(index)
            # return redirect(url_for('forget_update_change',id=index))
            return render_template('forget_update.html',**locals())    
    return redirect(url_for('forget'))
@app.route('/forget_update_change/<id>/', methods = ['GET', 'POST'])
def forget_update_change(id):
    
    task = memberDB.query.get_or_404(id)
    if request.method=='POST':
        print(request.values['pa'])
        task.pa = request.values['pa']
        try:
            db.session.commit()
            return redirect('/forget/')
        except:
            return 'There was an issue updating your task'
    return render_template('forget.html')

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    USR = request.form['user_id']
    PWD = request.form['password']
    user = User()  
    user.id = USR  
    login_user(user)
    sql_select='''SELECT TEL,pa FROM member '''
    conn=sqlite3.connect("DB/meal.db")
    data2=pd.read_sql_query(sql_select,conn) 
    judge=data2[(data2['TEL']==USR)&(data2['pa']==PWD)]
    if USR=='admin' and PWD=='admin':
        return redirect(url_for('home'))
    if judge.shape[0]==1:
        return redirect(url_for('home'))
    else:
        return '帳號密碼錯誤'
@app.route("/")
def home1():
    return render_template('home.html',**locals())
@app.route("/h")
@login_required
def home():
    USR = current_user.get_id()
    try:
        conn=sqlite3.connect("DB/meal.db")
        sql_select='''SELECT * FROM member where TEL='{}' '''.format(USR)
        data2=pd.read_sql_query(sql_select,conn)  
        name=data2['name1'][0]
        mail=data2['mail'][0]
        tel=data2['TEL'][0]
    except:
        Exception

    return render_template('main.html',**locals())
@app.route("/add",methods=["GET",'POST'])
@login_required
def meal_add():
    db.create_all()
    if request.method=='POST':
        try:
            Am= request.values['Am']
        except:
            Am=''
        try:
            Bm= request.values['Bm']
        except:
            Bm=''
        try:
            Cm= request.values['Cm']
        except:
            Cm=''
        try:
            Dm= request.values['Dm']
        except:
            Dm=''
        try:
            Em= request.values['Em']
        except:
            Em=''
        try:
            Fm= request.values['Fm']
        except:
            Fm=''
        try:
            Gm= request.values['Gm']
        except:
            Gm=''
        try:
            Hm= request.values['Hm']
        except:
            Hm=''
        try:
            final= request.values['final']
        except:
            final=''
        try:
            fina2= request.values['fina2']
        except:
            fina2=''
        meal=Am+'/'+Bm+'/'+Cm+'/'+Dm+'/'+Em+'/'+Fm+'/'+Gm+'/'+Hm
        if final=='':
            address=fina2
        else:
            address=final
        d= request.values['time']
        # print(meal,address),
        add_data = mealDB(meal=meal,address=address,d=d)
        try:
            db.session.add(add_data)
            db.session.commit()
            db.session.close()
        except Exception as e:
            print(e)
            # Exception

    return render_template('main.html')
@app.route("/meal_show")
def meal_show():
    conn=sqlite3.connect("DB/meal.db")
    sql_select='''SELECT * FROM meal '''
    data2=pd.read_sql_query(sql_select,conn)   
    data2html=data2.to_html(index=False)
    return data2html
@app.route("/member_show")
def member_show():
    conn=sqlite3.connect("DB/meal.db")
    sql_select='''SELECT * FROM member '''
    data2=pd.read_sql_query(sql_select,conn)   
    data2html=data2.to_html(index=False)
    return data2html
@app.route('/logout')
def logout():
    USR = current_user.get_id()
    logout_user()
    if USR is None:
        USR=''
    flash(f'{USR} 登出')
    return render_template('login.html')

if __name__ == '__main__':
  app.debug = True
  app.run(host="127.0.0.1",port=5001,debug=True)#