import os
from datetime import datetime

from flask import request, render_template, redirect, url_for, session
from werkzeug.utils import secure_filename

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.ComplainDAO import ComplainDAO
from project.com.vo.ComplainVO import ComplainVO

@app.route('/admin/viewComplain')
def adminViewComplain():
    try:
        if adminLoginSession()=='admin':


            complainDAO = ComplainDAO()
            complainVO = ComplainVO()
            complainVO.complainStatus = "pending"
            complainVOList = complainDAO.adminViewComplain(complainVO)
            print("__________________", complainVOList)
            return render_template('admin/viewComplain.html', complainVOList=complainVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/loadComplainReply')
def adminLoadComplainReply():
    try:
        if adminLoginSession() == 'admin':
            complainId = request.args.get('complainId')

            return render_template('admin/addComplainReply.html', complainId=complainId)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/admin/insertComplainReply', methods=['POST'])
def adminInsertComplainReply():
    try:
        if adminLoginSession() == 'admin':
            UPLOAD_FOLDER = 'project/static/adminResources/reply/'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            file = request.files['file']
            print(file)

            replyFileName = secure_filename(file.filename)
            print(replyFileName)
            replyFilePath = os.path.join(app.config['UPLOAD_FOLDER'])
            print(replyFilePath)

            file.save(os.path.join(replyFilePath, replyFileName))

            complainVO = ComplainVO()
            complainDAO = ComplainDAO()
            complainVO.complainId=request.form['complainId']
            complainVO.replyFileName = replyFileName
            complainVO.replyFilePath = replyFilePath
            complainVO.replyFilePath = replyFilePath.replace("project", "..")
            complainVO.replySubject = request.form['replySubject']
            complainVO.replyMessage = request.form['replyMessage']
            complainVO.complainStatus = "replied"
            complainVO.complainTo_LoginId = session['session_loginId']
            complainVO.replyDate = datetime.today()
            complainVO.replyTime = datetime.now().strftime('%H:%M:%S')
            complainDAO.updateComplain(complainVO)
            return redirect(url_for('adminViewComplain'))
        else:
            return adminLoginSession()
    except Exception as ex:
        print(ex)


@app.route('/user/loadComplain')
def userLoadComplain():
    try:
        return render_template("user/addComplain.html")
    except Exception as ex:
        print(ex)


@app.route('/user/insertComplain', methods=['POST'])
def userInsertComplain():
    try:
        if adminLoginSession() == 'user':
            complainVO = ComplainVO()
            complainDAO = ComplainDAO()

            UPLOAD_FOLDER = 'project/static/adminResources/complain/'
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            file = request.files['Attachment']
            print(file)
            complainFileName = secure_filename(file.filename)
            print(complainFileName)

            complainFilePath = os.path.join(app.config['UPLOAD_FOLDER'])
            print(complainFilePath)

            file.save(os.path.join(complainFilePath, complainFileName))

            complainVO.complainFileName = complainFileName
            complainVO.complainFilePath = complainFilePath
            complainVO.complainFilePath = complainFilePath.replace("project", "..")
            complainVO.complainSubject = request.form['complainSubject']
            complainVO.complainDescription = request.form['complainDescription']
            complainVO.complainStatus = "pending"
            complainVO.complainFrom_LoginId = session['session_loginId']
            complainVO.complainDate = datetime.today()
            complainVO.complainTime = datetime.now().strftime('%H:%M:%S')
            complainDAO.insertComplain(complainVO)

            return redirect(url_for('userViewComplain'))
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/viewComplain')
def userViewComplain():
    try:
        if adminLoginSession() == 'user':
            complainDAO = ComplainDAO()
            complainVO = ComplainVO()

            complainFrom_LoginId = session['session_loginId']
            complainVO.complainFrom_LoginId = complainFrom_LoginId

            complainVOList = complainDAO.viewComplain(complainVO)
            print("__________________", complainVOList)
            return render_template('user/viewComplain.html', complainVOList=complainVOList)
        else:
            return adminLogoutSession()

    except Exception as ex:
        print(ex)


@app.route('/user/viewComplainReply')
def userViewComplainReply():
    try:
        if adminLoginSession() == 'user':
            complainDAO = ComplainDAO()
            complainVO=ComplainVO()
            complainId = request.args.get("complainId")
            complainVO.complainId=complainId
            complainVOList = complainDAO.userViewComplain(complainVO)
            print("---------------------", complainVOList)
            return render_template('user/viewComplainReply.html',complainVOList=complainVOList)
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)


@app.route('/user/deleteComplain', methods=['GET'])
def userDeleteComplain():
    try:
        if adminLoginSession() == 'user':

            complainVO = ComplainVO()

            complainDAO = ComplainDAO()

            complainId = request.args.get('complainId')

            complainVO.complainId = complainId

            complainVOList = complainDAO.deleteComplain(complainVO)

            complainFilePath = complainVOList.complainFilePath
            complainFileName = complainVOList.complainFileName
            complainPath = complainFilePath.replace("..", "project") + complainFileName
            os.remove(complainPath)
            if complainVO.complainStatus=="replied":
                complainDAO = ComplainDAO()

                complainId = request.args.get('complainId')

                complainVO.complainId = complainId

                complainVOList = complainDAO.deleteComplain(complainVO)

                replyFilePath = complainVOList.replyFilePath
                replyFileName = complainVOList.replyFileName
                replyPath = replyFilePath.replace("..", "project") + replyFileName
                os.remove(replyPath)


            return redirect(url_for('userViewComplain'))
        else:
            return adminLogoutSession()
    except Exception as ex:
        print(ex)
