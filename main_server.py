from flask import Flask, jsonify, request
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_restful import Api
from requests import post

from data import db_session

from data.models.doctors import Doctor

from data.resources import doctor_resource, patient_resource, entry_resource, my_parsers

import logging

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
    app.run(port=8080, host='127.0.0.1')


@login_manager.user_loader
def load_user(doctor_id):
    db_sess = db_session.create_session()
    return db_sess.get(Doctor, doctor_id)


@app.route('/api/login', methods=['POST'])
def login():
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
