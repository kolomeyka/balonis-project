'use client';

import { useState, useEffect } from 'react';
import { apiClient, Product, Category, Color, Source } from '@/lib/api';

export default function CatalogPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [colors, setColors] = useState<Color[]>([]);
  const [sources, setSources] = useState<Source[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Фильтры
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [selectedColor, setSelectedColor] = useState<string>('');
  const [selectedSource, setSelectedSource] = useState<string>('');
  const [searchQuery, setSearchQuery] = useState<string>('');

  useEffect(() => {
    loadInitialData();
  }, []);

  useEffect(() => {
    loadProducts();
  }, [selectedCategory, selectedColor, selectedSource, searchQuery]);

  const loadInitialData = async () => {
    try {
      const [categoriesData, colorsData, sourcesData] = await Promise.all([
        apiClient.getCategories(),
        apiClient.getColors(),
        apiClient.getSources(),
      ]);
      
      setCategories(categoriesData.results || categoriesData);
      setColors(colorsData.results || colorsData);
      setSources(sourcesData.results || sourcesData);
    } catch (err) {
      console.error('Error loading initial data:', err);
      setError('Błąd ładowania danych');
    }
  };

  const loadProducts = async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      
      if (selectedCategory) params.append('category', selectedCategory);
      if (selectedColor) params.append('color', selectedColor);
      if (selectedSource) params.append('source', selectedSource);
      if (searchQuery) params.append('search', searchQuery);

      const data = await apiClient.getProducts(params);
      setProducts(data.results || data);
    } catch (err) {
      console.error('Error loading products:', err);
      setError('Błąd ładowania produktów');
    } finally {
      setLoading(false);
    }
  };

  const clearFilters = () => {
    setSelectedCategory('');
    setSelectedColor('');
    setSelectedSource('');
    setSearchQuery('');
  };

  if (error) {
    return (
      <div className="min-h-screen bg-stone-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-medium text-stone-800 mb-4">Błąd</h2>
          <p className="text-stone-600 mb-4">{error}</p>
          <button 
            onClick={() => window.location.reload()} 
            className="bg-emerald-600 text-white px-6 py-2 rounded-lg hover:bg-emerald-700 transition-colors"
          >
            Spróbuj ponownie
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-stone-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-stone-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <h1 className="text-4xl font-light text-stone-800 mb-4">Katalog kompozycji balonowych</h1>
          <p className="text-xl text-stone-600">Wybierz idealne balony na Twoje święto</p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Фильтры */}
          <div className="lg:w-1/4">
            <div className="bg-white rounded-2xl shadow-sm p-6 sticky top-4 border border-stone-200">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-lg font-medium text-stone-800">Filtry</h2>
                <button 
                  onClick={clearFilters}
                  className="text-sm text-emerald-600 hover:text-emerald-700"
                >
                  Wyczyść
                </button>
              </div>

              {/* Поиск */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-stone-700 mb-2">
                  Szukaj
                </label>
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Znajdź produkt..."
                  className="w-full px-3 py-2 border border-stone-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
                />
              </div>

              {/* Категории */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-stone-700 mb-2">
                  Kategoria
                </label>
                <select
                  value={selectedCategory}
                  onChange={(e) => setSelectedCategory(e.target.value)}
                  className="w-full px-3 py-2 border border-stone-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
                >
                  <option value="">Wszystkie kategorie</option>
                  {categories.map((category) => (
                    <option key={category.id} value={category.slug}>
                      {category.name}
                    </option>
                  ))}
                </select>
              </div>

              {/* Цвета */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-stone-700 mb-2">
                  Kolor
                </label>
                <select
                  value={selectedColor}
                  onChange={(e) => setSelectedColor(e.target.value)}
                  className="w-full px-3 py-2 border border-stone-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
                >
                  <option value="">Wszystkie kolory</option>
                  {colors.map((color) => (
                    <option key={color.id} value={color.id.toString()}>
                      {color.name}
                    </option>
                  ))}
                </select>
              </div>

              {/* Источники */}
              <div className="mb-6">
                <label className="block text-sm font-medium text-stone-700 mb-2">
                  Źródło materiałów
                </label>
                <select
                  value={selectedSource}
                  onChange={(e) => setSelectedSource(e.target.value)}
                  className="w-full px-3 py-2 border border-stone-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
                >
                  <option value="">Wszystkie źródła</option>
                  {sources.map((source) => (
                    <option key={source.id} value={source.id.toString()}>
                      {source.name}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {/* Товары */}
          <div className="lg:w-3/4">
            {loading ? (
              <div className="flex items-center justify-center py-12">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-600"></div>
              </div>
            ) : products.length === 0 ? (
              <div className="text-center py-12">
                <h3 className="text-lg font-medium text-stone-800 mb-2">Nie znaleziono produktów</h3>
                <p className="text-stone-600">Spróbuj zmienić filtry wyszukiwania</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                {products.map((product) => (
                  <ProductCard key={product.id} product={product} />
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

function ProductCard({ product }: { product: Product }) {
  const mainImage = product.images?.find(img => img.is_main) || product.images?.[0];

  return (
    <div className="bg-white rounded-2xl shadow-sm hover:shadow-md transition-all duration-300 border border-stone-200">
      {/* Изображение */}
      <div className="aspect-square bg-stone-100 rounded-t-2xl overflow-hidden">
        {mainImage ? (
          <img
            src={mainImage.image}
            alt={mainImage.alt_text || product.name}
            className="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-stone-400">
            <svg className="w-16 h-16" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clipRule="evenodd" />
            </svg>
          </div>
        )}
      </div>

      {/* Контент */}
      <div className="p-6">
        <h3 className="text-lg font-medium text-stone-800 mb-3 line-clamp-2">
          {product.name}
        </h3>
        
        {product.short_description && (
          <p className="text-sm text-stone-600 mb-4 line-clamp-2">
            {product.short_description}
          </p>
        )}

        {/* Цена */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-2">
            {product.has_discount && product.discount_price ? (
              <>
                <span className="text-lg font-medium text-emerald-600">
                  {product.discount_price} zł
                </span>
                <span className="text-sm text-stone-500 line-through">
                  {product.base_price} zł
                </span>
              </>
            ) : (
              <span className="text-lg font-medium text-stone-800">
                {product.current_price} zł
              </span>
            )}
          </div>
          
          {product.is_featured && (
            <span className="bg-emerald-100 text-emerald-800 text-xs font-medium px-2 py-1 rounded-full">
              Hit
            </span>
          )}
        </div>

        {/* Кнопка */}
        <button className="w-full bg-emerald-600 text-white py-3 px-4 rounded-xl hover:bg-emerald-700 transition-all duration-300 font-medium">
          Dodaj do zamówienia
        </button>
      </div>
    </div>
  );
}

