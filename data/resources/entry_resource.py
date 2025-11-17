import datetime
from random import choices
from string import digits, ascii_letters

from flask import jsonify, request
from flask_login import login_required, current_user
from flask_restful import abort, Resource
from .. import db_session
from . import my_parsers
from data.models.patients import Patient
from data.models.patient_entries import PatientEntry
import logging

logging.basicConfig(level=logging.INFO)

parser = my_parsers.PatientEntryParser()


def abort_if_entry_not_found(patients_id):
    session = db_session.create_session()
    patient = session.query(Patient).get(patients_id)
    if not patient:
        abort(404, message=f"Patient {patients_id} not found")


class EntriesListResource(Resource):
    @login_required
    def post(self):
        # if not request.is_json:
        #     return jsonify({'error': 'Request must be JSON'}), 415

        patient_id = request.json.get('patient_id')
        if not patient_id:
            return abort(404, message="Patient id not found")
        db_sess = db_session.create_session()
        entries = db_sess.query(PatientEntry).filter_by(patient_id=patient_id).all()
        out_dict = dict()
        for entry in entries:
            out_dict[entry.id] = entry.to_dict(only=('hr', 'her2', 'race', 'menopausal_status', 'entry_date'))
        return jsonify({
            'success': 'OK',
            'patients_id': current_user.id,
            'entries': out_dict
        })


class EntriesAddResource(Resource):
    @login_required
    def post(self):
        db_sess = db_session.create_session()
        args = parser.parse_args()

        entry = PatientEntry()
        rand_id = ''.join(choices(digits + ascii_letters + '-_', k=8))
        while rand_id in db_sess.query(Patient.id).all():
            rand_id = ''.join(choices(digits + ascii_letters + '-_', k=8))
        entry.id = rand_id
        entry.entry_date = datetime.date.today()
        entry.age = args['age']
        entry.legacy = args['legacy']
        entry.hr = args['hr']
        entry.her2 = args['her2']
        entry.race = args['race']
        entry.menopausal_status = args['menopausal_status']
        entry.patient_id = args['patient_id']

        db_sess.add(entry)
        db_sess.commit()
        return jsonify({'success': 'OK'})


# Скопировано с patient_resource.py, в случае чего тоже можно привести в силу
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
