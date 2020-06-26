from project import db
from project.com.vo.PurchaseVO import PurchaseVO
from project.com.vo.PackageVO import PackageVO
from project.com.vo.LoginVO import LoginVO


class PurchaseDAO:

    def insertPurchase(self, purchaseVO):
        db.session.add(purchaseVO)
        db.session.commit()

    # def viewUserPurchase(self):
    #     purchaseVOList = db.session.query(PurchaseVO, PackageVO)\
    #         .join(PackageVO,PackageVO.packageId == )\
    #         .join(PurchaseVO, LoginVO.loginId == PurchaseVO.purchase_LoginId)\
    #         .filter_by(PurchaseVO.purchase_PackageId == PackageVO.packageId).all()
    #     return purchaseVOList

    def viewUserPurchase(self, purchaseVO):
        print("---------",purchaseVO.purchase_LoginId)
        purchaseVOList = db.session.query(PurchaseVO, PackageVO, LoginVO).filter(PurchaseVO.purchase_LoginId == purchaseVO.purchase_LoginId).join(PackageVO, PackageVO.packageId == PurchaseVO.purchase_PackageId).join(LoginVO, LoginVO.loginId == PurchaseVO.purchase_LoginId).all()
        return purchaseVOList
