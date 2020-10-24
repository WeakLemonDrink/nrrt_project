# Script resets db and starts project from scratch

db_file="db.sqlite3"

source ./scripts/dev_setup_env.sh

if [ -f $db_file ] ; then
    rm $db_file
fi

python manage.py migrate
