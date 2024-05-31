from flask import render_template,Flask,request,redirect,url_for ,flash,jsonify,json, send_file,session
from flask_sqlalchemy import SQLAlchemy
# from config import MYSQL_USER, MYSQL_PASSWORD

# import models
import sqlite3
app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@localhost:3306/SOAMS'

app.config['SECRET_KEY'] = 'super secret key'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy()
db.init_app(app)

class VisitRecord(db.Model):
    __tablename__ = 'visit_record'
    id = db.Column(db.String(256),  primary_key=True, comment='學生學號')
    semester = db.Column(db.String(256), primary_key=True, comment='學年及學期') # 學年+學期

    visit_date_time = db.Column(db.DateTime, unique=False, nullable=False, comment='訪視時間')
    semester = db.Column(db.String(256), primary_key=True, comment='學年及學期') # 學年+學期

    visit_date_time = db.Column(db.DateTime, unique=False, nullable=False, comment='訪視時間')

    # 校外賃居資料（學生填寫）
    landlord_name = db.Column(db.String(256), unique=False, nullable=False, comment='房東姓名')
    landlord_tel = db.Column(db.String(256), unique=False, nullable=False, comment='房東電話')
    addr = db.Column(db.String(256), unique=False, nullable=False, comment='租賃地址')
    building_type = db.Column(db.String(256), unique=False, nullable=False, comment='租屋型態')
    room_type = db.Column(db.String(256), unique=False, nullable=False, comment='房間類型')
    rent = db.Column(db.Integer, unique=False, nullable=False, comment='每月租金')
    deposit = db.Column(db.Integer, unique=False, nullable=False, comment='押金')
    recommand = db.Column(db.Boolean, unique=False, nullable=False, comment='是否值得推薦其他同學租賃')
    
    # 賃居安全自主管理檢視資料（學生填寫）
    safe_manage1 = db.Column(db.Boolean, unique=False, nullable=False, comment='木造隔間或鐵皮加蓋')
    safe_manage2 = db.Column(db.Boolean, unique=False, nullable=False, comment='有火警警報器或偵煙器')
    safe_manage3 = db.Column(db.Boolean, unique=False, nullable=False, comment='逃生通道暢通且標示清楚')
    safe_manage4 = db.Column(db.Boolean, unique=False, nullable=False, comment='門禁及鎖具良好管理')
    safe_manage5 = db.Column(db.Boolean, unique=False, nullable=False, comment='有安裝照明設備(停車場及周邊)')
    safe_manage6 = db.Column(db.Boolean, unique=False, nullable=False, comment='瞭解熟悉電路安全及逃生要領')
    safe_manage7 = db.Column(db.Boolean, unique=False, nullable=False, comment='熟悉派出所、醫療、消防隊、學校校安專線電話')
    safe_manage8 = db.Column(db.Boolean, unique=False, nullable=False, comment='使用多種電器(高耗能)，是否同時插在同一條延長線')
    safe_manage9 = db.Column(db.Boolean, unique=False, nullable=False, comment='有滅火器且功能正常')
    safe_manage10 = db.Column(db.Boolean, unique=False, nullable=False, comment='熱水器(電熱式及瓦斯式)安全良好，無一氧化碳中毒疑慮')
    safe_manage11 = db.Column(db.Boolean, unique=False, nullable=False, comment='分間6個以上房間或10個以上床位')
    safe_manage12 = db.Column(db.Boolean, unique=False, nullable=False, comment='有安裝監視器設備')
    safe_manage13 = db.Column(db.Boolean, unique=False, nullable=False, comment='使用<內政部定型化租賃契約>')

    # 環境作息及評估（導師填寫）
    deposit_demand = db.Column(db.Boolean, unique=False, nullable=False, comment='押金要求。 True:合理 False:不合理')
    water_electric_bill_demand = db.Column(db.Boolean, unique=False, nullable=False, comment='水電費要求。 True:合理 False:不合理')
    environment = db.Column(db.Integer, unique=False, nullable=False, comment='居家環境。 0:佳 1:適中 2:欠佳')
    environment_description = db.Column(db.String(256), unique=False, nullable=True, comment='居家環境欠佳說明')
    facility = db.Column(db.Integer, unique=False, nullable=False, comment='生活設施。 0:佳 1:適中 2:欠佳')
    faclity_description = db.Column(db.String(256), unique=False, nullable=True, comment='生活設施欠佳說明')
    situation = db.Column(db.Integer, unique=False, nullable=False, comment='訪視現況。 0:生活規律 1:適中 2:待加強')
    situation_description = db.Column(db.String(256), unique=False, nullable=True, comment='訪視現況待加強說明')
    is_get_along_with = db.Column(db.Boolean, unique=False, nullable=False, comment='主客相處。 True:和睦 False:欠佳')

    # 訪視結果（導師填寫）
    result = db.Column(db.Integer, unique=False, nullable=False, comment='訪視結果。 0:整體賃居狀況良好 1:聯繫家長關注 2:安全堪慮請協助 3:其他')
    result_description = db.Column(db.String(256), unique=False, nullable=True, comment='其他說明')
    others1 = db.Column(db.String(256), unique=False, nullable=True, comment='其他紀載或建議事項')

    # 關懷宣導項目（懇請導師賃居訪視時多予關懷叮嚀）
    traffic_safty = db.Column(db.Boolean, unique=False, nullable=False, comment='交通安全')
    smoke = db.Column(db.Boolean, unique=False, nullable=False, comment='拒絕菸害')
    drug = db.Column(db.Boolean, unique=False, nullable=False, comment='拒絕毒品')
    dengue = db.Column(db.Boolean, unique=False, nullable=False, comment='登革熱防治')
    others2 = db.Column(db.String(256), unique=False, nullable=True, comment='其他說明')
    def __init__(self,id,semester,visit_date_time,landlord_name,landlord_tel,addr,building_type,room_type,rent,deposit,recommand,\
                 safe_manage1,safe_manage2,safe_manage3,safe_manage4,safe_manage5,safe_manage6,safe_manage7,safe_manage8,safe_manage9,safe_manage10,safe_manage11,safe_manage12,safe_manage13,\
                 deposit_demand,water_electric_bill_demand,environment,environment_description,facility   ):
        self.id = id
        self.semester=semester
        self.visit_date_time=visit_date_time
        self.landlord_name=landlord_name
        self.landlord_tel=landlord_tel
        self.addr=addr
        self.building_type=building_type
        self.room_type=room_type
        self.rent=rent
        self.deposit=deposit
        self.recommand=recommand
        self.safe_manage1=safe_manage1
        self.safe_manage2=safe_manage2
        self.safe_manage3=safe_manage3
        self.safe_manage4=safe_manage4
        self.safe_manage5=safe_manage5
        self.safe_manage6=safe_manage6
        self.safe_manage7=safe_manage7
        self.safe_manage8=safe_manage8
        self.safe_manage9=safe_manage9
        self.safe_manage10=safe_manage10
        self.safe_manage11=safe_manage11
        self.safe_manage12=safe_manage12
        self.safe_manage13=safe_manage13
        self.deposit_demand=deposit_demand
        self.water_electric_bill_demand=water_electric_bill_demand
        self.environment=environment
        self.environment_description=environment_description
        self.facility=facility


@app.route("/visit")
def hello():
    
    return render_template("visit.html")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 確保資料庫被創建
    app.debug = True
    app.run()
