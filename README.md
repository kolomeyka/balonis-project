# Balonis - Kompozycje Balonowe

> Bierzemy na siebie ciężar organizacji

Balonis to platforma do zamawiania pięknych kompozycji balonowych na różne okazje. Projekt składa się z Django REST API backend i Next.js frontend.

## 🎈 Funkcje

- **Katalog produktów** - przeglądanie kompozycji balonowych
- **System filtrowania** - wyszukiwanie według kategorii, kolorów, źródeł materiałów
- **Panel administracyjny** - zarządzanie produktami, zamówieniami, galerią
- **Responsywny design** - pełna kompatybilność z urządzeniami mobilnymi
- **Pasterny design** - minimalistyczny styl z kolorami logo

## 🛠 Technologie

### Backend
- **Django 4.2+** - framework webowy
- **Django REST Framework** - API
- **PostgreSQL** - baza danych
- **Django CORS Headers** - obsługa CORS

### Frontend
- **Next.js 14+** - React framework
- **TypeScript** - typowanie
- **Tailwind CSS** - stylowanie
- **Lucide Icons** - ikony

## 🚀 Szybki start

### Wymagania
- Python 3.8+
- Node.js 18+
- PostgreSQL 12+
- Git

### Klonowanie repozytorium
```bash
git clone <repository-url>
cd balonis-project
```

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Dostęp do aplikacji
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/

## 📁 Struktura projektu

```
balonis-project/
├── backend/                 # Django backend
│   ├── balloon_shop_backend/ # Główne ustawienia Django
│   ├── products/            # Aplikacja produktów
│   ├── orders/              # Aplikacja zamówień
│   ├── gallery/             # Aplikacja galerii
│   ├── manage.py
│   └── requirements.txt
├── frontend/                # Next.js frontend
│   ├── src/
│   │   ├── app/            # App Router
│   │   ├── components/     # Komponenty React
│   │   └── lib/           # Utilities i API client
│   ├── public/            # Statyczne pliki
│   └── package.json
├── docs/                   # Dokumentacja
├── scripts/               # Skrypty pomocnicze
└── README.md
```

## 🔧 Konfiguracja

### Zmienne środowiskowe

#### Backend (.env)
```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/balonis
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## 📊 Modele danych

### Products
- **Product** - kompozycje balonowe
- **Category** - kategorie produktów
- **Color** - dostępne kolory
- **Source** - źródła materiałów
- **ProductImage** - zdjęcia produktów

### Orders
- **Order** - zamówienia klientów
- **OrderItem** - pozycje zamówienia
- **DeliveryZone** - strefy dostawcze

### Gallery
- **GalleryImage** - zdjęcia w galerii
- **ClientReview** - opinie klientów

## 🎨 Design System

### Kolory
- **Primary**: Emerald (#059669)
- **Secondary**: Stone (#f5f5f4)
- **Accent**: Emerald Dark (#065f46)
- **Text**: Stone Dark (#1c1917)

### Typografia
- **Font**: System fonts (Inter, SF Pro)
- **Weights**: Light (300), Regular (400), Medium (500)

## 🚀 Deployment

### Backend (Django)
```bash
# Produkcja
pip install gunicorn
gunicorn balloon_shop_backend.wsgi:application
```

### Frontend (Next.js)
```bash
# Build
npm run build
npm start
```

## 🤝 Rozwój

### Dodawanie nowych funkcji
1. Utwórz nową gałąź: `git checkout -b feature/nazwa-funkcji`
2. Wprowadź zmiany
3. Zatwierdź: `git commit -m "feat: opis funkcji"`
4. Wypchnij: `git push origin feature/nazwa-funkcji`

### Konwencje commitów
- `feat:` - nowa funkcja
- `fix:` - poprawka błędu
- `docs:` - dokumentacja
- `style:` - formatowanie, brak zmian w logice
- `refactor:` - refaktoryzacja kodu
- `test:` - testy
- `chore:` - zadania maintenance

## 📝 Licencja

Projekt jest własnością Balonis. Wszystkie prawa zastrzeżone.

## 📞 Kontakt

- **Email**: dev@balonis.com
- **Website**: https://balonis.com

---

Wykonane z ❤️ dla Balonis

