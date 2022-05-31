from project import db
from project.com.vo.LoginVO import LoginVO
from project.com.vo.RegisterVO import RegisterVO


class LoginDAO:
    def insertLogin(self, loginVO):
        db.session.add(loginVO)
        db.session.commit()

    def validateLogin(self, loginVO):
        loginList = LoginVO.query.filter_by(loginUsername=loginVO.loginUsername,
                                                loginPassword=loginVO.loginPassword, loginStatus=loginVO.loginStatus)

        return loginList

    def viewLogin(self):
        loginList=db.session.query(RegisterVO,LoginVO)\
                  .join(LoginVO,RegisterVO.register_LoginId == LoginVO.loginId).all()
        return loginList



    def editLogin(self,loginVO):
        loginList=LoginVO.query.get(loginVO.loginId)
        loginList.loginStatus=loginVO.loginStatus
        db.session.commit()