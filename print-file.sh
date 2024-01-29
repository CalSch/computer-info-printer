#!/bin/bash
curl -X POST http://printer-server:8080/html  \
   -H "Content-Type: application/x-www-form-urlencoded"  \
   -d "text=$(cat $1)"
