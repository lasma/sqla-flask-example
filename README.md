# Requirements

Required packages:
* PostgreSQL + PostGIS (9.x + 2.x)
* Python 2.7.x
* Python modules:
** pip (Python package installer)
** flask
** sqlalchemy

## PostgreSQL & PostGIS Setup
Download installer from http://www.enterprisedb.com/downloads/postgres-postgresql-downloads
Run installer and follow the wizard, accepting defaults is recommended.
Set and memorize "postgres" database user password when prompted.
After installation run StackBuilder and install PostGIS template.
Verify installation by opening command prompt and type in:
    psql --help

# Project Setup
Update database configuration (port) within config.py file

Set up database:
$ python scripts/db_setup.py