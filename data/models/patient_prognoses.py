from datetime import date

import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class PatientPrognosis(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'patient_prognoses'

    id = sqlalchemy.Column(sqlalchemy.String(8),
                           primary_key=True, unique=True)
    optimal = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    entry_date = sqlalchemy.Column(sqlalchemy.Date, default=date.today())
    patient_id = sqlalchemy.Column(sqlalchemy.String(8), sqlalchemy.ForeignKey('doctors.id'))
    entry_id = sqlalchemy.Column(sqlalchemy.String(8), sqlalchemy.ForeignKey('patient_entries.id'))
#   Тут определиться какие вообще колонки
