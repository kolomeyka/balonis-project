'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { Star, ArrowRight, Heart, Gift, Truck, Shield, Users } from 'lucide-react';
import { apiClient, Product, GalleryImage, ClientReview } from '@/lib/api';

export default function HomePage() {
  const [featuredProducts, setFeaturedProducts] = useState<Product[]>([]);
  const [galleryImages, setGalleryImages] = useState<GalleryImage[]>([]);
  const [reviews, setReviews] = useState<ClientReview[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Пробуем загрузить featured данные, если их нет - загружаем обычные
        const [productsData, galleryData, reviewsData] = await Promise.all([
          apiClient.getFeaturedProducts().catch(() => apiClient.getProducts()),
          apiClient.getFeaturedGallery().catch(() => apiClient.getGalleryImages()),
          apiClient.getFeaturedReviews().catch(() => apiClient.getClientReviews()),
        ]);

        const products = productsData.results || productsData || [];
        const gallery = galleryData.results || galleryData || [];
        const clientReviews = reviewsData.results || reviewsData || [];

        setFeaturedProducts(Array.isArray(products) ? products : []);
        setGalleryImages(Array.isArray(gallery) ? gallery : []);
        setReviews(Array.isArray(clientReviews) ? clientReviews : []);
      } catch (error) {
        console.error('Error fetching data:', error);
        // Устанавливаем пустые массивы в случае ошибки
        setFeaturedProducts([]);
        setGalleryImages([]);
        setReviews([]);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const advantages = [
    {
      icon: <Truck className="w-8 h-8" />,
      title: 'Szybka dostawa',
      description: 'Dostarczamy w całej Warszawie tego samego dnia',
    },
    {
      icon: <Heart className="w-8 h-8" />,
      title: 'Indywidualne dekoracje',
      description: 'Tworzymy unikalne kompozycje według Twoich życzeń',
    },
    {
      icon: <Shield className="w-8 h-8" />,
      title: 'Gwarancja jakości',
      description: 'Używamy tylko wysokiej jakości materiałów',
    },
    {
      icon: <Users className="w-8 h-8" />,
      title: 'Doświadczony zespół',
      description: 'Ponad 5 lat tworzenia świątecznego nastroju',
    },
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-stone-100 via-stone-50 to-emerald-50 text-stone-800">
        <div className="absolute inset-0 bg-gradient-to-r from-emerald-100/30 to-stone-100/30"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-32">
          <div className="text-center">
            <h1 className="text-5xl md:text-7xl font-light mb-8 tracking-wide">
              <span className="text-emerald-700 font-medium">Balonis</span>
              <br />
              <span className="text-2xl md:text-3xl font-light text-stone-600 mt-4 block">
                Bierzemy na siebie ciężar organizacji
              </span>
            </h1>
            <p className="text-lg md:text-xl mb-12 max-w-2xl mx-auto text-stone-600 leading-relaxed">
              Zamieniamy Twoje wyjątkowe chwile w niezapomniane wspomnienia 
              dzięki pięknym kompozycjom balonowym
            </p>
            <div className="flex flex-col sm:flex-row gap-6 justify-center">
              <Link
                href="/catalog"
                className="bg-emerald-600 text-white px-10 py-4 rounded-full font-medium text-lg hover:bg-emerald-700 transition-all duration-300 flex items-center justify-center shadow-lg hover:shadow-xl"
              >
                Zobacz katalog
                <ArrowRight className="ml-3 w-5 h-5" />
              </Link>
              <Link
                href="/contacts"
                className="border-2 border-emerald-600 text-emerald-700 px-10 py-4 rounded-full font-medium text-lg hover:bg-emerald-50 transition-all duration-300"
              >
                Zamów konsultację
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Advantages Section */}
      <section className="py-20 bg-stone-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-light text-stone-800 mb-6">
              Dlaczego nas wybierają
            </h2>
            <p className="text-xl text-stone-600 max-w-2xl mx-auto leading-relaxed">
              Wiemy, jak uczynić Twoje święto wyjątkowym
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {advantages.map((advantage, index) => (
              <div
                key={index}
                className="text-center p-8 bg-white rounded-2xl shadow-sm hover:shadow-md transition-all duration-300 border border-stone-100"
              >
                <div className="text-emerald-600 mb-6 flex justify-center">
                  {advantage.icon}
                </div>
                <h3 className="text-xl font-medium text-stone-800 mb-4">
                  {advantage.title}
                </h3>
                <p className="text-stone-600 leading-relaxed">
                  {advantage.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Products */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Популярные композиции
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Наши самые любимые клиентами шариковые композиции
            </p>
          </div>

          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {[...Array(6)].map((_, index) => (
                <div key={index} className="bg-gray-200 animate-pulse rounded-xl h-80"></div>
              ))}
            </div>
          ) : featuredProducts.length === 0 ? (
            <div className="text-center py-12">
              <div className="text-gray-400 mb-4">
                <Gift className="w-16 h-16 mx-auto" />
              </div>
              <h3 className="text-lg font-medium text-gray-900 mb-2">Товары скоро появятся</h3>
              <p className="text-gray-600">Мы работаем над наполнением каталога</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {featuredProducts.slice(0, 6).map((product) => (
                <div
                  key={product.id}
                  className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-200"
                >
                  <div className="relative h-48">
                    {product.images && product.images.length > 0 ? (
                      <Image
                        src={product.images[0].image}
                        alt={product.name}
                        fill
                        className="object-cover"
                      />
                    ) : (
                      <div className="w-full h-full bg-gradient-to-br from-pink-100 to-purple-100 flex items-center justify-center">
                        <Gift className="w-16 h-16 text-pink-300" />
                      </div>
                    )}
                    {product.has_discount && (
                      <div className="absolute top-2 right-2 bg-red-500 text-white px-2 py-1 rounded-full text-sm font-semibold">
                        Скидка
                      </div>
                    )}
                  </div>
                  <div className="p-6">
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">
                      {product.name}
                    </h3>
                    <p className="text-gray-600 mb-4 line-clamp-2">
                      {product.short_description}
                    </p>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        {product.has_discount && (
                          <span className="text-gray-400 line-through">
                            {product.base_price}₽
                          </span>
                        )}
                        <span className="text-2xl font-bold text-pink-600">
                          {product.current_price}₽
                        </span>
                      </div>
                      <Link
                        href={`/products/${product.slug}`}
                        className="bg-pink-600 text-white px-4 py-2 rounded-lg hover:bg-pink-700 transition-colors duration-200"
                      >
                        Подробнее
                      </Link>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}

          <div className="text-center mt-12">
            <Link
              href="/catalog"
              className="bg-pink-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-pink-700 transition-colors duration-200 inline-flex items-center"
            >
              Посмотреть все товары
              <ArrowRight className="ml-2 w-5 h-5" />
            </Link>
          </div>
        </div>
      </section>

      {/* Gallery Preview */}
      <section className="py-16 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Наши работы
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Посмотрите, как мы украшаем праздники наших клиентов
            </p>
          </div>

          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[...Array(6)].map((_, index) => (
                <div key={index} className="bg-gray-200 animate-pulse rounded-xl h-64"></div>
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {galleryImages.slice(0, 6).map((image) => (
                <div
                  key={image.id}
                  className="relative rounded-xl overflow-hidden shadow-lg hover:shadow-xl transition-shadow duration-200 group"
                >
                  <div className="relative h-64">
                    <Image
                      src={image.image}
                      alt={image.title}
                      fill
                      className="object-cover group-hover:scale-105 transition-transform duration-200"
                    />
                    <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-all duration-200"></div>
                  </div>
                  <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black to-transparent p-4">
                    <h3 className="text-white font-semibold">{image.title}</h3>
                    <p className="text-gray-200 text-sm">{image.event_type}</p>
                  </div>
                </div>
              ))}
            </div>
          )}

          <div className="text-center mt-12">
            <Link
              href="/gallery"
              className="bg-purple-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-purple-700 transition-colors duration-200 inline-flex items-center"
            >
              Посмотреть все работы
              <ArrowRight className="ml-2 w-5 h-5" />
            </Link>
          </div>
        </div>
      </section>

      {/* Reviews Section */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Отзывы клиентов
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Что говорят о нас наши довольные клиенты
            </p>
          </div>

          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {[...Array(3)].map((_, index) => (
                <div key={index} className="bg-gray-200 animate-pulse rounded-xl h-48"></div>
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {reviews.slice(0, 3).map((review) => (
                <div
                  key={review.id}
                  className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-200"
                >
                  <div className="flex items-center mb-4">
                    {[...Array(5)].map((_, i) => (
                      <Star
                        key={i}
                        className={`w-5 h-5 ${
                          i < review.rating ? 'text-yellow-400 fill-current' : 'text-gray-300'
                        }`}
                      />
                    ))}
                  </div>
                  <p className="text-gray-700 mb-4 line-clamp-4">
                    {review.review_text}
                  </p>
                  <div className="flex items-center">
                    <div className="w-10 h-10 bg-gradient-to-r from-pink-500 to-purple-600 rounded-full flex items-center justify-center">
                      <span className="text-white font-semibold">
                        {review.name.charAt(0)}
                      </span>
                    </div>
                    <div className="ml-3">
                      <p className="font-semibold text-gray-900">{review.name}</p>
                      <p className="text-sm text-gray-500">
                        {new Date(review.created_at).toLocaleDateString('ru-RU')}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-16 bg-gradient-to-r from-pink-600 to-purple-600 text-white">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl md:text-4xl font-bold mb-4">
            Готовы создать незабываемый праздник?
          </h2>
          <p className="text-xl mb-8">
            Свяжитесь с нами прямо сейчас и получите бесплатную консультацию
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/contacts"
              className="bg-white text-purple-600 px-8 py-4 rounded-full font-semibold text-lg hover:bg-gray-100 transition-colors duration-200"
            >
              Заказать звонок
            </Link>
            <a
              href="https://wa.me/79999999999"
              target="_blank"
              rel="noopener noreferrer"
              className="border-2 border-white text-white px-8 py-4 rounded-full font-semibold text-lg hover:bg-white hover:text-purple-600 transition-colors duration-200"
            >
              Написать в WhatsApp
            </a>
          </div>
        </div>
      </section>
    </div>
  );
}

