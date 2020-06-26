from project import db
from project.com.vo.LoginVO import LoginVO


class ComplainVO(db.Model):
    __tablename__ = 'complainmaster'
    complainId = db.Column('complainId', db.Integer, primary_key=True, autoincrement=True)
    complainSubject = db.Column('complainSubject', db.String(100), nullable=False)
    complainDescription = db.Column('complainDescription', db.String(100), nullable=False)
    complainDate = db.Column('complainDate', db.DATE, nullable=False)
    complainTime = db.Column('complainTime', db.String(100), nullable=False)
    complainStatus = db.Column('complainStatus', db.String(100), nullable=False)
    complainFileName = db.Column('complainFileName', db.String(100))
    complainFilePath = db.Column('complainFilePath', db.String(100))
    complainTo_LoginId = db.Column('complainTo_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))
    complainFrom_LoginId = db.Column('complainFrom_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))
    replySubject = db.Column('replySubject', db.String(100))
    replyMessage = db.Column('replyMessage', db.String(100))
    replyFileName = db.Column('replyFileName', db.String(100))
    replyFilePath = db.Column('replyFilePath', db.String(100))
    replyDate = db.Column('replyDate', db.DATE)
    replyTime = db.Column('replyTime', db.String(100))

    def as_dict(self):
        return {
            'complainId': self.complainId,
            'complainSubject': self.complainSubject,
            'complainDescription': self.complainDescription,
            'complainDate': self.complainDate,
            'complainTime': self.complainTime,
            'complainStatus': self.complainStatus,
            'complainFileName': self.complainFileName,
            'complainFilePath': self.complainFilePath,
            'complainTo_LoginId': self.complainTo_LoginId,
            'complainFrom_LoginId': self.complainFrom_LoginId,
            'replySubject': self.replySubject,
            'replyMessage': self.replyMessage,
            'replyFileName': self.replyFileName,
            'replyFilePath': self.replyFilePath,
            'replyDate': self.replyDate,
            'replyTime': self.replyTime,

        }


db.create_all()
