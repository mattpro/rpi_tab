from flask import Flask, render_template, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields.simple import SubmitField
from wtforms.widgets import TextArea
from wtforms.fields import SubmitField
from wtforms.fields.core import StringField
from wtforms import validators
from threading import Thread

from tasks import LEDDisplay

class MenuForm(FlaskForm):
    todays_menu = StringField(u'Dziś w menu', [validators.required()], widget=TextArea())
    submit_button = SubmitField(u'Wyślij na tablice')

def create_app(configfile=None):
    default_menu = 'aaa'
    app = Flask(__name__)
    Bootstrap(app)
    app.config['SECRET_KEY'] = 'devkey'
    display = LEDDisplay()
    thread = Thread(target=display.threaded_rest)
    thread.daemon = True
    thread.start()

    @app.route('/', methods=('GET', 'POST'))
    def index():
        menu_text_saved = default_menu
        form = MenuForm()
        if form.validate_on_submit():  # to get error messages to the browser
            menu_text = ', '.join(form.todays_menu.data.splitlines())
            if (len(menu_text) < 1):
                flash('Za krotki tekst!', 'error')
            else:
                flash(str.format('Wysyłam na ekran {}', menu_text), 'debug')
                menu_text_saved = menu_text
                display.tasks_change_text(menu_text_saved)
        return render_template('index.html', form=form, menu=menu_text_saved)


    return app

if __name__ == '__main__':
    create_app().run(debug=False, host='0.0.0.0')