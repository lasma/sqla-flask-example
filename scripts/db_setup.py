import os
import subprocess
from config import db_config
import config

if __name__ == "__main__":

    # Check psql is on the system executable path
    ok = os.system("psql --version")
    if ok != 0:
        print "Please add path to psql utility to the system path!"
        exit(1)

    # Check shp2pgsql is on the system executable path
    with open(os.devnull, 'wb') as devnull:
        ok = subprocess.check_call(['shp2pgsql', '-?'], stdout=devnull, stderr=subprocess.STDOUT)
        if ok != 0:
            print "Please add path to shp2pgsql utility to the system path!"
            exit(1)

    # Get superuser pass for creating new user and db
    pg_pass = raw_input("Please enter password for database user postgres: ")
    os.environ['PGPASSWORD'] = pg_pass

    # Check connection using specified password
    ok = os.system("psql -h {host} -p {port} -d postgres -U postgres --no-password "
              "-c \"select 'DB connection OK';\"".format(**db_config))
    if ok != 0:
        print "Supplied postgres password is incorrect!"
        exit(1)

    # Create user "demo" with password "demo"
    os.system("psql -h {host} -p {port} -d postgres -U postgres --no-password "
              "-c \"CREATE ROLE {user} LOGIN ENCRYPTED PASSWORD '{password}' "
              "NOSUPERUSER INHERIT NOCREATEDB NOCREATEROLE NOREPLICATION;\"".format(**db_config))

    # Create database "demo" with owner "demo"
    os.system("psql -h {host} -p {port} -d postgres -U postgres --no-password "
              "-c \"CREATE DATABASE {database} WITH ENCODING='UTF8' OWNER={user} "
              "TEMPLATE={template} CONNECTION LIMIT=-1;\"".format(**db_config))

    # Load data in to the database:
    os.environ['PGPASSWORD'] = db_config["password"]
    # os.system("shp2pgsql -W LATIN1 -s 4326 -I ../data/ne_110m_admin_0_countries.shp public.countries "
    #           " | psql -h {host} -p {port} -d {database} -U {user} --no-password".format(**db_config))
    os.system("psql -h {host} -p {port} -d {database} -U {user} --no-password -f ../data/countries.sql".format(**db_config))
    os.system("psql -h {host} -p {port} -d {database} -U {user} --no-password -f ../data/cities.sql".format(**db_config))

    print "Done!"
