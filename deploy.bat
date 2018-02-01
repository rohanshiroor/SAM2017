rem delete sqlite3 database
del db.sqlite3

rem delete migration files
del papers\migrations\0*.py

rem make migrations
python manage.py makemigrations

rem generate database
python manage.py migrate

rem removing all files and folders inside staticroot folder
del media\*.* /s /Q

rem run the tool_share/management/command/deploy.py script to auto generate sample data
python manage.py deploy

rem start the server
python manage.py runserver