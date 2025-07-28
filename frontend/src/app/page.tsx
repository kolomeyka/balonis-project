'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import Image from "next/image"
import logoImage from './images/logo.jpg';
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
       <div
        style={{
          display: "flex",
          justifyContent: "center",
        }}
      >
        <Image src="/images/logo.jpg" width="500" height="500" />
      </div>
        {/*<div style={{maxWidth:'100%', width:'1000px'}}>*/}
          {/*<div style={{position:'relative', paddingBottom:'100%'}}>*/}
          {/*  <img*/}
          {/*      src="/images/logo.jpg"*/}
          {/*      // srcSet="/_next/image?url=/image.png&amp;w=320&amp;q=75 320w, /_next/image?url=/image.png&amp;w=420&amp;q=75 420w"*/}
          {/*      style={{visibility:'visible', height:'100%', left:100, position:'absolute', top:'0', width:'100%'}}  // <-- your style is added here*/}
          {/*  />*/}
          {/*</div>*/}

        {/*</div>*/}
        {/*<div>*/}
        {/*  <img src="/images/logo.jpg" alt="Description of image"/>*/}
        {/*</div>*/}
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-2">
          <div className="text-center">

            <h1 className="text-5xl md:text-7xl font-light mb-8 tracking-wide">
              {/*<span className="text-emerald-700 font-medium">Balonis</span>*/}
              <br/>

              <span className="text-2xl md:text-3xl font-light text-stone-600 mt-4 block">
                Bierzemy na siebie ciężar organizacji
              </span>
              <br/>
            </h1>
            {/*<p className="text-lg md:text-xl mb-12 max-w-2xl mx-auto text-stone-600 leading-relaxed">*/}
            {/*  Zamieniamy Twoje wyjątkowe chwile w niezapomniane wspomnienia */}
            {/*  dzięki pięknym kompozycjom balonowym*/}
            {/*</p>*/}
            <div className="flex flex-col sm:flex-row gap-6 justify-center">
              <Link
                  href="/catalog"
                  className="bg-emerald-600 text-white px-10 py-4 rounded-full font-medium text-lg hover:bg-emerald-700 transition-all duration-300 flex items-center justify-center shadow-lg hover:shadow-xl"
              >
                Zobacz katalog
                <ArrowRight className="ml-3 w-5 h-5"/>
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
    </div>
  );
}

