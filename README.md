# software-hospital
Ingeniería de Software - Visualizacion

## Instalación

```bash
# 1. Clona el repo
git clone <url> software-hospital
cd software-hospital

# 2. Backend
cd src/backend
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

# 3. Frontend
cd ../frontend
npm install
```
## Arranque 
cd software-hospital
docker-compose up    # si usas Docker

# o en paralelo:
cd src/backend && python manage.py runserver
cd src/frontend && npm run dev
