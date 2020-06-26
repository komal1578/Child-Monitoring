import os
from datetime import datetime, date
from flask import render_template, request, session, redirect, url_for
from werkzeug.utils import secure_filename
from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.ComplainDAO import ComplainDAO
from project.com.vo.ComplainVO import ComplainVO


@app.route( '/admin/viewComplain', methods=['GET'] )
def adminViewComplain():
    try:
        if adminLoginSession() == 'admin':

            complainDAO = ComplainDAO()
            adminComplainVOList = complainDAO.adminViewComplain()

            return render_template( 'admin/viewComplain.html', adminComplainVOList=adminComplainVOList )
        else:
            return adminLogoutSession()
    except Exception as ex:
        print( ex )


@app.route( '/admin/loadComplainReply', methods=['GET'] )
def adminLoadComplainReply():
    try:
        if adminLoginSession() == 'admin':
            complainVO = ComplainVO()
            complainId = request.args.get( "complainId" )
            complainVO.complainId = complainId

            return render_template( 'admin/addComplainReply.html', complainId=complainVO.complainId )
        else:
            return adminLogoutSession()

    except Exception as ex:
        print( ex )


@app.route( '/admin/insertComplainReply', methods=['POST'] )
def adminInsertComplainReplay():
    try:
        if adminLoginSession() == 'admin':
            UPLOAD_FOLDER2 = 'project/static/adminResource/reply/'
            app.config['UPLOAD_FOLDER2'] = UPLOAD_FOLDER2
            print( UPLOAD_FOLDER2 )

            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            complainId = request.form['complainId']
            replySubject = request.form['replySubject']
            replyMessage = request.form['replyMessage']
            replyFile = request.files['replyFile']

            print( ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>for_Check", complainId, replySubject, replyMessage )

            now = datetime.now()
            replyDate = now.date()
            replyTime = now.strftime( "%H:%M:%S" )

            replyFileName = secure_filename( replyFile.filename )
            replyFilePath = os.path.join( app.config['UPLOAD_FOLDER2'] )

            replyFile.save( os.path.join( replyFilePath, replyFileName ) )
            print( ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Done" )

            complainVO.complainId = complainId
            complainVO.replySubject = replySubject
            complainVO.replyMessage = replyMessage
            complainVO.replyFileName = replyFileName
            complainVO.replyFilePath = replyFilePath.replace( "project", ".." )
            complainVO.replyDate = replyDate
            complainVO.replyTime = replyTime
            complainVO.complainTo_LoginId = session['session_loginId']
            complainVO.complainStatus = 'replied'

            complainDAO.adminInsertReply( complainVO )

            return redirect( url_for( 'adminViewComplain' ) )
        else:
            return adminLogoutSession()

    except Exception as ex:
        print( ex )


"""--------------------------------------UserSide_Url_Pattern------------------------------------"""


@app.route( '/user/loadComplain' )
def userLoadComplain():
    try:
        return render_template( 'user/addComplain.html' )
    except Exception as ex:
        print( ex )


@app.route( '/user/insertComplain', methods=['POST'] )
def userInsertComplain():
    try:
        UPLOAD_FOLDER1 = 'project/static/adminResource/complain/'
        app.config['UPLOAD_FOLDER1'] = UPLOAD_FOLDER1

        complainSubject = request.form['complainSubject']
        complainDescription = request.form['complainDescription']
        complainfile = request.files['complainfile']

        print( complainSubject, complainDescription )

        now = datetime.now()
        complainDate = date.today()
        complainTime = now.strftime( "%H:%M:%S" )

        complainFileName = secure_filename( complainfile.filename )

        complainFilePath = os.path.join( app.config['UPLOAD_FOLDER1'] )

        complainfile.save( os.path.join( complainFilePath, complainFileName ) )

        complainVO = ComplainVO()
        complainDAO = ComplainDAO()

        complainVO.complainSubject = complainSubject
        complainVO.complainDescription = complainDescription
        complainVO.complainDate = complainDate
        complainVO.complainTime = complainTime
        complainVO.complainStatus = "Pending"
        complainVO.complainFileName = complainFileName
        complainVO.complainFilePath = complainFilePath.replace( "project", ".." )
        complainVO.complainFrom_LoginId = session['session_loginId']

        complainDAO.insertComplain( complainVO )

        return redirect( url_for( 'userViewComplain' ) )
    except Exception as ex:
        print( ex )


@app.route( '/user/viewComplain', methods=['GET'] )
def userViewComplain():
    try:
        complainDAO = ComplainDAO()
        complainFrom_LoginId = session['session_loginId']
        complainVOList = complainDAO.viewComplain( complainFrom_LoginId )
        return render_template( 'user/viewComplain.html', complainVOList=complainVOList )
    except Exception as ex:
        print( ex )


@app.route( '/user/deleteComplain', methods=['GET'] )
def userDeleteComplain():
    try:
        complainDAO = ComplainDAO()
        complainId = request.args.get( 'complainId' )
        complainList = complainDAO.deleteComplain( complainId )

        userFilePath = complainList.complainFilePath.replace( "..", "project" ) + complainList.complainFileName
        os.remove( userFilePath )

        print( "status", complainList.complainStatus )

        if complainList.complainStatus == "Replied":
            adminFilePath = complainList.replyFilePath.replace( "..", "project" ) + complainList.replyFileName
            print( "File....", adminFilePath )
            os.remove( adminFilePath )

        return redirect( url_for( 'userViewComplain' ) )

    except Exception as ex:
        print( ex )


@app.route( '/user/viewComplainReply', methods=['GET'] )
def viewComplainReply():
    try:
        complainVO = ComplainVO()
        complainDAO = ComplainDAO()

        complainId = request.args.get( "complainId" )

        print( ">>>>>>>>>>>>>>>>>>>", complainId )

        complainVO.complainId = complainId

        complainReplyVOList = complainDAO.viewComplainReply( complainVO )

        print( ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", complainReplyVOList )
        return render_template( 'user/viewComplainReply.html', complainReplyVOList=complainReplyVOList )

    except Exception as ex:
        print( ex )
