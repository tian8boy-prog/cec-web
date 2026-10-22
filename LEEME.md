# Probar en tu computadora
pip install -r requirements.txt
python app.py        # abre http://127.0.0.1:5000

# Publicarla para que todos entren a cualquier hora (gratis)
Render.com: sube la carpeta a GitHub > New Web Service >
  Build command: pip install -r requirements.txt
  Start command: gunicorn app:app
