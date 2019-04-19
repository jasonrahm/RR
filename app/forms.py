from wtforms import Form
from wtforms import BooleanField
from wtforms import IntegerField
from wtforms import PasswordField
from wtforms import SelectField
from wtforms import StringField
from wtforms import TextAreaField
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
    ], default='Worlds')
    a_lander_loc = SelectField('Lander Location Preference?', choices=[
        ('Crater Side', 'Crater Side'),
        ('Depot Side', 'Depot Side'),
        ('Neither', 'Neither')
    ])
    a_landed = BooleanField("Can They Land?", default=False)
    a_landed_rel = SelectField("Landing Reliability", choices=[
        (0, '<50%'),
        (.5, '50'),
        (.75, '75'),
        (.85, '85'),
        (.95, '95'),
    ], coerce=float, default=0)
    a_sample = BooleanField("Can They Sample?", default=False)
    a_sample_rel = SelectField("Sampling Reliability", choices=[
        (0, '<50%'),
        (.5, '50'),
        (.75, '75'),
        (.85, '85'),
        (.95, '95'),
    ], coerce=float, default=0)
    a_marker = BooleanField("Can They Deliver the Marker?", default=False)
    a_marker_rel = SelectField("Marker Reliability", choices=[
        (0, '<50%'),
        (.5, '50'),
        (.75, '75'),
        (.85, '85'),
        (.95, '95'),
    ], coerce=float, default=0)
    a_park = BooleanField("Can They Park?", default=False)
    a_park_rel = SelectField("Parking Reliability", choices=[
        (0, '<50%'),
        (.5, '50'),
        (.75, '75'),
        (.85, '85'),
        (.95, '95'),
    ], coerce=float, default=0)
    a_compatible = SelectField("How Compatible Are They?", choices=[
        (0, 'not'),
        (1, 'low'),
        (3, 'medium'),
        (5, 'high'),
    ], coerce=int, default=0)
    a_notes = TextAreaField("Autonomous Notes", [validators.Length(max=500)])
    t_score_lander = BooleanField("Can They Score in the Lander?", default=False)
    t_mineral = SelectField("What Minerals Can They Score?", choices=[
        ('Neither', 'Neither'),
        ('Gold', 'Gold'),
        ('Silver', 'Silver'),
        ('Both', 'Both'),
    ], default='Neither')
    t_cycle = IntegerField("How many loads can they delivery?", default=0)
    t_load = SelectField("What is Their Load Size?", choices=[
        (0, '0'),
        (1, '1'),
        (5, '2'),
    ], coerce=int, default=0)
    t_score_position = SelectField("Where is Their Preferred Scoring Position?", choices=[
        ('Gold Center', 'Gold Center'),
        ('Gold Corner', 'Gold Corner'),
        ('Silver Center', 'Silver Center'),
        ('Silver Corner', 'Silver Corner'),
        ('Both Center', 'Both Center'),
        ('Both Corner', 'Both Corner'),
        ('No Preference', 'No Preference')
    ], default='No Preference')
    t_notes = TextAreaField("TeleOp Notes", [validators.Length(max=500)])
    e_hang = BooleanField("Can They Hang?", default=False)
    e_hang_rel = SelectField("Hanging Reliability", choices=[
        (0, '<50%'),
        (.5, '50'),
        (.75, '75'),
        (.85, '85'),
        (.95, '95'),
    ], coerce=float, default=0)
    e_hangtime = IntegerField("How Many Seconds Remaining When They Hang?", default=0)
    e_notes = TextAreaField("Endgame Notes", [validators.Length(max=500)])


class ScoutingReportForm(Form):
    comp = SelectField('Competition', choices=[
        ('Meet3', 'Meet3'),
        ('Qualifier', 'Qualifier'),
        ('State', 'State'),
        ('Worlds', 'Worlds'),
    ], default='Worlds')
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


