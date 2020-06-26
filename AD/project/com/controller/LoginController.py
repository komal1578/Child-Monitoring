import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import request, render_template, url_for, redirect, session
from project import app
from project.com.dao.ComplainDAO import ComplainDAO
from project.com.dao.FeedbackDAO import FeedbackDAO
from project.com.dao.LoginDAO import LoginDAO
from project.com.dao.RegisterDAO import RegisterDAO
from project.com.vo.ComplainVO import ComplainVO
from project.com.vo.FeedbackVO import FeedbackVO
from project.com.vo.LoginVO import LoginVO


@app.route( '/', methods=['GET'] )
def adminLoadLogin():
    print( "in login" )
    session.clear()
    return render_template( 'admin/login.html' )


@app.route( "/admin/validateLogin", methods=['POST'] )
def adminValidateLogin():
    try:
        loginUsername = request.form['loginUsername']
        loginPassword = request.form['loginPassword']

        loginVO = LoginVO()
        loginDAO = LoginDAO()

        loginVO.loginUsername = loginUsername
        loginVO.loginPassword = loginPassword
        loginVO.loginStatus = "active"

        loginVOList = loginDAO.validateLogin( loginVO )

        loginDictList = [i.as_dict() for i in loginVOList]

        print( loginDictList )

        lenLoginDictList = len( loginDictList )

        if lenLoginDictList == 0:

            msg = 'Username Or Password is Incorrect !'

            return render_template( 'admin/login.html', error=msg )

        elif loginDictList[0]['loginStatus'] == "inactive":

            blockmsg = 'User is temporary blocked by Website Admin !'

            return render_template( 'admin/login.html', errorblock=blockmsg )

        else:

            for row1 in loginDictList:

                loginId = row1['loginId']

                loginUsername = row1['loginUsername']

                loginRole = row1['loginRole']

                session['session_loginId'] = loginId

                session['session_loginUsername'] = loginUsername

                session['session_loginRole'] = loginRole

                session.permanent = True

                if loginRole == 'admin':
                    return redirect( url_for( 'adminLoadDashboard' ) )
                elif loginRole == 'user':
                    return redirect( url_for( 'userLoadDashboard' ) )
                else:
                    return render_template( 'admin/login.html' )
    except Exception as ex:
        print( ex )


@app.route( '/admin/loadDashboard', methods=['GET'] )
def adminLoadDashboard():
    try:
        if adminLoginSession() == 'admin':
            complainCount = 0
            feedbackCount = 0
            userCount = 0

            complainDAO = ComplainDAO()
            complainList = complainDAO.complainCount()
            print( 'complainList>>>>>', complainList )
            complainCount = complainList[0][0]

            feedbackDAO = FeedbackDAO()
            feedbackList = feedbackDAO.adminViewFeedback()
            feedbackCount = len( feedbackList )

            registerDAO = RegisterDAO()
            registerList = registerDAO.viewRegister()
            userCount = len( registerList )

            return render_template( 'admin/index.html', complainCount=complainCount, feedbackCount=feedbackCount,
                                    userCount=userCount )
        else:
            return adminLogoutSession()
    except Exception as ex:
        print( ex )


@app.route( '/user/loadDashboard', methods=['GET'] )
def userLoadDashboard():
    try:
        if adminLoginSession() == 'user':
            pendingComplainCount = 0
            repliedComplainCount = 0

            loginID = session['session_loginId']
            complainDAO = ComplainDAO()

            complainList = complainDAO.viewComplain( loginID )
            print( 'complainList>>>>>', complainList )

            for i in complainList:
                if i.complainStatus == 'replied':
                    repliedComplainCount += 1
                elif i.complainStatus == 'Pending':
                    pendingComplainCount += 1

            feedbackVO = FeedbackVO()
            feedbackDAO = FeedbackDAO()
            feedbackVO.feedbackFrom_LoginId = loginID
            feedbackList = feedbackDAO.viewFeedback( feedbackVO )
            feedbackCount = len( feedbackList )

            return render_template( 'user/index.html', pendingComplainCount=pendingComplainCount,
                                    repliedComplainCount=repliedComplainCount, feedbackCount=feedbackCount )
        else:
            return adminLogoutSession()
    except Exception as ex:
        print( ex )


@app.route( '/admin/loginSession' )
def adminLoginSession():
    try:
        if 'session_loginId' and 'session_loginRole' in session:

            if session['session_loginRole'] == 'admin':

                return 'admin'


            elif session['session_loginRole'] == 'user':

                return 'user'

            print( "<<<<<<<<<<<<<<<<True>>>>>>>>>>>>>>>>>>>>" )

        else:

            print( "<<<<<<<<<<<<<<<<False>>>>>>>>>>>>>>>>>>>>" )

            return False

    except Exception as ex:
        print( ex )


@app.route( "/admin/logoutSession", methods=['GET'] )
def adminLogoutSession():
    session.clear()

    return redirect( url_for( 'adminLoadLogin' ) )


@app.route( '/admin/blockUser' )
def adminBlockUser():
    try:
        if adminLoginSession() == 'admin':
            loginDAO = LoginDAO()
            loginVO = LoginVO()

            loginId = request.args.get( 'loginId' )
            loginStatus = 'inactive'

            loginVO.loginId = loginId
            loginVO.loginStatus = loginStatus

            loginDAO.adminUpdateUser( loginVO )

            return redirect( url_for( 'adminViewUser' ) )
        else:
            return adminLogoutSession()
    except Exception as ex:
        print( ex )


