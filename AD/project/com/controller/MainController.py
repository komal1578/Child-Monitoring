from flask import render_template
from project import app
from project.com.dao.RegisterDAO import RegisterDAO
from project.com.dao.LoginDAO import LoginDAO

from project.com.controller.LoginController import adminLoginSession, adminLogoutSession


@app.route( '/admin/viewUser' )
def adminViewUser():
    try:
        if adminLoginSession() == 'admin':
            registerDAO = RegisterDAO()
            registerVOList = registerDAO.viewRegister()
            return render_template( 'admin/viewUser.html', registerVOList=registerVOList )
        else:
            return adminLogoutSession()
    except Exception as ex:
        print( ex )
