source /usr/src/app/.venv/bin/activate
cd /usr/src/app
export PYTHONPATH=/usr/src/app
python -c "from Mozilla.exception.mozilla_cdi_database_error import CdiDatabaseError; print('Mozilla OK')"