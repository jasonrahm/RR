from flask_wtf import FlaskForm
from models import Competitions
from models import CompetitionTeam
from models import Teams
from models import Users
from wtforms import BooleanField
from wtforms import HiddenField
from wtforms import PasswordField
from wtforms import SelectField
from wtforms import StringField
from wtforms import SubmitField
from wtforms import validators
from wtforms.fields.html5 import DateField
from wtforms.fields.html5 import IntegerField
from wtforms.widgets import TextArea


class CompetitionsForm(FlaskForm):
    name = StringField('Name',
                       [validators.DataRequired(
                           'Please enter the competition name.')])
    date = DateField('Date',
                     [validators.DataRequired(
                         'Please enter the competition date.')],
                     format='%Y-%m-%d')
    submit = SubmitField('Add Competition')

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)


class CompetitionTeamForm(FlaskForm):
    competition = HiddenField('competition')
    team = SelectField('Team', coerce=int)
    submit = SubmitField('Add Team')

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.team.choices = [
            (a.id, a.number) for a in Teams.query.order_by('number')]

    def validate(self):
        if not FlaskForm.validate(self):
            return False

        comp = Competitions.query.filter_by(name=self.competition).first()
        checkteam = CompetitionTeam.query.filter(
            (CompetitionTeam.competitions == comp.id) &
            (CompetitionTeam.teams == self.team.data)).first()
        if checkteam:
            self.team.errors.append("Team is already part of this competition")
            return False
        else:
            return True


class LoginForm(FlaskForm):
    email = StringField('Email', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    remember_me = BooleanField("Remember me?", default=True)
    submit = SubmitField('Sign In')

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self):
        if not FlaskForm.validate(self):
            return False

        self.user = Users.authenticate(self.email.data, self.password.data)
        if not self.user:
            self.email.errors.append("Invalid email or password")
            return False

        return True


class ReportingForm(FlaskForm):
    a_jewel = SelectField('Jewel (a)', choices=[
        (0, 'Ignore'),
        (1, 'Important'),
        (3, 'Critical')], coerce=int, default=3)
    a_glyphs = SelectField('Glyphs (a)', choices=[
        (0, 'Ignore'),
        (1, 'Important'),
        (3, 'Critical')], coerce=int, default=3)
    a_column = SelectField('Correct Column (a)', choices=[
        (0, 'Ignore'),
        (1, 'Important'),
        (3, 'Critical')], coerce=int, default=3)
    a_park = SelectField('Park (a)', choices=[
        (0, 'Ignore'),
        (1, 'Important'),
        (3, 'Critical')], coerce=int, default=1)
    t_glyphs = SelectField('Glyphs (t)', choices=[
        (0, 'Ignore'),
        (1, 'Important'),
        (3, 'Critical')], coerce=int, default=1)
    t_columns = SelectField('Columns (t)', choices=[
        (0, 'Ignore'),
        (1, 'Important'),
        (3, 'Critical')], coerce=int, default=3)
    t_rows = SelectField('Rows (t)', choices=[
        (0, 'Ignore'),
        (1, 'Important'),
        (3, 'Critical')], coerce=int, default=3)
    t_cipher = SelectField('Cipher (t)', choices=[
        (0, 'Ignore'),
        (1, 'Important'),
        (3, 'Critical')], coerce=int, default=3)
    t_relic1 = SelectField('Relic 1 (t)', choices=[
        (0, 'Ignore'),
        (1, 'Important'),
        (3, 'Critical')], coerce=int, default=3)
    t_relic2 = SelectField('Relic 2 (t)', choices=[
        (0, 'Ignore'),
        (1, 'Important'),
        (3, 'Critical')], coerce=int, default=3)
    t_park = SelectField('Park (t)', choices=[
        (0, 'Ignore'),
        (1, 'Important'),
        (3, 'Critical')], coerce=int, default=1)

    submit = SubmitField('Run Report')

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)


