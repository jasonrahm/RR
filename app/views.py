from app import app

from BeautifulSoup import BeautifulSoup as bs
from flask import abort
from flask import flash
from flask import Markup
from flask import render_template
from flask import redirect
from flask import request
from flask import session
from flask import url_for
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user

from forms import CompetitionsForm
from forms import CompetitionTeamForm
from forms import LoginForm
from forms import ReportingForm
from forms import ScoringForm
from forms import ScoutingForm
from forms import TeamForm

from itertools import islice

from models import db
from models import Competitions
from models import CompetitionTeam
from models import Scoring
from models import Scouting
from models import Teams
from models import Users

from sqlalchemy import and_

import datetime
import pandas as pd
import requests

# Id of current competition
cur_comp = 1


@app.errorhandler(404)
def missing_file(error):
    return render_template('servererror.html')


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@app.route('/awards', methods=['GET'])
def awards():
    return render_template('awards.html')


@app.route('/camps', methods=['GET'])
def camps():
    return render_template('camps.html')


@app.route('/competitions', methods=['GET', 'POST'])
@login_required
def competitions():
    form = CompetitionsForm()

    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('competitions.html', form=form)
        else:
            newcomp = Competitions(name=form.name.data,
                                   date=form.date.data,
                                   timestamp=datetime.datetime.now())
            db.session.add(newcomp)
            db.session.commit()

            flash('Competition successfully added.')
            return redirect(url_for('competitions'))

    elif request.method == 'GET':
        comps = db.session.query(Competitions).all()
        return render_template('competitions.html',
                               competitions=comps,
                               form=form)


@app.route('/competitions/<int:id>', methods=['GET', 'POST'])
@login_required
def manage_competition(id):
    form = CompetitionTeamForm(request.values, competition=id)
    comp = Competitions.query.get(id)
    form.competition = comp.name

    teams = db.session.query(CompetitionTeam).filter(
        CompetitionTeam.competitions == id).all()

    team_list = []
    for team in teams:
        team_list.append(int(team.teams))
    team_data = db.session.query(Teams).filter(
        Teams.id.in_(team_list)).order_by(Teams.number).all()

    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('competition_details.html',
                                   form=form,
                                   id=id,
                                   team_data=team_data)
        else:
            postdata = request.values
            comp = int(postdata['competition'])
            team = int(postdata['team'])

            newteam = CompetitionTeam(competitions=comp,
                                      teams=team,
                                      timestamp=datetime.datetime.now())
            db.session.add(newteam)
            db.session.commit()

            flash('Team successfully added to the competition.')
            return redirect(url_for('manage_competition', id=id))

    elif request.method == 'GET':
        return render_template('competition_details.html',
                               form=form,
                               id=id,
                               team_data=team_data)


@app.route('/competitions/<int:comp_id>/delete/<int:team_id>', methods=['GET'])
@login_required
def delete_team_from_comp(comp_id, team_id):
    team = Teams.query.get(team_id)
    records = CompetitionTeam.query.filter(and_(
        CompetitionTeam.competitions == comp_id,
        CompetitionTeam.teams == team_id)).first()
    db.session.delete(records)
    db.session.commit()
    flash('Team {0} deleted from competition'.format(team.name))
    return redirect(url_for('manage_competition', id=comp_id))


