from flask import url_for
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash


class Patient(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'patients'

    id = sqlalchemy.Column(sqlalchemy.String(8),
                           primary_key=True, unique=True)
    nickname = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    doctors_id = sqlalchemy.Column(sqlalchemy.String(8), sqlalchemy.ForeignKey('doctors.id'))
