# Balonis API Documentation

REST API dla platformy Balonis umożliwia zarządzanie produktami, zamówieniami i galerią.

## 🔗 Base URL

```
http://localhost:8000/api/
```

## 🔐 Uwierzytelnianie

Większość endpointów jest publicznych. Operacje administracyjne wymagają uwierzytelniania Django.

## 📦 Products API

### Produkty

#### GET /products/
Pobiera listę wszystkich aktywnych produktów.

**Parametry zapytania:**
- `category` - filtruj według kategorii (slug)
- `colors` - filtruj według kolorów (ID)
- `sources` - filtruj według źródeł materiałów (ID)
- `shape` - filtruj według kształtu
- `theme` - filtruj według motywu
- `is_featured` - tylko produkty wyróżnione (true/false)
- `search` - wyszukiwanie w nazwie i opisie
- `min_price` - minimalna cena
- `max_price` - maksymalna cena
- `ordering` - sortowanie (created_at, base_price, views_count, name)

**Przykład odpowiedzi:**
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Kompozycja urodzinowa różowa",
      "slug": "kompozycja-urodzinowa-rozowa",
      "short_description": "Piękna kompozycja na urodziny",
      "category": {
        "id": 1,
        "name": "Urodziny",
        "slug": "urodziny"
      },
      "shape": "round",
      "theme": "birthday",
      "base_price": "150.00",
      "discount_price": null,
      "current_price": "150.00",
      "has_discount": false,
      "is_featured": true,
      "main_image": {
        "id": 1,
        "image": "/media/products/balloon1.jpg",
        "alt_text": "Kompozycja różowa"
      },
      "views_count": 45
    }
  ]
}
```

#### GET /products/{slug}/
Pobiera szczegóły produktu.

**Przykład odpowiedzi:**
```json
{
  "id": 1,
  "name": "Kompozycja urodzinowa różowa",
  "slug": "kompozycja-urodzinowa-rozowa",
  "description": "Szczegółowy opis produktu...",
  "short_description": "Piękna kompozycja na urodziny",
  "category": {
    "id": 1,
    "name": "Urodziny",
    "slug": "urodziny",
    "description": "Produkty urodzinowe",
    "image": "/media/categories/birthday.jpg"
  },
  "colors": [
    {
      "id": 1,
      "name": "Różowy",
      "hex_code": "#FF69B4"
    }
  ],
  "sources": [
    {
      "id": 1,
      "name": "Sklep Balonowy Warszawa",
      "url": "https://example.com",
      "description": "Wysokiej jakości balony"
    }
  ],
  "images": [
    {
      "id": 1,
      "image": "/media/products/balloon1.jpg",
      "alt_text": "Kompozycja różowa",
      "is_main": true,
      "order": 1
    }
  ],
  "reviews": [
    {
      "id": 1,
      "name": "Anna Kowalska",
      "rating": 5,
      "comment": "Piękne balony!",
      "created_at": "2025-01-27T10:00:00Z"
    }
  ],
  "min_quantity": 1,
  "max_quantity": 10,
  "is_customizable": true,
  "custom_text_available": true,
  "created_at": "2025-01-27T10:00:00Z"
}
```

#### GET /products/featured/
Pobiera listę produktów wyróżnionych.

#### GET /products/popular/
Pobiera listę popularnych produktów (sortowane według views_count).

### Kategorie

#### GET /products/categories/
Pobiera listę wszystkich aktywnych kategorii.

**Przykład odpowiedzi:**
```json
[
  {
    "id": 1,
    "name": "Urodziny",
    "slug": "urodziny",
    "description": "Produkty urodzinowe",
    "image": "/media/categories/birthday.jpg"
  }
]
```

### Kolory

#### GET /products/colors/
Pobiera listę wszystkich aktywnych kolorów.

**Przykład odpowiedzi:**
```json
[
  {
    "id": 1,
    "name": "Różowy",
    "hex_code": "#FF69B4"
  }
]
```

### Źródła materiałów

#### GET /products/sources/
Pobiera listę wszystkich aktywnych źródeł materiałów.

**Przykład odpowiedzi:**
```json
[
  {
    "id": 1,
    "name": "Sklep Balonowy Warszawa",
    "url": "https://example.com",
    "description": "Wysokiej jakości balony lateksowe"
  }
]
```

### Filtry

#### GET /products/filters/
Pobiera wszystkie dostępne opcje filtrowania.

**Przykład odpowiedzi:**
```json
{
  "categories": [...],
  "colors": [...],
  "sources": [...],
  "shapes": [
    {"value": "round", "label": "Okrągłe"},
    {"value": "heart", "label": "Serce"}
  ],
  "themes": [
    {"value": "birthday", "label": "Urodziny"},
    {"value": "wedding", "label": "Ślub"}
  ],
  "price_range": {
    "min": 50,
    "max": 500
  }
}
```

### Wyszukiwanie

#### GET /products/search/?q={query}
Wyszukuje produkty według nazwy i opisu.

## 🛒 Orders API

### Zamówienia

#### POST /orders/create/
Tworzy nowe zamówienie.

**Przykład żądania:**
```json
{
  "customer_name": "Jan Kowalski",
  "customer_phone": "+48123456789",
  "customer_email": "jan@example.com",
  "delivery_address": "ul. Przykładowa 123, 00-001 Warszawa",
  "delivery_date": "2025-02-01",
  "delivery_time": "14:00:00",
  "payment_method": "cash",
  "total_amount": "300.00",
  "delivery_cost": "20.00",
  "notes": "Proszę zadzwonić przed dostawą",
  "items": [
    {
      "product": 1,
      "selected_color": 1,
      "custom_text": "Wszystkiego najlepszego!",
      "quantity": 2,
      "price": "150.00",
      "notes": "Dodatkowe balony"
    }
  ]
}
```

#### GET /orders/{id}/
Pobiera szczegóły zamówienia (wymaga uwierzytelniania).

#### POST /orders/calculate-cart/
Kalkuluje koszt koszyka.

**Przykład żądania:**
```json
{
  "items": [
    {
      "product_id": 1,
      "color_id": 1,
      "quantity": 2,
      "custom_text": "Tekst",
      "notes": "Uwagi"
    }
  ]
}
```

#### POST /orders/calculate-delivery/
Kalkuluje koszt dostawy.

**Przykład żądania:**
```json
{
  "delivery_address": "Warszawa, Śródmieście",
  "total_amount": "300.00"
}
```

### Strefy dostawcze

#### GET /orders/delivery-zones/
Pobiera listę stref dostawczych.

**Przykład odpowiedzi:**
```json
[
  {
    "id": 1,
    "name": "Warszawa - Śródmieście",
    "description": "Centrum miasta",
    "delivery_cost": "15.00",
    "min_order_amount": "100.00"
  }
]
```

## 🖼 Gallery API

### Galeria

#### GET /gallery/
Pobiera listę zdjęć w galerii.

**Parametry zapytania:**
- `category_name` - filtruj według kategorii
- `event_type` - filtruj według typu wydarzenia
- `is_featured` - tylko wyróżnione (true/false)

**Przykład odpowiedzi:**
```json
{
  "count": 50,
  "results": [
    {
      "id": 1,
      "title": "Urodziny Ani",
      "description": "Piękna dekoracja urodzinowa",
      "image": "/media/gallery/birthday1.jpg",
      "category_name": "Urodziny",
      "event_type": "birthday",
      "is_featured": true,
      "views_count": 120,
      "created_at": "2025-01-27T10:00:00Z"
    }
  ]
}
```

#### GET /gallery/{id}/
Pobiera szczegóły zdjęcia z galerii.

#### GET /gallery/featured/
Pobiera wyróżnione zdjęcia z galerii.

#### GET /gallery/categories/
Pobiera kategorie galerii.

#### GET /gallery/category/{slug}/
Pobiera zdjęcia z określonej kategorii.

### Opinie klientów

#### GET /gallery/reviews/
Pobiera opinie klientów.

**Przykład odpowiedzi:**
```json
[
  {
    "id": 1,
    "name": "Anna Kowalska",
    "review_text": "Fantastyczna obsługa i piękne balony!",
    "rating": 5,
    "gallery_image": {
      "id": 1,
      "title": "Urodziny Ani",
      "image": "/media/gallery/birthday1.jpg"
    },
    "is_featured": true,
    "created_at": "2025-01-27T10:00:00Z"
  }
]
```

#### GET /gallery/reviews/featured/
Pobiera wyróżnione opinie klientów.

#### POST /gallery/reviews/create/
Tworzy nową opinię klienta.

**Przykład żądania:**
```json
{
  "name": "Jan Kowalski",
  "email": "jan@example.com",
  "review_text": "Świetna jakość i szybka dostawa!",
  "rating": 5,
  "gallery_image": 1
}
```

## 📊 Kody odpowiedzi HTTP

- `200 OK` - Żądanie zakończone sukcesem
- `201 Created` - Zasób utworzony pomyślnie
- `400 Bad Request` - Błędne dane w żądaniu
- `404 Not Found` - Zasób nie znaleziony
- `500 Internal Server Error` - Błąd serwera

## 🔧 Przykłady użycia

### JavaScript/TypeScript

```typescript
// Pobierz produkty
const response = await fetch('http://localhost:8000/api/products/');
const data = await response.json();

