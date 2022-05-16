INSTALACJA

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

URUCHAMIANIE
source venv/bin/activate
export FLASK_APP=main_web.py
flask run --host=0.0.0.0
