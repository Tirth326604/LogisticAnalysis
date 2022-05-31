from project import db
from project.com.vo.LoginVO import LoginVO


class RegisterVO(db.Model):
    __tablename__ = "registermaster"
    registerId = db.Column('registerId', db.Integer, primary_key=True, autoincrement=True)
    registerFirstName = db.Column('registerFirstName', db.String(100))
    registerLastName = db.Column('registerLastName', db.String(100))
    registerGender = db.Column('registerGender', db.String(50))
    registerContact = db.Column('registerContact', db.String(10))
    registerAddress = db.Column('registerAddress', db.String(100))
    register_LoginId = db.Column('register_LoginId', db.Integer, db.ForeignKey(LoginVO.loginId))

    def as_dict(self):
        return {
            'registerId': self.registerId,
            'registerFirstName': self.registerFirstName,
            'registerLastName': self.registerLastName,
            'registerGender': self.registerGender,
            'registerContact': self.registerContact,
            'registerAddress': self.registerAddress,
            'register_LoginId': self.register_LoginId

        }


db.create_all()
