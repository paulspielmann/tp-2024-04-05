start:
	FLASK_APP=webapp flask run --reload

start-windows:
	start.bat

deps:
	bash -c 'source ~/v3/bin/activate && pip install -r libtodolist/requirements.txt'


create-venv:
	python3 -m venv ~/v3

test:
	pytest tests/1-webapp-test.py --verbose

# Exercice 6 (si tu le trouves): mettre à jour make test avec tous les tests que tu as écrit
