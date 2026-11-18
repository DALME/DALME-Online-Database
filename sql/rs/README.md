# sql/rs

Initialisation scripts for the local ResourceSpace DAM database (`rs.db`,
MySQL). The directory is mounted as `/docker-entrypoint-initdb.d`, so any `.sql`
file here runs when the `rs.db` volume is first created.

SQL files here are gitignored.
