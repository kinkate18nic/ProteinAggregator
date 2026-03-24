"use client";

import { useState, useEffect, useMemo, useRef } from 'react';

interface ProteinProduct {
  id: string;
  brand: string;
  product_name: string;
  product_url: string;
  live_price_inr: number | null;
  last_updated: string;
  in_stock: boolean | null;
  protein_per_serving_g: number | null;
  serving_size_g: number | null;
  protein_claimed_percent: number | null;
  num_servings: number | null;
  total_weight_g: number | null;
  cost_per_gram_claimed: number | null;
  cost_per_gram_verified: number | null;
  is_lab_tested: boolean;
  protein_verified_percent: number | null;
  lab_details?: {
    source: string;
    report_url: string;
  };
}

export default function Home() {
  const [data, setData] = useState<ProteinProduct[]>([]);
  const [budgetLimit, setBudgetLimit] = useState<number>(10000);
  const [filterLabTested, setFilterLabTested] = useState(false);
  const [filterInStock, setFilterInStock] = useState(false);
  const [filterBrand, setFilterBrand] = useState('All');
  const [loadedCount, setLoadedCount] = useState(12);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('master_catalog.json')
      .then((res) => res.json())
      .then((json) => {
        setData(json);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Could not load catalog", err);
        setLoading(false);
      });
  }, []);

  // Searchable Dropdown State
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [brandSearch, setBrandSearch] = useState('');
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close dropdown on click outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setDropdownOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const brands = useMemo(() => {
    const list = Array.from(new Set(data.map(p => p.brand)));
    return ['All', ...list.sort()];
  }, [data]);

  const processedData = useMemo(() => {
    return data
      .filter(product => {
        if (filterBrand !== 'All' && product.brand !== filterBrand) return false;
        if (product.live_price_inr !== null && product.live_price_inr > budgetLimit) return false;
        if (filterLabTested && !product.is_lab_tested) return false;
        if (filterInStock && product.in_stock === false) return false;
        return true;
      })
      .sort((a, b) => {
        const aCpg = a.cost_per_gram_claimed;
        const bCpg = b.cost_per_gram_claimed;
        if (aCpg === null && bCpg === null) return 0;
        if (aCpg === null) return 1;
        if (bCpg === null) return -1;
        return aCpg - bCpg;
      });
  }, [data, budgetLimit, filterLabTested, filterInStock, filterBrand]);

  const visibleData = processedData.slice(0, loadedCount);

  return (
    <main className="max-w-5xl mx-auto p-4 md:p-8 min-h-screen">
      {/* Hero Header */}
      <header className="mb-10 text-center md:text-left">
        <div>
          <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight pb-2 text-slate-100">ProteinDB <span className="text-3xl">🇮🇳</span></h1>
        </div>
        <p className="text-slate-400 mt-2 text-base font-medium max-w-xl">
          The ultimate live comparison engine for Indian protein supplements. Ranked honestly by <span className="text-indigo-300 font-bold bg-indigo-500/10 border border-indigo-500/20 px-2 py-0.5 rounded-md">Cost per Gram</span>.
        </p>
      </header>

      {/* Control Panel (Glassmorphism style) */}
      <section className="bg-slate-900/60 backdrop-blur-xl p-5 md:p-6 rounded-3xl shadow-lg border border-slate-800 mb-10 flex flex-col md:flex-row gap-6 md:gap-10 items-start md:items-center justify-between sticky top-4 z-10 transition-shadow hover:shadow-slate-900/50">
        
        {/* Budget Slider */}
        <div className="flex flex-col w-full md:flex-1">
          <label className="text-sm font-bold text-slate-300 mb-3 flex justify-between">
            <span>Max Price Filter</span>
            <span className="text-indigo-300 bg-indigo-500/10 border border-indigo-500/20 px-2.5 py-0.5 rounded-lg">₹{budgetLimit}</span>
          </label>
          <input 
            type="range" min="500" max="15000" step="500" 
            value={budgetLimit} 
            onChange={(e) => setBudgetLimit(Number(e.target.value))}
            className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-indigo-500 hover:accent-indigo-400 transition-colors"
          />
        </div>

        {/* Filters Group */}
        <div className="flex flex-col sm:flex-row gap-5 md:gap-8 w-full md:w-auto">
          {/* Searchable Brand Select */}
          <div className="flex flex-col w-full sm:w-56" ref={dropdownRef}>
            <label className="text-sm font-bold text-slate-300 mb-2">Brand</label>
            <div className="relative">
              <div 
                className="w-full bg-slate-800 border border-slate-700 hover:border-slate-600 text-slate-200 py-2 px-4 pr-8 rounded-xl font-medium cursor-pointer text-sm flex items-center justify-between transition-colors shadow-inner"
                onClick={() => setDropdownOpen(!dropdownOpen)}
              >
                <span className="truncate">{filterBrand}</span>
                <svg className={`fill-current h-4 w-4 text-slate-400 transition-transform ${dropdownOpen ? 'rotate-180' : ''}`} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
              </div>
              
              {dropdownOpen && (
                <div className="absolute z-50 mt-2 w-full bg-slate-800 border border-slate-700 rounded-xl shadow-2xl overflow-hidden flex flex-col max-h-64">
                  <div className="p-2 border-b border-slate-700 bg-slate-800/90 sticky top-0 backdrop-blur-md">
                    <input 
                      type="text" 
                      placeholder="Search brand..." 
                      className="w-full text-sm bg-slate-900 border-slate-700 text-slate-200 placeholder-slate-500 rounded-lg px-3 py-1.5 focus:outline-none focus:ring-1 focus:ring-indigo-500 border"
                      value={brandSearch}
                      onChange={(e) => setBrandSearch(e.target.value)}
                      onClick={(e) => e.stopPropagation()}
                      autoFocus
                    />
                  </div>
                  <ul className="overflow-y-auto">
                    {brands.filter(b => b.toLowerCase().includes(brandSearch.toLowerCase())).length === 0 ? (
                      <li className="px-4 py-3 text-sm text-slate-500 text-center">No brands found</li>
                    ) : (
                      brands.filter(b => b.toLowerCase().includes(brandSearch.toLowerCase())).map(b => (
                        <li 
                          key={b} 
                          className={`px-4 py-2.5 text-sm cursor-pointer transition-colors ${filterBrand === b ? 'bg-indigo-500/20 text-indigo-300 font-bold border-l-2 border-indigo-500' : 'text-slate-300 hover:bg-slate-700/50 border-l-2 border-transparent'}`}
                          onClick={() => {
                            setFilterBrand(b);
                            setDropdownOpen(false);
                            setBrandSearch('');
                          }}
                        >
                          {b}
                        </li>
                      ))
                    )}
                  </ul>
                </div>
              )}
            </div>
          </div>

          {/* Toggles */}
          <div className="flex flex-row sm:flex-col gap-4 sm:gap-3 py-1 justify-center">
            <label className="flex items-center space-x-2.5 cursor-pointer select-none group">
              <div className="relative flex items-center justify-center">
                <input type="checkbox" checked={filterLabTested} onChange={(e) => setFilterLabTested(e.target.checked)} className="peer sr-only" />
                <div className="w-5 h-5 bg-slate-800 border-2 border-slate-600 rounded peer-checked:bg-indigo-500 peer-checked:border-indigo-500 transition-colors shadow-inner"></div>
                <svg className="absolute w-3 h-3 text-white opacity-0 peer-checked:opacity-100 transition-opacity drop-shadow-sm" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="3"><path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7"/></svg>
              </div>
              <span className="text-sm font-semibold text-slate-400 group-hover:text-slate-200 transition-colors">Lab Verified Only</span>
            </label>
            <label className="flex items-center space-x-2.5 cursor-pointer select-none group">
              <div className="relative flex items-center justify-center">
                <input type="checkbox" checked={filterInStock} onChange={(e) => setFilterInStock(e.target.checked)} className="peer sr-only" />
                <div className="w-5 h-5 bg-slate-800 border-2 border-slate-600 rounded peer-checked:bg-emerald-500 peer-checked:border-emerald-500 transition-colors shadow-inner"></div>
                <svg className="absolute w-3 h-3 text-white opacity-0 peer-checked:opacity-100 transition-opacity drop-shadow-sm" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="3"><path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7"/></svg>
              </div>
              <span className="text-sm font-semibold text-slate-400 group-hover:text-slate-200 transition-colors">In Stock Only</span>
            </label>
          </div>
        </div>
      </section>

      {/* Results */}
      {loading ? (
        <div className="text-center py-12 text-slate-500 font-medium animate-pulse">Loading catalog...</div>
      ) : (
        <section className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {visibleData.map((product) => (
            <div key={product.id} className="bg-slate-900/40 backdrop-blur-sm border border-slate-800 rounded-3xl p-5 md:p-6 hover:shadow-[0_8px_30px_rgb(0,0,0,0.4)] hover:shadow-indigo-500/10 hover:border-slate-700/80 hover:-translate-y-1.5 transition-all duration-300 flex flex-col justify-between group">
              
              {/* Header */}
              <div className="flex justify-between items-start mb-5 relative pb-4 border-b border-slate-800/80">
                <div className="pr-3">
                  <p className="text-[10px] text-indigo-400 font-black uppercase tracking-widest mb-1.5">{product.brand}</p>
                  <h2 className="font-extrabold text-lg text-slate-100 leading-snug">
                    <a href={product.product_url} target="_blank" rel="noreferrer" className="group-hover:text-indigo-400 transition-colors drop-shadow-sm">
                      {product.product_name}
                    </a>
                  </h2>
                </div>
                {/* Cost per gram badge */}
                <div className={`${product.cost_per_gram_claimed ? 'bg-indigo-500/10 border-indigo-500/20 text-indigo-300' : 'bg-slate-800/50 border-slate-700/50 text-slate-500'} border-2 font-black px-3 py-2 rounded-2xl text-base whitespace-nowrap shadow-sm`}>
                  {product.cost_per_gram_claimed ? (
                    <>₹{product.cost_per_gram_claimed} <span className="text-[10px] font-bold text-indigo-400/80 uppercase">/g</span></>
                  ) : (
                    <span className="text-sm">N/A</span>
                  )}
                </div>
              </div>
              
              {/* Data Grid */}
              <div className="grid grid-cols-2 gap-3 text-sm">
                {/* Price */}
                <div className="bg-slate-800/50 p-3 rounded-2xl border border-slate-700/50">
                  <span className="text-slate-500 text-[11px] font-bold uppercase block mb-1">Price</span>
                  <span className={`font-black ${product.live_price_inr ? 'text-slate-200 text-base' : 'text-amber-500 text-sm'}`}>
                    {product.live_price_inr ? `₹${product.live_price_inr}` : "N/A"}
                  </span>
                </div>
                
                {/* Stock Status */}
                <div className="bg-slate-800/50 p-3 rounded-2xl border border-slate-700/50">
                  <span className="text-slate-500 text-[11px] font-bold uppercase block mb-1">Stock</span>
                  {product.in_stock === true && <span className="font-bold text-emerald-400 text-sm">In Stock</span>}
                  {product.in_stock === false && <span className="font-bold text-rose-500 text-sm">Out of Stock</span>}
                  {product.in_stock === null && <span className="font-bold text-slate-500 text-sm">Unknown</span>}
                </div>

                {/* Claimed Protein % */}
                <div className="bg-slate-800/50 p-3 rounded-2xl border border-slate-700/50">
                  <span className="text-slate-500 text-[11px] font-bold uppercase block mb-1">Protein (Claimed)</span>
                  <span className={`font-black ${product.protein_claimed_percent ? 'text-slate-200 text-base' : 'text-slate-500 text-sm'}`}>
                    {product.protein_claimed_percent ? `${product.protein_claimed_percent}%` : "N/A"}
                  </span>
                </div>

                {/* Protein per Serving */}
                <div className="bg-slate-800/50 p-3 rounded-2xl border border-slate-700/50">
                  <span className="text-slate-500 text-[11px] font-bold uppercase block mb-1">Per Serving</span>
                  <span className={`font-black ${product.protein_per_serving_g ? 'text-slate-200 text-base' : 'text-slate-500 text-sm'}`}>
                    {product.protein_per_serving_g ? `${product.protein_per_serving_g}g` : "N/A"}
                  </span>
                </div>

                {/* Lab Verified Row */}
                {product.is_lab_tested && (
                  <div className="bg-emerald-500/10 p-4 rounded-2xl col-span-2 border border-emerald-500/20 flex justify-between items-center shadow-inner">
                     <div>
                        <span className="text-emerald-400 text-[9px] font-black block uppercase tracking-widest mb-1 flex items-center gap-1">
                          <svg className="w-3 h-3 text-emerald-400" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"></path></svg>
                          Lab Verified
                        </span>
                        <a href={product.lab_details?.report_url || "#"} target="_blank" rel="noreferrer" className="font-extrabold text-emerald-200 hover:text-emerald-100 underline decoration-emerald-500/50 text-sm transition-colors">
                          {product.lab_details?.source} Report
                        </a>
                     </div>
                     <div className="text-right">
                        <span className="text-emerald-400/80 text-[10px] font-black block uppercase tracking-wider mb-0.5">Verified</span>
                        <span className="font-black text-emerald-300 text-xl drop-shadow-sm">{product.protein_verified_percent}%</span>
                     </div>
                     {product.cost_per_gram_verified && (
                       <div className="text-right ml-3 pl-3 border-l border-emerald-500/20">
                         <span className="text-emerald-400/80 text-[10px] font-black block uppercase tracking-wider mb-0.5">₹/g Verified</span>
                         <span className="font-black text-emerald-300 text-lg drop-shadow-sm">₹{product.cost_per_gram_verified}</span>
                       </div>
                     )}
                  </div>
                )}

                {/* Total Weight & Servings Info */}
                {(product.total_weight_g || product.num_servings) && (
                  <div className="bg-slate-800/30 p-3 rounded-2xl col-span-2 border border-slate-700/30 flex justify-between">
                    <div>
                      <span className="text-slate-500 text-[10px] font-bold uppercase block mb-0.5">Net Weight</span>
                      <span className="font-bold text-slate-300 text-sm">{product.total_weight_g ? `${product.total_weight_g}g` : "N/A"}</span>
                    </div>
                    <div className="text-center">
                      <span className="text-slate-500 text-[10px] font-bold uppercase block mb-0.5">Serving Size</span>
                      <span className="font-bold text-slate-300 text-sm">{product.serving_size_g ? `${product.serving_size_g}g` : "N/A"}</span>
                    </div>
                    <div className="text-right">
                      <span className="text-slate-500 text-[10px] font-bold uppercase block mb-0.5">Servings</span>
                      <span className="font-bold text-slate-300 text-sm">{product.num_servings ?? "N/A"}</span>
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
          
          {visibleData.length === 0 && (
            <div className="col-span-full text-center py-20 px-4 bg-slate-900/50 rounded-3xl border-2 border-dashed border-slate-800">
              <div className="w-16 h-16 bg-slate-800 rounded-full flex items-center justify-center mx-auto mb-4 border border-slate-700">
                <svg className="w-8 h-8 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
              </div>
              <p className="text-slate-200 font-extrabold text-xl mb-2">No products found</p>
              <p className="text-slate-500 text-sm">Try adjusting your filters, budget, or brand selection.</p>
            </div>
          )}
        </section>
      )}

      {/* Pagination Load More */}
      {!loading && loadedCount < processedData.length && (
        <div className="mt-12 text-center pb-8">
          <button 
            onClick={() => setLoadedCount(c => c + 15)}
            className="bg-slate-800/80 hover:bg-slate-700 border border-slate-700/80 text-slate-200 font-bold tracking-wide py-3 px-8 rounded-xl shadow-lg hover:shadow-indigo-500/10 transition-all duration-200 text-sm active:scale-95 backdrop-blur-sm"
          >
            Load More Products ({processedData.length - loadedCount} remaining)
          </button>
        </div>
      )}
    </main>
  );
}
