#!/bin/sh

su -m celery_user -c "celery -A celeryTasks worker --loglevel=info"
