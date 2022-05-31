from flask import *

from project import app
from project.com.dao.LoginDAO import LoginDAO
from project.com.dao.RegisterDAO import RegisterDAO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.RegisterVO import RegisterVO


@app.route('/')
def adminLoadlogin():
    return render_template('admin/login.html')


@app.route("/admin/validateLogin", methods=['POST'])
def adminValidateLogin():
    loginUsername = request.form['loginUsername']
    loginPassword = request.form['loginPassword']

    loginVO = LoginVO()
    loginDAO = LoginDAO()

    loginVO.loginUsername = loginUsername
    loginVO.loginPassword = loginPassword
    loginVO.loginStatus = "active"

    loginVOList = loginDAO.validateLogin(loginVO)

    loginDictList = [i.as_dict() for i in loginVOList]

    print(loginDictList)

    lenLoginDictList = len(loginDictList)

    if lenLoginDictList == 0:

        msg = 'Username Or Password is Incorrect !'


        return render_template('admin/login.html', error=msg)

    elif loginDictList[0]['loginStatus']=='inactive':

        msg="u r temporary blocked by admin:"
        return render_template('admin/login.html',error=msg)

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
                return redirect(url_for('adminLoadDashboard'))

            elif loginRole == 'user':
                registerVO=RegisterVO()
                registerDAO=RegisterDAO()
                registerVO.register_LoginId=loginId
                registerVOList=registerDAO.viewRegister(registerVO)
                print(registerVOList)
                session['session_registerFirstName']=[i.registerFirstName for i in registerVOList][0]

                return redirect(url_for('userLoadDashboard'))




@app.route('/admin/viewUser')
def adminViewUser():
    try:
        loginDAO=LoginDAO()
        loginList=loginDAO.viewLogin()
        print("-----------",loginList)
        return render_template("admin/viewUser.html",loginList=loginList)
    except Exception as ex:
        print(ex)


@app.route('/admin/editUser')
def adminEditUser():
    try:
        loginVO=LoginVO()
        loginDAO=LoginDAO()
        loginId=request.args.get('loginId')
        loginVO.loginId=loginId
        loginStatus=request.args.get('loginStatus')
        loginVO.loginStatus=loginStatus
        loginDAO.editLogin(loginVO)
        return redirect(url_for('adminViewUser'))
    except Exception as ex:
        print(ex)



@app.route('/admin/loadDashboard', methods=['GET'])
def adminLoadDashboard():
    if adminLoginSession() == 'admin':

        return render_template('admin/index.html')
    else:
        return adminLogoutSession()


@app.route('/user/loadDashboard')
def userLoadDashboard():
    if adminLoginSession() == 'user':

        return render_template('user/index.html')
    else:
        return adminLogoutSession()


@app.route('/admin/loginSession')
def adminLoginSession():
    if 'session_loginId' and 'session_loginRole' in session:

        if session['session_loginRole'] == 'admin':

            return 'admin'

        elif session['session_loginRole'] == 'user':

            return 'user'

        print("<<<<<<<<<<<<<<<<True>>>>>>>>>>>>>>>>>>>>")

    else:

        print("<<<<<<<<<<<<<<<<False>>>>>>>>>>>>>>>>>>>>")

        return False


@app.route("/admin/logoutSession", methods=['GET'])
def adminLogoutSession():
    session.clear()

    return redirect('/')