// Utwórz zamówienie
const orderData = {
  customer_name: "Jan Kowalski",
  // ... inne dane
};

const response = await fetch('http://localhost:8000/api/orders/create/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(orderData),
});
```

### Python

```python
import requests

# Pobierz produkty
response = requests.get('http://localhost:8000/api/products/')
products = response.json()

# Utwórz zamówienie
order_data = {
    'customer_name': 'Jan Kowalski',
    # ... inne dane
}

response = requests.post(
    'http://localhost:8000/api/orders/create/',
    json=order_data
)
```

### cURL

```bash
# Pobierz produkty
curl -X GET "http://localhost:8000/api/products/"

# Utwórz zamówienie
curl -X POST "http://localhost:8000/api/orders/create/" \
  -H "Content-Type: application/json" \
  -d '{"customer_name": "Jan Kowalski", ...}'
```

## 🚀 Rate Limiting

API nie ma obecnie ograniczeń częstotliwości żądań, ale zaleca się rozsądne użytkowanie.

## 📝 Uwagi

- Wszystkie daty są w formacie ISO 8601 (YYYY-MM-DDTHH:MM:SSZ)
- Ceny są w formacie dziesiętnym z dwoma miejscami po przecinku
- Obrazy zwracają pełne URL względem domeny serwera
- API obsługuje CORS dla żądań z frontendu

