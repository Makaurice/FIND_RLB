"use client";

import React from 'react';
import Header from '../../components/Header';
import Carousel from '../../components/Carousel';

export default function PropertyDetail({ params }: any) {
  // params.id is available when using Next dynamic routes in App Router; for Pages router we can parse router.query
  const images = [
    'https://images.unsplash.com/photo-1560185127-6ae1b9d6f2c4?auto=format&fit=crop&w=1400&q=80',
    'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1400&q=80',
  ];

  return (
    <div className="min-h-screen">
      <Header />
      <main className="container py-12">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2">
            <Carousel images={images} />
            <div className="mt-6 card">
              <h2 className="text-2xl font-bold">Ocean View 2BR Apartment</h2>
              <div className="mt-2 muted">Nyali, Mombasa</div>
              <div className="mt-4 text-xl font-semibold">$1,250 / month</div>
              <p className="mt-4 muted">Beautiful apartment with sea view, close to beach and amenities. Flexible lease terms available.</p>
            </div>
          </div>

          <aside className="lg:col-span-1">
            <div className="card">
              <h3 className="font-semibold">Contact landlord</h3>
              <div className="mt-4">
                <button className="btn-primary w-full">Request viewing</button>
              </div>
              <div className="mt-4 muted text-sm">Earn rewards for timely payments.</div>
            </div>
          </aside>
        </div>
      </main>
    </div>
  );
}
