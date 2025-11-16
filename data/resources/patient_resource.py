import datetime
from random import choices
from string import digits, ascii_letters

from flask import jsonify, request
from flask_login import login_required, current_user
from flask_restful import abort, Resource
from .. import db_session, my_parsers
from ..patients import Patient
import logging

from ..doctors import Doctor
from .nickname_generator import generate_nickname

logging.basicConfig(level=logging.INFO)

parser = my_parsers.PublicationParser()


def abort_if_patients_not_found(patients_id):
    session = db_session.create_session()
    patient = session.query(Patient).get(patients_id)
    if not patient:
        abort(404, message=f"Patient {patients_id} not found")


# Я тут оставил базовые эндпойнты на случай если пригодятся. Эти работают с
# конкретным пациентом по его айди, и надо будет в строке подключения апи переменную сделать
#
# class PatientsResource(Resource):
    # def get(self, patients_id):
    # тогда abort_if_patients_not_found(patients_id) db_sess = db_session.create_session() patient = db_sess.query(
    # Patient).get(patients_id) out_dict = patient.to_dict(only=('id', 'nickname', 'doctors_id')) return jsonify({
    # 'patient': out_dict})

    # def delete(self, patients_id):
    #     abort_if_patients_not_found(patients_id)
    #     db_sess = db_session.create_session()
    #     patient = db_sess.query(Patient).get(patients_id)
    #     db_sess.delete(patient)
    #     db_sess.commit()
    #     return jsonify({'success': 'OK'})
    #
    # def put(self, patients_id):
    #     abort_if_patients_not_found(patients_id)
    #     if not request.json:
    #         return jsonify({'error': 'Empty request'})
    #     db_sess = db_session.create_session()
    #     if request.json.get('id') and request.json.get('id') in [patient.id for patient
    #                                                              in db_sess.query(Patient).all()]:
    #         return jsonify({'error': 'Id already exists'})
    #     patient = db_sess.query(Patient).get(patients_id)
    #     patient.id = request.json['id'] if request.json.get('id') else patient.id
    #     patient.nickname = request.json['nickname'] if request.json.get('nickname') else patient.nickname
    #     patient.doctors_id = request.json['doctors_id'] if request.json.get('doctors_id') else patient.doctors_id
    #     db_sess.commit()
    #     return jsonify({'success': 'OK'})


class PatientsListResource(Resource):
    @login_required
    def get(self):
        db_sess = db_session.create_session()
        patients = db_sess.query(Patient).filter(Patient.doctors_id == current_user.id).all()
        out_dict = dict()
        for patient in patients:
            out_dict[patient.id] = patient.nickname
        return jsonify({
            'success': 'OK',
            'doctors_id': current_user.id,
            'patients': out_dict
        })
    @login_required
    def post(self):
        db_sess = db_session.create_session()

        patient = Patient()
        rand_id = ''.join(choices(digits + ascii_letters + '-_', k=8))
        while rand_id in db_sess.query(Patient.id).all():
            rand_id = ''.join(choices(digits + ascii_letters + '-_', k=8))
        patient.id = rand_id
        rand_nickname = generate_nickname()
        while rand_nickname in db_sess.query(Patient.nickname).all():
            rand_nickname = generate_nickname()
        patient.nickname = rand_nickname
        patient.doctors_id = current_user.id

        db_sess.add(patient)
        db_sess.commit()
        return jsonify({'success': 'OK'})
