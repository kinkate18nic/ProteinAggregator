"use client";

import { useState, useEffect, useMemo } from 'react';

interface LabDetails {
  is_tested: boolean;
  source: string | null;
  report_url: string | null;
  protein_claimed_percent: number;
  protein_verified_percent: number | null;
  amino_spiking_detected: boolean | null;
  heavy_metals_pass: boolean | null;
}

interface ProteinProduct {
  id: string;
  brand: string;
  product_name: string;
  product_url: string;
  live_price_inr: number;
  last_updated: string;
  is_tested: boolean;
  cost_per_gram: number;
  protein_verified_percent: number | null;
  quality_score_note: string;
  lab_details?: LabDetails;
}

export default function Home() {
  const [data, setData] = useState<ProteinProduct[]>([]);
  const [budgetLimit, setBudgetLimit] = useState<number>(5000);
  const [filterLabTested, setFilterLabTested] = useState(false);
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
        if (product.live_price_inr > budgetLimit) return false;
        if (filterLabTested && !product.is_tested) return false;
        return true;
      })
      .sort((a, b) => a.cost_per_gram - b.cost_per_gram);
  }, [data, budgetLimit, filterLabTested]);

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
            Max Unit Price: <span className="text-blue-600">₹{budgetLimit}</span>
          </label>
          <input 
            type="range" min="1000" max="6000" step="100" 
            value={budgetLimit} 
            onChange={(e) => setBudgetLimit(Number(e.target.value))}
            className="w-full accent-blue-600 cursor-pointer"
          />
        </div>
        
        <label className="flex items-center space-x-3 cursor-pointer group p-3 hover:bg-gray-50 rounded-xl border border-transparent hover:border-gray-200 transition-all select-none">
          <input 
            type="checkbox" 
            checked={filterLabTested} 
            onChange={(e) => setFilterLabTested(e.target.checked)} 
            className="w-5 h-5 rounded border-gray-300 text-blue-600 focus:ring-blue-500 cursor-pointer"
          />
          <span className="text-sm font-bold text-gray-600 group-hover:text-gray-900">
            Show Lab-Tested Only
          </span>
        </label>
      </section>

      {/* Results Grid */}
      {loading ? (
        <div className="text-center py-12 text-gray-500 font-medium">Loading catalog...</div>
      ) : (
        <section className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {processedData.map((product) => (
            <div key={product.id} className="bg-white border border-gray-200 rounded-3xl p-6 shadow-sm hover:shadow-lg hover:-translate-y-1 transition-all duration-200 flex flex-col justify-between">
              
              <div className="flex justify-between items-start mb-6">
                <div className="pr-4">
                  <p className="text-[10px] text-gray-400 font-black uppercase tracking-widest mb-1.5">{product.brand}</p>
                  <h2 className="font-extrabold text-lg text-gray-900 leading-snug">
                    <a href={product.product_url} target="_blank" rel="noreferrer" className="hover:text-blue-600 transition-colors">
                      {product.product_name}
                    </a>
                  </h2>
                </div>
                <div className="bg-blue-50 border border-blue-100 text-blue-800 font-black px-3 py-2 rounded-xl text-base whitespace-nowrap shadow-sm">
                  ₹{product.cost_per_gram} <span className="text-[11px] font-bold text-blue-600 uppercase">/g</span>
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-3 text-sm flex-grow items-end">
                <div className="bg-gray-50 p-3.5 rounded-2xl border border-gray-100 flex flex-col justify-center">
                  <span className="text-gray-400 text-[11px] font-bold uppercase tracking-wide block mb-1">Live Tub Price</span>
                  <span className="font-black text-gray-900 text-base">₹{product.live_price_inr}</span>
                </div>
                
                <div className="bg-gray-50 p-3.5 rounded-2xl border border-gray-100 flex flex-col justify-center">
                  <span className="text-gray-400 text-[11px] font-bold uppercase tracking-wide block mb-1">Status</span>
                  {product.is_tested ? (
                     <span className="font-bold text-green-600 flex items-center text-sm">
                        <svg className="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M5 13l4 4L19 7"></path></svg>
                        Lab Verified
                     </span>
                  ) : (
                     <span className="font-bold text-amber-500 text-sm">Unverified</span>
                  )}
                </div>

                {product.is_tested && product.lab_details && (
                  <div className="bg-green-50 p-4 rounded-2xl col-span-2 border border-green-200 flex justify-between items-center mt-1">
                     <div>
                        <span className="text-green-700 text-[10px] font-black block uppercase tracking-wider mb-0.5">Independent Test</span>
                        <a href={product.lab_details.report_url || "#"} target="_blank" rel="noreferrer" className="font-extrabold text-green-800 hover:text-green-600 underline decoration-green-300 underline-offset-4 tracking-tight text-sm">
                          {product.lab_details.source} Report
                        </a>
                     </div>
                     <div className="text-right">
                        <span className="text-green-700 text-[10px] font-black block uppercase tracking-wider mb-0.5">Verified Yield</span>
                        <span className="font-black text-green-800 text-xl">{product.lab_details.protein_verified_percent}%</span>
                     </div>
                  </div>
                )}
                
                {!product.is_tested && (
                  <div className="bg-amber-50/50 p-4 rounded-2xl col-span-2 border border-amber-100 mt-1">
                     <p className="text-amber-800/80 text-[11px] leading-relaxed font-semibold">
                        Metrics calculated based on the brand's label claim. Independent lab data is currently unavailable.
                     </p>
                  </div>
                )}
              </div>
            </div>
          ))}
          
          {processedData.length === 0 && (
            <div className="col-span-1 md:col-span-2 text-center py-16 px-4 bg-gray-50 rounded-3xl border border-dashed border-gray-200">
              <p className="text-gray-500 font-bold text-lg mb-2">No products found</p>
              <p className="text-gray-400 text-sm">Try adjusting your filters or budget to see more results.</p>
            </div>
          )}
        </section>
      )}
    </main>
  );
}
