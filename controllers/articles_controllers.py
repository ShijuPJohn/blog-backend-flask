from flask import render_template, current_app as app

from main import db


@app.route("/")
def hello_world():
    return "Hello World"


# @app.route("/create")
# def student_create_get():
#     student = Student(roll_number="123A", first_name="SHIJU", last_name="JOHN")
#     db.session.add(student)
#     db.session.commit()
#     return str(student)
#
#
# @app.route("/fetch")
# def students_fetch_get():
#     students = Student.query.all()
#     return str(students[0])

# @app.route('/articles', methods=['GET'])
# def articles_get():
#     articles = Article.query.all()
#     for arti in articles:
#         print(arti.title)
#         print(arti.content)
#     return render_template("articles.html")