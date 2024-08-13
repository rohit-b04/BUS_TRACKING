from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, IntegerField, DateTimeField, DateField, TimeField
class admin_entries(FlaskForm):
    bus_id=StringField(label='Bus Id')
    cur_stop=StringField(label='Bus Stand')
    dest_stop=StringField(label='Going to')
    arrival_time=TimeField(label='Departure Time')
    submit=SubmitField(label='Submit')


class acceptFromUser(FlaskForm):
    From=SelectField(label='From')
    To=SelectField(label='To')