@app.route('/competitions/delete/<int:id>', methods=['GET'])
@login_required
def delete_competition_entry(id):
    competition = Competitions.query.get(id)
    if competition is None:
        abort(404)
    db.session.delete(competition)
    db.session.commit()

    flash('Competition deleted.')
    return redirect(url_for('competitions'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = LoginForm(request.form)
        if form.validate_on_submit():
            user = Users.query.filter_by(email=form.email.data).first()
            login_user(user, remember=form.remember_me.data)
            flash('Login Successful.')
            return redirect(request.args.get('next') or url_for('index'))
    else:
        form = LoginForm()

    return render_template('login.html', form=form)


@app.route('/logout/', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/projections/', defaults={'comp': cur_comp}, methods=['GET'])
@app.route('/projections/competitions/<int:comp>', methods=['GET'])
@login_required
def projections(comp):

    pitr = {}
    pit_records = db.session.query(Scouting).filter(
        Scouting.competitions == comp).all()
    for record in pit_records:
        pitr[str(record.team).split(':')[0]] = record.score_projection

    # tables = pd.read_html(r'/Users/rahm/Downloads/matchlist1.html')
    tables = pd.read_html('https://ftc-results.firstillinoisrobotics.org/live/il-cmp-rr/upload/d2/matchlist.html')
    table = tables[0]
    table.columns = ['Number', 'Red 1', 'Red 2', 'Blue 1', 'Blue 2']

    projection_data = []
    for (idx, row) in islice(table.iterrows(), 1, None):
        if not isinstance(row['Red 1'], str):
            r1 = row['Red 1'].replace("*", "")
        if not isinstance(row['Red 2'], str):
            r2 = row['Red 2'].replace("*", "")
        if not isinstance(row['Blue 1'], str):
            b1 = row['Blue 1'].replace("*", "")
        if not isinstance(row['Blue 2'], str):
            b2 = row['Blue 2'].replace("*", "")

        match = row['Number']
        red_score = pitr[r1] + pitr[r2]
        blue_score = pitr[b1] + pitr[b2]

        projection_data.append([match, r1, r2, red_score, b1, b2, blue_score])

    return render_template('projections.html', data=projection_data)


@app.route('/rankings', methods=['GET'])
def rankings():
    rank = 'https://ftc-results.firstillinoisrobotics.org/live/il-cmp-rr/upload/d2/rankings.html'
    rank_response = requests.get(rank, verify=False)
    rank_soup = bs(rank_response.text)
    rank_data = rank_soup.findAll('table')[0]

    match = 'https://ftc-results.firstillinoisrobotics.org/live/il-cmp-rr/upload/d2/matchresults.html'
    match_response = requests.get(match, verify=False)
    match_soup = bs(match_response.text)
    match_data = match_soup.findAll('table')[0]

    return render_template('rankings.html',
                           rank_data=Markup(rank_data),
                           match_data=Markup(match_data))


@app.route('/report', methods=['GET'])
@login_required
def report():
    data = session['report']
    if data == '':
        redirect(url_for(reporting))
    else:
        return render_template('report.html', data=data)


@app.route('/reporting/', defaults={'comp': cur_comp}, methods=['GET', 'POST'])
@app.route('/reporting/competitions/<int:comp>', methods=['GET', 'POST'])
@login_required
def reporting(comp):
    form = ReportingForm(request.values)

    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('reporting.html', form=form)
        else:
            postdata = request.values
            pit_records = db.session.query(Scouting).filter(
                Scouting.competitions == comp).all()
            pitr = {}
            for record in pit_records:
                pitr[record.teams] = record.score_projection

            teams_scored = db.session.query(Scoring.teams).filter(
                Scoring.competitions == comp).distinct()
            teams = []
            for x in teams_scored:
                sql_text = '''select Teams.id, Teams.name, Teams.number,
                           avg(total_score), max(total_score),
                           (avg(a_hit_jewel)*30*%d) +
                           (avg(a_glyphs_delivered)*15*%d) +
                           (avg(a_glyph_correct)*30*%d) +
                           (avg(a_park)*10*%d) +
                           (avg(t_glyphs_delivered)*2*%d) +
                           (avg(t_crypto_columns)*20*%d) +
                           (avg(t_crypto_rows)*10*%d) +
                           (avg(t_crypto_cipher)*30*%d) +
                           (avg(t_relic1)*%d) +
                           (avg(t_relic2)*%d) +
                           (avg(t_park)*20*%d)
                           AS Score
                           FROM Scoring
                           INNER JOIN Teams
                             On Scoring.teams = Teams.id
                           WHERE competitions = %d AND teams = %d
                           ORDER BY Score
                           DESC''' % (int(postdata['a_jewel']),
                                      int(postdata['a_glyphs']),
                                      int(postdata['a_column']),
                                      int(postdata['a_park']),
                                      int(postdata['t_glyphs']),
                                      int(postdata['t_columns']),
                                      int(postdata['t_rows']),
                                      int(postdata['t_cipher']),
                                      int(postdata['t_relic1']),
                                      int(postdata['t_relic2']),
                                      int(postdata['t_park']),
                                      comp,
                                      x[0])
                result = db.engine.execute(sql_text)
                for row in result:
                    teams.append([row[1], row[2], row[3], row[4], row[5], pitr.get(row[0]), row[0]])

            session['report'] = teams

            flash('Report Ran Successfully.')
            return redirect(url_for('report'))

    elif request.method == 'GET':
        return render_template('reporting.html', form=form)


@app.route('/resources', methods=['GET'])
def resources():
    return render_template('resources.html')


@app.route('/robots', methods=['GET'])
def robots():
    return render_template('robots.html')


@app.route('/scoring/', defaults={'comp': cur_comp},
           methods=['GET', 'POST'])
@app.route('/scoring/competitions/<int:comp>', methods=['GET', 'POST'])
def scoring(comp):
    form = ScoringForm(request.values)

    sql_text = '''SELECT *
              FROM
                CompetitionTeams ct
              INNER JOIN
                Teams t ON ct.teams = t.id
              WHERE
                ct.competitions = {}
              ORDER BY t.number ASC'''.format(comp)
    result = db.engine.execute(sql_text)

    form.team.choices = [(a.id,
                          "{}: {}".format(a.number, a.name)) for a in result]

    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('scoring.html', form=form)
        else:
            team = request.form.get('team', '')
            match_number = request.form.get('match_number', '')
            a_hit_jewel = (False, True)[request.form.get('a_hit_jewel', '') == u'y']
            a_glyphs_delivered = request.form.get('a_glyphs_delivered', '')
            a_glyph_correct = (False, True)[request.form.get('a_glyphs_correct', '') == u'y']
            a_park = (False, True)[request.form.get('a_park', '') == u'y']
            t_glyphs_delivered = request.form.get('t_glyphs_delivered', '')
            t_crypto_columns = request.form.get('t_crypto_columns', '')
            t_crypto_rows = request.form.get('t_crypto_rows', '')
            t_crypto_cipher = (False, True)[request.form.get('t_crypto_cipher', '') == u'y']
            t_relic1 = request.form.get('t_relic1', '')
            t_relic2 = request.form.get('t_relic2', '')
            t_park = (False, True)[request.form.get('t_park', '') == u'y']
            a_score = request.form.get('a_score', '')
            t_score = request.form.get('t_score', '')
            total_score = request.form.get('total_score', '')
            match_notes = request.form.get('match_notes', '')

            matchscore = Scoring(
                competitions=comp,
                teams=team,
                match_number=match_number,
                a_hit_jewel=a_hit_jewel,
                a_glyphs_delivered=a_glyphs_delivered,
                a_glyph_correct=a_glyph_correct,
                a_park=a_park,
                t_glyphs_delivered=t_glyphs_delivered,
                t_crypto_columns=t_crypto_columns,
                t_crypto_rows=t_crypto_rows,
                t_crypto_cipher=t_crypto_cipher,
                t_relic1=t_relic1,
                t_relic2=t_relic2,
                t_park=t_park,
                a_score=a_score,
                t_score=t_score,
                total_score=total_score,
                match_notes=match_notes,
                timestamp=datetime.datetime.now())

            db.session.add(matchscore)
            db.session.commit()

            flash('Score Added Successfully')
            return redirect(url_for('scoring'))

    elif request.method == 'GET':
        matches = db.session.query(Scoring).filter(
        Scoring.competitions == comp).all()
        return render_template('scoring.html',
                           action='Add', form=form, matches=matches)


@app.route('/scoring/delete/<int:id>', methods=['GET'])
@login_required
def delete_match_record(id):
    record = Scoring.query.get(id)
    if record is None:
        abort(404)
    db.session.delete(record)
    db.session.commit()

    flash('Match record deleted.')
    return redirect(url_for('scoutinglinks'))


@app.route('/scouting/', defaults={'comp': cur_comp},
           methods=['GET', 'POST'])
@app.route('/scouting/competitions/<int:comp>', methods=['GET', 'POST'])
@login_required
def scouting(comp):
    form = ScoutingForm(request.values)

    sql_text = '''
      select
        t.id, t.number, t.name
      from
        CompetitionTeams ct
      inner join
        Teams t on ct.teams = t.id
      left join
        Scouting st on t.id = st.teams
      where
        st.id is NULL and ct.competitions = {}
      order by
        t.number
      asc'''.format(comp)
    result = db.engine.execute(sql_text)

    form.team.choices = [(a.id,
                          "{}: {}".format(a.number, a.name)) for a in result]

    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('scouting.html', form=form)
        else:
            # Put Code to process form and add to DB here
            team = request.form.get('team', '')
            a_jewel = (False, True)[request.form.get('a_jewel', '') == u'y']
            a_glyphs = request.form.get('a_glyphs', '')
            a_glyph_correct = (False, True)[request.form.get('a_glyphs_correct', '') == u'y']
            a_park = (False, True)[request.form.get('a_park', '') == u'y']
            t_glyphs = request.form.get('t_glyphs', '')
            t_crypto_columns = request.form.get('t_crypto_columns', '')
            t_crypto_rows = request.form.get('t_crypto_rows', '')
            t_crypto_cipher = (False, True)[request.form.get('t_crypto_cipher', '') == u'y']
            t_relics = request.form.get('t_relic_zone', '')
            t_relic1 = request.form.get('t_relic1', '')
            t_relic2 = request.form.get('t_relic2', '')
            t_park = (False, True)[request.form.get('t_park', '') == u'y']
            score_projection = request.form.get('score_projection', '')
            notes = request.form.get('notes', '')

            scouting_data = Scouting(
                competitions=comp,
                teams=team,
                a_jewel=a_jewel,
                a_glyphs=a_glyphs,
                a_glyph_correct=a_glyph_correct,
                a_park=a_park,
                t_glyphs=t_glyphs,
                t_crypto_columns=t_crypto_columns,
                t_crypto_rows=t_crypto_rows,
                t_crypto_cipher=t_crypto_cipher,
                t_relics=t_relics,
                t_relic1=t_relic1,
                t_relic2=t_relic2,
                t_park=t_park,
                score_projection=score_projection,
                notes=notes,
                timestamp=datetime.datetime.now())

            db.session.add(scouting_data)
            db.session.commit()

            flash('Pit scouting data added successfully')
            return redirect(url_for('scouting'))

    elif request.method == 'GET':
        records = db.session.query(Scouting).filter(
            Scouting.competitions == comp).all()
        return render_template('scouting.html', form=form, records=records)


@app.route('/scouting/delete/<int:id>', methods=['GET'])
@login_required
def delete_scouting_record(id):
    record = Scouting.query.get(id)
    if record is None:
        abort(404)
    db.session.delete(record)
    db.session.commit()

    flash('Scouting record deleted.')
    return redirect(url_for('scoutinglinks'))


@app.route('/scoutinglinks', methods=['GET'])
@login_required
def scoutinglinks():
    return render_template('scoutinglinks.html')


@app.route('/sponsors', methods=['GET'])
def sponsors():
    return render_template('sponsors.html')


@app.route('/teams', methods=['GET', 'POST'])
@login_required
def teams():

    form = TeamForm()

    teams = db.session.query(Teams).order_by(Teams.number).all()

    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('teams.html', teams=teams, form=form)
        else:
            newteam = Teams(number=form.number.data,
                            name=form.name.data,
                            timestamp=datetime.datetime.now())
            db.session.add(newteam)
            db.session.commit()

            flash('Team successfully added.')
            return redirect(url_for('teams'))

    elif request.method == 'GET':
        return render_template('teams.html', teams=teams, form=form)


@app.route('/teams/<int:id>', methods=['GET'])
@login_required
def team(id):
    team = db.session.query(Teams).filter(Teams.id == id).all()
    competitions = db.session.query(Competitions).filter(Teams.id == id).all()

    return render_template('team.html',
                           id=id,
                           team=team,
                           competitions=competitions)


@app.route('/teams/<int:team_id>/comp/<int:comp_id>', methods=['GET'])
@login_required
def team_scores_by_comp(team_id, comp_id):
    team = db.session.query(Teams).filter(Teams.id == team_id).all()
    comp = db.session.query(
        Competitions).filter(Competitions.id == comp_id).all()
    match_scores = db.session.query(
        Scoring).filter(
        and_(Scoring.teams == team_id,
             Scoring.competitions == comp_id)).all()
    pit_scouting = db.session.query(
        Scouting).filter(
        and_(Scouting.teams == team_id,
             Scouting.competitions == comp_id)).all()

    return render_template('team_scores.html',
                           team_id=team_id,
                           comp_id=comp_id,
                           team=team,
                           comp=comp,
                           match_scores=match_scores,
                           pit_scouting=pit_scouting)


@app.route('/teams/delete/<int:id>', methods=['GET'])
@login_required
def delete_team_entry(id):

    team = Teams.query.get(id)
    if team is None:
        abort(404)
    db.session.delete(team)
    db.session.commit()

    flash('Team deleted.')
    return redirect(url_for('teams'))
