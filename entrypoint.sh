#!/bin/bash

until  psql ${DATABASE_DSN} -c "\q"; do
  sleep 5
done
uvicorn src.main:APP --host 0.0.0.0 --port 5000 --reload