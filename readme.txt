STEP 1 :
	1 . create env for python
	for window :
		open cmd and write 
			virtualenv env
			env\Scripts\activate
	for linux :
		open terminal and write
			virtualenv --python=python3 env
			source env/bin/activate
STEP 2 :
	install required modules 
	open cmd or terminal and write
		python -m pip install -r requirements.txt
STEP3 : 
	python manage.py makemigrations
	python manage.py migrate
	python manage.py runserver

STEP 4 : 
	connect the zoho (url/zohoadmin in my case)
	http://localhost:8000/zohoadmin
STEP 5:
	done.
