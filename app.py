from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from getting_id import get_id

app = Flask(__name__)

# say whether you are testing or want to push to heroku. change the variable 'env' to dev or prod
env = 'prod'

if env == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:kenny@localhost/kenny'
else:
    app.debug = False
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'postgres://tiufidaeyhwyjb:b67e03362847896afaa0b0d987704351c56455f618bef8a6f60dfb8cc6c424f0@ec2-174-129-253-45.compute-1.amazonaws.com:5432/d6rs2t6sltfo3c'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['NAME']
        _email = request.form['EMAIL']
        sender_message = request.form['MESSAGE']
        subject = request.form['SUBJECT']

        import smtplib, ssl
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        sender_email = "**************"
        receiver_email = "**************"
        password = "**************"

        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = receiver_email

        # Create HTML version of your message

        html = f"""\
        <html>
          <body style='font-family:Halyard; font-size:16px;'>
            <div style='border: 2px solid black; '>
            <p style=' margin:0; padding:14px; background-color:gray; display:inherit'>{sender_message}</p><p style='margin:0; padding:14px; background-color:lightgreen; display:inherit'>--{name}--</p>
            <i style=' margin:0; padding:14px; background-color:darkred; color:white; display:inherit'>{_email}</i>
            </div>
          </body>
        </html>
        """

        # Turn into html MIMEText object

        part2 = MIMEText(html, "html")

        # Add HTML part to MIMEMultipart message

        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
        return redirect(url_for('home'))
    return render_template('Boeken.html')


# boek verslag kenny
class Xala_Boek(db.Model):
    __tablename__ = 'hele_boekverslag'
    id = db.Column(db.Integer, primary_key=True)
    sentence = db.Column(db.Text())

    def __int__(self, sentence):
        self.sentence = sentence


class K_Boek(db.Model):
    __tablename__ = 'kenny_boekverslag'
    id = db.Column(db.Integer, primary_key=True)
    sentence = db.Column(db.Text())

    def __int__(self, sentence):
        self.sentence = sentence


@app.route('/edit-par', methods=['POST', 'GET'])
def edit_paragraph():
    allofit = Xala_Boek.query.all()[-1]
    ID = get_id(str(allofit))
    db_data = Xala_Boek.query.filter_by(id=ID)
    if request.method == 'POST':
        updated_sentence = request.form['TEXT']
        code = request.form['PIN']

        if code == 'KENNY':
            data = Xala_Boek(sentence=updated_sentence)
            db.session.add(data)
            db.session.commit()
            return redirect(url_for('xala'))
        else:
            return render_template('try_again.html')
    return render_template('edit.html', para=db_data[0].sentence)


@app.route('/edit-par-k', methods=['POST', 'GET'])
def edit_paragraph_kboek():
    allofit = K_Boek.query.all()[-1]
    ID = get_id(str(allofit))
    db_data = K_Boek.query.filter_by(id=ID)
    if request.method == 'POST':
        updated_sentence = request.form['TEXT']
        code = request.form['PIN']

        if code == 'KENNY':
            data = K_Boek(sentence=updated_sentence)
            db.session.add(data)
            db.session.commit()
            return redirect(url_for('kboek'))
        else:
            return render_template('try_again.html')
    return render_template('edit_kboek.html', para=db_data[0].sentence)


@app.route('/boekverslag-k')
def xala():
    allofit = Xala_Boek.query.all()[-1]
    ID = get_id(str(allofit))
    db_data = Xala_Boek.query.filter_by(id=ID)
    return render_template('Xala-Sembene_Ousmane.html', para=db_data[0].sentence)


@app.route('/boekverslag-k2')
def kboek():
    allofit = K_Boek.query.all()[-1]
    ID = get_id(str(allofit))
    db_data = K_Boek.query.filter_by(id=ID)
    return render_template('lijnen-v-liefde.html', para=db_data[0].sentence)


@app.route('/kenny', methods=['POST', 'GET'])
def kenny():
    if request.method == 'POST':
        name = request.form['NAME']
        email = request.form['EMAIL']
        sender_message = request.form['MESSAGE']
        subject = request.form['SUBJECT']

        import smtplib, ssl
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        sender_email = "**************"
        receiver_email = "**************"
        password = "**************"

        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = receiver_email

        # Create HTML version of your message

        html = f"""\
        <html>
          <body style='font-family:Halyard; font-size:16px;'>
            <div style='border: 2px solid black; '>
            <p style=' margin:0; padding:14px; background-color:gray; display:inherit'>{sender_message}</p><p style='margin:0; padding:14px; background-color:lightgreen; display:inherit'>--{name}--</p>
            <i style=' margin:0; padding:14px; background-color:darkred; color:white; display:inherit'>{email}(email of the sender)</i>
            </div>
          </body>
        </html>
        """

        # Turn into html MIMEText object

        part2 = MIMEText(html, "html")

        # Add HTML part to MIMEMultipart message

        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
        return redirect(url_for('kenny'))
    return render_template('kenny.html')


