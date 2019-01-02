from app import app, mysql
from flask import render_template, flash, redirect, url_for, session, logging, request
from forms import RegisterForm, ScoutingForm
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
        email = form.name.data
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
    result = cur.execute('SELECT * FROM scouting')

    if result > 0:
        records = cur.fetchall()
        return render_template('dashboard.html', records=records)
    else:
        msg = 'No Scouting Records Found'
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
