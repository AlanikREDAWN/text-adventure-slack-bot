# PORT="$1"
# export PORT="$PORT"

# kill -9 $(lsof -ti ":$PORT") 2>/dev/null
# git pull
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# gunicorn -b ":$PORT" app:app
python3 app.py