import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import render_template, request,redirect,session

from project import app
from project.com.controller.LoginController import adminLoginSession, adminLogoutSession
from project.com.dao.LoginDAO import LoginDAO
from project.com.dao.RegisterDAO import RegisterDAO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.RegisterVO import RegisterVO


@app.route('/user/loadRegister')
def userLoadRegister():


        return render_template('user/register.html')


@app.route('/user/insertRegister', methods=['POST'])
def userInsertRegister():
    try:

            if adminLoginSession() == 'user':

                loginVO = LoginVO()
                loginDAO = LoginDAO()

                registerVO = RegisterVO()
                registerDAO = RegisterDAO()

                loginUsername = request.form['loginUsername']

                registerFirstName = request.form['registerFirstName']
                registerLastName = request.form['registerLastName']
                registerGender = request.form['registerGender']
                registerAddress = request.form['registerAddress']
                registerContact = request.form['registerContact']

                loginPassword = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(8))

                print("loginPassword=" + loginPassword)

                sender = "pythondemodonotreply@gmail.com"

                receiver = loginUsername

                msg = MIMEMultipart()

                msg['From'] = sender

                msg['To'] = receiver

                msg['Subject'] = "LOGIN PASSWORD"

                msg.attach(MIMEText(loginPassword, 'plain'))

                server = smtplib.SMTP('smtp.gmail.com', 587)

                server.starttls()

                server.login(sender, "qazwsxedcrfvtgb1234567890")

                text = msg.as_string()

                server.sendmail(sender, receiver, text)

                loginVO.loginUsername = loginUsername
                loginVO.loginPassword = loginPassword
                loginVO.loginRole = "user"
                loginVO.loginStatus = "active"

                loginDAO.insertLogin(loginVO)

                registerVO.registerFirstName = registerFirstName
                registerVO.registerLastName = registerLastName
                registerVO.registerGender = registerGender
                registerVO.registerAddress = registerAddress
                registerVO.registerContact = registerContact
                registerVO.register_LoginId = loginVO.loginId

                registerDAO.insertRegister(registerVO)

                server.quit()

                return redirect('/')

            else:
                return adminLogoutSession()
    except Exception as ex:
        print(ex)