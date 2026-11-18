# sql/dumps

Local Postgres dumps for restoring a development database. The directory is
mounted into `ida.db` at `/opt/db/dumps`; restore one with
`make db.load dump=<file>` or `make db.load.restore dump=<file>`.

Dumps are gitignored.
