import React from 'react';
import Link from 'next/link';

type Props = {
  title: string;
  price?: string;
  location?: string;
  image?: string;
  href?: string;
}

export default function PropertyCard({ title, price, location, image, href }: Props) {
  const img = image || 'https://images.unsplash.com/photo-1560185127-6ae1b9d6f2c4?auto=format&fit=crop&w=1200&q=80';

  return (
    <Link href={href || '#'} className="block card hover:scale-105 transform transition">
      <div className="h-44 rounded-lg bg-cover bg-center mb-4" style={{ backgroundImage: `url('${img}')` }} />
      <div className="flex items-start justify-between">
        <div>
          <div className="text-lg font-semibold text-white">{title}</div>
          <div className="text-sm muted">{location}</div>
        </div>
        <div className="text-right">
          <div className="text-lg font-bold">{price || '—'}</div>
          <div className="text-sm muted">/month</div>
        </div>
      </div>
    </Link>
  );
}
