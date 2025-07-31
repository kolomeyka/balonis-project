'use client';

import Link from 'next/link';
import { Heart, Phone, Mail, MapPin, Instagram, MessageCircle } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Company Info */}
          <div className="space-y-4">
            <div className="flex items-center">
              <div className="w-8 h-8 bg-gradient-to-r from-pink-500 to-purple-600 rounded-full flex items-center justify-center">
                <Heart className="w-5 h-5 text-white" />
              </div>
              <span className="ml-2 text-lg font-bold">Balloon Shop</span>
            </div>
            <p className="text-gray-300 text-sm">
              Tworzymy twoje momenty.
              Indiwidualne podejscie do zamówień i gwarancja jakosci.
            </p>
            <div className="flex space-x-4">
              <a
                href="https://instagram.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-pink-500 transition-colors duration-200"
              >
                <Instagram className="w-5 h-5" />
              </a>
              <a
                href="https://wa.me/79999999999"
                target="_blank"
                rel="noopener noreferrer"
                className="text-gray-400 hover:text-green-500 transition-colors duration-200"
              >
                <MessageCircle className="w-5 h-5" />
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Nawigacja</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/catalog" className="text-gray-300 hover:text-white transition-colors duration-200">
                  Katalog
                </Link>
              </li>
              <li>
                <Link href="/gallery" className="text-gray-300 hover:text-white transition-colors duration-200">
                  Nasze realizacje
                </Link>
              </li>
              <li>
                <Link href="/delivery" className="text-gray-300 hover:text-white transition-colors duration-200">
                  Dostawa i platnośc
                </Link>
              </li>
              <li>
                <Link href="/contacts" className="text-gray-300 hover:text-white transition-colors duration-200">
                  Kontakt
                </Link>
              </li>
            </ul>
          </div>

          {/* Categories */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">Категории</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/catalog?theme=birthday" className="text-gray-300 hover:text-white transition-colors duration-200">
                  День рождения
                </Link>
              </li>
              <li>
                <Link href="/catalog?theme=wedding" className="text-gray-300 hover:text-white transition-colors duration-200">
                  Свадьба
                </Link>
              </li>
              <li>
                <Link href="/catalog?theme=corporate" className="text-gray-300 hover:text-white transition-colors duration-200">
                  Корпоративы
                </Link>
              </li>
              <li>
                <Link href="/catalog?theme=baby_shower" className="text-gray-300 hover:text-white transition-colors duration-200">
                  Рождение ребенка
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact Info */}
          <div className="space-y-4">
            <h3 className="text-lg font-semibold">KONTAKT</h3>
            <div className="space-y-3">
              <div className="flex items-center space-x-3">
                <Phone className="w-4 h-4 text-pink-500" />
                <a
                  href="tel:+489999999999"
                  className="text-gray-300 hover:text-white transition-colors duration-200"
                >
                  +48 (999) 999-99-99
                </a>
              </div>
              <div className="flex items-center space-x-3">
                <Mail className="w-4 h-4 text-pink-500" />
                <a
                  href="mailto:info@balonis.pl"
                  className="text-gray-300 hover:text-white transition-colors duration-200"
                >
                  info@balonis.pl
                </a>
              </div>
              <div className="flex items-start space-x-3">
                <MapPin className="w-4 h-4 text-pink-500 mt-1" />
                <span className="text-gray-300">
                  Krakow
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-gray-800 mt-8 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <p className="text-gray-400 text-sm">
              © 2024 Balloon Shop. Все права защищены.
            </p>
            <div className="flex space-x-6 mt-4 md:mt-0">
              <Link href="/privacy" className="text-gray-400 hover:text-white text-sm transition-colors duration-200">
                Политика конфиденциальности
              </Link>
              <Link href="/terms" className="text-gray-400 hover:text-white text-sm transition-colors duration-200">
                Условия использования
              </Link>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}

