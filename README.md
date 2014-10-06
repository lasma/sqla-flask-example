# Requirements

Required packages:
* PostgreSQL + PostGIS (9.x + 2.x)
* Python 2.7.x
* Python modules:
    * pip (Python package installer)
    * flask
    * sqlalchemy
    * geoalchemy


## PostgreSQL & PostGIS Setup

Download standard `PostgreSQL 9.3` installer from http://www.enterprisedb.com/downloads/postgres-postgresql-downloads

Run installer and follow the wizard setting up:
* Installation Directory (accepting default is recommended) - remember this directory as you might be required to add bin
directory within this directory to your system path!
* Data Directory (accepting default is recommended)
* Database superuser (postgres) password - memorize this password!
* Port number (default 5432 is recommended)
* Locale for database cluster (accept default)

On completion of PostgreSQL installation wizard accept launch of `StackBuilder` and install `PostGIS` extension.
In StackBuilder wizard:
* Select currently installed PostgreSQL server
* From Categories->Spatial Extension select PostGIS 2.1.x and follow the wizard to download and install the package:
    * provide memorized postgres password when prompted and run the installer till completion
* Exit StackBuilder


Verify installation by opening command prompt and type in:

    psql --help
    shp2pgsql --help

If these commands are not recognised then add {Installation Directory}/bin to the system path,e.g.

    export PATH=$PATH:/opt/PostgreSQL/9.3/bin

## Installing Python Modules

TBD

# Project Setup
Update database configuration (such as port number) within `config.py` file.

Execute `scripts/db_setup.py` to set up database:

    $ python scripts/db_setup.py