class ScoringForm(Form):
    comp = SelectField('Competition', choices=[
        ('Meet3', 'Meet3'),
        ('Qualifier', 'Qualifier'),
        ('State', 'State'),
        ('Worlds', 'Worlds'),
    ], default='Worlds')
    match = StringField("Match #")
    r1 = IntegerField("Team #1", default=0)
    r2 = IntegerField("Team #2", default=0)
    # Autonomous
    a_r1_land = BooleanField('R1 Landing')
    a_r1_sample = BooleanField('R1 Sampling')
    a_r1_depot = BooleanField('R1 Marker')
    a_r1_park = BooleanField('R1 Parking')
    a_r1_auto_score = IntegerField('R1 Autonomous Score', default=0)
    a_r1_notes = TextAreaField('R1 Autonomous Notes')
    a_r2_land = BooleanField('R2 Landing')
    a_r2_sample = BooleanField('R2 Sampling')
    a_r2_depot = BooleanField('R2 Marker')
    a_r2_park = BooleanField('R2 Marking')
    a_r2_auto_score = IntegerField('R2 Autonomous Score', default=0)
    a_r2_notes = TextAreaField('R2 Autonomous Notes')
    # TeleOp
    t_r1_lander_minerals = IntegerField('R1 Lander', default=0)
    t_r1_depot_minerals = IntegerField('R1 Depot', default=0)
    t_r1_teleop_score = IntegerField('R1 TeleOp Score', default=0)
    t_r2_lander_minerals = IntegerField('R2 Lander', default=0)
    t_r2_depot_minerals = IntegerField('R2 Depot', default=0)
    t_r2_teleop_score = IntegerField('R2 TeleOp Score', default=0)
    # Endgame
    e_r1_latched = BooleanField('R1 Latched')
    e_r1_park = SelectField('R1 Parking',
                          choices=[(0, 'Not In'),
                                   (15, 'In'),
                                   (25, 'Fully In')],
                          coerce=int,
                          default=0)
    e_r1_endgame_score = IntegerField('R1 Endgame Score', default=0)
    e_r2_latched = BooleanField('R2 Latched')
    e_r2_park = SelectField('R2 Parking',
                          choices=[(0, 'Not In'),
                                   (15, 'In'),
                                   (25, 'Fully In')],
                          coerce=int,
                          default=0)
    e_r2_endgame_score = IntegerField('R2 Endgame Score', default=0)
    # Overall Scores
    r1_total_score = IntegerField('R1 Total Score', default=0)
    r2_total_score = IntegerField('R2 Total Score', default=0)
    match_score = IntegerField('Combined Score', default=0)
    e_r1_notes = TextAreaField('R1 TeleOp Notes')
    e_r2_notes = TextAreaField('R2 TeleOp Notes')


class ScoringEditForm(Form):
    comp = SelectField('Competition', choices=[
        ('Meet3', 'Meet3'),
        ('Qualifier', 'Qualifier'),
        ('State', 'State'),
        ('Worlds', 'Worlds'),
    ], default='Worlds')
    match = StringField("Match #")
    team = IntegerField("Team #")
    # Autonomous
    a_land = BooleanField('Landing')
    a_sample = BooleanField('Sampling')
    a_depot = BooleanField('Marker')
    a_park = BooleanField('Parking')
    a_score = IntegerField('Autonomous Score')
    a_notes = TextAreaField('Autonomous Notes')
    # TeleOp
    t_lander_minerals = IntegerField('Lander Minerals')
    t_depot_minerals = IntegerField('Depot Minerals')
    t_score = IntegerField('TeleOp Score')
    # Endgame
    e_latched = BooleanField('Latched')
    e_park = SelectField('Parking',
                          choices=[(0, 'Not In'),
                                   (15, 'In'),
                                   (25, 'Fully In')],
                          coerce=int,
                          default=0)
    e_score = IntegerField('Endgame Score', default=0)
    # Overall Scores
    total_score = IntegerField('Total Score')
    match_score = IntegerField('Combined Score')
    e_notes = TextAreaField('TeleOp Notes')


class ScoringReportForm(Form):
    comp = SelectField('Competition', choices=[
        ('Meet3', 'Meet3'),
        ('Qualifier', 'Qualifier'),
        ('State', 'State'),
        ('Worlds', 'Worlds'),
    ], default='Worlds')
    # auto = SelectField('Autonomous Score',
    #                      choices=[(0, 'Ignore'),
    #                               (1, 'Important'),
    #                               (4, 'Critical')],
    #                      coerce=int,
    #                      default=1)
    # teleop = SelectField('TeleOp Score',
    #                    choices=[(0, 'Ignore'),
    #                             (1, 'Important'),
    #                             (4, 'Critical')],
    #                    coerce=int,
    #                    default=1)
    # endgame = SelectField('Endgame Score',
    #                    choices=[(0, 'Ignore'),
    #                             (1, 'Important'),
    #                             (4, 'Critical')],
    #                    coerce=int,
    #                    default=1)
    # total = SelectField('Total Score',
    #                    choices=[(0, 'Ignore'),
    #                             (1, 'Important'),
    #                             (4, 'Critical')],
    #                    coerce=int,
    #                    default=1)