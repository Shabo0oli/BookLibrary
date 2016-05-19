# -*- coding:utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import ValidationError
from wtforms.validators import Email, Length, DataRequired, EqualTo
from app.models import User
from app import db


class LoginForm(Form):
    email = StringField('Email',
                        validators=[DataRequired(message=u"该项忘了填写了!"), Length(1, 64), Email(message=u"你确定这是 Email ?")])
    password = PasswordField(u'密码', validators=[DataRequired(message=u"该项忘了填写了!"), Length(6, 32)])
    remember_me = BooleanField(u"保持我的登入状态", default=True)
    submit = SubmitField(u'登入')


class RegistrationForm(Form):
    email = StringField('Email',
                        validators=[DataRequired(message=u"该项忘了填写了!"), Length(1, 64), Email(message=u"你确定这是 Email ?")])
    name = StringField(u'用户名', validators=[DataRequired(message=u"该项忘了填写了!"), Length(1, 64)])
    password = PasswordField(u'密码',
                             validators=[DataRequired(message=u"该项忘了填写了!"), EqualTo('password2', message=u'密码必须匹配'),
                                         Length(6, 32)])
    password2 = PasswordField(u'再次确认密码', validators=[DataRequired(message=u"该项忘了填写了!")])
    submit = SubmitField(u'注册')

    def validate_email(self, filed):
        if User.query.filter(db.func.lower(User.email) == db.func.lower(filed.data)).first():
            raise ValidationError(u'该 Email 已经被注册了')


class ChangePasswordForm(Form):
    old_password = PasswordField(u'旧密码', validators=[DataRequired(message=u"该项忘了填写了!")])
    new_password = PasswordField(u'新密码', validators=[DataRequired(message=u"该项忘了填写了!"),
                                                     EqualTo('confirm_password', message=u'密码必须匹配'),
                                                     Length(6, 32)])
    confirm_password = PasswordField(u'确认新密码', validators=[DataRequired(message=u"该项忘了填写了!")])
    submit = SubmitField(u"保存密码")

    def validate_old_password(self, filed):
        from flask.ext.login import current_user
        if not current_user.verify_password(filed.data):
            raise ValidationError(u'原密码错误')
