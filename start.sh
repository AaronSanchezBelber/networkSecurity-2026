#!/bin/sh

nohup airflow scheduler > scheduler.log 2>&1 &
nohup airflow webserver > webserver.log 2>&1 &
