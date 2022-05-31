from datetime import datetime

from flask import request, render_template, redirect, url_for, session

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.FeedbackDAO import FeedbackDAO
from project.com.vo.FeedbackVO import FeedbackVO


@app.route('/admin/viewFeedback')
def adminViewFeedback():
    try:
        if adminLoginSession() == 'admin':
            feedbackVO = FeedbackVO()
            feedbackDAO = FeedbackDAO()

            feedbackVOList = feedbackDAO.adminViewFeedback()
            print("__________________", feedbackVOList)
            return render_template('admin/viewFeedback.html', feedbackVOList=feedbackVOList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/loadFeedback')
def userLoadFeedback():
    try:
        return render_template("user/addFeedback.html")
    except Exception as ex:
        print(ex)


@app.route('/user/insertFeedback', methods=['POST'])
def userInsertFeedback():
    try:
        if adminLoginSession() == 'user':
            feedbackVO = FeedbackVO()
            feedbackDAO = FeedbackDAO()

            feedbackVO.feedbackSubject = request.form['feedbackSubject']
            feedbackVO.feedbackDescription = request.form['feedbackDescription']
            feedbackVO.feedbackFrom_LoginId = session['session_loginId']
            feedbackVO.feedbackRating = request.form['rate']
            feedbackVO.feedbackDate = datetime.today()
            feedbackVO.feedbackTime = datetime.now().strftime('%H:%M:%S')
            feedbackDAO.insertFeedback(feedbackVO)

            return redirect(url_for('userViewFeedback'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/viewFeedback')
def userViewFeedback():
    try:
        if adminLoginSession() == 'user':
            feedbackVO = FeedbackVO()
            feedbackDAO = FeedbackDAO()

            feedbackFrom_LoginId = session['session_loginId']
            feedbackVO.feedbackFrom_LoginId = feedbackFrom_LoginId

            feedbackVOList = feedbackDAO.viewFeedback(feedbackVO)
            print("__________________", feedbackVOList)
            return render_template('user/viewFeedback.html', feedbackVOList=feedbackVOList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/deleteFeedback', methods=['GET'])
def userDeleteFeedback():
    try:
        if adminLoginSession() == 'user':

            feedbackVO = FeedbackVO()
            feedbackDAO = FeedbackDAO()
            feedbackId = request.args.get('feedbackId')

            feedbackVO.feedbackId = feedbackId

            feedbackDAO.deleteFeedback(feedbackVO)
            return redirect(url_for('userViewFeedback'))
        else:
            adminLogoutSession()
    except Exception as ex:
        print(ex)

@app.route('/admin/reviewFeedback')
def adminReviewFeedback():
    try:
        if adminLoginSession() == 'admin':
            feedbackDAO=FeedbackDAO()
            feedbackVO=FeedbackVO()
            feedbackVO.feedbackId=request.args.get("feedbackId")
            feedbackVO.feedbackTo_LoginId=session['session_loginId']
            feedbackDAO.updateFeedback(feedbackVO)


            return redirect(url_for("adminViewFeedback"))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
