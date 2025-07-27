#!/bin/bash

# GitHub Setup Script for Balonis Project
# Skrypt do podłączenia lokalnego repozytorium do GitHub

set -e

echo "🐙 GitHub Setup for Balonis Project"
echo "==================================="

# Kolory
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
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

print_error() {
    echo -e "${RED}[BŁĄD]${NC} $1"
}

# Sprawdź czy jesteśmy w repozytorium Git
check_git_repo() {
    if [ ! -d ".git" ]; then
        print_error "To nie jest repozytorium Git. Uruchom skrypt z katalogu balonis-project"
        exit 1
    fi
    
    print_success "Repozytorium Git znalezione"
}

# Sprawdź czy GitHub remote już istnieje
check_existing_remote() {
    if git remote | grep -q "origin"; then
        print_warning "Remote 'origin' już istnieje:"
        git remote -v
        echo
        read -p "Czy chcesz go zastąpić? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git remote remove origin
            print_info "Usunięto istniejący remote 'origin'"
        else
            print_info "Zachowano istniejący remote"
            return 0
        fi
    fi
}

# Dodaj GitHub remote
add_github_remote() {
    echo
    print_info "Wprowadź dane GitHub repozytorium:"
    echo
    
    read -p "GitHub username: " GITHUB_USER
    read -p "Repository name [balonis-project]: " REPO_NAME
    REPO_NAME=${REPO_NAME:-balonis-project}
    
    GITHUB_URL="https://github.com/$GITHUB_USER/$REPO_NAME.git"
    
    print_info "Dodawanie remote: $GITHUB_URL"
    git remote add origin "$GITHUB_URL"
    
    print_success "Remote 'origin' dodany pomyślnie"
}

# Sprawdź połączenie z GitHub
test_github_connection() {
    print_info "Sprawdzanie połączenia z GitHub..."
    
    if git ls-remote origin &> /dev/null; then
        print_success "Połączenie z GitHub działa"
        return 0
    else
        print_warning "Nie można połączyć się z GitHub"
        echo
        echo "Możliwe przyczyny:"
        echo "1. Repozytorium nie istnieje na GitHub"
        echo "2. Brak uprawnień dostępu"
        echo "3. Nieprawidłowy URL"
        echo
        echo "Sprawdź czy:"
        echo "- Repozytorium zostało utworzone na GitHub"
        echo "- Masz uprawnienia do repozytorium"
        echo "- URL jest poprawny: $(git remote get-url origin)"
        return 1
    fi
}

# Wypchnij kod na GitHub
push_to_github() {
    print_info "Wysyłanie kodu na GitHub..."
    
    # Sprawdź czy są commity do wypchnięcia
    if [ -z "$(git log --oneline)" ]; then
        print_error "Brak commitów do wypchnięcia"
        return 1
    fi
    
    # Wypchnij main branch
    print_info "Wysyłanie branch 'main'..."
    if git push -u origin main; then
        print_success "Branch 'main' wysłany pomyślnie"
    else
        print_error "Błąd podczas wysyłania branch 'main'"
        return 1
    fi
    
    # Wypchnij tagi
    if git tag -l | grep -q .; then
        print_info "Wysyłanie tagów..."
        if git push --tags; then
            print_success "Tagi wysłane pomyślnie"
        else
            print_warning "Błąd podczas wysyłania tagów"
        fi
    else
        print_info "Brak tagów do wysłania"
    fi
}

# Pokaż informacje o repozytorium
show_repo_info() {
    echo
    print_success "Repozytorium GitHub skonfigurowane!"
    echo
    echo "📊 Informacje o repozytorium:"
    echo "Remote URL: $(git remote get-url origin)"
    echo "Current branch: $(git branch --show-current)"
    echo "Last commit: $(git log -1 --oneline)"
    echo "Tags: $(git tag -l | tr '\n' ' ')"
    echo
    echo "🌐 GitHub URL:"
    GITHUB_URL=$(git remote get-url origin | sed 's/\.git$//')
    echo "$GITHUB_URL"
    echo
    echo "📁 Dostępne sekcje:"
    echo "- Code: $GITHUB_URL"
    echo "- Issues: $GITHUB_URL/issues"
    echo "- Pull Requests: $GITHUB_URL/pulls"
    echo "- Releases: $GITHUB_URL/releases"
    echo "- Settings: $GITHUB_URL/settings"
}

# Pokaż następne kroki
show_next_steps() {
    echo
    print_info "Następne kroki:"
    echo
    echo "1. 🔐 Skonfiguruj dostęp dla automatycznych commitów:"
    echo "   a) Utwórz Personal Access Token w GitHub"
    echo "   b) Lub dodaj współpracownika do repozytorium"
    echo
    echo "2. 🛡️ Skonfiguruj ochronę branch 'main' (opcjonalnie):"
    echo "   - Przejdź do Settings → Branches"
    echo "   - Dodaj regułę ochrony dla 'main'"
    echo
    echo "3. 📋 Skonfiguruj Issues i Project management:"
    echo "   - Włącz Issues w Settings"
    echo "   - Utwórz szablony Issues"
    echo
    echo "4. 🚀 Skonfiguruj GitHub Actions (opcjonalnie):"
    echo "   - Automatyczne testy"
    echo "   - Automatyczne wdrożenia"
    echo
    echo "5. 📖 Skonfiguruj GitHub Pages dla dokumentacji (opcjonalnie):"
    echo "   - Settings → Pages"
    echo "   - Source: Deploy from branch 'main' /docs"
}

# Główna funkcja
main() {
    echo "Ten skrypt podłączy lokalny projekt Balonis do GitHub."
    echo "Upewnij się, że utworzyłeś już repozytorium na GitHub."
    echo
    
    read -p "Czy chcesz kontynuować? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 0
    fi
    
    check_git_repo
    check_existing_remote
    add_github_remote
    
    if test_github_connection; then
        push_to_github
        show_repo_info
        show_next_steps
    else
        echo
        print_error "Konfiguracja nie została ukończona z powodu problemów z połączeniem"
        echo "Sprawdź ustawienia i spróbuj ponownie"
        exit 1
    fi
}

# Uruchom główną funkcję
main "$@"

