'use client';

import { useState, useEffect } from 'react';
import { apiClient } from '@/lib/api';

interface Product {
  id: number;
  name: string;
  description: string;
  base_price: number;
  discount_price?: number;
  current_price: number;
  is_featured: boolean;
  image?: string;
  category: {
    id: number;
    name: string;
  };
  color: {
    id: number;
    name: string;
    hex_code: string;
  };
  sources: Array<{
    id: number;
    name: string;
    url: string;
    description?: string;
  }>;
}

interface Category {
  id: number;
  name: string;
  slug: string;
}

interface Color {
  id: number;
  name: string;
  hex_code: string;
}

interface Source {
  id: number;
  name: string;
  url: string;
  description?: string;
}

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
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <h1 className="text-4xl font-light text-stone-800 mb-4">Katalog kompozycji balonowych</h1>
          <p className="text-xl text-stone-600">Wybierz idealne balony na Twoje święto</p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Фильтры */}
        <div className="bg-white rounded-2xl shadow-sm p-6 sticky top-4 border border-stone-200 mb-8">
          <div className="flex flex-col lg:flex-row gap-8">
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
                className="w-full px-3 py-2 border border-stone-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
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
                className="w-full px-3 py-2 border border-stone-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
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
                className="w-full px-3 py-2 border border-stone-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
              >
                <option value="">Wszystkie kolory</option>
                {colors.map((color) => (
                  <option key={color.id} value={color.name}>
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
                className="w-full px-3 py-2 border border-stone-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500"
              >
                <option value="">Wszystkie źródła</option>
                {sources.map((source) => (
                  <option key={source.id} value={source.name}>
                    {source.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Кнопка очистки */}
            <div className="flex items-end">
              <button
                onClick={clearFilters}
                className="text-sm text-emerald-600 hover:text-emerald-700 font-medium px-2 py-1 rounded-full"
              >
                Wyczyść
              </button>
            </div>
          </div>
        </div>

        {/* Товары */}
        <div className="flex flex-col lg:flex-row gap-8">
          <div className="flex-1">
            {loading ? (
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center space-x-2">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-emerald-600"></div>
                  <span className="text-lg font-medium text-stone-800">
                    Ładowanie produktów...
                  </span>
                </div>
              </div>
            ) : (
              <>
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-lg font-medium text-stone-800">
                    {products.length} produktów
                  </h2>
                </div>

                {products.length === 0 ? (
                  <div className="text-center py-12">
                    <p className="text-stone-600 text-lg line-clamp-2">
                      {product.short_description}
                    </p>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {products.map((product) => (
                      <div key={product.id} className="bg-white rounded-2xl shadow-sm overflow-hidden border border-stone-200 hover:shadow-md transition-shadow">
                        <div className="aspect-square bg-stone-100 relative">
                          {product.image ? (
                            <img
                              src={product.image}
                              alt={product.name}
                              className="w-full h-full object-cover"
                              onError={(e) => {
                                const target = e.target as HTMLImageElement;
                                target.src = '/images/placeholder-product.jpg';
                              }}
                            />
                          ) : (
                            <div className="w-full h-full flex items-center justify-center">
                              <span className="text-stone-400 text-sm">Brak zdjęcia</span>
                            </div>
                          )}
                          {product.is_featured && (
                            <span className="absolute top-4 left-4 bg-emerald-100 text-emerald-800 text-xs font-medium px-2 py-1 rounded-full">
                              Hit
                            </span>
                          )}
                        </div>
                        
                        <div className="p-6">
                          <h3 className="text-lg font-medium text-stone-800 mb-2">
                            {product.name}
                          </h3>
                          <p className="text-stone-600 text-sm mb-4 line-clamp-2">
                            {product.description}
                          </p>
                          
                          <div className="flex items-center justify-between mb-6">
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
                          
                          {/* Кнопка */}
                          <button className="w-full bg-emerald-600 text-white py-3 px-4 rounded-xl hover:bg-emerald-700 transition-colors font-medium">
                            Dodaj do zamówienia
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