@app.route( '/admin/unblockUser' )
def adminUnblockUser():
    try:
        if adminLoginSession() == 'admin':
            loginDAO = LoginDAO()
            loginVO = LoginVO()

            loginId = request.args.get( 'loginId' )
            loginStatus = 'active'

            loginVO.loginId = loginId
            loginVO.loginStatus = loginStatus

            loginDAO.adminUpdateUser( loginVO )

            return redirect( url_for( 'adminViewUser' ) )
        else:
            return adminLogoutSession()
    except Exception as ex:
        print( ex )


@app.route( '/user/loadForgetPassword' )
def userLoadForgetPassword():
    try:
        return render_template( 'user/forgetPassword.html' )
    except Exception as ex:
        print( ex )


@app.route( '/user/generateOTP', methods=['POST'] )
def userGenerateOTP():
    try:
        loginDAO = LoginDAO()
        loginVO = LoginVO()

        loginUsername = request.form['loginUsername']
        loginVO.loginUsername = loginUsername

        loginDictList = [i.as_dict() for i in loginDAO.validateLoginUsername( loginVO )]

        if len( loginDictList ) != 0:
            passwordOTP = ''.join( (random.choice( string.digits )) for x in range( 4 ) )

            session['session_OTP'] = passwordOTP
            session['session_loginUsername'] = loginUsername
            session['session_loginId'] = loginDictList[0]['loginId']

            sender = "spotteractivity@gmail.com"

            receiver = loginUsername

            msg = MIMEMultipart()

            msg['From'] = sender

            msg['To'] = receiver

            msg['subject'] = "ACCOUNT PASSWORD"

            msg.attach( MIMEText( 'OTP to reset password is:' ) )

            msg.attach( MIMEText( passwordOTP, 'plain' ) )

            server = smtplib.SMTP( 'smtp.gmail.com', 587 )

            server.starttls()

            server.login( sender, "9925646618" )

            text = msg.as_string()

            server.sendmail( sender, receiver, text )

            server.quit()

            return render_template( 'user/addOTP.html' )

        else:
            error = "The given Username is not registered yet!"
            return render_template( "admin/login.html", error=error )

    except Exception as ex:
        print( ex )


@app.route( '/user/validateOTP', methods=['POST'] )
def userValidateOTP():
    try:
        passwordOTP = request.form['passwordOTP']

        if passwordOTP == session['session_OTP']:

            loginPassword = ''.join( (random.choice( string.ascii_letters + string.digits )) for x in range( 8 ) )

            loginUsername = session['session_loginUsername']

            sender = "spotteractivity@gmail.com"

            receiver = loginUsername

            msg = MIMEMultipart()

            msg['From'] = sender

            msg['To'] = receiver

            msg['subject'] = "Reset Password"

            msg.attach( MIMEText( 'Your new Password is:' ) )

            msg.attach( MIMEText( loginPassword, 'plain' ) )

            server = smtplib.SMTP( 'smtp.gmail.com', 587 )

            server.starttls()

            server.login( sender, "9925646618" )

            text = msg.as_string()

            server.sendmail( sender, receiver, text )

            server.quit()

            loginVO = LoginVO()
            loginDAO = LoginDAO()

            loginVO.loginUsername = loginUsername
            loginVO.loginId = session['session_loginId']
            loginVO.loginPassword = loginPassword

            loginDAO.adminUpdateUser( loginVO )

            return render_template( "admin/login.html", error="Your new password is sent to your email address!" )
        else:
            return render_template( 'admin/login.html', error="Invalid OTP,Please ty again!" )

    except Exception as ex:
        print( ex )


@app.route( '/user/loadResetPassword' )
def userLoadResetPassword():
    try:
        if adminLoginSession() == 'user':
            return render_template( 'user/resetPassword.html' )
        else:
            return redirect( url_for( "adminLogoutSession" ) )

    except Exception as ex:
        print( ex )


@app.route( '/user/resetPassword', methods=['POST'] )
def userResetPassword():
    try:
        if adminLoginSession() == 'user':
            oldLoginPassword = request.form['oldLoginPassword']
            newLoginPassword = request.form['newLoginPassword']
            confirmNewLoginPassword = request.form['confirmNewLoginPassword']

            loginVO = LoginVO()
            loginDAO = LoginDAO()

            loginVO.loginId = session['session_loginId']
            print( loginVO.loginId )
            loginVO.loginUsername = session['session_loginUsername']
            print( loginVO.loginUsername )
            loginVO.loginPassword = oldLoginPassword
            print( loginVO.loginPassword )

            loginDictList = [i.as_dict() for i in loginDAO.validateLogin( loginVO )]
            print( loginDictList )

            if len( loginDictList ) != 0:
                print( [i.as_dict() for i in loginDAO.validateLogin( loginVO )] )
                if newLoginPassword == confirmNewLoginPassword:
                    loginVO.loginPassword = newLoginPassword
                    loginDAO.adminUpdateUser( loginVO )
                    return render_template( "user/index.html" )
                else:
                    return render_template( 'user/resetPassword.html',
                                            error="Invalid confirmation of new password,Please try again!" )
            else:
                return render_template( 'user/resetPassword.html',
                                        error="Invalid old password,please enter valid Password!" )

        else:
            return redirect( url_for( "adminLogoutSession" ) )

    except Exception as ex:
        print( ex )
