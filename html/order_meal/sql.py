from flask_sqlalchemy import SQLAlchemy
class tool_score(db.Model):
    __bind_key__ ='tool' 
    __tablename__ = 'meal'
    Id = db.Column(db.Integer, primary_key=True)
    meal = db.Column(db.String(256),nullable=False)
    address = db.Column(db.String(256))
    def __init__(self , meal,address):
        self.meal = meal
        self.address = address