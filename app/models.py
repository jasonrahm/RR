from app import bcrypt
from app import db
from app import login_manager
from slugify import slugify
import datetime


@login_manager.user_loader
def _user_loader(user_id):
    return Users.query.get(int(user_id))


class Competitions(db.Model):
    __tablename__ = 'Competitions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120), nullable=False)
    date = db.Column(db.Date, nullable=False)
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    modified_timestamp = db.Column(
        db.DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now)

    def __init__(self, name, date, timestamp):
        self.name = name
        self.date = date
        self.created_timestamp = timestamp

    def __repr__(self):
        return self.name


class CompetitionTeam(db.Model):
    __tablename__ = 'CompetitionTeams'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    competitions = db.Column(db.ForeignKey('Competitions.id'),
                             nullable=False,
                             index=True)
    teams = db.Column(db.ForeignKey('Teams.id'), nullable=False, index=True)
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    modified_timestamp = db.Column(
        db.DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now)

    competition = db.relationship('Competitions')
    team = db.relationship('Teams')

    def __init__(self, competitions, teams, timestamp):
        self.competitions = competitions
        self.teams = teams
        self.created_timestamp = timestamp

    def __repr__(self):
        return '<CompetitionTeam %r %r %r>' % (self.id,
                                               self.competitions,
                                               self.teams)


class Scoring(db.Model):
    __tablename__ = 'Scoring'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teams = db.Column(db.ForeignKey('Teams.id'), index=True)
    competitions = db.Column(db.ForeignKey('Competitions.id'), index=True)
    match_number = db.Column(db.Integer)
    a_hit_jewel = db.Column(db.Boolean)
    a_glyphs_delivered = db.Column(db.Integer)
    a_glyph_correct = db.Column(db.Boolean)
    a_park = db.Column(db.Boolean)
    t_glyphs_delivered = db.Column(db.Integer)
    t_crypto_columns = db.Column(db.Integer)
    t_crypto_rows = db.Column(db.Integer)
    t_crypto_cipher = db.Column(db.Integer)
    t_relic_score = db.Column(db.Integer)
    t_park = db.Column(db.Boolean)
    a_score = db.Column(db.Integer)
    t_score = db.Column(db.Integer)
    total_score = db.Column(db.Integer)
    match_notes = db.Column(db.String(500))
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    modified_timestamp = db.Column(
        db.DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now)

    competition = db.relationship('Competitions')
    team = db.relationship('Teams')

    def __init__(self,
                 teams,
                 competitions,
                 match_number,
                 a_hit_jewel,
                 a_glyphs_delivered,
                 a_glyph_correct,
                 a_park,
                 t_glyphs_delivered,
                 t_crypto_columns,
                 t_crypto_rows,
                 t_crypto_cipher,
                 t_relic_score,
                 t_park,
                 a_score,
                 t_score,
                 total_score,
                 match_notes,
                 timestamp):
        self.teams = teams
        self.competitions = competitions
        self.match_number = match_number
        self.a_hit_jewel = a_hit_jewel
        self.a_glyphs_delivered = a_glyphs_delivered
        self.a_glyph_correct = a_glyph_correct
        self.a_park = a_park
        self.t_glyphs_delivered = t_glyphs_delivered
        self.t_crypto_columns = t_crypto_columns
        self.t_crypto_rows = t_crypto_rows
        self.t_crypto_cipher = t_crypto_cipher
        self.t_relic_score = t_relic_score
        self.t_park = t_park
        self.a_score = a_score
        self.t_score = t_score
        self.total_score = total_score

        self.match_notes = match_notes
        self.created_timestamp = timestamp

    def __repr__(self):
        return '<MatchScore %r %r %r>' % (self.id, self.teams, self.total_score)


class Scouting(db.Model):
    __tablename__ = 'Scouting'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teams = db.Column(db.ForeignKey('Teams.id'), index=True)
    competitions = db.Column(db.ForeignKey('Competitions.id'), index=True)
    a_jewel = db.Column(db.Boolean)
    a_glyphs = db.Column(db.Integer)
    a_glyph_correct = db.Column(db.Boolean)
    a_park = db.Column(db.Boolean)
    t_glyphs = db.Column(db.Integer)
    t_crypto_columns = db.Column(db.Integer)
    t_crypto_rows = db.Column(db.Integer)
    t_crypto_cipher = db.Column(db.Boolean)
    t_relic_zone = db.Column(db.Integer)
    t_park = db.Column(db.Boolean)
    score_projection = db.Column(db.Integer)
    notes = db.Column(db.String(500))
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    modified_timestamp = db.Column(
        db.DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now)

    competition = db.relationship('Competitions')
    team = db.relationship('Teams')

    def __init__(self,
                 teams,
                 competitions,
                 a_jewel,
                 a_glyphs,
                 a_glyph_correct,
                 a_park,
                 t_glyphs,
                 t_crypto_columns,
                 t_crypto_rows,
                 t_crypto_cipher,
                 t_relic_zone,
                 t_park,
                 score_projection,
                 notes,
                 timestamp):
        self.teams = teams
        self.competitions = competitions
        self.a_jewel = a_jewel
        self.a_glyphs = a_glyphs
        self.a_glyph_correct = a_glyph_correct
        self.a_park = a_park
        self.t_glyphs = t_glyphs
        self.t_crypto_columns = t_crypto_columns
        self.t_crypto_rows = t_crypto_rows
        self.t_crypto_cipher = t_crypto_cipher
        self.t_relic_zone = t_relic_zone
        self.t_park = t_park
        self.score_projection = score_projection
        self.notes = notes
        self.created_timestamp = timestamp

    def __repr__(self):
        return '<PitScouting %r %r %r>' % (self.id,
                                           self.teams,
                                           self.competitions)


class Teams(db.Model):
    __tablename__ = 'Teams'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
    modified_timestamp = db.Column(
        db.DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now)

    def __init__(self,
                 number,
                 name,
                 timestamp):
        self.number = number
        self.name = name
        self.created_timestamp = timestamp

    def __repr__(self):
        return '%r: %r' % (self.number, str(self.name))


class Users(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(255))
    name = db.Column(db.String(64))
    slug = db.Column(db.String(64), unique=True)
    active = db.Column(db.Boolean, default=True)
    created_timestamp = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, *args, **kwargs):
        super(Users, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.name:
            self.slug = slugify(unicode(self.name, "utf-8"))

    def __repr__(self):
        return '<Users %r>' % self.email

    # Start Flask-Login interface methods
    def get_id(self):
        return unicode(self.id)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    @staticmethod
    def make_password(plaintext):
        return bcrypt.generate_password_hash(plaintext)

    def check_password(self, raw_password):
        return bcrypt.check_password_hash(self.password_hash, raw_password)

    @classmethod
    def create(cls, email, password, **kwargs):
        return Users(
            email=email,
            password_hash=Users.make_password(password),
            **kwargs)

    @staticmethod
    def authenticate(email, password):
        user = Users.query.filter(Users.email == email).first()
        if user and user.check_password(password):
            return user
        return False