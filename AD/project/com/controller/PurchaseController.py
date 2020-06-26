from flask import request, render_template, url_for, redirect,session
from project import app
from datetime import datetime, date
from project.com.vo.PurchaseVO import PurchaseVO
from project.com.dao.PurchaseDAO import PurchaseDAO
from project.com.vo.PackageVO import PackageVO
from project.com.dao.PackageDAO import PackageDAO


@app.route('/user/viewPackage')
def userViewPackage():
    try:
        packageDAO = PackageDAO()
        packageVOList = packageDAO.viewPackage()
        print("__________________", packageVOList)
        return render_template('user/viewPackage.html', packageVOList=packageVOList)
    except Exception as ex:
        print(ex)


@app.route('/user/insertPurchase', methods=['post'])
def userInsertpurchase():
    try:
        print( ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        packageVO = PackageVO()
        purchaseDate = date.today()
        purchaseTime = datetime.now().strftime("%H:%M:%S")


        packageId = request.form['packageId']
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",packageId)
        purchaseVO = PurchaseVO()
        purchaseDAO = PurchaseDAO()

        purchaseVO.purchaseDate = purchaseDate
        purchaseVO.purchaseTime = purchaseTime
        purchaseVO.purchase_PackageId = packageId
        purchaseVO.purchase_LoginId = session['session_loginId']

        purchaseDAO.insertPurchase(purchaseVO)

        return redirect(url_for('userViewPurchase'))
    except Exception as ex:
        print(ex)

# @app.route('/user/viewPurchase', methods=['GET'])
# def userViewPurchase():
#     try:
#         print(">>>>>>>>>>>>>>>>>>>viewPurchase")
#         purchaseVO = PurchaseVO()
#         purchaseDAO = PurchaseDAO()
#
#         purchaseId = request.args.get('purchaseId')
#         print(">>>>>>>>>>>>>>>>>>>viewPurchase", purchaseId)
#         purchaseVO.purchaseId = purchaseId
#         purchaseVOList = purchaseDAO.viewUserPurchase(purchaseVO)
#         print(">>>>>>>>>>>>>>>>>>>viewPurchase", purchaseVOList)
#     except Exception as ex:
#         print(ex)

@app.route('/user/viewPurchase', methods=['GET'])
def userViewPurchase():
    try:
        purchaseDAO = PurchaseDAO()
        purchaseVO = PurchaseVO()

        purchaseVO.purchase_LoginId = session['session_loginId']
        purchaseVOList = purchaseDAO.viewUserPurchase(purchaseVO)
        print("__________________", purchaseVOList)
        return render_template('user/viewPurchase.html', purchaseVOList=purchaseVOList)

    except Exception as ex:
        print(ex)
