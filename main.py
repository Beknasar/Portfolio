import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import smtplib

app = Flask(__name__)
app.app_context().push()

# #CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

my_email = os.environ.get('EMAIL')
my_password = os.environ.get('PASSWORD')


# CONFIGURE TABLE
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(150))
    img_url = db.Column(db.String(250), unique=True, nullable=False)

    def __repr__(self):
        return f"{self.title}"


db.create_all()
projects = db.session.query(Project).all()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form
        for key, value in request.form.items():
            print(f"{key}: {value}")

        with smtplib.SMTP("smtp.mail.ru") as connection:
            connection.starttls()
            connection.login(user=my_email, password=my_password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs='680633@gmail.com',
                msg=f"Subject:New Message\n\nName: {data['username']}\nEmail: {data['email']}\nPhone: {data['phone']}\nMessage:\n{data['message']}"
            )
        return redirect(url_for('index'))
    return render_template('index.html', all_projects=projects[:4])


@app.route('/all_projects')
def show_all_projects():
    return render_template('all_projects.html', all_projects=projects)


@app.route('/project/<int:project_id>')
def show_project(project_id):
    requested_project = db.session.query(Project).get(project_id)
    return render_template('project_view.html', project=requested_project)


if __name__ == '__main__':
    app.run(debug=True)
