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
        ('Meet3', 'Meet3'),
        ('Qualifier', 'Qualifier'),
        ('State', 'State'),
        ('Worlds', 'Worlds'),
    ])
    a_lander_loc = SelectField('Lander Location Preference?', choices=[
        ('Crater Side', 'Crater Side'),
        ('Depot Side', 'Depot Side'),
    ])
    a_landed = BooleanField("Can They Land?", default=False)
    a_landed_rel = SelectField("Landing Reliability", choices=[
        (0, '<50%'),
        (.5, '50'),
        (.75, '75'),
        (.85, '85'),
        (.95, '95'),
    ], coerce=float)
    a_sample = BooleanField("Can They Sample?", default=False)
    a_sample_rel = SelectField("Sampling Reliability", choices=[
        (0, '<50%'),
        (.5, '50'),
        (.75, '75'),
        (.85, '85'),
        (.95, '95'),
    ], coerce=float)
    a_marker = BooleanField("Can They Deliver the Marker?", default=False)
    a_marker_rel = SelectField("Marker Reliability", choices=[
        (0, '<50%'),
        (.5, '50'),
        (.75, '75'),
        (.85, '85'),
        (.95, '95'),
    ], coerce=float)
    a_park = BooleanField("Can They Park?", default=False)
    a_park_rel = SelectField("Parking Reliability", choices=[
        (0, '<50%'),
        (.5, '50'),
        (.75, '75'),
        (.85, '85'),
        (.95, '95'),
    ], coerce=float)
    a_compatible = SelectField("How Compatible Are They?", choices=[
        (0, 'not'),
        (1, 'low'),
        (3, 'medium'),
        (5, 'high'),
    ], coerce=int)
    a_notes = StringField("Autonomous Notes", [validators.Length(max=500)])
    t_score_lander = BooleanField("Can They Score in the Lander?", default=False)
    t_mineral = SelectField("What Minerals Can They Score?", choices=[
        ('Neither', 'Neither'),
        ('Gold', 'Gold'),
        ('Silver', 'Silver'),
        ('Both', 'Both'),
    ])
    t_cycle = SelectField("What is Their Cycle Time?", choices=[
        (10, '0-5 sec'),
        (7, '5-10 sec'),
        (3, '10-15 sec'),
        (2, '15-20 sec'),
        (1, '20+ sec'),
    ], coerce=int)
    t_load = SelectField("What is Their Load Size?", choices=[
        (0, '0'),
        (1, '1'),
        (5, '2'),
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
    e_hang_rel = SelectField("Hanging Reliability", choices=[
        (0, '<50%'),
        (.5, '50'),
        (.75, '75'),
        (.85, '85'),
        (.95, '95'),
    ], coerce=float)
    e_hangtime = IntegerField("How Many Seconds Remaining When They Hang?", default=0)
    e_notes = StringField("Endgame Notes", [validators.Length(max=500)])


class ScoutingReportForm(Form):
    comp = SelectField('Competition', choices=[
        ('Meet3', 'Meet3'),
        ('Qualifier', 'Qualifier'),
        ('State', 'State'),
        ('Worlds', 'Worlds'),
    ])
    landing = SelectField('Landing',
                       choices=[(0, 'Ignore'),
                                (1, 'Important'),
                                (4, 'Critical')],
                       coerce=int,
                       default=1)
    landing_rel = BooleanField('Landing Reliability', default=True)
    sampling = SelectField('Sampling',
                                  choices=[(0, 'Ignore'),
                                           (1, 'Important'),
                                           (4, 'Critical')],
                                  coerce=int,
                                  default=1)
    sampling_rel = BooleanField('Sampling Reliability', default=True)
    marker = SelectField('Marker Delivery',
                           choices=[(0, 'Ignore'),
                                    (1, 'Important'),
                                    (4, 'Critical')],
                           coerce=int,
                           default=1)
    marker_rel = BooleanField('Marker Reliability', default=True)
    parking = SelectField('Parking',
                         choices=[(0, 'Ignore'),
                                  (1, 'Important'),
                                  (4, 'Critical')],
                         coerce=int,
                         default=0)
    parking_rel = BooleanField('Parking Reliability', default=False)
    compatibility = SelectField('Compatibility',
                         choices=[(0, 'Ignore'),
                                  (1, 'Important'),
                                  (4, 'Critical')],
                         coerce=int,
                         default=1)
    lander_scoring = SelectField('Lander Scoring',
                                choices=[(0, 'Ignore'),
                                         (1, 'Important'),
                                         (4, 'Critical')],
                                coerce=int,
                                default=1)
    cycle_time = SelectField('Cycle Time',
                                 choices=[(0, 'Ignore'),
                                          (1, 'Important'),
                                          (4, 'Critical')],
                                 coerce=int,
                                 default=1)
    load_size = SelectField('Load Size',
                          choices=[(0, 'Ignore'),
                                   (1, 'Important'),
                                   (4, 'Critical')],
                          coerce=int,
                          default=0)
    hanging = SelectField('Hanging',
                          choices=[(0, 'Ignore'),
                                   (1, 'Important'),
                                   (4, 'Critical')],
                          coerce=int,
                          default=4)
    hanging_rel = BooleanField('Hanging Reliability', default=True)
