from main import db


class Student(db.Model):
    __tablename__ = "student"
    student_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    roll_number = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)

    def __str__(self):
        return str(self.student_id) + "id and name : " + self.first_name
