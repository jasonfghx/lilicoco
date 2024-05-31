from extensions import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(256), primary_key=True, comment='使用者ID')
    passwd = db.Column(db.String(256), unique=False, nullable=False, comment='使用者密碼')
    name = db.Column(db.String(256), unique=False, nullable=False, comment='使用者名稱')
    email = db.Column(db.String(256), unique=False, nullable=False, comment='使用者信箱')
    tel = db.Column(db.String(256), unique=False, nullable=True, comment='使用者電話')
    type = db.Column(db.String(256), comment='使用者類別：管理員、導師、學生、房東')

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

class Administrator(User):
    __tablename__ = 'administrator'
    id = db.Column(db.String(256), db.ForeignKey('user.id'), primary_key=True, comment='管理員ID')

    __mapper_args__ = {
        'polymorphic_identity': 'administrator'
    }

class Advisor(User):
    __tablename__ = 'advisor'
    id = db.Column(db.String(256), db.ForeignKey('user.id'), primary_key=True, comment='導師ID')
    dept = db.Column(db.String(256), unique=False, nullable=False, comment='導師所屬系所')
    rank = db.Column(db.String(256), unique=False, nullable=False, comment='導師職級：教授、副教授、助理教授')
    office_addr = db.Column(db.String(256), unique=False, nullable=False, comment='導師辦公室位址')
    office_tel = db.Column(db.String(256), unique=False, nullable=False, comment='導師辦公室電話')

    __mapper_args__ = {
        'polymorphic_identity': 'advisor'
    }

class Student(User):
    __tablename__ = 'student'
    id = db.Column(db.String(256), db.ForeignKey('user.id'), primary_key=True, comment='學生學號')
    dept = db.Column(db.String(256), unique=False, nullable=False, comment='學生所屬系所')
    enroll_year = db.Column(db.Integer, unique=False, nullable=False, comment='學生入學年分')
    sex = db.Column(db.Boolean, unique=False, nullable=True, comment='學生性別')
    home_addr = db.Column(db.String(256), unique=False, nullable=True, comment='學生家中地址')
    home_tel = db.Column(db.String(256), unique=False, nullable=True, comment='學生家裡電話')
    contact_name = db.Column(db.String(256), unique=False, nullable=True, comment='家裡聯絡人姓名')
    contact_tel = db.Column(db.String(256), unique=False, nullable=True, comment='家裡聯絡人電話')
    advisor_id = db.Column(db.String(256), db.ForeignKey('advisor.id'), unique=False, nullable=False, comment='學生的導師')

    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }

class Landlord(User):
    __tablename__ = 'landlord'
    id = db.Column(db.String(256), db.ForeignKey('user.id'), primary_key=True, comment='房東ID')

    __mapper_args__ = {
        'polymorphic_identity': 'landlord'
    }

#訪視紀錄
class VisitRecord(db.Model):
    __tablename__ = 'visit_record'
    id = db.Column(db.String(256), db.ForeignKey('student.id'), primary_key=True, comment='學生學號')
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

# 住宿資料
class AccommodationInfo(db.Model):
    __tablename__ = 'accommodation_info'
    id = db.Column(db.String(256), db.ForeignKey('student.id'), primary_key=True, comment='學生學號')
    semester = db.Column(db.String(256), primary_key=True, comment='學年及學期')
    
    where_to_live = db.Column(db.Integer, unique=False, nullable=False, comment='住宿地。 0:住家裡 1:寄居親友家 2:住校 3:在外租屋')
    addr = db.Column(db.String(256), unique=False, nullable=True, comment='住宿地址')
    landlord_name = db.Column(db.String(256), unique=False, nullable=True, comment='房東姓名')
    landlord_tel = db.Column(db.String(256), unique=False, nullable=True, comment='房東電話')
    rent = db.Column(db.Integer, unique=False, nullable=True, comment='租金')
    roommate_id = db.Column(db.String(256), db.ForeignKey('student.id'), unique=False, nullable=True, comment='同住室友學號')
    


class Advertisement(db.Model):
    __tablename__ = 'advertisement'
    id = db.Column(db.Integer, primary_key=True, comment='租屋廣告編號')
    title = db.Column(db.String(256), unique=False, nullable=False, comment='租屋廣告標題')
    building_age = db.Column(db.Integer, unique=False, nullable=False ,comment='屋齡')
    building_type = db.Column(db.String(256), unique=False, nullable=False, comment='建物類型')
    addr = db.Column(db.String(256), unique=False, nullable=False, comment='地址')
    rental_limit = db.Column(db.String(256), unique=False, nullable=False, comment='限租條件')
    rent = db.Column(db.Integer, unique=False, nullable=False ,comment='月租金')
    image_urls = db.Column(db.Text, unique=False, nullable=True, comment='廣告圖檔路徑')
    pulish_date = db.Column(db.DateTime, unique=False, nullable=True, comment='刊登日期')
    due_date = db.Column(db.DateTime, unique=False, nullable=True, comment='截止日期')
    
    suite = db.Column(db.Integer, unique=False, nullable=False, comment='套房數量')
    room = db.Column(db.Integer, unique=False, nullable=False, comment='雅房數量')

    electricity_meter = db.Column(db.Boolean, unique=False, nullable=False, comment='有無獨立電表')
    smoke = db.Column(db.Boolean, unique=False, nullable=False, comment='無菸租屋')
    wash_machine = db.Column(db.Boolean, unique=False, nullable=False, comment='有無洗衣機')
    water_dispenser = db.Column(db.Boolean, unique=False, nullable=False, comment='有無飲水機')
    internet = db.Column(db.Boolean, unique=False, nullable=False, comment='有無網路')
    parking = db.Column(db.Boolean, unique=False, nullable=False, comment='有無停車位')
    air_con = db.Column(db.Boolean, unique=False, nullable=False, comment='有無冷氣')
    water_heater = db.Column(db.Boolean, unique=False, nullable=False, comment='有無熱水器')
    
    description = db.Column(db.Text, unique=False, nullable=True, comment='屋況簡述')
    timestamp = db.Column(db.DateTime, unique=False, nullable=False, comment='送出刊登請求的時間')
    status = db.Column(db.Integer, unique=False, nullable=False, comment='審核狀態。 0:待審核 1:通過 2:未通過')
    landlord_id = db.Column(db.String(10), db.ForeignKey('user.id'), unique=False, nullable=False, comment='房東ID')

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, comment='Po文編號')
    title = db.Column(db.String(50), unique=False, nullable=False, comment='Po文標題')
    text = db.Column(db.Text, unique=False, nullable=False, comment='Po文內容')
    timestamp = db.Column(db.DateTime, unique=False, nullable=False, comment='Po文時間')
    image_urls = db.Column(db.Text, unique=False, nullable=True, comment='Po文圖檔路徑')
    user_id = db.Column(db.String(10), db.ForeignKey('user.id'), unique=False, nullable=False, comment='Po文者ID')

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, comment='留言編號')
    text = db.Column(db.Text, unique=False, nullable=False, comment='留言內容')
    timestamp = db.Column(db.DateTime, unique=False, nullable=False, comment='留言時間')
    image_urls = db.Column(db.Text, unique=False, nullable=True, comment='留言圖檔路徑')
    user_id = db.Column(db.String(256), db.ForeignKey('user.id'), unique=False, nullable=False, comment='留言者ID')
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), unique=False, nullable=False, comment='文章ID')