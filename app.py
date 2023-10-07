from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect
from models import *
from forms import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pilot_key'
csrf = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbdbdb.db'
db.init_app(app)


# Не смог записать в БД без строк 14-15, иначе получал "OperationalError no such table: user". Не разобраться, в чём было дело.
with app.app_context():
    db.create_all()
    
        
# @app.cli.command("init-db")
# def init_db():
#     db.create_all()
#     print('OK')
    
@app.route('/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate:
        name = form.name.data
        surname = form.surname.data
        email = form.email.data
        password = form.password.data
        existing_user = User.query.filter(User.email == email or User.password == password).first()
        if existing_user:
            error_msg = 'Email or password already exixsts'
            form.name.errors.append(error_msg)
            return render_template('register.html', form = form)
        new_user = User(name=name, surname=surname, email=email, password=password)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return 'Successful registration.'
    return render_template('register.html', form = form)

if __name__ == '__main__':
    app.run(debug=True)