import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import Header from '@/components/Header'
import Footer from '@/components/Footer'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Balloon Shop - Шариковые композиции в Москве',
  description: 'Создаем незабываемые моменты с помощью красивых шариковых композиций. Доставка по Москве, индивидуальный подход, гарантия качества.',
  keywords: 'шарики, воздушные шары, композиции, праздник, день рождения, свадьба, доставка шаров москва',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ru">
      <body className={inter.className}>
        <Header />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  )
}

