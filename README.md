Instaling
=====

1. Clone the repository.

`git clone https://github.com/Smilkoski/messenger.git`

`cd messenger`

3. Create a virtualenv with Python 3.8 or above

`python -m venv .venv`

4. Activate the virtualenv.

`.venv\Scripts\activate` for Windows

`source .venv/bin/activate` for Mac OS / Linux

6. Install the dependencies.

`pip install -r requirements.txt`

7. Make migrations

`python manage.py makemigrations`
`python manage.py migrate`

8. Run the app.

`python manage.py runserver`
