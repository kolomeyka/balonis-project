#!/bin/bash

# Balonis Project Deployment Script
# Skrypt do wdrażania projektu Balonis w środowisku produkcyjnym

set -e

echo "🚀 Balonis Production Deployment"
echo "================================"

# Kolory
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_step() {
    echo -e "${BLUE}[KROK]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUKCES]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[UWAGA]${NC} $1"
}

print_error() {
    echo -e "${RED}[BŁĄD]${NC} $1"
}

# Sprawdź czy jesteśmy w głównym katalogu projektu
if [ ! -f "README.md" ] || [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    print_error "Uruchom skrypt z głównego katalogu projektu Balonis"
    exit 1
fi

# Konfiguracja produkcyjna
configure_production() {
    print_step "Konfiguracja środowiska produkcyjnego..."
    
    read -p "Domena aplikacji (np. balonis.com): " DOMAIN
    read -p "Email administratora: " ADMIN_EMAIL
    read -s -p "Hasło do bazy danych produkcyjnej: " DB_PASSWORD
    echo
    read -p "Host bazy danych [localhost]: " DB_HOST
    DB_HOST=${DB_HOST:-localhost}
    
    # Generuj secret key
    SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
}

# Wdrożenie backend
deploy_backend() {
    print_step "Wdrażanie Django backend..."
    
    cd backend
    
    # Utwórz wirtualne środowisko produkcyjne
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi
    
    source venv/bin/activate
    
    # Zainstaluj zależności produkcyjne
    pip install -r requirements.txt
    pip install gunicorn whitenoise
    
    # Utwórz plik .env produkcyjny
    cat > .env << EOF
DEBUG=False
SECRET_KEY=$SECRET_KEY
DATABASE_URL=postgresql://balonis_user:$DB_PASSWORD@$DB_HOST:5432/balonis
ALLOWED_HOSTS=$DOMAIN,www.$DOMAIN
CORS_ALLOWED_ORIGINS=https://$DOMAIN,https://www.$DOMAIN
ADMIN_EMAIL=$ADMIN_EMAIL
EOF
    
    # Wykonaj migracje
    python manage.py migrate
    
    # Zbierz pliki statyczne
    python manage.py collectstatic --noinput
    
    # Utwórz superużytkownika (jeśli nie istnieje)
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', '$ADMIN_EMAIL', 'admin')" | python manage.py shell
    
    print_success "Backend skonfigurowany dla produkcji"
    
    cd ..
}

# Wdrożenie frontend
deploy_frontend() {
    print_step "Wdrażanie Next.js frontend..."
    
    cd frontend
    
    # Zainstaluj zależności
    npm ci --only=production
    
    # Utwórz plik .env.local produkcyjny
    cat > .env.local << EOF
NEXT_PUBLIC_API_URL=https://$DOMAIN/api
EOF
    
    # Zbuduj aplikację
    npm run build
    
    print_success "Frontend zbudowany dla produkcji"
    
    cd ..
}

# Utwórz pliki systemd
create_systemd_services() {
    print_step "Tworzenie usług systemd..."
    
    # Usługa Django
    sudo tee /etc/systemd/system/balonis-backend.service > /dev/null << EOF
[Unit]
Description=Balonis Django Backend
After=network.target

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory=$(pwd)/backend
Environment=PATH=$(pwd)/backend/venv/bin
ExecStart=$(pwd)/backend/venv/bin/gunicorn balloon_shop_backend.wsgi:application --bind 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF
    
    # Usługa Next.js
    sudo tee /etc/systemd/system/balonis-frontend.service > /dev/null << EOF
[Unit]
Description=Balonis Next.js Frontend
After=network.target

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory=$(pwd)/frontend
Environment=PATH=/usr/bin:/bin
Environment=NODE_ENV=production
ExecStart=/usr/bin/npm start
Restart=always

[Install]
WantedBy=multi-user.target
EOF
    
    # Przeładuj systemd i uruchom usługi
    sudo systemctl daemon-reload
    sudo systemctl enable balonis-backend balonis-frontend
    sudo systemctl start balonis-backend balonis-frontend
    
    print_success "Usługi systemd utworzone i uruchomione"
}

# Konfiguracja Nginx
configure_nginx() {
    print_step "Konfiguracja Nginx..."
    
    sudo tee /etc/nginx/sites-available/balonis << EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    
    # Przekierowanie na HTTPS
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name $DOMAIN www.$DOMAIN;
    
    # Certyfikaty SSL (skonfiguruj z Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/$DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DOMAIN/privkey.pem;
    
    # Frontend (Next.js)
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
    }
    
    # Backend API (Django)
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    # Django Admin
    location /admin/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    # Pliki statyczne Django
    location /static/ {
        alias $(pwd)/backend/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Pliki medialne Django
    location /media/ {
        alias $(pwd)/backend/media/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF
    
    # Włącz konfigurację
    sudo ln -sf /etc/nginx/sites-available/balonis /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl reload nginx
    
    print_success "Nginx skonfigurowany"
}

# Konfiguracja SSL z Let's Encrypt
setup_ssl() {
    print_step "Konfiguracja SSL z Let's Encrypt..."
    
    # Zainstaluj certbot
    sudo apt update
    sudo apt install -y certbot python3-certbot-nginx
    
    # Uzyskaj certyfikat
    sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN --email $ADMIN_EMAIL --agree-tos --non-interactive
    
    print_success "SSL skonfigurowany"
}

# Konfiguracja firewall
configure_firewall() {
    print_step "Konfiguracja firewall..."
    
    sudo ufw allow 22/tcp
    sudo ufw allow 80/tcp
    sudo ufw allow 443/tcp
    sudo ufw --force enable
    
    print_success "Firewall skonfigurowany"
}

# Główna funkcja
main() {
    echo "Ten skrypt wdroży projekt Balonis w środowisku produkcyjnym."
    echo "Upewnij się, że masz uprawnienia sudo i skonfigurowaną bazę danych PostgreSQL."
    echo
    
    read -p "Czy chcesz kontynuować? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
    
    configure_production
    deploy_backend
    deploy_frontend
    create_systemd_services
    configure_nginx
    setup_ssl
    configure_firewall
    
    echo
    print_success "Wdrożenie zakończone!"
    echo
    echo "Aplikacja jest dostępna pod adresem: https://$DOMAIN"
    echo "Panel administracyjny: https://$DOMAIN/admin/"
    echo
    echo "Przydatne komendy:"
    echo "- Status usług: sudo systemctl status balonis-backend balonis-frontend"
    echo "- Logi backend: sudo journalctl -u balonis-backend -f"
    echo "- Logi frontend: sudo journalctl -u balonis-frontend -f"
    echo "- Restart usług: sudo systemctl restart balonis-backend balonis-frontend"
}

# Uruchom główną funkcję
main "$@"

