from datetime import date

from flask import url_for
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash


class PatientEntry(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'patient_entries'

    id = sqlalchemy.Column(sqlalchemy.String(8),
                           primary_key=True, unique=True)
    legacy = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    entry_date = sqlalchemy.Column(sqlalchemy.Date, default=date.today())
    patient_id = sqlalchemy.Column(sqlalchemy.String(8), sqlalchemy.ForeignKey('patients.id'))
#   Тут добавить оставшиеся миллиарды колонок
