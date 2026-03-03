"use client";

import React from 'react';
import Header from '../components/Header';
import PropertyCard from '../components/PropertyCard';
import { ProtectedPage } from '../components/ProtectedPage';
import { useAuth } from '../hooks/useAuth';

export default function TenantHome() {
  const { user, logout } = useAuth();

  const sampleProperties = [
    { title: 'Ocean View 2BR Apartment', price: '$1,250', location: 'Nyali, Mombasa', image: '/images/nyali-1.jpg', href: '/property/1' },
    { title: 'Modern Studio Close to Beach', price: '$850', location: 'Nyali, Mombasa', image: '/images/nyali-2.jpg', href: '/property/2' },
    { title: 'Spacious 3BR Family Home', price: '$1,900', location: 'Kizingo, Mombasa', image: '/images/nyali-3.jpg', href: '/property/3' },
  ];

  return (
    <ProtectedPage requiredRole="tenant">
      <div className="min-h-screen">
        <Header />

        <main className="container py-12">
          <section className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center mb-12">
            <div>
              <h1 className="text-4xl md:text-5xl font-extrabold leading-tight">Find your next home in Nyali</h1>
              <p className="mt-4 text-lg muted">Discover curated listings, AI recommendations, and flexible payment options.</p>
              <div className="mt-6 flex gap-3">
                <a className="btn-primary" href="#search">Start Searching</a>
                <a className="px-4 py-2 rounded-md border border-white/10 muted" href="#learn">How it works</a>
              </div>
            </div>
            <div className="rounded-2xl overflow-hidden shadow-xl">
              <img src="/images/nyali-hero.jpg" alt="Nyali coastline" className="w-full h-72 object-cover" />
            </div>
          </section>

          <section id="search">
            <h2 className="text-2xl font-semibold mb-4">Featured listings</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {sampleProperties.map((p, i) => (
                <PropertyCard key={i} title={p.title} price={p.price} location={p.location} image={p.image} href={p.href} />
              ))}
            </div>
          </section>
        </main>
      </div>
    </ProtectedPage>
  );
}
