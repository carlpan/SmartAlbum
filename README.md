# SmartAlbum

Instructions on how to run:

1. Run pip install requirements.txt
2. Start redis server with command redis-server
3. In the new terminal, run python manage.py run server command
4. Open another terminal, run command: celery -A SmartAlbum worker -l info to start a celery worker
5. In another new terminal, run command: celery - A SmartAlbum beat -l info to start periodic task
