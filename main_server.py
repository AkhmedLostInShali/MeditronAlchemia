from flask import Flask, jsonify, request, render_template, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_restful import Api
from requests import post, get
from sqlalchemy import desc

import predict_module.data_controller
from data import db_session
from data.forms.login import LoginForm

from data.models.doctors import Doctor
from data.models.patient_entries import PatientEntry
from data.models.patients import Patient

from data.resources import doctor_resource, patient_resource, entry_resource, my_parsers

import logging

from data.resources.doctor_resource import DoctorsListResource, abort_if_doctor_not_found
from predict_module import data_controller

logging.basicConfig(level=logging.WARNING)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'almost_secret_key' # закрыть от гита, если будем лить
path = 'http://localhost:8080'
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)

doctor_parser = my_parsers.DoctorParser()


def main():
    db_session.global_init()  # добавить название БД
    # api.add_resource(doctor_resource.DoctorsResource, '/api/doctors')  доп модули на будущее
    # api.add_resource(patient_resource.PatientsResource, '/api/patients/<string:patients_id>')
    api.add_resource(doctor_resource.DoctorsListResource, '/api/doctors')
    api.add_resource(patient_resource.PatientsListResource, '/api/patients')
    api.add_resource(entry_resource.EntriesListResource, '/api/entries')
    api.add_resource(entry_resource.EntriesAddResource, '/api/add_entries')
    app.run(port=8080, host='127.0.0.1')


@login_manager.user_loader
def load_user(doctor_id):
    db_sess = db_session.create_session()
    return db_sess.get(Doctor, doctor_id)


@app.route('/api/login', methods=['POST'])
def api_login():
    db_sess = db_session.create_session()
    email = request.json.get('email').lower()
    password = request.json.get('password')
    remember_me = request.json.get('remember_me')
    doctor = db_sess.query(Doctor).filter_by(email=email).first()
    if not doctor:
        return jsonify({'error': 'No doctor with such email'})
    if doctor.check_password(password=password):
        login_user(doctor, remember=remember_me)
        return jsonify({'success': 'OK'})
    return jsonify({'error': 'Incorrect password'})


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        doctor = db_sess.query(Doctor).filter_by(email=form.email.data).first()
        if not doctor:
            return jsonify({'error': 'No doctor with such email'})
        if doctor.check_password(password=form.password.data):
            login_user(doctor, remember=form.remember_me.data)
            return redirect("/")
        return jsonify({'error': 'Incorrect password'})

    return render_template("login.html", title="Авторизация", form=form)


@login_required
@app.route('/', methods=['GET', 'POST'])
@app.route('/<patient_id>', methods=['GET', 'POST'])
def main_page(patient_id=''):
    abort_if_doctor_not_found(current_user.id)
    db_sess = db_session.create_session()

    doctor = db_sess.get(Doctor, current_user.id)
    doctors_info = doctor.to_dict(only=('id', 'surname', 'name', 'email'))

    patients = db_sess.query(Patient).filter_by(doctors_id=current_user.id).all()
    patients_info = {patient.id: patient.nickname for patient in patients}
    prognosis = {}

    if patient_id:
        entries = db_sess.query(PatientEntry).filter_by(patient_id=patient_id).order_by(desc(PatientEntry.entry_date)).all()
        entries_info = [entry.to_dict(only=('id', 'legacy', 'entry_date', 'age', 'hr', 'her2', 'mp', 'race', 'menopausal_status'))
                        for entry in entries]
        if len(entries_info) > 0:
            prog_entry = entries_info[0]
            hr = 1 if prog_entry['hr'] else 0
            her2 = 1 if prog_entry['her2'] else 0
            mp = 1 if prog_entry['mp'] else 0
            menopausal_status = prog_entry['menopausal_status'].lower()
            prognosis = data_controller.get_chances(hr, her2, mp, menopausal_status)
    else:
        entries_info = []

    return render_template("main_page.html",
                           title="BreastAlchemy",
                           doctors_info=doctors_info,
                           patients_info=patients_info,
                           patient_id=patient_id,
                           entries_info=entries_info,
                           prognosis=prognosis
                           )


@login_required
@app.route('/api/logout')
def logout():
    logout_user()
    return jsonify({'success': 'OK'})


@app.route('/api/registration', methods=['POST'])
def registration():
    email = request.json.get('email').lower()
    password = request.json.get('password')
    password_again = request.json.get('password_again')
    name = request.json.get('name')
    surname = request.json.get('surname')
    remember_me = request.json.get('remember_me')
    req = post(path + '/api/doctors',
               json={'email': email,
                     'password': password,
                     'password_again': password_again,
                     'name': name,
                     'surname': surname}).json()
    if 'error' in req:
        return req
    logging.info(str(req))
    db_sess = db_session.create_session()
    doctor = db_sess.query(Doctor).filter_by(email=req['email']).first()
    login_user(doctor, remember=remember_me)
    return jsonify({'success': 'OK'})


if __name__ == '__main__':
    main()
