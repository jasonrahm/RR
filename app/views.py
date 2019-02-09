from app import app, mysql
from flask import render_template, flash, redirect, url_for, session, request
from forms import RegisterForm, ScoutingForm, ScoutingReportForm, ScoringForm, ScoringEditForm, ScoringReportForm
from functools import wraps
from passlib.hash import sha256_crypt


# Check login status decorator
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))

    return wrap


# Pages w/o db access or forms

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


@app.route('/resources', methods=['GET'])
def resources():
    return render_template('resources.html')


@app.route('/robots', methods=['GET'])
def robots():
    return render_template('robots.html')


@app.route('/sponsors', methods=['GET'])
def sponsors():
    return render_template('sponsors.html')


# Pages with db access and/or forms

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']

        cur = mysql.connection.cursor()
        result = cur.execute('SELECT * FROM users WHERE username = %s', [username])

        if result > 0:
            data = cur.fetchone()
            password = data['password']

            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))

            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)

            cur.close()

        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')


@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)",
                    (name, email, username, password))

        mysql.connection.commit()
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/dashboard')
@is_logged_in
def dashboard():

    cur = mysql.connection.cursor()
    scouting_result = cur.execute('SELECT * FROM scouting')
    if scouting_result > 0:
        scouting_records = cur.fetchall()

    scoring_result = cur.execute('SELECT * FROM scoring')
    if scoring_result > 0:
        scoring_records = cur.fetchall()

    if scouting_result > 0 and scoring_result > 0:
        return render_template('dashboard.html', scouting_records=scouting_records, scoring_records=scoring_records)
    elif scouting_result > 0:
        return render_template('dashboard.html', scouting_records=scouting_records)
    elif scoring_result > 0:
        return render_template('dashboard.html', scoring_records=scoring_records)
    else:
        msg = 'No Records Found'
        return render_template('dashboard.html', msg=msg)

    cur.close()


@app.route('/add_scouting_record', methods=['GET', 'POST'])
@is_logged_in
def add_scouting_record():
    form = ScoutingForm(request.form)
    if request.method == 'POST' and form.validate():
        team_number = form.team_number.data
        team_name = form.team_name.data
        comp = form.comp.data
        a_lander_loc = form.a_lander_loc.data
        a_landed = form.a_landed.data
        a_landed_rel = form.a_landed_rel.data
        a_sample = form.a_sample.data
        a_sample_rel = form.a_sample_rel.data
        a_marker = form.a_marker.data
        a_marker_rel = form.a_marker_rel.data
        a_park = form.a_park.data
        a_park_rel = form.a_park_rel.data
        a_compatible = form.a_compatible.data
        a_notes = form.a_notes.data
        t_score_lander = form.t_score_lander.data
        t_mineral = form.t_mineral.data
        t_cycle = form.t_cycle.data
        t_load = form.t_load.data
        t_score_position = form.t_score_position.data
        t_notes = form.t_notes.data
        e_hang = form.e_hang.data
        e_hang_rel = form.e_hang_rel.data
        e_hangtime = form.e_hangtime.data
        e_notes = form.e_notes.data

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO scouting(scout, team_number, team_name, comp, a_lander_loc, a_landed, '
                    'a_landed_rel, a_sample, a_sample_rel, a_marker, a_marker_rel, a_park, a_park_rel, a_compatible,'
                    'a_notes,  t_score_lander, t_mineral, t_cycle, t_load, t_score_position, t_notes, e_hang,'
                    'e_hang_rel, e_hangtime, e_notes ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,'
                    ' %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (session['username'], team_number, team_name, comp,
                                                                     a_lander_loc, a_landed, a_landed_rel, a_sample,
                                                                     a_sample_rel, a_marker, a_marker_rel, a_park,
                                                                     a_park_rel, a_compatible, a_notes, t_score_lander,
                                                                     t_mineral, t_cycle, t_load, t_score_position,
                                                                     t_notes, e_hang, e_hang_rel, e_hangtime, e_notes))
        mysql.connection.commit()
        cur.close()

        flash('Scouting record created', 'success')

        return redirect(url_for('dashboard'))


    return render_template('add_scouting_record.html', form=form)


