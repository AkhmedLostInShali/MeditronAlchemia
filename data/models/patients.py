import sqlalchemy
from sqlalchemy_serializer import SerializerMixin

from data.db_session import SqlAlchemyBase


class Patient(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'patients'

    id = sqlalchemy.Column(sqlalchemy.String(8),
                           primary_key=True, unique=True)
    nickname = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    doctors_id = sqlalchemy.Column(sqlalchemy.String(8), sqlalchemy.ForeignKey('doctors.id'))
