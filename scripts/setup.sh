#!/bin/bash

# Balonis Project Setup Script
# Automatyczna konfiguracja projektu Balonis

set -e  # Zatrzymaj przy błędzie

echo "🎈 Balonis Project Setup"
echo "======================="

# Kolory dla output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funkcje pomocnicze
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

# Sprawdź wymagania systemowe
check_requirements() {
    print_step "Sprawdzanie wymagań systemowych..."
    
    # Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 nie jest zainstalowany"
        exit 1
    fi
    
    # Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js nie jest zainstalowany"
        exit 1
    fi
    
    # Git
    if ! command -v git &> /dev/null; then
        print_error "Git nie jest zainstalowany"
        exit 1
    fi
    
    print_success "Wszystkie wymagania spełnione"
}

# Konfiguracja bazy danych (SQLite)
setup_database() {
    print_step "Konfiguracja bazy danych SQLite..."
    
    # SQLite nie wymaga dodatkowej konfiguracji
    # Plik bazy danych zostanie utworzony automatycznie przy pierwszej migracji
    print_success "SQLite skonfigurowane (baza danych zostanie utworzona automatycznie)"
}

# Konfiguracja backend
setup_backend() {
    print_step "Konfiguracja Django backend..."
    
    cd backend
    
    # Utwórz wirtualne środowisko
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        print_success "Utworzono wirtualne środowisko"
    fi
    
    # Aktywuj wirtualne środowisko
    source venv/bin/activate
    
    # Zainstaluj zależności
    pip install -r requirements.txt
    print_success "Zainstalowano zależności Python"
    
    # Utwórz plik .env
    if [ ! -f ".env" ]; then
        cat > .env << EOF
DEBUG=True
SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
EOF
        print_success "Utworzono plik .env"
    fi
    
    # Wykonaj migracje
    python manage.py makemigrations
    python manage.py migrate
    print_success "Wykonano migracje bazy danych"
    
    # Utwórz superużytkownika
    echo "Tworzenie superużytkownika..."
    python manage.py createsuperuser
    
    cd ..
}

# Konfiguracja frontend
setup_frontend() {
    print_step "Konfiguracja Next.js frontend..."
    
    cd frontend
    
    # Zainstaluj zależności
    npm install
    print_success "Zainstalowano zależności Node.js"
    
    # Utwórz plik .env.local
    if [ ! -f ".env.local" ]; then
        cat > .env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000/api
EOF
        print_success "Utworzono plik .env.local"
    fi
    
    cd ..
}

# Główna funkcja
main() {
    echo "Ten skrypt skonfiguruje projekt Balonis na Twoim systemie."
    echo
    
    check_requirements
    setup_database
    setup_backend
    setup_frontend
    
    echo
    print_success "Konfiguracja zakończona!"
    echo
    echo "Aby uruchomić projekt:"
    echo "1. Backend:  cd backend && source venv/bin/activate && python manage.py runserver"
    echo "2. Frontend: cd frontend && npm run dev"
    echo
    echo "Dostęp do aplikacji:"
    echo "- Frontend: http://localhost:3000"
    echo "- Backend API: http://localhost:8000/api/"
    echo "- Panel admin: http://localhost:8000/admin/"
}

# Uruchom główną funkcję
main "$@"