class ScoringForm(FlaskForm):
    team = SelectField('Team', coerce=int)
    match_number = IntegerField('Match Number', [validators.NumberRange(min=1, max=100)], default=1)
    a_hit_jewel = BooleanField('Hit correct jewel (a)?')
    a_glyphs_delivered = IntegerField('Glyphs scored (a)?', default=0)
    a_glyph_correct = BooleanField('Glyph correct column (a)?')
    a_park = BooleanField('Safe Park (a)?')
    t_glyphs_delivered = IntegerField('Glyphs scored (t)?', default=0)
    t_crypto_columns = IntegerField('Crypto Columns (t)', default=0)
    t_crypto_rows = IntegerField('Crypto Rows (t)?', default=0)
    t_crypto_cipher = BooleanField('Cipher Completed (t)?')
    t_relic1 = SelectField('Relic 1 Score (t)?',
                            choices=[(0, 'No Score'),
                                     (10, 'Zone 1'),
                                     (25, 'Zone 1 - Upright'),
                                     (20, 'Zone 2'),
                                     (35, 'Zone 2 - Upright'),
                                     (40, 'Zone 3'),
                                     (55, 'Zone 3 - Upright')], coerce=int)
    t_relic2 = SelectField('Relic 2 Score (t)?',
                           choices=[(0, 'No Score'),
                                    (10, 'Zone 1'),
                                    (25, 'Zone 1 - Upright'),
                                    (20, 'Zone 2'),
                                    (35, 'Zone 2 - Upright'),
                                    (40, 'Zone 3'),
                                    (55, 'Zone 3 - Upright')], coerce=int)
    t_park = BooleanField('Balanced Park (t)?')
    a_score = IntegerField('Autonomous Score', default=0)
    t_score = IntegerField('Teleop Score', default=0)
    total_score = IntegerField('Total Score', default=0)
    match_notes = StringField('Match Notes',
                              [validators.Length(
                                  max=500,
                                  message='Max length 500 characters.')],
                              widget=TextArea())

    submit = SubmitField('Add Score')

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.team.choices = [
            (a.id, a.number) for a in Teams.query.order_by('number')]


class ScoutingForm(FlaskForm):
    team = SelectField('Team', coerce=int)
    a_jewel = BooleanField('Hit correct jewel (a)?')
    a_glyphs = IntegerField('Glyphs scored (a)?', [validators.NumberRange(min=0, max=24)], default=0)
    a_glyph_correct = BooleanField('Glyph correct column (a)?')
    a_park = BooleanField('Safe Park (a)?')
    t_glyphs = IntegerField('Glyphs scored (t)?', [validators.NumberRange(min=0, max=24)], default=0)
    t_crypto_columns = IntegerField('Crypto Columns (t)?', [validators.NumberRange(min=0, max=6)], default=0)
    t_crypto_rows = IntegerField('Crypto Rows (t)?', [validators.NumberRange(min=0, max=8)], default=0)
    t_crypto_cipher = BooleanField('Cipher Completed (t)?')
    t_relics = SelectField('How many relics can they score (t)?',
                           choices=[(0, 'None'),
                                    (1, 'One'),
                                    (2, 'Two')], coerce=int)
    t_relic1 = SelectField('Relic Zone (t)?',
                                choices=[(0, 'Not Applicable'),
                                         (10, 'Zone 1'),
                                         (25, 'Zone 1 - Upright'),
                                         (20, 'Zone 2'),
                                         (35, 'Zone 2 - Upright'),
                                         (40, 'Zone 3'),
                                         (55, 'Zone 3 - Upright')], coerce=int)
    t_relic2 = SelectField('Relic Zone (t)?',
                           choices=[(0, 'Not Applicable'),
                                    (10, 'Zone 1'),
                                    (25, 'Zone 1 - Upright'),
                                    (20, 'Zone 2'),
                                    (35, 'Zone 2 - Upright'),
                                    (40, 'Zone 3'),
                                    (55, 'Zone 3 - Upright')], coerce=int)
    t_park = BooleanField('Balanced Park (t)?')
    score_projection = IntegerField('Score Projection', default=0)
    notes = StringField('Notes',
                        [validators.Length(
                            max=500,
                            message='Please limit to 500 characters.')],
                        widget=TextArea())

    submit = SubmitField('Add Scouting Report')

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.team.choices = [
            (a.id, a.number) for a in Teams.query.order_by('number')]


class TeamForm(FlaskForm):
    number = IntegerField('Number',
                          [validators.DataRequired(
                              'Please enter the team number.')])
    name = StringField('Name',
                       [validators.DataRequired(
                           'Please enter the team name.')])
    submit = SubmitField('Add Team')

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self):
        if not FlaskForm.validate(self):
            return False

        checkteam = Teams.query.filter_by(number=self.number.data).first()
        if checkteam:
            self.number.errors.append("Team is already in the system.")
            return False
        else:
            return True
