"use client";

import { useState, useEffect, useMemo } from 'react';

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

  const processedData = useMemo(() => {
    return data
      .filter(product => {
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
  }, [data, budgetLimit, filterLabTested, filterInStock]);

  return (
    <main className="max-w-4xl mx-auto p-4 md:p-8">
      <header className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight text-gray-900">ProteinDB 🇮🇳</h1>
        <p className="text-gray-500 mt-2 text-sm font-medium">Live Cost-per-Gram Comparison Dashboard</p>
      </header>

      {/* Control Panel */}
      <section className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100 mb-8 flex flex-col md:flex-row gap-6 items-start md:items-center justify-between">
        <div className="flex flex-col w-full md:w-1/2">
          <label className="text-sm font-bold text-gray-700 mb-3 block">
            Max Price: <span className="text-blue-600">₹{budgetLimit}</span>
          </label>
          <input 
            type="range" min="500" max="15000" step="500" 
            value={budgetLimit} 
            onChange={(e) => setBudgetLimit(Number(e.target.value))}
            className="w-full accent-blue-600 cursor-pointer"
          />
        </div>
        <div className="flex flex-col gap-3">
          <label className="flex items-center space-x-2 cursor-pointer select-none text-sm font-bold text-gray-600">
            <input type="checkbox" checked={filterLabTested} onChange={(e) => setFilterLabTested(e.target.checked)} className="w-4 h-4 rounded text-blue-600" />
            <span>Lab-Tested Only</span>
          </label>
          <label className="flex items-center space-x-2 cursor-pointer select-none text-sm font-bold text-gray-600">
            <input type="checkbox" checked={filterInStock} onChange={(e) => setFilterInStock(e.target.checked)} className="w-4 h-4 rounded text-blue-600" />
            <span>In Stock Only</span>
          </label>
        </div>
      </section>

      {/* Results */}
      {loading ? (
        <div className="text-center py-12 text-gray-500 font-medium">Loading catalog...</div>
      ) : (
        <section className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {processedData.map((product) => (
            <div key={product.id} className="bg-white border border-gray-200 rounded-3xl p-6 shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all duration-200 flex flex-col justify-between">
              
              {/* Header */}
              <div className="flex justify-between items-start mb-5">
                <div className="pr-4">
                  <p className="text-[10px] text-gray-400 font-black uppercase tracking-widest mb-1.5">{product.brand}</p>
                  <h2 className="font-extrabold text-lg text-gray-900 leading-snug">
                    <a href={product.product_url} target="_blank" rel="noreferrer" className="hover:text-blue-600 transition-colors">
                      {product.product_name}
                    </a>
                  </h2>
                </div>
                {/* Cost per gram badge */}
                <div className={`${product.cost_per_gram_claimed ? 'bg-blue-50 border-blue-100 text-blue-800' : 'bg-gray-100 border-gray-200 text-gray-400'} border font-black px-3 py-2 rounded-xl text-base whitespace-nowrap shadow-sm`}>
                  {product.cost_per_gram_claimed ? (
                    <>₹{product.cost_per_gram_claimed} <span className="text-[11px] font-bold uppercase">/g</span></>
                  ) : (
                    <span className="text-sm">N/A</span>
                  )}
                </div>
              </div>
              
              {/* Data Grid */}
              <div className="grid grid-cols-2 gap-3 text-sm">
                {/* Price */}
                <div className="bg-gray-50 p-3 rounded-2xl border border-gray-100">
                  <span className="text-gray-400 text-[11px] font-bold uppercase block mb-1">Price</span>
                  <span className={`font-black ${product.live_price_inr ? 'text-gray-900 text-base' : 'text-amber-600 text-sm'}`}>
                    {product.live_price_inr ? `₹${product.live_price_inr}` : "N/A"}
                  </span>
                </div>
                
                {/* Stock Status */}
                <div className="bg-gray-50 p-3 rounded-2xl border border-gray-100">
                  <span className="text-gray-400 text-[11px] font-bold uppercase block mb-1">Stock</span>
                  {product.in_stock === true && <span className="font-bold text-green-600 text-sm">In Stock</span>}
                  {product.in_stock === false && <span className="font-bold text-red-500 text-sm">Out of Stock</span>}
                  {product.in_stock === null && <span className="font-bold text-gray-400 text-sm">Unknown</span>}
                </div>

                {/* Claimed Protein % */}
                <div className="bg-gray-50 p-3 rounded-2xl border border-gray-100">
                  <span className="text-gray-400 text-[11px] font-bold uppercase block mb-1">Protein (Claimed)</span>
                  <span className={`font-black ${product.protein_claimed_percent ? 'text-gray-900 text-base' : 'text-gray-400 text-sm'}`}>
                    {product.protein_claimed_percent ? `${product.protein_claimed_percent}%` : "N/A"}
                  </span>
                </div>

                {/* Protein per Serving */}
                <div className="bg-gray-50 p-3 rounded-2xl border border-gray-100">
                  <span className="text-gray-400 text-[11px] font-bold uppercase block mb-1">Per Serving</span>
                  <span className={`font-black ${product.protein_per_serving_g ? 'text-gray-900 text-base' : 'text-gray-400 text-sm'}`}>
                    {product.protein_per_serving_g ? `${product.protein_per_serving_g}g` : "N/A"}
                  </span>
                </div>

                {/* Lab Verified Row */}
                {product.is_lab_tested && (
                  <div className="bg-green-50 p-3.5 rounded-2xl col-span-2 border border-green-200 flex justify-between items-center">
                     <div>
                        <span className="text-green-700 text-[10px] font-black block uppercase tracking-wider mb-0.5">Lab Verified</span>
                        <a href={product.lab_details?.report_url || "#"} target="_blank" rel="noreferrer" className="font-extrabold text-green-800 hover:text-green-600 underline text-sm">
                          {product.lab_details?.source} Report
                        </a>
                     </div>
                     <div className="text-right">
                        <span className="text-green-700 text-[10px] font-black block uppercase tracking-wider mb-0.5">Verified</span>
                        <span className="font-black text-green-800 text-xl">{product.protein_verified_percent}%</span>
                     </div>
                     {product.cost_per_gram_verified && (
                       <div className="text-right ml-3 pl-3 border-l border-green-200">
                         <span className="text-green-700 text-[10px] font-black block uppercase tracking-wider mb-0.5">₹/g Verified</span>
                         <span className="font-black text-green-800 text-lg">₹{product.cost_per_gram_verified}</span>
                       </div>
                     )}
                  </div>
                )}

                {/* Total Weight & Servings Info */}
                {(product.total_weight_g || product.num_servings) && (
                  <div className="bg-gray-50 p-3 rounded-2xl col-span-2 border border-gray-100 flex justify-between">
                    <div>
                      <span className="text-gray-400 text-[10px] font-bold uppercase block mb-0.5">Net Weight</span>
                      <span className="font-bold text-gray-700 text-sm">{product.total_weight_g ? `${product.total_weight_g}g` : "N/A"}</span>
                    </div>
                    <div className="text-center">
                      <span className="text-gray-400 text-[10px] font-bold uppercase block mb-0.5">Serving Size</span>
                      <span className="font-bold text-gray-700 text-sm">{product.serving_size_g ? `${product.serving_size_g}g` : "N/A"}</span>
                    </div>
                    <div className="text-right">
                      <span className="text-gray-400 text-[10px] font-bold uppercase block mb-0.5">Servings</span>
                      <span className="font-bold text-gray-700 text-sm">{product.num_servings ?? "N/A"}</span>
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
          
          {processedData.length === 0 && (
            <div className="col-span-1 md:col-span-2 text-center py-16 px-4 bg-gray-50 rounded-3xl border border-dashed border-gray-200">
              <p className="text-gray-500 font-bold text-lg mb-2">No products found</p>
              <p className="text-gray-400 text-sm">Try adjusting your filters or budget.</p>
            </div>
          )}
        </section>
      )}
    </main>
  );
}
