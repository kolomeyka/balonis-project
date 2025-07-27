# Instrukcje wdrożenia Balonis

Ten dokument zawiera szczegółowe instrukcje dotyczące wdrażania projektu Balonis z repozytorium Git.

## 📋 Wymagania systemowe

### Oprogramowanie
- **Python 3.8+**
- **Node.js 18+**
- **PostgreSQL 12+**
- **Git**
- **npm lub yarn**

### Systemy operacyjne
- Ubuntu 20.04+ (zalecane)
- macOS 10.15+
- Windows 10+ (z WSL2)

## 🚀 Wdrożenie z repozytorium Git

### 1. Klonowanie repozytorium

```bash
# Klonuj repozytorium
git clone <repository-url> balonis-project
cd balonis-project

# Sprawdź dostępne wersje
git tag -l

# Przełącz się na najnowszą stabilną wersję
git checkout v1.0.0
```

### 2. Konfiguracja bazy danych PostgreSQL

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib

# macOS (z Homebrew)
brew install postgresql
brew services start postgresql

# Utwórz bazę danych
sudo -u postgres psql
CREATE DATABASE balonis;
CREATE USER balonis_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE balonis TO balonis_user;
\q
```

### 3. Konfiguracja Backend (Django)

```bash
cd backend

# Utwórz wirtualne środowisko
python -m venv venv

# Aktywuj wirtualne środowisko
# Linux/macOS:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# Zainstaluj zależności
pip install -r requirements.txt

# Utwórz plik .env
cat > .env << EOF
DEBUG=True
SECRET_KEY=your-very-secret-key-here-change-in-production
DATABASE_URL=postgresql://balonis_user:your_password@localhost:5432/balonis
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
EOF

# Wykonaj migracje
python manage.py makemigrations
python manage.py migrate

# Utwórz superużytkownika
python manage.py createsuperuser

# Uruchom serwer deweloperski
python manage.py runserver
```

### 4. Konfiguracja Frontend (Next.js)

```bash
# W nowym terminalu
cd frontend

# Zainstaluj zależności
npm install

# Utwórz plik .env.local
cat > .env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000/api
EOF

# Uruchom serwer deweloperski
npm run dev
```

### 5. Weryfikacja instalacji

Po uruchomieniu obu serwerów sprawdź:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/
- **Panel administracyjny**: http://localhost:8000/admin/

## 🔧 Konfiguracja produkcyjna

### Backend (Django)

```bash
# Zainstaluj dodatkowe zależności produkcyjne
pip install gunicorn whitenoise

# Utwórz plik .env dla produkcji
cat > .env << EOF
DEBUG=False
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://user:password@host:port/database
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
EOF

# Zbierz pliki statyczne
python manage.py collectstatic --noinput

# Uruchom z Gunicorn
gunicorn balloon_shop_backend.wsgi:application --bind 0.0.0.0:8000
```

### Frontend (Next.js)

```bash
# Zbuduj aplikację
npm run build

# Uruchom w trybie produkcyjnym
npm start

# Lub eksportuj jako statyczne pliki
npm run build && npm run export
```

## 🐳 Wdrożenie z Docker

### Dockerfile dla Backend

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "balloon_shop_backend.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Dockerfile dla Frontend

```dockerfile
# frontend/Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: balonis
      POSTGRES_USER: balonis_user
      POSTGRES_PASSWORD: your_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://balonis_user:your_password@db:5432/balonis
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000/api
    depends_on:
      - backend

volumes:
  postgres_data:
```

```bash
# Uruchom z Docker Compose
docker-compose up -d
```

## 🔄 Aktualizacje

### Aktualizacja do nowej wersji

```bash
# Zatrzymaj serwery
# Ctrl+C w terminalach lub:
pkill -f "python manage.py runserver"
pkill -f "npm run dev"

# Pobierz najnowsze zmiany
git fetch --tags
git checkout v1.1.0  # lub najnowsza wersja

# Aktualizuj backend
cd backend
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput

# Aktualizuj frontend
cd ../frontend
npm install
npm run build

# Uruchom ponownie serwery
```

### Backup bazy danych

```bash
# Utwórz backup
pg_dump -h localhost -U balonis_user balonis > backup_$(date +%Y%m%d_%H%M%S).sql

# Przywróć z backup
psql -h localhost -U balonis_user balonis < backup_20250127_120000.sql
```

## 🛠 Narzędzia deweloperskie

### Przydatne komendy Git

```bash
# Sprawdź status repozytorium
git status

# Zobacz historię commitów
git log --oneline

# Sprawdź różnice
git diff

# Przełącz się na gałąź deweloperską
git checkout develop

# Utwórz nową gałąź funkcji
git checkout -b feature/new-feature
```

### Debugowanie

```bash
# Backend - sprawdź logi Django
python manage.py runserver --verbosity=2

# Frontend - sprawdź logi Next.js
npm run dev -- --debug

# Sprawdź połączenie z bazą danych
python manage.py dbshell
```

## 📊 Monitoring

### Logi aplikacji

```bash
# Backend logi
tail -f backend/logs/django.log

# Frontend logi
npm run dev 2>&1 | tee frontend.log
```

### Sprawdzenie wydajności

```bash
# Sprawdź użycie zasobów
htop

# Sprawdź połączenia sieciowe
netstat -tulpn | grep :8000
netstat -tulpn | grep :3000
```

## 🔒 Bezpieczeństwo

### Checklist bezpieczeństwa

- [ ] Zmień domyślny SECRET_KEY w produkcji
- [ ] Ustaw DEBUG=False w produkcji
- [ ] Skonfiguruj HTTPS
- [ ] Ustaw silne hasła do bazy danych
- [ ] Skonfiguruj firewall
- [ ] Regularnie aktualizuj zależności
- [ ] Monitoruj logi bezpieczeństwa

### Aktualizacja zależności

```bash
# Backend
pip list --outdated
pip install --upgrade package_name

# Frontend
npm outdated
npm update
```

## 📞 Wsparcie

W przypadku problemów:

1. Sprawdź logi aplikacji
2. Sprawdź dokumentację w `/docs`
3. Sprawdź issues w repozytorium Git
4. Skontaktuj się z zespołem deweloperskim

---

**Uwaga**: Te instrukcje dotyczą wersji 1.0.0. Sprawdź najnowszą dokumentację dla nowszych wersji.

