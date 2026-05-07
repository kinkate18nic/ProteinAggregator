"use client";

import { useState, useEffect, useMemo, useRef } from 'react';

type SortKey = 'cost_per_gram_claimed' | 'cost_per_gram_verified' | 'live_price_inr' | 'protein_claimed_percent' | 'brand';

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

const SORT_LABELS: Record<SortKey, string> = {
  cost_per_gram_claimed: 'Cost/g (Claimed)',
  cost_per_gram_verified: 'Cost/g (Verified)',
  live_price_inr: 'Price: Low to High',
  protein_claimed_percent: 'Protein %: High to Low',
  brand: 'Brand: A-Z',
};

export default function Home() {
  const [data, setData] = useState<ProteinProduct[]>([]);
  const [budgetLimit, setBudgetLimit] = useState<number>(10000);
  const [filterLabTested, setFilterLabTested] = useState(false);
  const [filterInStock, setFilterInStock] = useState(false);
  const [filterBrand, setFilterBrand] = useState('All');
  const [sortBy, setSortBy] = useState<SortKey>('cost_per_gram_claimed');
  const [loadedCount, setLoadedCount] = useState(12);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [expandedCards, setExpandedCards] = useState<Set<string>>(new Set());

  // Searchable Dropdown State
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [brandSearch, setBrandSearch] = useState('');
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Sort dropdown state
  const [sortDropdownOpen, setSortDropdownOpen] = useState(false);
  const sortDropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetch(`master_catalog.json?v=${Date.now()}`)
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((json) => {
        setData(json);
        setLoading(false);
        setError(null);
      })
      .catch((err) => {
        console.error("Could not load catalog", err);
        setError("Failed to load product catalog. Please try again.");
        setLoading(false);
      });
  }, []);

  // Close dropdowns on click outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setDropdownOpen(false);
      }
      if (sortDropdownRef.current && !sortDropdownRef.current.contains(event.target as Node)) {
        setSortDropdownOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const brands = useMemo(() => {
    const list = Array.from(new Set(data.map(p => p.brand)));
    return ['All', ...list.sort()];
  }, [data]);

  const hasActiveFilters = budgetLimit !== 15000 || filterLabTested || filterInStock || filterBrand !== 'All';

  const processedData = useMemo(() => {
    let filtered = data
      .filter(product => {
        if (filterBrand !== 'All' && product.brand !== filterBrand) return false;
        if (product.live_price_inr !== null && product.live_price_inr > budgetLimit) return false;
        if (filterLabTested && !product.is_lab_tested) return false;
        if (filterInStock && product.in_stock === false) return false;
        return true;
      });

    filtered.sort((a, b) => {
      const aVal = a[sortBy];
      const bVal = b[sortBy];
      if (aVal === null && bVal === null) return 0;
      if (aVal === null) return 1;
      if (bVal === null) return -1;
      // For protein %, sort descending (higher is better)
      // For brand, sort ascending alphabetically
      // For everything else, sort ascending (lower price/cost is better)
      if (sortBy === 'protein_claimed_percent') return (bVal as number) - (aVal as number);
      if (sortBy === 'brand') return (aVal as string).localeCompare(bVal as string);
      return (aVal as number) - (bVal as number);
    });

    return filtered;
  }, [data, budgetLimit, filterLabTested, filterInStock, filterBrand, sortBy]);

  const visibleData = processedData.slice(0, loadedCount);

  function clearAllFilters() {
    setBudgetLimit(15000);
    setFilterLabTested(false);
    setFilterInStock(false);
    setFilterBrand('All');
    setSortBy('cost_per_gram_claimed');
  }

  function toggleExpanded(id: string) {
    setExpandedCards(prev => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }

  return (
    <main className="max-w-5xl mx-auto p-4 md:p-8 min-h-screen">
      {/* Hero Header */}
      <header className="mb-12 text-center md:text-left">
        <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight text-slate-100">
          ProteinDB
        </h1>
        <p className="text-slate-400 mt-3 text-base font-medium max-w-xl leading-relaxed">
          The ultimate live comparison engine for Indian protein supplements. Ranked honestly by{" "}
          <span className="text-indigo-300 font-bold">cost per verified gram</span>.
        </p>
      </header>

      {/* Error State */}
      {error && (
        <div className="mb-8 p-6 bg-rose-500/10 border border-rose-500/20 rounded-2xl text-center">
          <p className="text-rose-300 font-semibold mb-3">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="bg-rose-500/20 hover:bg-rose-500/30 text-rose-200 font-semibold py-2 px-6 rounded-lg transition-colors"
          >
            Retry
          </button>
        </div>
      )}

      {/* Control Panel */}
      <section className="bg-slate-900/60 backdrop-blur-xl p-5 md:p-6 rounded-3xl shadow-lg border border-slate-800 mb-8 flex flex-col lg:flex-row gap-6 lg:gap-8 items-start lg:items-center justify-between sticky top-4 z-10">
        
        {/* Budget Slider */}
        <div className="flex flex-col w-full lg:flex-1 lg:max-w-xs">
          <label className="text-sm font-bold text-slate-300 mb-2 flex justify-between">
            <span>Max Budget</span>
            <span className="text-indigo-300 font-mono">₹{budgetLimit.toLocaleString()}</span>
          </label>
          <input 
            type="range" min="500" max="15000" step="500" 
            value={budgetLimit} 
            onChange={(e) => setBudgetLimit(Number(e.target.value))}
            className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-indigo-500"
          />
        </div>

        {/* Filters Group */}
        <div className="flex flex-col sm:flex-row gap-4 sm:gap-6 w-full lg:w-auto">
          {/* Brand Select */}
          <div className="flex flex-col w-full sm:w-48" ref={dropdownRef}>
            <label className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1.5">Brand</label>
            <div className="relative">
              <button
                className="w-full bg-slate-800 border border-slate-700 hover:border-slate-600 text-slate-200 py-2.5 px-4 pr-8 rounded-xl font-medium text-sm flex items-center justify-between transition-colors text-left"
                onClick={() => setDropdownOpen(!dropdownOpen)}
              >
                <span className="truncate">{filterBrand}</span>
                <svg className={`absolute right-3 h-4 w-4 text-slate-400 transition-transform ${dropdownOpen ? 'rotate-180' : ''}`} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path fill="currentColor" d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
              </button>
              
              {dropdownOpen && (
                <div className="absolute z-50 mt-2 w-full bg-slate-800 border border-slate-700 rounded-xl shadow-2xl overflow-hidden flex flex-col max-h-64">
                  <div className="p-2 border-b border-slate-700">
                    <input 
                      type="text" 
                      placeholder="Search brand..." 
                      className="w-full text-sm bg-slate-900 border-slate-700 text-slate-200 placeholder-slate-500 rounded-lg px-3 py-2 focus:outline-none focus:ring-1 focus:ring-indigo-500 border"
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
                          className={`px-4 py-2.5 text-sm cursor-pointer transition-colors ${filterBrand === b ? 'bg-indigo-500/20 text-indigo-300 font-bold' : 'text-slate-300 hover:bg-slate-700/50'}`}
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

          {/* Sort Select */}
          <div className="flex flex-col w-full sm:w-56" ref={sortDropdownRef}>
            <label className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1.5">Sort By</label>
            <div className="relative">
              <button
                className="w-full bg-slate-800 border border-slate-700 hover:border-slate-600 text-slate-200 py-2.5 px-4 pr-8 rounded-xl font-medium text-sm flex items-center justify-between transition-colors text-left"
                onClick={() => setSortDropdownOpen(!sortDropdownOpen)}
              >
                <span className="truncate">{SORT_LABELS[sortBy]}</span>
                <svg className={`absolute right-3 h-4 w-4 text-slate-400 transition-transform ${sortDropdownOpen ? 'rotate-180' : ''}`} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path fill="currentColor" d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
              </button>
              
              {sortDropdownOpen && (
                <div className="absolute z-50 mt-2 w-full bg-slate-800 border border-slate-700 rounded-xl shadow-2xl overflow-hidden flex flex-col">
                  {(Object.entries(SORT_LABELS) as [SortKey, string][]).map(([key, label]) => (
                    <button
                      key={key}
                      className={`px-4 py-2.5 text-sm text-left cursor-pointer transition-colors ${sortBy === key ? 'bg-indigo-500/20 text-indigo-300 font-bold' : 'text-slate-300 hover:bg-slate-700/50'}`}
                      onClick={() => {
                        setSortBy(key);
                        setSortDropdownOpen(false);
                      }}
                    >
                      {label}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Toggles */}
          <div className="flex flex-row sm:flex-col gap-3 sm:gap-2 justify-center sm:justify-start">
            <label className="flex items-center space-x-2 cursor-pointer select-none group">
              <div className="relative flex items-center justify-center">
                <input type="checkbox" checked={filterLabTested} onChange={(e) => setFilterLabTested(e.target.checked)} className="peer sr-only" />
                <div className="w-4 h-4 bg-slate-800 border border-slate-600 rounded peer-checked:bg-indigo-500 peer-checked:border-indigo-500 transition-colors"></div>
                <svg className="absolute w-2.5 h-2.5 text-white opacity-0 peer-checked:opacity-100" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="3"><path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7"/></svg>
              </div>
              <span className="text-xs font-semibold text-slate-400 group-hover:text-slate-200">Lab Verified</span>
            </label>
            <label className="flex items-center space-x-2 cursor-pointer select-none group">
              <div className="relative flex items-center justify-center">
                <input type="checkbox" checked={filterInStock} onChange={(e) => setFilterInStock(e.target.checked)} className="peer sr-only" />
                <div className="w-4 h-4 bg-slate-800 border border-slate-600 rounded peer-checked:bg-emerald-500 peer-checked:border-emerald-500 transition-colors"></div>
                <svg className="absolute w-2.5 h-2.5 text-white opacity-0 peer-checked:opacity-100" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="3"><path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7"/></svg>
              </div>
              <span className="text-xs font-semibold text-slate-400 group-hover:text-slate-200">In Stock</span>
            </label>
          </div>
        </div>

        {/* Clear All */}
        {hasActiveFilters && (
          <button
            onClick={clearAllFilters}
            className="text-xs font-semibold text-slate-500 hover:text-slate-300 transition-colors underline decoration-slate-700 underline-offset-4"
          >
            Clear All
          </button>
        )}
      </section>

      {/* Results Count */}
      {!loading && !error && (
        <div className="mb-4 text-sm text-slate-500">
          Showing {visibleData.length} of {processedData.length} products
          {processedData.length < data.length && (
            <span> (filtered from {data.length})</span>
          )}
        </div>
      )}

      {/* Results */}
      {loading ? (
        <div className="text-center py-16">
          <div className="animate-pulse space-y-4">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="bg-slate-900/40 rounded-3xl p-6 h-48 border border-slate-800/50"></div>
            ))}
          </div>
        </div>
      ) : (
        <section className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {visibleData.map((product) => {
            const isExpanded = expandedCards.has(product.id);
            return (
              <article key={product.id} className="bg-slate-900/40 border border-slate-800 rounded-3xl p-5 md:p-6 hover:border-slate-700/60 transition-all duration-300 group flex flex-col">
                
                {/* HERO: Cost per gram */}
                <div className="mb-1">
                  {product.cost_per_gram_claimed ? (
                    <div className="flex items-baseline gap-1">
                      <span className="text-3xl md:text-4xl font-black text-indigo-300 tracking-tight">
                        ₹{product.cost_per_gram_claimed}
                      </span>
                      <span className="text-sm font-bold text-indigo-400/60">/g</span>
                    </div>
                  ) : (
                    <span className="text-3xl font-black text-slate-500">N/A</span>
                  )}
                </div>

                {/* Brand + Name */}
                <div className="mb-4">
                  <p className="text-[10px] font-black uppercase tracking-widest text-indigo-400/70 mb-1">
                    {product.brand}
                  </p>
                  <h2 className="font-bold text-base text-slate-200 leading-snug">
                    <a href={product.product_url} target="_blank" rel="noreferrer" className="hover:text-indigo-300 transition-colors">
                      {product.product_name}
                    </a>
                  </h2>
                </div>

                {/* Supporting Row: Price | Stock | Protein */}
                <div className="flex items-center gap-4 mb-4 text-sm">
                  <div className="flex items-center gap-1.5">
                    <span className="text-slate-500 text-xs">Price</span>
                    <span className={`font-bold ${product.live_price_inr ? 'text-slate-200' : 'text-amber-500'}`}>
                      {product.live_price_inr ? `₹${product.live_price_inr.toLocaleString()}` : "N/A"}
                    </span>
                  </div>
                  <span className="text-slate-700">|</span>
                  <div className="flex items-center gap-1.5">
                    {product.in_stock === true && <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>}
                    {product.in_stock === false && <span className="w-1.5 h-1.5 rounded-full bg-rose-400"></span>}
                    {product.in_stock === null && <span className="w-1.5 h-1.5 rounded-full bg-slate-500"></span>}
                    <span className={`font-medium text-xs ${
                      product.in_stock === true ? 'text-emerald-400' :
                      product.in_stock === false ? 'text-rose-400' :
                      'text-slate-500'
                    }`}>
                      {product.in_stock === true ? 'In Stock' :
                       product.in_stock === false ? 'Out of Stock' :
                       'Unknown'}
                    </span>
                  </div>
                  <span className="text-slate-700">|</span>
                  <div className="flex items-center gap-1.5">
                    <span className="text-slate-500 text-xs">Protein</span>
                    <span className={`font-bold ${product.protein_claimed_percent ? 'text-slate-200' : 'text-slate-500'}`}>
                      {product.protein_claimed_percent ? `${product.protein_claimed_percent}%` : "N/A"}
                    </span>
                  </div>
                </div>

                {/* Lab Verified Section */}
                {product.is_lab_tested && (
                  <div className="bg-emerald-500/5 p-4 rounded-2xl border border-emerald-500/15 mb-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="flex items-center gap-1.5 mb-1">
                          <svg className="w-3.5 h-3.5 text-emerald-400" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/></svg>
                          <span className="text-[10px] font-black uppercase tracking-widest text-emerald-400">Lab Verified</span>
                        </div>
                        <a href={product.lab_details?.report_url || "#"} target="_blank" rel="noreferrer" className="text-xs font-semibold text-emerald-300/80 hover:text-emerald-200 underline decoration-emerald-500/30 transition-colors">
                          {product.lab_details?.source} Report →
                        </a>
                      </div>
                      <div className="text-right">
                        <div className="text-[10px] font-bold uppercase tracking-wider text-emerald-400/60">Verified</div>
                        <div className="text-2xl font-black text-emerald-300">{product.protein_verified_percent}%</div>
                        {product.cost_per_gram_verified && (
                          <div className="text-xs font-bold text-emerald-400/80">₹{product.cost_per_gram_verified}/g</div>
                        )}
                      </div>
                    </div>
                  </div>
                )}

                {/* Expandable Details */}
                <div className="mt-auto pt-3 border-t border-slate-800/60">
                  <button
                    onClick={() => toggleExpanded(product.id)}
                    className="text-xs font-semibold text-slate-500 hover:text-slate-300 transition-colors flex items-center gap-1"
                  >
                    <span>{isExpanded ? 'Hide' : 'Show'} Details</span>
                    <svg className={`w-3 h-3 transition-transform ${isExpanded ? 'rotate-180' : ''}`} fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"/></svg>
                  </button>
                  
                  {isExpanded && (
                    <div className="mt-3 grid grid-cols-3 gap-3 text-xs">
                      <div>
                        <span className="text-slate-500 block mb-0.5">Net Weight</span>
                        <span className="font-bold text-slate-300">{product.total_weight_g ? `${product.total_weight_g}g` : "N/A"}</span>
                      </div>
                      <div>
                        <span className="text-slate-500 block mb-0.5">Serving Size</span>
                        <span className="font-bold text-slate-300">{product.serving_size_g ? `${product.serving_size_g}g` : "N/A"}</span>
                      </div>
                      <div>
                        <span className="text-slate-500 block mb-0.5">Servings</span>
                        <span className="font-bold text-slate-300">{product.num_servings ?? "N/A"}</span>
                      </div>
                      <div>
                        <span className="text-slate-500 block mb-0.5">Protein/Serving</span>
                        <span className="font-bold text-slate-300">{product.protein_per_serving_g ? `${product.protein_per_serving_g}g` : "N/A"}</span>
                      </div>
                    </div>
                  )}
                </div>
              </article>
            );
          })}
          
          {visibleData.length === 0 && (
            <div className="col-span-full text-center py-20 px-4">
              <div className="w-16 h-16 bg-slate-800 rounded-full flex items-center justify-center mx-auto mb-4 border border-slate-700">
                <svg className="w-8 h-8 text-slate-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
              </div>
              <p className="text-slate-200 font-bold text-xl mb-2">No products found</p>
              <p className="text-slate-500 text-sm mb-4">Try adjusting your filters or budget.</p>
              <button
                onClick={clearAllFilters}
                className="bg-indigo-500/20 hover:bg-indigo-500/30 text-indigo-300 font-semibold py-2 px-6 rounded-lg transition-colors"
              >
                Clear All Filters
              </button>
            </div>
          )}
        </section>
      )}

      {/* Load More */}
      {!loading && !error && loadedCount < processedData.length && (
        <div className="mt-10 text-center pb-8">
          <button 
            onClick={() => setLoadedCount(c => c + 15)}
            className="bg-slate-800 hover:bg-slate-700 border border-slate-700 text-slate-200 font-semibold py-3 px-8 rounded-xl transition-colors text-sm"
          >
            Load More ({processedData.length - loadedCount})
          </button>
        </div>
      )}
    </main>
  );
}