# boek verslag shivaro
class S_Boek(db.Model):
    __tablename__ = 'shivaro_boekverslag'
    id = db.Column(db.Integer, primary_key=True)
    sentence = db.Column(db.Text())

    def __int__(self, sentence):
        self.sentence = sentence


@app.route('/boekverslag-s')
def sboek():
    allofit = S_Boek.query.all()[-1]
    ID = get_id(str(allofit))
    db_data = S_Boek.query.filter_by(id=ID)
    return render_template('shivaro-boek.html', para=db_data[0].sentence)


@app.route('/edit-par-sboek', methods=['POST', 'GET'])
def edit_paragraph_sboek():
    allofit = S_Boek.query.all()[-1]
    ID = get_id(str(allofit))
    db_data = S_Boek.query.filter_by(id=ID)
    if request.method == 'POST':
        updated_sentence = request.form['TEXT']
        code = request.form['PIN']

        if code == 'SHIVARO':
            data = S_Boek(sentence=updated_sentence)
            db.session.add(data)
            db.session.commit()
            return redirect(url_for('sboek'))
        else:
            return render_template('try_again.html')
    return render_template('edit_sboek.html', para=db_data[0].sentence)


@app.route('/shivaro', methods=['POST', 'GET'])
def shivaro():
    if request.method == 'POST':
        name = request.form['NAME']
        email = request.form['EMAIL']
        sender_message = request.form['MESSAGE']
        subject = request.form['SUBJECT']

        import smtplib, ssl
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        sender_email = "**************"
        receiver_email = "**************"
        password = "**************"

        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = receiver_email

        # Create HTML version of your message

        html = f"""\
        <html>
          <body style='font-family:Halyard; font-size:16px;'>
            <div style='border: 2px solid black; '>
            <p style=' margin:0; padding:14px; background-color:gray; display:inherit'>{sender_message}</p><p style='margin:0; padding:14px; background-color:lightgreen; display:inherit'>--{name}--</p>
            <i style=' margin:0; padding:14px; background-color:darkred; color:white; display:inherit'>{email}(email of the sender)</i>
            </div>
          </body>
        </html>
        """

        # Turn into html MIMEText object

        part2 = MIMEText(html, "html")

        # Add HTML part to MIMEMultipart message

        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
        return redirect(url_for('shivaro'))
    return render_template('shivaro.html')


# boek verslag cerano
@app.route('/cerano', methods=['POST', 'GET'])
def cerano():
    if request.method == 'POST':
        name = request.form['NAME']
        email = request.form['EMAIL']
        sender_message = request.form['MESSAGE']
        subject = request.form['SUBJECT']

        import smtplib, ssl
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        sender_email = "**************"
        receiver_email = "**************"
        password = "**************"

        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = receiver_email

        # Create HTML version of your message

        html = f"""\
        <html>
          <body style='font-family:Halyard; font-size:16px;'>
            <div style='border: 2px solid black; '>
            <p style=' margin:0; padding:14px; background-color:gray; display:inherit'>{sender_message}</p><p style='margin:0; padding:14px; background-color:lightgreen; display:inherit'>--{name}--</p>
            <i style=' margin:0; padding:14px; background-color:darkred; color:white; display:inherit'>{email}(email of the sender)</i>
            </div>
          </body>
        </html>
        """

        # Turn into html MIMEText object

        part2 = MIMEText(html, "html")

        # Add HTML part to MIMEMultipart message

        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
        return redirect(url_for('cerano'))
    return render_template('cerano.html')


# boek verslag xafy
@app.route('/xafy', methods=['POST', 'GET'])
def xafy():
    if request.method == 'POST':
        name = request.form['NAME']
        email = request.form['EMAIL']
        sender_message = request.form['MESSAGE']
        subject = request.form['SUBJECT']

        import smtplib, ssl
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart

        sender_email = "**************"
        receiver_email = "**************"
        password = "**************"

        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = receiver_email

        # Create HTML version of your message

        html = f"""\
        <html>
          <body style='font-family:Halyard; font-size:16px;'>
            <div style='border: 2px solid black; '>
            <p style=' margin:0; padding:14px; background-color:gray; display:inherit'>{sender_message}</p><p style='margin:0; padding:14px; background-color:lightgreen; display:inherit'>--{name}--</p>
            <i style=' margin:0; padding:14px; background-color:darkred; color:white; display:inherit'>{email}(email of the sender)</i>
            </div>
          </body>
        </html>
        """

        # Turn into html MIMEText object

        part2 = MIMEText(html, "html")

        # Add HTML part to MIMEMultipart message

        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )
        return redirect(url_for('xafy'))
    return render_template('xafy.html')


if __name__ == '__main__':
    app.run()
