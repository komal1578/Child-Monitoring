from flask import request, render_template, url_for, redirect
from project import app
from project.com.dao.PackageDAO import PackageDAO
from project.com.vo.PackageVO import PackageVO
from project.com.controller.LoginController import adminLoginSession,adminLogoutSession



@app.route('/admin/loadPackage')
def adminLoadPackage():
    try:
        if adminLoginSession() == 'admin':
            return render_template('admin/addPackage.html')
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/insertPackage', methods=['post'])
def adminInsertPackage():
    try:
        if adminLoginSession() == 'admin':
            packageName = request.form['packageName']
            packageDuration = request.form['packageDuration']
            packagePrice = request.form['packagePrice']

            packageVO = PackageVO()
            packageDAO = PackageDAO()

            packageVO.packageName = packageName
            packageVO.packageDuration = packageDuration
            packageVO.packagePrice = packagePrice

            packageDAO.insertPackage(packageVO)

            return redirect(url_for('adminViewPackage'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/viewPackage')
def adminViewPackage():
    try:
        if adminLoginSession() == 'admin':
            packageDAO = PackageDAO()
            packageVOList = packageDAO.viewPackage()
            print("__________________", packageVOList)
            return render_template('admin/viewPackage.html', packageVOList=packageVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/deletePackage')
def adminDeletePackage():
    try:
        if adminLoginSession() == 'admin':
            packageVO = PackageVO()

            packageDAO = PackageDAO()

            packageId = request.args.get('packageId')

            packageVO.packageId = packageId

            packageDAO.deletePackage(packageVO)

            return redirect(url_for('adminViewPackage'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/admin/editPackage')
def adminEditPackage():
    try:
        if adminLoginSession() == 'admin':
            packageVO = PackageVO()

            packageDAO = PackageDAO()

            packageId = request.args.get('packageId')

            packageVO.packageId = packageId

            packageVOList = packageDAO.editPackage(packageVO)

            print("=======packageVOList=======", packageVOList)

            print("=======type of packageVOList=======", type(packageVOList))

            return render_template('admin/editPackage.html', packageVOList=packageVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/updatePackage', methods=['post'])
def adminUpdatePackage():
    try:
        if adminLoginSession() == 'admin':
            packageId = request.form['packageId']
            packageName = request.form['packageName']
            packageDuration = request.form['packageDuration']
            packagePrice = request.form['packagePrice']

            print(packageId, packageName, packageDuration, packagePrice)

            packageVO = PackageVO()
            packageDAO = PackageDAO()

            packageVO.packageId = packageId
            packageVO.packageName = packageName
            packageVO.packageDuration = packageDuration
            packageVO.packagePrice = packagePrice

            packageDAO.updatePackage(packageVO)
        else:
            return adminLogoutSession()

        return redirect(url_for('adminViewPackage'))
    except Exception as ex:
        print(ex)
