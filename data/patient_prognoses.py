from datetime import date

from flask import url_for
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash


class PatientPrognosis(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'patient_prognoses'

    id = sqlalchemy.Column(sqlalchemy.String(8),
                           primary_key=True, unique=True)
    optimal = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    entry_date = sqlalchemy.Column(sqlalchemy.Date, default=date.today())
    patient_id = sqlalchemy.Column(sqlalchemy.String(8), sqlalchemy.ForeignKey('doctors.id'))
    entry_id = sqlalchemy.Column(sqlalchemy.String(8), sqlalchemy.ForeignKey('patient_entries.id'))
#   Тут определиться какие вообще колонки
