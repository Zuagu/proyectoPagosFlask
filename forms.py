from wtforms import Form 
from wtforms import StringField,TextFiel
from wtforms.fields.html5 import EmailField

class CommentForm(Form):
    username = StringField('username')
    email = EmailField('Correo electrinico')
    comment = TextFiel('Comentario')