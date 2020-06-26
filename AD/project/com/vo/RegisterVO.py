from project import db
from project.com.vo.LoginVO import LoginVO


class RegisterVO( db.Model ):
    __tablename__ = 'registermaster'
    registerId = db.Column( 'registerId', db.Integer, primary_key=True, autoincrement=True )
    registerFirstname = db.Column( 'registerFirstname', db.String( 100 ), nullable=False )
    registerLastname = db.Column( 'registerLastname', db.String( 100 ), nullable=False )
    registerGender = db.Column( 'registerGender', db.String( 10 ), nullable=False )
    registerAddress = db.Column( 'registerAddress', db.String( 100 ), nullable=False )
    registerContactNumber = db.Column( 'registerContactNumber', db.BIGINT, nullable=False )
    register_LoginId = db.Column( 'register_LoginId', db.Integer, db.ForeignKey( LoginVO.loginId ) )

    def as_dict(self):
        return {
            'registerId': self.registerId,
            'registerFirstname': self.registerFirstname,
            'registerLastname': self.registerLastname,
            'registerGender': self.registerGender,
            'registerAddress': self.registerAddress,
            'registerContactNumber': self.registerContactNumber,
            'register_LoginId': self.register_LoginId
        }


db.create_all()
