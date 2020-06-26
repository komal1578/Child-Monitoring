from project import db
from project.com.vo.PackageVO import PackageVO
from project.com.vo.LoginVO import LoginVO


class PurchaseVO(db.Model):
    __tablename__ = 'purchasemaster'
    purchaseId = db.Column('purchaseId', db.Integer, primary_key=True, autoincrement=True)
    purchaseDate = db.Column('purchaseDate', db.DATE, nullable=False)
    purchaseTime = db.Column('purchaseTime', db.TIME, nullable=False)
    purchase_PackageId = db.Column('purchase_PackageId', db.Integer, db.ForeignKey(PackageVO.packageId))
    purchase_LoginId = db.Column('purchase_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))

    def as_dict(self):
        return {
            'purchaseId': self.purchaseId,
            'purchaseDate': self.purchaseDate,
            'purchaseTime': self.purchaseTime,
            'purchase_LoginId': self.purchase_LoginId,
            'purchase_PackageId': self.purchase_PackageId
            }

db.create_all()
