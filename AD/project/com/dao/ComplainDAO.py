from project import db
from project.com.vo.ComplainVO import ComplainVO
from project.com.vo.LoginVO import LoginVO
from sqlalchemy import func

class ComplainDAO:
    def insertComplain(self, complainVO):
        db.session.add(complainVO)
        db.session.commit()

    def viewComplain(self, complainFrom_LoginId):
        complainList = db.session.query(ComplainVO).filter(ComplainVO.complainFrom_LoginId == complainFrom_LoginId)

        return complainList

    def adminViewComplain(self):
        print('fggsthsjjjk')
        adminComplainList = db.session.query(ComplainVO, LoginVO)\
            .join(LoginVO,ComplainVO.complainFrom_LoginId == LoginVO.loginId)\
            .all()
        print('sgdjjjdyjfgnfgn,', adminComplainList)
        return adminComplainList

    def deleteComplain(self, complainId):
        complainList = ComplainVO.query.get(complainId)
        db.session.delete(complainList)
        db.session.commit()

        return complainList

    def adminInsertReply(self, complainVO):
        db.session.merge(complainVO)
        db.session.commit()

    def viewComplainReply(self, complainVO):
        complainReplyList = ComplainVO.query.filter_by(complainId=complainVO.complainId)
        return complainReplyList

    def complainCount(self):
        complainList = db.session.query(func.count(ComplainVO.complainId)).all()

        return complainList
