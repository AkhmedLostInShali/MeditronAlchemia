from datetime import date

import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class PatientEntry(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'patient_entries'

    id = sqlalchemy.Column(sqlalchemy.String(8),
                           primary_key=True, unique=True)
    legacy = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    entry_date = sqlalchemy.Column(sqlalchemy.Date, default=date.today())
    patient_id = sqlalchemy.Column(sqlalchemy.String(8), sqlalchemy.ForeignKey('patients.id'))
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    hr = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)
    her2 = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)
    race = sqlalchemy.Column(sqlalchemy.String, default='White')
    menopausal_status = sqlalchemy.Column(sqlalchemy.String, nullable=False)
