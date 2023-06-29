# install dependencies
pip install -r requirements.txt

# run migration
python manage.py collectstatic --no-input
python manage.py migrate