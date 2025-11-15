import datetime
from email.policy import default

from flask_restful import reqparse


class PublicationParser(reqparse.RequestParser):
    def __init__(self):
        super().__init__()
        self.add_argument('id', required=False, type=int)
        self.add_argument('title', required=True)
        self.add_argument('photo', required=True)
        self.add_argument('description', required=False)
        self.add_argument('reported', type=bool, required=False)
        self.add_argument('publication_date', required=False, type=datetime.datetime)
        self.add_argument('author', required=True, type=int)


class DoctorParser(reqparse.RequestParser):
    def __init__(self):
        super().__init__()
        self.add_argument('id', required=False)
        self.add_argument('email', required=True)
        self.add_argument('password', required=True)
        self.add_argument('password_again', required=True)
        self.add_argument('surname', required=False)
        self.add_argument('name', required=False)
        self.add_argument('remember_me', default=False, required=False, type=bool)


class MessageParser(reqparse.RequestParser):
    def __init__(self):
        super().__init__()
        self.add_argument('id', required=False, type=int)
        self.add_argument('text', required=True)
        self.add_argument('send_time', required=False, type=datetime.datetime)
        self.add_argument('sender_id', required=True, type=int)
        self.add_argument('receiver_id', required=True, type=int)


class CommentParser(reqparse.RequestParser):
    def __init__(self):
        super().__init__()
        self.add_argument('id', required=False, type=int)
        self.add_argument('text', required=True)
        self.add_argument('send_time', required=False, type=datetime.datetime)
        self.add_argument('sender', required=True, type=int)
        self.add_argument('receiver', required=True, type=int)
