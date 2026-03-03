"use client";

import React, { useEffect, useState } from 'react';
import Header from '../components/Header';
import PropertyCard from '../components/PropertyCard';
import FiltersSidebar from '../components/FiltersSidebar';
import axios from 'axios';
import MapView from '../components/MapView';

type Prop = { id:number, title:string, location:string, property_type:string, beds:number, price:number, image?:string, href?:string }

export default function Listings() {
  const [properties, setProperties] = useState<Prop[]>([]);
  const [loading, setLoading] = useState(false);
  const [showMap, setShowMap] = useState(false);

  async function fetchProperties(filters: any = {}){
    setLoading(true);
    try{
      const params = new URLSearchParams();
      Object.entries(filters).forEach(([k,v])=>{ if(v !== undefined && v !== null && v !== '') params.append(k, String(v)); });
      const url = `/api/search/properties${params.toString()?('?'+params.toString()):''}`;
      const res = await axios.get(url);
      const data = res.data.map((p:any)=>({ ...p, price: p.price, image: p.image }));
      setProperties(data);
    }catch(e){
      console.error('fetchProperties error', e);
    }finally{ setLoading(false); }
  }

  useEffect(()=>{ fetchProperties(); }, []);

  return (
    <div className="min-h-screen">
      <Header />
      <main className="container py-12">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          <div className="lg:col-span-1">
            <FiltersSidebar onChange={(f)=>fetchProperties(f)} />
          </div>
          <div className="lg:col-span-3">
            <div className="flex items-center justify-between mb-6">
              <h1 className="text-2xl font-semibold">Available properties</h1>
              <div className="muted">Showing {properties.length} results</div>
            </div>

            <div className="mb-4 flex items-center justify-between">
              <div>
                <label className="inline-flex items-center gap-2">
                  <input type="checkbox" checked={showMap} onChange={(e)=>setShowMap(e.target.checked)} />
                  <span className="ml-1 muted">Show map view</span>
                </label>
              </div>
              {loading ? <div className="muted">Loading…</div> : <div className="muted">Showing {properties.length} results</div>}
            </div>

            {showMap ? (
              <MapView properties={properties} />
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {properties.map((p) => (
                  <PropertyCard key={p.id} title={p.title} price={`$${p.price}`} location={p.location} image={p.image} href={`/property/${p.id}`} />
                ))}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
