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
          apiClient.getGalleryImages().catch(() => []),
          apiClient.getClientReviews().catch(() => []),
        ]);

        const products = productsData.results || productsData || [];
        const gallery = galleryData.results || galleryData || [];
        const clientReviews = reviewsData.results || reviewsData || [];

        setFeaturedProducts(products);
        setGalleryImages(gallery);
        setReviews(clientReviews);
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
      icon: <Gift className="w-8 h-8" />,
      title: 'Szybka dostawa',
      description: 'Dostarczamy w całej Warszawie tego samego dnia',
    },
    {
      icon: <Truck className="w-8 h-8" />,
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
      {/* Hero Section - изменен фон под цвет лого */}
      <section className="relative py-20 px-4 sm:px-6 lg:px-8" style={{ backgroundColor: '#F8F6F0' }}>
        <div className="max-w-7xl mx-auto text-center">
          <div className="mb-8">
            <Image
              src="/images/logo.jpg"
              alt="Balonis Logo"
              width={200}
              height={200}
              className="mx-auto rounded-full shadow-lg"
            />
          </div>
          <h1 className="text-5xl md:text-6xl font-light mb-6" style={{ color: '#2D4A32' }}>
            Balonis
          </h1>
          <p className="text-xl md:text-2xl mb-8 font-light" style={{ color: '#4A7C59' }}>
            Bierzemy na siebie ciężar organizacji świąt
          </p>
          <p className="text-lg mb-12 max-w-3xl mx-auto leading-relaxed" style={{ color: '#2D4A32' }}>
            Tworzymy magiczne kompozycje balonowe, które sprawią, że Twoje święto będzie niezapomniane.
            Każda dekoracja jest starannie przygotowana z myślą o Twoich marzeniach.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/catalog"
              className="inline-flex items-center px-8 py-4 text-lg font-medium rounded-full shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
              style={{ backgroundColor: '#4A7C59', color: 'white' }}
            >
              Zobacz katalog
              <ArrowRight className="ml-2 w-5 h-5" />
            </Link>
            <Link
              href="#gallery"
              className="inline-flex items-center px-8 py-4 text-lg font-medium rounded-full border-2 hover:shadow-lg transition-all duration-300"
              style={{ borderColor: '#4A7C59', color: '#4A7C59', backgroundColor: 'white' }}
            >
              Nasza galeria
            </Link>
          </div>
        </div>
      </section>

      {/* Advantages Section - обновлены цвета */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-white">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl font-light text-center mb-16" style={{ color: '#2D4A32' }}>
            Dlaczego wybierają nas
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {advantages.map((advantage, index) => (
              <div
                key={index}
                className="text-center p-8 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
                style={{ backgroundColor: '#B8D4D1' }}
              >
                <div className="inline-flex items-center justify-center w-16 h-16 rounded-full mb-6" style={{ backgroundColor: '#4A7C59', color: 'white' }}>
                  {advantage.icon}
                </div>
                <h3 className="text-xl font-medium mb-4" style={{ color: '#2D4A32' }}>
                  {advantage.title}
                </h3>
                <p style={{ color: '#2D4A32' }}>
                  {advantage.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Products Section - исправлена загрузка изображений */}
      <section className="py-20 px-4 sm:px-6 lg:px-8" style={{ backgroundColor: '#F8F6F0' }}>
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl font-light text-center mb-16" style={{ color: '#2D4A32' }}>
            Polecane kompozycje
          </h2>

          {loading ? (
            <div className="text-center py-12">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2" style={{ borderColor: '#4A7C59' }}></div>
              <p className="mt-4" style={{ color: '#4A7C59' }}>Ładowanie produktów...</p>
            </div>
          ) : featuredProducts && featuredProducts.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {featuredProducts.slice(0, 6).map((product) => (
                <div
                  key={product.id}
                  className="bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 overflow-hidden"
                >
                  <div className="aspect-w-16 aspect-h-12 relative">
                    <Image
                      src={apiClient.getImageUrl(product.image)}
                      alt={product.name}
                      fill
                      className="object-cover"
                      onError={(e) => {
                        const target = e.target as HTMLImageElement;
                        target.src = '/images/placeholder.jpg';
                      }}
                    />
                  </div>
                  <div className="p-6">
                    <h3 className="text-xl font-medium mb-2" style={{ color: '#2D4A32' }}>
                      {product.name}
                    </h3>
                    <p className="mb-4" style={{ color: '#4A7C59' }}>
                      {product.description}
                    </p>
                    <div className="flex items-center justify-between">
                      <span className="text-2xl font-light" style={{ color: '#2D4A32' }}>
                        {product.price} zł
                      </span>
                      <div className="flex items-center">
                        <Star className="w-4 h-4 fill-current" style={{ color: '#4A7C59' }} />
                        <Star className="w-4 h-4 fill-current" style={{ color: '#4A7C59' }} />
                        <Star className="w-4 h-4 fill-current" style={{ color: '#4A7C59' }} />
                        <Star className="w-4 h-4 fill-current" style={{ color: '#4A7C59' }} />
                        <Star className="w-4 h-4 fill-current" style={{ color: '#4A7C59' }} />
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <p className="text-xl" style={{ color: '#4A7C59' }}>
                Produkty będą wkrótce dostępne
              </p>
            </div>
          )}

          <div className="text-center mt-12">
            <Link
              href="/catalog"
              className="inline-flex items-center px-8 py-4 text-lg font-medium rounded-full shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
              style={{ backgroundColor: '#4A7C59', color: 'white' }}
            >
              Zobacz wszystkie produkty
              <ArrowRight className="ml-2 w-5 h-5" />
            </Link>
          </div>
        </div>
      </section>

      {/* Gallery Section */}
      <section id="gallery" className="py-20 px-4 sm:px-6 lg:px-8 bg-white">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl font-light text-center mb-16" style={{ color: '#2D4A32' }}>
            Nasza galeria
          </h2>

          {galleryImages && galleryImages.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {galleryImages.slice(0, 6).map((image) => (
                <div
                  key={image.id}
                  className="aspect-w-16 aspect-h-12 rounded-2xl overflow-hidden shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
                >
                  <Image
                    src={apiClient.getImageUrl(image.image)}
                    alt={image.title}
                    fill
                    className="object-cover"
                    onError={(e) => {
                      const target = e.target as HTMLImageElement;
                      target.src = '/images/placeholder.jpg';
                    }}
                  />
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <p className="text-xl" style={{ color: '#4A7C59' }}>
                Galeria będzie wkrótce dostępna
              </p>
            </div>
          )}
        </div>
      </section>

      {/* Reviews Section */}
      {reviews && reviews.length > 0 && (
        <section className="py-20 px-4 sm:px-6 lg:px-8" style={{ backgroundColor: '#F8F6F0' }}>
          <div className="max-w-7xl mx-auto">
            <h2 className="text-4xl font-light text-center mb-16" style={{ color: '#2D4A32' }}>
              Opinie klientów
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {reviews.slice(0, 3).map((review) => (
                <div
                  key={review.id}
                  className="bg-white p-8 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300"
                >
                  <div className="flex items-center mb-4">
                    {[...Array(5)].map((_, i) => (
                      <Star
                        key={i}
                        className={`w-5 h-5 ${
                          i < review.rating ? 'fill-current' : ''
                        }`}
                        style={{ color: '#4A7C59' }}
                      />
                    ))}
                  </div>
                  <p className="mb-4 italic" style={{ color: '#2D4A32' }}>
                    "{review.comment}"
                  </p>
                  <p className="font-medium" style={{ color: '#4A7C59' }}>
                    — {review.client_name}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </section>
      )}
    </div>
  );
}