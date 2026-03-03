import React, { useState, useEffect } from 'react';

export default function Carousel({ images }: { images: string[] }) {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    const t = setInterval(() => setIndex(i => (i + 1) % images.length), 4000);
    return () => clearInterval(t);
  }, [images.length]);

  if (!images || images.length === 0) return null;

  return (
    <div className="relative rounded-2xl overflow-hidden">
      <div className="h-64 md:h-96">
        {images.map((src, i) => (
          <img
            key={i}
            src={src}
            alt={`slide-${i}`}
            className={`w-full h-full object-cover absolute inset-0 transition-opacity duration-700 ${i === index ? 'opacity-100' : 'opacity-0'}`}
          />
        ))}
      </div>

      <div className="absolute left-4 top-1/2 transform -translate-y-1/2">
        <button onClick={() => setIndex((index-1+images.length)%images.length)} className="px-3 py-2 rounded-full bg-black/30 text-white">◀</button>
      </div>
      <div className="absolute right-4 top-1/2 transform -translate-y-1/2">
        <button onClick={() => setIndex((index+1)%images.length)} className="px-3 py-2 rounded-full bg-black/30 text-white">▶</button>
      </div>
    </div>
  );
}
