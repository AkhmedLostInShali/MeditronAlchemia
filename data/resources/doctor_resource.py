from random import choices
from string import digits, ascii_letters

from flask import jsonify, request
from flask_login import login_required, current_user
from flask_restful import abort, Resource
from .. import db_session, my_parsers
from ..doctors import Doctor
import logging

logging.basicConfig(level=logging.INFO)

parser = my_parsers.DoctorParser()


def abort_if_doctor_not_found(doctors_id):
    session = db_session.create_session()
    doctor = session.query(Doctor).get(doctors_id)
    if not doctor:
        abort(404, message=f"Doctor {doctors_id} not found")


class DoctorsResource(Resource):
    @login_required
    def get(self, doctors_id):
        if current_user.id != doctors_id:
            return abort(403)
        abort_if_doctor_not_found(doctors_id)
        db_sess = db_session.create_session()
        doctor = db_sess.query(Doctor).get(doctors_id)
        doctor_dict = doctor.to_dict(only=('id', 'surname', 'name', 'email', 'hashed_password'))
        return jsonify({'doctor': doctor_dict})

    def delete(self, doctors_id):
        abort_if_doctor_not_found(doctors_id)
        db_sess = db_session.create_session()
        doctor = db_sess.query(Doctor).get(doctors_id)
        db_sess.delete(doctor)
        db_sess.commit()
        return jsonify({'success': 'OK'})

    def put(self, doctors_id):
        abort_if_doctor_not_found(doctors_id)
        if not request.json:
            return jsonify({'error': 'Empty request'})
        db_sess = db_session.create_session()
        if request.json.get('id') and request.json.get('id') in [user.id for user in db_sess.query(Doctor).all()]:
            return jsonify({'error': 'Id already exists'})
        if request.json.get('email') and request.json.get('email') in [user.email for user
                                                                       in db_sess.query(Doctor).all()]:
            return jsonify({'error': 'email already exists'})
        doctor = db_sess.query(Doctor).get(doctors_id)
        doctor.email = request.json['email'].lower() if request.json.get('email') else doctor.email
        doctor.surname = request.json['surname'] if request.json.get('surname') else doctor.surname
        doctor.name = request.json['name'] if request.json.get('name') else doctor.name
        if request.json.get('password') and request.json.get('password_again'):
            if request.json['password'] != request.json['password_again']:
                return jsonify({'error': "Passwords doesn't match"})
            doctor.set_password(request.json.get('password'))
        elif request.json.get('password') or request.json.get('password_again'):
            return jsonify({'error': "Requires both of 'password' and 'password again' or none of them"})
        db_sess.commit()
        return jsonify({'success': 'OK'})


class DoctorsListResource(Resource):
    # def get(self):  # не требуется
    #     db_sess = db_session.create_session()
    #     doctors = db_sess.query(Doctor).all()
    #     return jsonify({'doctors': [doctor.to_dict(only=('id', 'surname', 'name'))
    #                               for doctor in doctors]})

    def post(self):
        args = parser.parse_args()
        if request.json['password'] != request.json['password_again']:
            return jsonify({'error': "Passwords doesn't match"})
        db_sess = db_session.create_session()
        # if request.json.get('id') and request.json.get('id') in [doctor.id for doctor in db_sess.query(Doctor).all()]:
        #     return jsonify({'error': 'Id already exists'})  # заменить генератором айдишника
        if request.json.get('email') in [doctor.email for doctor in db_sess.query(Doctor).all()]:
            return jsonify({'error': 'Email already exists'})

        doctor = Doctor()
        rand_id = ''.join(choices(digits + ascii_letters + '-_', k=8))
        while rand_id in db_sess.query(Doctor.id).all():
            rand_id = ''.join(choices(digits + ascii_letters + '-_', k=8))
        doctor.id = rand_id
        doctor.email = args['email'].lower()
        doctor.surname = args['surname']
        doctor.name = args['name']
        doctor.set_password(args['password'])

        db_sess.add(doctor)
        db_sess.commit()
        return jsonify({
            'success': 'OK',
            'email': doctor.email
        })