@app.route('/edit_scouting_record/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_scouting_record(id):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM scouting WHERE id = %s", [id])
    scouting_record = cur.fetchone()

    form = ScoutingForm(request.form)
    form.team_number.data = scouting_record['team_number']
    form.team_name.data = scouting_record['team_name']
    form.comp.data = scouting_record['comp']
    form.a_lander_loc.data = scouting_record['a_lander_loc']
    form.a_landed.data = scouting_record['a_landed']
    form.a_landed_rel.data = scouting_record['a_landed_rel']
    form.a_sample.data = scouting_record['a_sample']
    form.a_sample_rel.data = scouting_record['a_sample_rel']
    form.a_marker.data = scouting_record['a_marker']
    form.a_marker_rel.data = scouting_record['a_marker_rel']
    form.a_park.data = scouting_record['a_park']
    form.a_park_rel.data = scouting_record['a_park_rel']
    form.a_compatible.data = scouting_record['a_compatible']
    form.a_notes.data = scouting_record['a_notes']
    form.t_score_lander.data = scouting_record['t_score_lander']
    form.t_mineral.data = scouting_record['t_mineral']
    form.t_cycle.data = scouting_record['t_cycle']
    form.t_load.data = scouting_record['t_load']
    form.t_score_position.data = scouting_record['t_score_position']
    form.t_notes.data = scouting_record['t_notes']
    form.e_hang.data = scouting_record['e_hang']
    form.e_hang_rel.data = scouting_record['e_hang_rel']
    form.e_hangtime.data = scouting_record['e_hangtime']
    form.e_notes.data = scouting_record['e_notes']

    if request.method == 'POST' and form.validate():
        # match_number = request.form.get('match_number', '')
        # a_hit_jewel = (False, True)[request.form.get('a_hit_jewel', '') == u'y']
        team_number = request.form['team_number']
        team_name = request.form['team_name']
        comp = request.form['comp']
        a_lander_loc = request.form['a_lander_loc']
        a_landed = (False, True)[request.form.get('a_landed', '') == u'y']
        a_landed_rel = request.form['a_landed_rel']
        a_sample = (False, True)[request.form.get('a_sample', '') == u'y']
        a_sample_rel = request.form['a_sample_rel']
        a_marker = (False, True)[request.form.get('a_marker', '') == u'y']
        a_marker_rel = request.form['a_marker_rel']
        a_park = (False, True)[request.form.get('a_park', '') == u'y']
        a_park_rel = request.form['a_park_rel']
        a_compatible = request.form['a_compatible']
        a_notes = request.form['a_notes']
        t_score_lander = (False, True)[request.form.get('t_score_lander', '') == u'y']
        t_mineral = request.form['t_mineral']
        t_cycle = request.form['t_cycle']
        t_load = request.form['t_load']
        t_score_position = request.form['t_score_position']
        t_notes = request.form['t_notes']
        e_hang = (False, True)[request.form.get('e_hang', '') == u'y']
        e_hang_rel = request.form['e_hang_rel']
        e_hangtime = request.form['e_hangtime']
        e_notes = request.form['e_notes']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE scouting SET team_number=%s, team_name=%s, comp=%s, a_lander_loc=%s, a_landed=%s, "
                    "a_landed_rel=%s, a_sample=%s, a_sample_rel=%s, a_marker=%s, a_marker_rel=%s, a_park=%s,"
                    "a_park_rel=%s, a_compatible=%s, a_notes=%s, t_score_lander=%s, t_mineral=%s, t_cycle=%s,"
                    "t_load=%s, t_score_position=%s, t_notes=%s, e_hang=%s, e_hang_rel=%s, e_hangtime=%s, e_notes=%s "
                    "WHERE id = %s", (team_number, team_name, comp, a_lander_loc, a_landed, a_landed_rel, a_sample,
                                      a_sample_rel, a_marker, a_marker_rel, a_park, a_park_rel, a_compatible, a_notes,
                                      t_score_lander, t_mineral, t_cycle, t_load, t_score_position, t_notes, e_hang,
                                      e_hang_rel, e_hangtime, e_notes, id))
        mysql.connection.commit()

        cur.close()

        flash('Scouting record updated', 'success')

        return redirect(url_for('dashboard'))

    return render_template('edit_scouting_record.html', form=form)



