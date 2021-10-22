#!/bin/bash
source venv/bin/activate
python3 manage.py runsslserver --certificate /etc/letsencrypt/live/digipackweb.com/fullchain.pem --key /etc/letsencrypt/live/digipackweb.com/privkey.pem 0.0.0.0:8000
exit 0
