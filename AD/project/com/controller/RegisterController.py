import random
import smtplib
import string
from project import app
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import render_template, request,session,redirect,url_for
from project.com.vo.LoginVO import LoginVO
from project.com.dao.LoginDAO import LoginDAO
from project.com.dao.RegisterDAO import RegisterDAO
from project.com.vo.RegisterVO import RegisterVO
from project.com.controller.LoginController import adminLoginSession
from project.com.controller.LoginController import adminLogoutSession


@app.route( '/user/loadRegister' )
def userLoadRegister():
    try:
        return render_template( 'user/register.html' )
    except Exception as ex:
        print( ex )


@app.route( '/user/insertRegister', methods=['POST'] )
def userInsertRegister():
    try:
        loginVO = LoginVO()
        loginDAO = LoginDAO()

        registerVO = RegisterVO()
        registerDAO = RegisterDAO()

        loginUsername = request.form['loginUsername']
        loginPassword = ''.join( (random.choice( string.ascii_letters + string.digits )) for x in range( 8 ) )

        registerFirstname = request.form['registerFirstname']
        registerLastname = request.form['registerLastname']
        registerGender = request.form['registerGender']
        registerAddress = request.form['registerAddress']
        registerContactNumber = request.form['registerContactNumber']

        print( "loginPassword=" + loginPassword )

        sender = "spotteractivity@gmail.com"

        receiver = loginUsername

        msg = MIMEMultipart()

        msg['From'] = sender

        msg['To'] = receiver

        msg['Subject'] = "PYTHON PASSWORD"

        msg.attach( MIMEText( loginPassword, 'plain' ) )
        print( loginPassword, "loginpassword" )

        server = smtplib.SMTP( 'smtp.gmail.com', 587 )

        server.starttls()

        server.login( sender, "9925646618" )

        text = msg.as_string()

        server.sendmail( sender, receiver, text )

        loginVO.loginUsername = loginUsername
        loginVO.loginPassword = loginPassword
        loginVO.loginRole = "user"
        loginVO.loginStatus = "active"

        loginDAO.insertLogin( loginVO )

        registerVO.registerFirstname = registerFirstname
        registerVO.registerLastname = registerLastname
        registerVO.registerGender = registerGender
        registerVO.registerAddress = registerAddress
        registerVO.registerContactNumber = registerContactNumber
        registerVO.register_LoginId = loginVO.loginId

        registerDAO.insertRegister( registerVO )

        server.quit()

        return render_template("admin/login.html")

    except Exception as ex:
        print( ex )


@app.route('/user/editRegister', methods=['GET'])
def userEditRegister():
    try:
        if adminLoginSession() == 'user':
            loginId = session['session_loginId']

            registerVO = RegisterVO()
            registerDAO = RegisterDAO()

            registerVO.register_LoginId = loginId

            registerVOList = registerDAO.editProfile(registerVO)

            return render_template('user/editProfile.html', registerVOList=registerVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/updateRegister', methods=['POST'])
def userUpdateRegister():
    try:
        if adminLoginSession() == 'user':
            registerVO = RegisterVO()
            registerDAO = RegisterDAO()

            loginId = request.form['loginId']
            loginUsername = request.form['loginUsername']

            registerId = request.form['registerId']
            registerFirstname = request.form['registerFirstname']
            registerLastname = request.form['registerLastname']
            registerGender = request.form['registerGender']
            registerAddress = request.form['registerAddress']
            registerContactNumber = request.form['registerContactNumber']

            loginVO = LoginVO()
            loginDAO = LoginDAO()
            loginVO.loginId = loginId
            loginList = loginDAO.viewLogin(loginVO)

            if loginList[0].loginUsername == loginUsername:
                pass
            else:
                loginPassword = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))

                sender = "spotteractivity@gmail.com"

                receiver = loginUsername

                msg = MIMEMultipart()

                msg['From'] = sender

                msg['To'] = receiver

                msg['Subject'] = "ACCOUNT PASSWORD"

                msg.attach(MIMEText(loginPassword, 'plain'))

                server = smtplib.SMTP('smtp.gmail.com', 587)

                server.starttls()

                server.login(sender, "9925646618")

                text = msg.as_string()

                server.sendmail(sender, receiver, text)

                server.quit()

                loginVO.loginUsername = loginUsername
                loginVO.loginPassword = loginPassword

                loginDAO.adminUpdateUser(loginVO)

            registerVO.registerId = registerId
            registerVO.registerFirstname = registerFirstname
            registerVO.registerLastname = registerLastname
            registerVO.registerGender = registerGender
            registerVO.registerAddress = registerAddress
            registerVO.registerContactNumber = registerContactNumber

            registerDAO.updateRegister(registerVO)

            return redirect(url_for('userLoadDashboard'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)