from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class filter_stocks(FlaskForm):
    cash_check = BooleanField('Yes---')
    cash_a = StringField('輸入兩年內投資金額超過股本的倍數:',\
                           validators=[DataRequired(), Length(min=1, max=20)])
    bigguy_check = BooleanField('Yes---')
    bigguy_a = StringField('千張以上持股比例超過的%數:', \
                           validators=[DataRequired(), Length(min=1, max=20)])
    capital_check = BooleanField('Yes---')
    capital_a = StringField('股本不超過:', \
                           validators=[DataRequired(), Length(min=1, max=20)])
    estab_check = BooleanField('Yes---')
    estab_a = StringField('成立時間不超過:', \
                           validators=[DataRequired(), Length(min=1, max=20)])
    up_check = BooleanField('Yes---')
    up_a = StringField('掛牌時間不超過:', \
                           validators=[DataRequired(), Length(min=1, max=20)])
    netrate_check = BooleanField('Yes---')
    netrate_a = StringField('毛利率超過:', \
                           validators=[DataRequired(), Length(min=1, max=20)])
    oprate_check = BooleanField('Yes---')
    oprate_a = StringField('淨利率超過:',
                           validators=[DataRequired(), Length(min=1, max=20)])
    price_check = BooleanField('Yes---')
    price_a = StringField('成交價創n日新高:',
                           validators=[DataRequired(), Length(min=1, max=20)])
    amount_check = BooleanField('Yes---')
    amount_a = StringField('成交量創n日新高:',
                           validators=[DataRequired(), Length(min=1, max=20)])
    # email = StringField('Email',
    #                     validators=[DataRequired(), Email()])
    # password = PasswordField('Password', validators=[DataRequired()])
    # confirm_password = PasswordField('Confirm Password',
    #                                  validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class InputId(FlaskForm):
    password = StringField('stockid', validators=[DataRequired()])
    submit = SubmitField('Send')
