#!/bin/bash

# Balonis Project Start Script
# Uruchamia backend i frontend w trybie deweloperskim

set -e

echo "🎈 Uruchamianie projektu Balonis"
echo "================================"

# Kolory
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUKCES]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[UWAGA]${NC} $1"
}

# Sprawdź czy jesteśmy w głównym katalogu projektu
if [ ! -f "README.md" ] || [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "Błąd: Uruchom skrypt z głównego katalogu projektu Balonis"
    exit 1
fi

# Funkcja do uruchomienia backend
start_backend() {
    print_info "Uruchamianie Django backend..."
    
    cd backend
    
    # Sprawdź czy istnieje wirtualne środowisko
    if [ ! -d "venv" ]; then
        print_warning "Brak wirtualnego środowiska. Uruchom najpierw scripts/setup.sh"
        exit 1
    fi
    
    # Aktywuj wirtualne środowisko
    source venv/bin/activate
    
    # Sprawdź czy istnieje plik .env
    if [ ! -f ".env" ]; then
        print_warning "Brak pliku .env. Uruchom najpierw scripts/setup.sh"
        exit 1
    fi
    
    # Wykonaj migracje (na wszelki wypadek)
    python manage.py migrate --run-syncdb
    
    # Uruchom serwer
    print_success "Backend uruchomiony na http://localhost:8000"
    python manage.py runserver &
    BACKEND_PID=$!
    
    cd ..
}

# Funkcja do uruchomienia frontend
start_frontend() {
    print_info "Uruchamianie Next.js frontend..."
    
    cd frontend
    
    # Sprawdź czy istnieje node_modules
    if [ ! -d "node_modules" ]; then
        print_info "Instalowanie zależności Node.js..."
        npm install
    fi
    
    # Sprawdź czy istnieje plik .env.local
    if [ ! -f ".env.local" ]; then
        print_warning "Brak pliku .env.local. Uruchom najpierw scripts/setup.sh"
        exit 1
    fi
    
    # Uruchom serwer deweloperski
    print_success "Frontend uruchomiony na http://localhost:3000"
    npm run dev &
    FRONTEND_PID=$!
    
    cd ..
}

# Funkcja do zatrzymania serwerów
cleanup() {
    print_info "Zatrzymywanie serwerów..."
    
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    
    # Zatrzymaj wszystkie procesy Django i Node.js
    pkill -f "python manage.py runserver" 2>/dev/null || true
    pkill -f "npm run dev" 2>/dev/null || true
    pkill -f "next dev" 2>/dev/null || true
    
    print_success "Serwery zatrzymane"
    exit 0
}

# Obsługa sygnału przerwania (Ctrl+C)
trap cleanup SIGINT SIGTERM

# Główna funkcja
main() {
    # Sprawdź argumenty
    case "${1:-}" in
        "backend")
            start_backend
            wait $BACKEND_PID
            ;;
        "frontend")
            start_frontend
            wait $FRONTEND_PID
            ;;
        "")
            # Uruchom oba serwery
            start_backend
            sleep 3  # Daj czas na uruchomienie backend
            start_frontend
            
            echo
            print_success "Projekt Balonis uruchomiony!"
            echo
            echo "Dostęp do aplikacji:"
            echo "- Frontend: http://localhost:3000"
            echo "- Backend API: http://localhost:8000/api/"
            echo "- Panel admin: http://localhost:8000/admin/"
            echo
            echo "Naciśnij Ctrl+C aby zatrzymać serwery"
            
            # Czekaj na oba procesy
            wait $BACKEND_PID $FRONTEND_PID
            ;;
        *)
            echo "Użycie: $0 [backend|frontend]"
            echo
            echo "Opcje:"
            echo "  backend   - uruchom tylko Django backend"
            echo "  frontend  - uruchom tylko Next.js frontend"
            echo "  (brak)    - uruchom oba serwery"
            exit 1
            ;;
    esac
}

# Uruchom główną funkcję
main "$@"

