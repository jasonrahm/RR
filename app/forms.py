from wtforms import Form
from wtforms import BooleanField
from wtforms import IntegerField
from wtforms import PasswordField
from wtforms import SelectField
from wtforms import StringField
from wtforms import validators


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


class ScoutingForm(Form):
    team_number = IntegerField('Team Number')
    team_name = StringField('Team Name', [validators.Length(min=1, max=50)])
    comp = SelectField('Competition', choices=[
        ('IL Southern Meet #1', 'IL Southern Meet #1'),
        ('IL Southern Meet #2', 'IL Southern Meet #2'),
        ('IL Southern Meet #3', 'IL Southern Meet #3'),
        ('IL South/Central East Qualifier', 'IL South/Central East Qualifier'),
        ('IL State', 'IL State'),
        ('Detroit World Championships', 'Detroit World Championships'),
    ])
    a_lander_loc = SelectField('Lander Location Preference?', choices=[
        ('Crater Side', 'Crater Side'),
        ('Depot Side', 'Depot Side'),
    ])
    a_landed = BooleanField("Can They Land?", default=False)
    a_landed_rel = SelectField("Landing Reliability?", choices=[
        (0, '<50%'),
        (1, '50'),
        (2, '75'),
        (3, '85'),
        (5, '95'),
    ], coerce=int)
    a_sample = BooleanField("Can They Sample", default=False)
    a_sample_rel = SelectField("Sampling Reliability?", choices=[
        (0, '<50%'),
        (1, '50'),
        (2, '75'),
        (3, '85'),
        (5, '95'),
    ], coerce=int)
    a_marker = BooleanField("Can They Deliver the Marker?", default=False)
    a_marker_rel = SelectField("Marker Reliability?", choices=[
        (0, '<50%'),
        (1, '50'),
        (2, '75'),
        (3, '85'),
        (5, '95'),
    ], coerce=int)
    a_park = BooleanField("Can They Park?", default=False)
    a_park_rel = SelectField("Parking Reliability?", choices=[
        (0, '<50%'),
        (1, '50'),
        (2, '75'),
        (3, '85'),
        (5, '95'),
    ], coerce=int)
    a_compatible = SelectField("How Compatible Are They?", choices=[
        (0, 'low'),
        (1, 'medium'),
        (3, 'high'),
    ], coerce=int)
    a_notes = StringField("Autonomous Notes", [validators.Length(max=500)])
    t_score_lander = BooleanField("Can They Score in the Lander?", default=False)
    t_mineral = SelectField("What Minerals Can They Score?", choices=[
        ('Neither', 'Neither'),
        ('Gold', 'Gold'),
        ('Silver', 'Silver'),
        ('Both', 'Both'),
    ])
    t_cycle = IntegerField("What is Their Cycle Time?")
    t_load = SelectField("What is Their Load Size?", choices=[
        (0, '0'),
        (1, '1'),
        (3, '2'),
    ], coerce=int)
    t_score_position = SelectField("Where is Their Preferred Scoring Position?", choices=[
        ('Gold Center', 'Gold Center'),
        ('Gold Corner', 'Gold Corner'),
        ('Silver Center', 'Silver Center'),
        ('Silver Corner', 'Silver Corner'),
        ('Both Center', 'Both Center'),
        ('Both Corner', 'Both Corner'),
    ])
    t_notes = StringField("TeleOp Notes", [validators.Length(max=500)])
    e_hang = BooleanField("Can They Hang?", default=False)
    e_hang_rel = SelectField("Hanging Reliability?", choices=[
        (0, '<50%'),
        (1, '50'),
        (2, '75'),
        (3, '85'),
        (5, '95'),
    ], coerce=int)
    e_hangtime = IntegerField("How Many Seconds Remaining When They Hang?")
    e_notes = StringField("Endgame Notes", [validators.Length(max=500)])
