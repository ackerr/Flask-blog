from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class UsernameForm(FlaskForm):
    username = StringField('请输入你的名字', validators=[DataRequired(), ])
    submit = SubmitField('提交')