@app.route('/delete_scouting_record/<string:id>', methods=['POST'])
@is_logged_in
def delete_scouting_record(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM scouting WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()

    flash('Scouting record deleted', 'success')
    return redirect(url_for('dashboard'))


@app.route('/run_scouting_report', methods=['GET', 'POST'])
@is_logged_in
def run_scouting_report():
    form = ScoutingReportForm(request.form)
    if request.method == 'POST':
        competition = request.form['comp']
        landing = request.form['landing']
        landing_rel = (False, True)[request.form.get('landing_rel', '') == u'y']
        sampling = request.form['sampling']
        sampling_rel = (False, True)[request.form.get('sampling_rel', '') == u'y']
        marker = request.form['marker']
        marker_rel = (False, True)[request.form.get('marker_rel', '') == u'y']
        parking = request.form['parking']
        parking_rel = (False, True)[request.form.get('parking_rel', '') == u'y']
        compatibility = request.form['compatibility']
        lander_scoring = request.form['lander_scoring']
        cycle_time = request.form['cycle_time']
        load_size = request.form['load_size']
        hanging = request.form['hanging']
        hanging_rel = (False, True)[request.form.get('hanging_rel', '') == u'y']

        sql_text = '''select comp, team_number, team_name,
                        (a_landed * {}) * (1 + a_landed_rel * {}) +
                        (a_sample * {}) * (1 + a_sample_rel * {}) +
                        (a_marker * {}) * (1 + a_marker_rel * {}) +
                        (a_park * {}) * (1 + a_park_rel * {}) + 
                        (a_compatible * {}) + 
                        (t_score_lander * {}) +
                        (t_cycle * {}) + 
                        (t_load * {}) +
                        (e_hang * {}) * (1 + e_hang_rel * {})
                      AS Score
                      FROM scouting
                      WHERE comp = '{}'
                      ORDER BY Score
                      DESC'''.format(int(landing),
                                 1 if landing_rel is True else 0,
                                 int(sampling),
                                 1 if sampling_rel is True else 0,
                                 int(marker),
                                 1 if marker_rel is True else 0,
                                 int(parking),
                                 1 if parking_rel is True else 0,
                                 int(compatibility),
                                 int(lander_scoring),
                                 int(cycle_time),
                                 int(load_size),
                                 int(hanging),
                                 1 if hanging_rel is True else 0,
                                 competition)
        cur = mysql.connection.cursor()
        result = cur.execute(sql_text)
        if result > 0:
            records = cur.fetchall()
            teams = []
            for row in records:
                teams.append([row['comp'], row['team_number'], row['team_name'], row['Score']])
            session['scouting_report'] = teams
            flash('Report run succesfully', 'success')
            return redirect(url_for('scouting_report'))
        else:
            flash('No records found', 'error')

        cur.close()

    return render_template('run_scouting_report.html', form=form)


@app.route('/scouting_report', methods=['GET'])
@is_logged_in
def scouting_report():
    data = session['scouting_report']
    if data == '':
        redirect(url_for('run_scouting_report'))
    else:
        return render_template('scouting_report.html', data=data)


@app.route('/add_scoring_record', methods=['GET', 'POST'])
@is_logged_in
def add_scoring_record():
    form = ScoringForm(request.form)

    if request.method == 'POST':
        comp = form.comp.data
        match = form.match.data
        r1_team = form.r1.data
        r2_team = form.r2.data
        a_r1_land = form.a_r1_land.data
        a_r1_sample = form.a_r1_sample.data
        a_r1_depot = form.a_r1_depot.data
        a_r1_park = form.a_r1_park.data
        a_r1_auto_score = form.a_r1_auto_score.data
        a_r1_notes = form.a_r1_notes.data
        a_r2_land = form.a_r2_land.data
        a_r2_sample = form.a_r2_sample.data
        a_r2_depot = form.a_r2_depot.data
        a_r2_park = form.a_r2_park.data
        a_r2_auto_score = form.a_r2_auto_score.data
        a_r2_notes = form.a_r2_notes.data
        t_r1_lander_minerals = form.t_r1_lander_minerals.data
        t_r1_depot_minerals = form.t_r1_depot_minerals.data
        t_r1_teleop_score = form.t_r1_teleop_score.data
        t_r2_lander_minerals = form.t_r2_lander_minerals.data
        t_r2_depot_minerals = form.t_r2_depot_minerals.data
        t_r2_teleop_score = form.t_r2_teleop_score.data
        e_r1_latched = form.e_r1_latched.data
        e_r1_park = form.e_r1_park.data
        e_r1_endgame_score = form.e_r1_endgame_score.data
        e_r2_latched = form.e_r2_latched.data
        e_r2_park = form.e_r2_park.data
        e_r2_endgame_score = form.e_r2_endgame_score.data
        r1_total_score = form.r1_total_score.data
        r2_total_score = form.r2_total_score.data
        e_r1_notes = form.e_r1_notes.data
        e_r2_notes = form.e_r2_notes.data

        # cols = '(comp, match_num, team_num, land, sample, depot, a_park, a_score, crater_minerals, depot_minerals, t_score, latched, e_park, e_score, score)'


        sql_text = "INSERT INTO scoring(scout, comp, match_num, team_num, land, sample, depot, a_park, a_score, a_notes, lander_minerals, depot_minerals, t_score, latched, e_park, e_score, score, e_notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        lstval = [(session['username'], comp, match, int(r1_team), int(a_r1_land), int(a_r1_sample), int(a_r1_depot), int(a_r1_park),
                 int(a_r1_auto_score), a_r1_notes, int(t_r1_lander_minerals),
                 int(t_r1_depot_minerals), int(t_r1_teleop_score), int(e_r1_latched), int(e_r1_park),
                 int(e_r1_endgame_score), int(r1_total_score), e_r1_notes),
                 (session['username'], comp, match, int(r2_team), int(a_r2_land), int(a_r2_sample), int(a_r2_depot), int(a_r2_park),
                 int(a_r2_auto_score), a_r2_notes, int(t_r2_lander_minerals),
                 int(t_r2_depot_minerals), int(t_r2_teleop_score), int(e_r2_latched), int(e_r2_park),
                 int(e_r2_endgame_score), int(r2_total_score), e_r2_notes)
                ]

        cur = mysql.connection.cursor()
        cur.executemany(sql_text, lstval)
        mysql.connection.commit()
        cur.close()

        flash('Scoring records created', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_scoring_record.html', form=form)


@app.route('/delete_scoring_record/<string:id>', methods=['POST'])
@is_logged_in
def delete_scoring_record(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM scoring WHERE id = %s", [id])
    mysql.connection.commit()
    cur.close()

    flash('Scoring record deleted', 'success')
    return redirect(url_for('dashboard'))


@app.route('/edit_scoring_record/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_scoring_record(id):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM scoring WHERE id = %s", [id])
    scoring_record = cur.fetchone()

    form = ScoringEditForm(request.form)
    form.comp.data = scoring_record['comp']
    form.match.data = scoring_record['match_num']
    form.team.data = scoring_record['team_num']
    form.a_land.data = scoring_record['land']
    form.a_sample.data = scoring_record['sample']
    form.a_depot.data = scoring_record['depot']
    form.a_park.data = scoring_record['a_park']
    form.a_score.data = scoring_record['a_score']
    form.a_notes.data = scoring_record['a_notes']
    form.t_lander_minerals.data = scoring_record['lander_minerals']
    form.t_depot_minerals.data = scoring_record['depot_minerals']
    form.t_score.data = scoring_record['t_score']
    form.e_latched.data = scoring_record['latched']
    form.e_park.data = scoring_record['e_park']
    form.e_score.data = scoring_record['e_score']
    form.total_score.data = scoring_record['score']
    form.e_notes.data = scoring_record['e_notes']

    if request.method == 'POST' and form.validate():
        comp = request.form['comp']
        match_num = request.form['match']
        team_num = request.form['team']
        land = (False, True)[request.form.get('a_land', '') == u'y']
        sample = (False, True)[request.form.get('a_sample', '') == u'y']
        depot = (False, True)[request.form.get('a_depot', '') == u'y']
        a_park = (False, True)[request.form.get('a_park', '') == u'y']
        a_score = request.form['a_score']
        a_notes = request.form['a_notes']
        lander_minerals = request.form['t_lander_minerals']
        depot_minerals = request.form['t_depot_minerals']
        t_score = request.form['t_score']
        latched = (False, True)[request.form.get('e_latched', '') == u'y']
        e_park = request.form['e_park']
        e_score = request.form['e_score']
        score = request.form['total_score']
        e_notes = request.form['e_notes']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE scoring SET comp=%s, match_num=%s, team_num=%s, land=%s, sample=%s, "
                    "depot=%s, a_park=%s, a_score=%s, a_notes=%s, lander_minerals=%s, depot_minerals=%s, "
                    "t_score=%s, latched=%s, e_park=%s, e_score=%s, score=%s, e_notes=%s "
                    "WHERE id = %s", (comp, match_num, team_num, land, sample, depot, a_park, a_score, a_notes, lander_minerals,
                                      depot_minerals, t_score, latched, e_park, e_score, score, e_notes, id))
        mysql.connection.commit()
        cur.close()

        flash('Scoring record updated', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_scoring_record.html', form=form)


@app.route('/run_scoring_report', methods=['GET', 'POST'])
@is_logged_in
def run_scoring_report():
    form = ScoringReportForm(request.form)

    if request.method == 'POST':
        comp = request.form['comp']

        cur = mysql.connection.cursor()
        cur.execute('SELECT DISTINCT team_num FROM scoring where comp=%s', [comp])
        teams = cur.fetchall()

        data = []
        for x in teams:
            cur.execute('SELECT team_num, avg(a_score), avg(t_score), avg(e_score), avg(score), max(score) '
                        'from scoring where team_num=%s and comp=%s', [x['team_num'], comp])
            result = cur.fetchall()
            for row in result:
                # Order: team, max score, avg score, avg auto score, avg teleop score, avg endgame score
                data.append([row['team_num'], row['max(score)'],
                             float(row['avg(score)']),
                             float(row['avg(a_score)']),
                             float(row['avg(t_score)']),
                             float(row['avg(e_score)'])]
                )

        cur.close()

        session['scoring_report'] = data

        flash('Scoring report ran successfully', 'success')

        return redirect(url_for('scoring_report'))


    return render_template('run_scoring_report.html', form=form)


@app.route('/scoring_report', methods=['GET'])
@is_logged_in
def scoring_report():
    data = session['scoring_report']
    if data == '':
        redirect(url_for('run_scoring_report'))
    else:
        return render_template('scoring_report.html', data=data)


@app.route('/team/<string:id>', methods=['GET'])
@is_logged_in
def team(id):

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM scouting where team_number=%s", [id])
    scouting_records = cur.fetchall()
    cur.execute("SELECT * FROM scoring where team_num=%s", [id])
    scoring_records = cur.fetchall()
    cur.close()

    return render_template('team.html', id=id, scouting_records=scouting_records, scoring_records=scoring_records)

