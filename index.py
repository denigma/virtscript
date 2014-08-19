from flask import Flask, render_template, request
app = Flask(__name__)

from wtforms import Form, BooleanField, IntegerField, StringField, PasswordField, validators

class ContainerForm(Form):
    id = IntegerField('CTID') # VEID контейнера
    name = StringField("CTNAME")   # IP адрес контейнера
    ip = StringField("CTIP")  # hostname контейнера
    banned = StringField("BANNED") # IP адрес контейнера
    allow2ct = StringField("10.0.5.18")# Разрешаем соединения между DMZ контейнером и этими подсетями
    verelay = StringField("VERELAY")# Можно ли контейнеру спамить?
    DNAT4PORTS_TCP = StringField("DNAT4PORTS_TCP")  # Можно ли контейнеру спамить?
    DNAT2PORTS_TCP= StringField("DNAT2PORTS_TCP") # Пробрасываем на указанный порт контейнера внешний порт
    DNAT4PORTS_UDP = StringField("DNAT4PORTS_UDP") # Пробрасываем указанный внешний порт на контейнер
    DNAT2PORTS_UDP=StringField("DNAT2PORTS_UDP") # Пробрасываем на указанный порт контейнера внешний порт
    DMZSTATUS = StringField(" DMZSTATUS")  # В DMZ ли данный контейнер?


@app.route("/", methods=['GET', 'POST'])
def index():
    form = ContainerForm(request.form)
    return render_template('ports.html',form = form, result = "")


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404




@app.route('/register', methods=['GET', 'POST'])
def register():
    form = ContainerForm(request.form)
    print(form)
    return render_template('ports.html', form=form, result = "<h1>SUCCESS</h1>")

if __name__ == "__main__":
    app.run(debug=True)