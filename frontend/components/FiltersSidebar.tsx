import React, { useState } from 'react';

export default function FiltersSidebar({ onChange }: { onChange?: (f:any)=>void }) {
  const [priceMin, setPriceMin] = useState('');
  const [priceMax, setPriceMax] = useState('');
  const [beds, setBeds] = useState('');
  const [propertyType, setPropertyType] = useState('');
  const [location, setLocation] = useState('');
  const [lat, setLat] = useState('');
  const [lon, setLon] = useState('');
  const [radius, setRadius] = useState('');
  const [sortBy, setSortBy] = useState('');
  const [order, setOrder] = useState('asc');

  function apply() {
    const payload: any = {};
    if (priceMin) payload.price_min = priceMin;
    if (priceMax) payload.price_max = priceMax;
    if (beds) payload.beds = beds;
    if (propertyType) payload.property_type = propertyType;
    if (location) payload.location = location;
    if (lat) payload.lat = lat;
    if (lon) payload.lon = lon;
    if (radius) payload.radius_km = radius;
    if (sortBy) payload.sort_by = sortBy;
    if (order) payload.order = order;
    if (onChange) onChange(payload);
  }

  return (
    <aside className="card w-full lg:w-80">
      <h3 className="text-lg font-semibold mb-4">Filters</h3>

      <div className="space-y-4">
        <div>
          <label className="text-sm muted">Location</label>
          <input value={location} onChange={(e)=>setLocation(e.target.value)} placeholder="City or neighborhood" className="w-full mt-2 rounded-md p-2 bg-white/6" />
        </div>

        <div>
          <label className="text-sm muted">Center (lat, lon)</label>
          <div className="mt-2 flex gap-2">
            <input value={lat} onChange={(e)=>setLat(e.target.value)} placeholder="lat e.g. -4.0435" className="w-1/2 rounded-md p-2 bg-white/6" />
            <input value={lon} onChange={(e)=>setLon(e.target.value)} placeholder="lon e.g. 39.6636" className="w-1/2 rounded-md p-2 bg-white/6" />
          </div>
        </div>

        <div>
          <label className="text-sm muted">Radius (km)</label>
          <input value={radius} onChange={(e)=>setRadius(e.target.value)} placeholder="e.g. 2" className="w-full mt-2 rounded-md p-2 bg-white/6" />
        </div>

        <div>
          <label className="text-sm muted">Price range (USD)</label>
          <div className="mt-2 flex gap-2">
            <input value={priceMin} onChange={(e)=>setPriceMin(e.target.value)} placeholder="Min" className="w-1/2 rounded-md p-2 bg-white/6" />
            <input value={priceMax} onChange={(e)=>setPriceMax(e.target.value)} placeholder="Max" className="w-1/2 rounded-md p-2 bg-white/6" />
          </div>
        </div>

        <div>
          <label className="text-sm muted">Bedrooms</label>
          <select value={beds} onChange={(e)=>setBeds(e.target.value)} className="w-full mt-2 rounded-md p-2 bg-white/6">
            <option value="">Any</option>
            <option value="1">1+</option>
            <option value="2">2+</option>
            <option value="3">3+</option>
          </select>
        </div>

        <div>
          <label className="text-sm muted">Property type</label>
          <select value={propertyType} onChange={(e)=>setPropertyType(e.target.value)} className="w-full mt-2 rounded-md p-2 bg-white/6">
            <option value="">Any</option>
            <option value="Apartment">Apartment</option>
            <option value="House">House</option>
            <option value="Studio">Studio</option>
          </select>
        </div>

        <div>
          <label className="text-sm muted">Sort</label>
          <div className="mt-2 flex gap-2">
            <select value={sortBy} onChange={(e)=>setSortBy(e.target.value)} className="w-1/2 rounded-md p-2 bg-white/6">
              <option value="">Relevance</option>
              <option value="price">Price</option>
              <option value="beds">Bedrooms</option>
              <option value="distance_km">Distance</option>
            </select>
            <select value={order} onChange={(e)=>setOrder(e.target.value)} className="w-1/2 rounded-md p-2 bg-white/6">
              <option value="asc">Asc</option>
              <option value="desc">Desc</option>
            </select>
          </div>
        </div>

        <div className="pt-2">
          <button onClick={apply} className="btn-primary w-full">Apply filters</button>
        </div>
      </div>
    </aside>
  );
}
