from project.com.vo.LoginVO import LoginVO
from project import db

class LoginDAO:
    def validateLogin(self, loginVO):
        loginList = LoginVO.query.filter_by(loginUsername=loginVO.loginUsername, loginPassword=loginVO.loginPassword)

        return loginList

    def insertLogin(self, loginVO):
        db.session.add( loginVO )
        db.session.commit()

    def viewLogin(self, loginVO):
        loginList = LoginVO.query.filter_by( loginId=loginVO.loginId ).all()
        return loginList

    def adminUpdateUser(self, loginVO):
        db.session.merge(loginVO)
        db.session.commit()

    def validateLoginUsername(self, loginVO):
        loginList = LoginVO.query.filter_by( loginUsername=loginVO.loginUsername ).all()
        return loginList
