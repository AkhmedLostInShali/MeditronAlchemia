from flask_restful import reqparse


class DoctorParser(reqparse.RequestParser):
    def __init__(self):
        super().__init__()
        self.add_argument('email', required=True)
        self.add_argument('password', required=True)
        self.add_argument('password_again', required=True)
        self.add_argument('surname', required=False)
        self.add_argument('name', required=False)
        self.add_argument('remember_me', default=False, required=False, type=bool)


class PatientEntryParser(reqparse.RequestParser):
    def __init__(self):
        super().__init__()
        # self.add_argument('entry_date', required=False, type=datetime.date)  дата будет устанавливаться с помощью today()
        self.add_argument('age', required=True, type=int)
        self.add_argument('legacy', required=True, type=bool)
        self.add_argument('hr', required=True, type=bool)
        self.add_argument('her2', required=True, type=bool)
        self.add_argument('race', required=True)
        self.add_argument('menopausal_status', required=True)
        self.add_argument('patient_id', required=True)
