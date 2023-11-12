#!/usr/bin/sh

mariadb -u root -p$MARIADB_ROOT_PASSWORD $MARIADB_DATABASE < /docker-entrypoint-initdb.d/sql/init.sql
mariadb -u root -p$MARIADB_ROOT_PASSWORD $MARIADB_DATABASE < /docker-entrypoint-initdb.d/sql/procedures.sql
