#!/bin/bash
mysql -h "api-services.c0wj8qdslqom.ap-southeast-1.rds.amazonaws.com" -P 3306 -u "askmeapi" -p < db_create.sql
# askmeservice2017