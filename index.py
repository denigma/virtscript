from flask import Flask, render_template, request
app = Flask(__name__)

from jinja2 import Environment, FileSystemLoader

from wtforms import Form, BooleanField, IntegerField, StringField, PasswordField, validators
from wtforms.validators import DataRequired

class ContainerForm(Form):
    id = IntegerField('CTID', default=101, validators=[DataRequired()]) # VEID контейнера
    name = StringField("CTNAME", default="semantic", validators=[DataRequired()])   # IP адрес контейнера
    ip = StringField("CTIP", default="192.168.1.104", validators=[DataRequired()])  # hostname контейнера
    banned = StringField("BANNED", default="") # IP адрес контейнера
    allow2ct = StringField("ALLOW2CT", default="")# Разрешаем соединения между DMZ контейнером и этими подсетями
    verelay = StringField("VERELAY", default="yes")# Можно ли контейнеру спамить?
    DNAT4PORTS_TCP = StringField("DNAT4PORTS_TCP", default="4569 9000 7070 5000")   # Пробрасываем указанный внешний порт на контейнер
    DNAT2PORTS_TCP= StringField("DNAT2PORTS_TCP", default="22 80 7070 5000") # Пробрасываем на указанный порт контейнера внешний порт
    DNAT4PORTS_UDP = StringField("DNAT4PORTS_UDP", default="") # Пробрасываем указанный внешний порт на контейнер
    DNAT2PORTS_UDP=StringField("DNAT2PORTS_UDP", default="") # Пробрасываем на указанный порт контейнера внешний порт
    DMZSTATUS = StringField(" DMZSTATUS", default="no")  # В DMZ ли данный контейнер?


@app.route("/", methods=['GET', 'POST'])
def index():
    form = ContainerForm(request.form)
    return render_template('ports.html',form = form, result = "")


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


def save(form,path = "./firewall/"):
    env = Environment(loader=FileSystemLoader('templates'))
    filename = path+form.name.data+".dmz.inc"
    template = env.get_template('file_to_save.txt')
    f = open(filename,'w')
    f.write(template.render(form=form))
    f.close()


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = ContainerForm(request.form)
    save(form)
    return render_template('ports.html', form=form, result = "<h1>SUCCESS</h1>")

if __name__ == "__main__":
    app.run(debug=True)