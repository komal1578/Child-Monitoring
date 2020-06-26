from datetime import datetime
from flask import request, render_template, redirect, url_for, session
from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.FeedbackDAO import FeedbackDAO
from project.com.vo.FeedbackVO import FeedbackVO


@app.route( '/user/loadFeedback', methods=['GET'] )
def userLoadFeedback():
    try:
        return render_template( 'user/addFeedback.html' )
    except Exception as ex:
        print( ex )


@app.route( '/user/insertFeedback', methods=['POST'] )
def userInsertFeedback():
    try:
        feedbackSubject = request.form['feedbackSubject']
        feedbackDescription = request.form['feedbackDescription']
        feedbackRating = request.form['feedbackRating']

        feedbackVO = FeedbackVO()
        feedbackDAO = FeedbackDAO()

        todayDate = str( datetime.now().date() )
        timeNow = datetime.now().strftime( "%H:%M:%S" )

        feedbackVO.feedbackSubject = feedbackSubject
        feedbackVO.feedbackDescription = feedbackDescription
        feedbackVO.feedbackRating = feedbackRating
        feedbackVO.feedbackDate = todayDate
        feedbackVO.feedbackTime = timeNow
        feedbackVO.feedbackFrom_LoginId = session['session_loginId']

        feedbackDAO.insertFeedback( feedbackVO )

        return redirect( url_for( 'userViewFeedback' ) )

    except Exception as ex:
        print( ex )


@app.route( '/user/viewFeedback' )
def userViewFeedback():
    try:
        feedbackDAO = FeedbackDAO()
        feedbackVO = FeedbackVO()

        feedbackFrom_LoginId = session['session_loginId']
        print(feedbackFrom_LoginId)
        feedbackVO.feedbackFrom_LoginId = feedbackFrom_LoginId
        print(feedbackVO.feedbackFrom_LoginId)
        feedbackVOList = feedbackDAO.viewFeedback( feedbackVO )
        print( "______________", feedbackVOList )

        return render_template( 'user/viewFeedback.html', feedbackVOList=feedbackVOList )

    except Exception as ex:
        print( ex )


@app.route( '/user/deleteFeedback' )
def userDeleteFeedback():
    try:
        feedbackVO = FeedbackVO()
        feedbackDAO = FeedbackDAO()

        feedbackId = request.args.get( "feedbackId" )

        feedbackVO.feedbackId = feedbackId

        feedbackDAO.deleteFeedback( feedbackVO )

        return redirect( url_for( 'userViewFeedback' ) )

    except Exception as ex:
        print( ex )


"""-------------------------------------admin_side_url_pattern--------------------------------------"""


@app.route('/admin/viewFeedback', methods=['GET'])
def adminViewFeedback():
    try:
        if adminLoginSession() == 'admin':
            feedbackDAO = FeedbackDAO()

            feedbackVOList = feedbackDAO.adminViewFeedback()

            print("__________________", feedbackVOList)

            return render_template('admin/viewFeedback.html', feedbackVOList=feedbackVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)

@app.route('/admin/reviewFeedback')
def adminReviewFeedback():
    try:
        if adminLoginSession() == 'admin':
            feedbackDAO = FeedbackDAO()
            feedbackVO = FeedbackVO()

            feedbackId = request.args.get('feedbackId')
            feedbackTo_LoginId = session['session_loginId']

            feedbackVO.feedbackId = feedbackId
            feedbackVO.feedbackTo_LoginId = feedbackTo_LoginId

            feedbackDAO.adminReviewFeedback(feedbackVO)

            return redirect(url_for('adminViewFeedback'))
        else:
            return redirect('/admin/logoutSession')
    except Exception as ex:
        print(ex)