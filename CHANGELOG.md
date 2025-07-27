# Changelog

Wszystkie istotne zmiany w projekcie Balonis będą dokumentowane w tym pliku.

Format oparty na [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
i projekt przestrzega [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-27

### Added
- Początkowa konfiguracja projektu z Django backend i Next.js frontend
- Django REST API backend z aplikacjami products, orders, gallery
- Next.js frontend z TypeScript i Tailwind CSS
- Konfiguracja bazy danych PostgreSQL
- Model Source dla źródeł materiałów (zastępuje model Size)
- Polska lokalizacja i branding Balonis
- Pasterny minimalistyczny design z kolorami logo
- Konfiguracja CORS dla komunikacji frontend-backend

### Features
- **Katalog produktów**: Przeglądanie kompozycji balonowych z filtrowaniem
- **System zarządzania**: Panel administracyjny Django
- **Responsywny design**: Pełna kompatybilność z urządzeniami mobilnymi
- **API endpoints**: RESTful API dla wszystkich operacji
- **Galeria**: System zarządzania zdjęciami i opiniami klientów
- **Zamówienia**: Kompletny system obsługi zamówień

### Technical Details
- Django 4.2+ z Django REST Framework
- Next.js 14+ z TypeScript
- PostgreSQL jako główna baza danych
- Tailwind CSS dla stylowania
- Lucide Icons dla ikon
- CORS skonfigurowany dla komunikacji cross-origin

### Design System
- **Kolory główne**: Emerald (#059669), Stone (#f5f5f4)
- **Typografia**: System fonts z wagami Light, Regular, Medium
- **Komponenty**: Minimalistyczne karty produktów, formularze, nawigacja
- **Layout**: Responsywny grid system z Tailwind CSS

### API Endpoints
- `/api/products/` - Zarządzanie produktami
- `/api/orders/` - Obsługa zamówień
- `/api/gallery/` - Galeria zdjęć
- `/api/products/sources/` - Źródła materiałów
- `/api/products/colors/` - Kolory
- `/api/products/categories/` - Kategorie

### Database Schema
- **Products**: Product, Category, Color, Source, ProductImage, Review
- **Orders**: Order, OrderItem, DeliveryZone
- **Gallery**: GalleryImage, ClientReview

### Localization
- Pełna polska lokalizacja interfejsu użytkownika
- Polskie nazwy w panelu administracyjnym
- Dostosowanie do polskiego rynku (Warszawa jako główne miasto)

### Branding
- Nazwa: "Balonis"
- Hasło: "Bierzemy na siebie ciężar organizacji"
- Logo: Stylizowany Atlas trzymający balony
- Kolorystyka: Emerald green i stone beige

