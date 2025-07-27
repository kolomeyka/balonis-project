# Contributing to Balonis

Dziękujemy za zainteresowanie współpracą z projektem Balonis! 🎈

## 📋 Spis treści

- [Code of Conduct](#code-of-conduct)
- [Jak mogę pomóc?](#jak-mogę-pomóc)
- [Zgłaszanie błędów](#zgłaszanie-błędów)
- [Proponowanie funkcji](#proponowanie-funkcji)
- [Proces rozwoju](#proces-rozwoju)
- [Konwencje kodu](#konwencje-kodu)
- [Testowanie](#testowanie)
- [Dokumentacja](#dokumentacja)

## Code of Conduct

Projekt Balonis przestrzega [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/). Uczestnicząc w projekcie, zobowiązujesz się przestrzegać tego kodeksu.

## Jak mogę pomóc?

Istnieje wiele sposobów na wniesienie wkładu w projekt Balonis:

### 🐛 Zgłaszanie błędów
- Sprawdź [istniejące issues](../../issues) przed zgłoszeniem nowego
- Użyj szablonu bug report
- Podaj szczegółowe informacje o środowisku i krokach do odtworzenia

### ✨ Proponowanie funkcji
- Sprawdź [istniejące feature requests](../../issues?q=is%3Aissue+label%3Aenhancement)
- Użyj szablonu feature request
- Opisz szczegółowo proponowaną funkcję i jej uzasadnienie

### 💻 Kod
- Poprawki błędów
- Nowe funkcje
- Poprawa wydajności
- Refaktoryzacja kodu

### 📚 Dokumentacja
- Poprawa istniejącej dokumentacji
- Dodawanie przykładów
- Tłumaczenia
- Tutoriale

### 🧪 Testowanie
- Pisanie testów jednostkowych
- Testowanie integracyjne
- Testowanie UI/UX
- Testowanie wydajności

## Zgłaszanie błędów

Przed zgłoszeniem błędu:

1. **Sprawdź istniejące issues** - może ktoś już zgłosił ten problem
2. **Sprawdź dokumentację** - upewnij się, że to rzeczywiście błąd
3. **Przetestuj na najnowszej wersji** - błąd może być już naprawiony

### Jak zgłosić błąd

1. Przejdź do [Issues](../../issues/new/choose)
2. Wybierz "Bug Report"
3. Wypełnij szablon z następującymi informacjami:
   - Jasny opis błędu
   - Kroki do odtworzenia
   - Oczekiwane vs rzeczywiste zachowanie
   - Środowisko (OS, przeglądarka, wersja)
   - Zrzuty ekranu (jeśli dotyczy)
   - Logi błędów

## Proponowanie funkcji

Przed zaproponowaniem nowej funkcji:

1. **Sprawdź roadmap** - może funkcja jest już planowana
2. **Sprawdź istniejące feature requests** - może ktoś już to zaproponował
3. **Przemyśl use case** - czy funkcja będzie przydatna dla innych użytkowników

### Jak zaproponować funkcję

1. Przejdź do [Issues](../../issues/new/choose)
2. Wybierz "Feature Request"
3. Wypełnij szablon z następującymi informacjami:
   - Opis funkcji
   - Motywacja i use case
   - Szczegółowy opis implementacji
   - Mockupy/szkice (jeśli dotyczy)
   - Alternatywne rozwiązania

## Proces rozwoju

### 1. Fork i Clone

```bash
# Fork repozytorium na GitHub
# Następnie sklonuj swój fork
git clone https://github.com/YOUR_USERNAME/balonis-project.git
cd balonis-project

# Dodaj upstream remote
git remote add upstream https://github.com/ORIGINAL_OWNER/balonis-project.git
```

### 2. Utwórz branch

```bash
# Utwórz nowy branch dla swojej funkcji/poprawki
git checkout -b feature/nazwa-funkcji
# lub
git checkout -b fix/nazwa-poprawki
```

### 3. Rozwój

```bash
# Skonfiguruj środowisko deweloperskie
./scripts/setup.sh

# Uruchom aplikację
./scripts/start.sh

# Wprowadź zmiany...
```

### 4. Testowanie

```bash
# Backend testy
cd backend
source venv/bin/activate
python manage.py test

# Frontend testy (gdy będą dostępne)
cd frontend
npm test
```

### 5. Commit

```bash
# Dodaj zmiany
git add .

# Commit z opisową wiadomością
git commit -m "feat: add new balloon filtering feature"
```

### 6. Push i Pull Request

```bash
# Wypchnij branch
git push origin feature/nazwa-funkcji

# Utwórz Pull Request na GitHub
```

## Konwencje kodu

### Konwencje commitów

Używamy [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - nowa funkcja
- `fix:` - poprawka błędu
- `docs:` - dokumentacja
- `style:` - formatowanie kodu
- `refactor:` - refaktoryzacja
- `test:` - testy
- `chore:` - zadania maintenance

**Przykłady:**
```
feat: add product filtering by price range
fix: resolve CORS issue in production
docs: update API documentation
style: format code with black
refactor: extract common validation logic
test: add unit tests for product model
chore: update dependencies
```

### Python (Django Backend)

```python
# Używaj Black do formatowania
black .

# Używaj isort do sortowania importów
isort .

# Sprawdź kod z flake8
flake8 .

# Konwencje nazewnictwa
class ProductModel(models.Model):  # PascalCase dla klas
    def get_featured_products(self):  # snake_case dla funkcji
        pass

CONSTANT_VALUE = "value"  # UPPER_CASE dla stałych
```

### TypeScript (Next.js Frontend)

```typescript
// Używaj ESLint i Prettier
npm run lint
npm run format

// Konwencje nazewnictwa
interface ProductData {  // PascalCase dla interfejsów
  id: number;
  name: string;
}

const ProductCard = () => {  // PascalCase dla komponentów
  const [isLoading, setIsLoading] = useState(false);  // camelCase dla zmiennych
  
  return <div>...</div>;
};

export default ProductCard;
```

### CSS/Tailwind

```css
/* Używaj Tailwind CSS classes */
<div className="bg-emerald-50 p-4 rounded-lg shadow-sm">
  <h2 className="text-xl font-medium text-emerald-800">Title</h2>
</div>

/* Dla custom CSS używaj BEM notation */
.product-card {
  /* block */
}

.product-card__title {
  /* element */
}

.product-card--featured {
  /* modifier */
}
```

## Testowanie

### Backend (Django)

```python
# Testy jednostkowe
from django.test import TestCase
from products.models import Product

class ProductModelTest(TestCase):
    def test_product_creation(self):
        product = Product.objects.create(
            name="Test Product",
            price=100.00
        )
        self.assertEqual(product.name, "Test Product")

# Testy API
from rest_framework.test import APITestCase

class ProductAPITest(APITestCase):
    def test_get_products(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, 200)
```

### Frontend (Next.js)

```typescript
// Testy komponentów (gdy będą dostępne)
import { render, screen } from '@testing-library/react';
import ProductCard from './ProductCard';

test('renders product name', () => {
  render(<ProductCard name="Test Product" />);
  const nameElement = screen.getByText(/test product/i);
  expect(nameElement).toBeInTheDocument();
});
```

## Dokumentacja

### API Documentation

Aktualizuj `docs/API.md` gdy:
- Dodajesz nowe endpointy
- Zmieniasz istniejące endpointy
- Modyfikujesz struktury danych

### Code Documentation

```python
# Python docstrings
def get_featured_products(limit: int = 10) -> QuerySet:
    """
    Pobiera listę wyróżnionych produktów.
    
    Args:
        limit: Maksymalna liczba produktów do pobrania
        
    Returns:
        QuerySet z wyróżnionymi produktami
        
    Raises:
        ValueError: Gdy limit jest mniejszy niż 1
    """
    if limit < 1:
        raise ValueError("Limit must be at least 1")
    
    return Product.objects.filter(is_featured=True)[:limit]
```

```typescript
// TypeScript JSDoc
/**
 * Komponent karty produktu
 * 
 * @param product - Dane produktu do wyświetlenia
 * @param onAddToCart - Callback wywoływany przy dodaniu do koszyka
 * @returns JSX element karty produktu
 */
interface ProductCardProps {
  product: Product;
  onAddToCart: (productId: number) => void;
}

const ProductCard: React.FC<ProductCardProps> = ({ product, onAddToCart }) => {
  // ...
};
```

## Pull Request Guidelines

### Przed utworzeniem PR

- [ ] Kod jest sformatowany zgodnie z konwencjami
- [ ] Wszystkie testy przechodzą
- [ ] Dokumentacja jest aktualna
- [ ] Commit messages są zgodne z konwencjami
- [ ] Branch jest aktualny z main

### Opis PR

Użyj szablonu PR i wypełnij:
- Opis zmian
- Powiązane issues
- Typ zmiany
- Kroki do testowania
- Checklist

### Review Process

1. **Automatyczne sprawdzenia** - CI/CD pipeline musi przejść
2. **Code review** - co najmniej jeden maintainer musi zaaprobować
3. **Testing** - zmiany muszą być przetestowane
4. **Documentation** - dokumentacja musi być aktualna

## Wsparcie

Jeśli masz pytania:

1. **Sprawdź dokumentację** - README.md, docs/
2. **Sprawdź istniejące issues** - może ktoś już zadał to pytanie
3. **Utwórz nowe issue** - użyj szablonu "Question"
4. **Skontaktuj się z maintainerami** - przez GitHub issues

## Uznanie

Wszyscy kontrybutorzy będą wymienieni w sekcji Contributors w README.md.

---

Dziękujemy za wkład w rozwój Balonis! 🎈

