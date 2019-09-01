# Databases

## Dump with inserts
pg_dump -h 127.0.0.1 -p 5432 -U user -d database --column-inserts --data-only --table=table > inserts.sql

## Load those inserts
psql -h 0.0.0.0 -p 5432 -d database -U user -f inserts.sql

