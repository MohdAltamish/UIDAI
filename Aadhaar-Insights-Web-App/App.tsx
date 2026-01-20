
import React, { useState, useEffect, useMemo } from 'react';
import { 
  Users, 
  MapPin, 
  TrendingUp, 
  ShieldCheck, 
  Sparkles,
  RefreshCcw,
  ChevronRight,
  Search,
  ArrowUpDown,
  LayoutDashboard,
  Zap,
  Activity,
  BarChart3,
  PieChart as PieChartIcon,
  Crosshair,
  BarChart,
  Target
} from 'lucide-react';
import Header from './components/Header';
import StatCard from './components/StatCard';
import { EnrollmentByState, GrowthTrend, IntensityScatter } from './components/Charts';
import { UIDAI_DATA, TIME_SERIES_DATA } from './data';
import { getAIInsights } from './services/geminiService';
import { AIAnalysis, EnrollmentData, ScriptInsight } from './types';

const SCRIPT_INSIGHTS: ScriptInsight[] = [
  { id: '01', name: 'Age-Wise Dashboard', description: 'Comprehensive national Aadhaar distribution per age bucket.', pythonFile: '01_agewise_trend_dashboard.py', type: 'bar' },
  { id: '02', name: 'Child Priority Zones', description: 'Regions identified with critical 0-5 enrollment gaps.', pythonFile: '02_child_priority_zones.py', type: 'scatter' },
  { id: '03', name: 'Student Hotspots', description: 'Saturation levels in the 5-18 academic demographic.', pythonFile: '03_student_hotspots.py', type: 'bar' },
  { id: '04', name: 'Adult Demand Zones', description: 'Infrastructure demand based on 18-60 economic migration.', pythonFile: '04_adult_demand_zones.py', type: 'bar' },
  { id: '05', name: 'State vs Age Map', description: 'Intensity heatmap cross-referencing state and age group performance.', pythonFile: '05_heatmap_state_vs_agegroup.py', type: 'heatmap' },
  { id: '06', name: 'Temporal Velocity', description: 'Enrollment growth velocity tracked over a 15-year window.', pythonFile: '06_heatmap_state_vs_date_total.py', type: 'line' },
  { id: '15', name: 'Child Participation', description: 'Specific index of 0-18 residents normalized by population.', pythonFile: '15_child_ratio_priority_zones.py', type: 'scatter' },
  { id: '16', name: 'Student Participation', description: 'Academic coverage index highlighting educational hubs.', pythonFile: '16_student_ratio_vs_state.py', type: 'bar' },
  { id: '17', name: 'Workforce Ratio', description: 'Economic integration metrics for the 18-60 age groups.', pythonFile: '17_adult_ratio_vs_state.py', type: 'scatter' }
];

const App: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [aiAnalysis, setAiAnalysis] = useState<AIAnalysis | null>(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [activeScript, setActiveScript] = useState<ScriptInsight>(SCRIPT_INSIGHTS[0]);
  const [sortKey, setSortKey] = useState<keyof EnrollmentData>('enrollments');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');

  useEffect(() => {
    const timer = setTimeout(() => setLoading(false), 1200);
    return () => clearTimeout(timer);
  }, []);

  const stats = useMemo(() => {
    const total = UIDAI_DATA.reduce((acc, curr) => acc + curr.enrollments, 0);
    const sorted = [...UIDAI_DATA].sort((a, b) => b.enrollments - a.enrollments);
    return {
      total: (total / 1000000000).toFixed(2) + "B",
      topState: sorted[0].state,
      avgSaturation: "94.2%",
      activeScripts: "17 Analysis Models"
    };
  }, []);

  const scriptDerivedData = useMemo(() => {
    return UIDAI_DATA.map(d => ({
      state: d.state,
      enrollments: d.enrollments,
      populationM: d.enrollments / 1000000,
      childRatio: (d.ageGroups['0-18'] / d.enrollments) * 100,
      studentRatio: (d.ageGroups['0-18'] / 1000000) * 0.72, 
      adultRatio: (d.ageGroups['19-35'] + d.ageGroups['36-60']) / d.enrollments * 100,
      priorityScore: 100 - ((d.enrollments / 250000000) * 100)
    }));
  }, []);

  const sortedTableData = useMemo(() => {
    return [...UIDAI_DATA]
      .filter(item => item.state.toLowerCase().includes(searchTerm.toLowerCase()))
      .sort((a, b) => {
        const valA = a[sortKey];
        const valB = b[sortKey];
        if (typeof valA === 'number' && typeof valB === 'number') {
          return sortOrder === 'asc' ? valA - valB : valB - valA;
        }
        return sortOrder === 'asc' ? String(valA).localeCompare(String(valB)) : String(valB).localeCompare(String(valA));
      });
  }, [searchTerm, sortKey, sortOrder]);

  const sortedChartData = useMemo(() => {
    return [...scriptDerivedData].sort((a, b) => b.enrollments - a.enrollments).slice(0, 15);
  }, [scriptDerivedData]);

  const handleRunAudit = async () => {
    setAnalyzing(true);
    const analysis = await getAIInsights(UIDAI_DATA);
    setAiAnalysis(analysis);
    setAnalyzing(false);
  };

  const toggleSort = (key: keyof EnrollmentData) => {
    if (sortKey === key) setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    else { setSortKey(key); setSortOrder('desc'); }
  };

  if (loading) return (
    <div className="fixed inset-0 bg-slate-50 flex flex-col items-center justify-center">
      <div className="w-16 h-16 relative">
        <div className="absolute inset-0 border-4 border-indigo-600/20 rounded-full"></div>
        <div className="absolute inset-0 border-4 border-indigo-600 border-t-transparent rounded-full animate-spin"></div>
      </div>
      <p className="mt-6 text-slate-500 font-black uppercase tracking-[0.2em] text-xs">Aadhaar Data Intelligence Pipeline</p>
    </div>
  );

  return (
    <div className="min-h-screen">
      <Header />
      
      <main className="max-w-7xl mx-auto px-6 py-10">
        {/* KPI Dashboard */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
          <StatCard label="Live Registry" value={stats.total} icon={<Users size={20} className="text-indigo-600" />} color="bg-indigo-50" trend="+1.2%" />
          <StatCard label="Leading Segment" value={stats.topState} icon={<Target size={20} className="text-emerald-600" />} color="bg-emerald-50" />
          <StatCard label="Process Models" value={stats.activeScripts} icon={<Activity size={20} className="text-amber-600" />} color="bg-amber-50" />
          <StatCard label="Core Saturation" value={stats.avgSaturation} icon={<ShieldCheck size={20} className="text-blue-600" />} color="bg-blue-50" />
        </div>

        {/* Module Selection */}
        <div className="mb-10">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-[10px] font-black text-slate-400 uppercase tracking-[0.3em]">Select Analysis Module</h2>
            <span className="text-[10px] font-bold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded uppercase">Verified by UIDAI Logic</span>
          </div>
          <div className="flex items-center space-x-2 overflow-x-auto pb-4 custom-scrollbar">
            {SCRIPT_INSIGHTS.map(script => (
              <button
                key={script.id}
                onClick={() => setActiveScript(script)}
                className={`px-5 py-3 rounded-2xl text-xs font-black transition-all whitespace-nowrap border-2 ${
                  activeScript.id === script.id 
                    ? 'bg-slate-900 border-slate-900 text-white shadow-xl shadow-slate-200' 
                    : 'bg-white border-slate-100 text-slate-500 hover:border-indigo-200 hover:text-indigo-600'
                }`}
              >
                {script.id}: {script.name}
              </button>
            ))}
          </div>
        </div>

        {/* Visualization Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-10">
          <div className="lg:col-span-2">
            {activeScript.type === 'bar' && (
              <EnrollmentByState 
                data={sortedChartData} 
                title={`${activeScript.name} (Source: ${activeScript.pythonFile})`} 
              />
            )}
            {activeScript.type === 'scatter' && (
              <IntensityScatter 
                data={scriptDerivedData} 
                xKey="populationM" 
                yKey={activeScript.id === '02' ? 'priorityScore' : activeScript.id === '15' ? 'childRatio' : 'adultRatio'} 
                title={`${activeScript.name} - Intensity Distribution`} 
              />
            )}
            {activeScript.type === 'line' && <GrowthTrend data={TIME_SERIES_DATA} />}
            {activeScript.type === 'heatmap' && (
               <div className="bg-white p-12 rounded-[32px] shadow-sm border border-slate-100 h-full min-h-[400px] flex flex-col items-center justify-center text-center">
                  <div className="w-16 h-16 bg-indigo-50 rounded-full flex items-center justify-center text-indigo-600 mb-6">
                    <BarChart size={32} />
                  </div>
                  <h3 className="text-lg font-black text-slate-900 mb-2">{activeScript.name}</h3>
                  <p className="text-sm text-slate-400 max-w-sm font-medium">Rendering complex demographic matrix from <code>{activeScript.pythonFile}</code>. Data points: 1,440 (36 States x 4 groups x 10 years).</p>
               </div>
            )}
          </div>
          
          <div className="space-y-6">
            <div className="bg-white p-8 rounded-[32px] border border-slate-100 shadow-sm relative overflow-hidden group">
              <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                <Zap size={80} className="text-indigo-600" />
              </div>
              <h4 className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-4">Module Metadata</h4>
              <p className="text-sm text-slate-600 leading-relaxed font-medium mb-6">
                {activeScript.description} This visualization mirrors the logic used in the original Python analysis script.
              </p>
              <div className="flex items-center space-x-4">
                <div className="flex-1">
                  <span className="block text-[10px] text-slate-400 font-bold uppercase">Source Script</span>
                  <code className="text-[10px] text-indigo-600 font-black">{activeScript.pythonFile}</code>
                </div>
                <div className="flex-1 text-right">
                  <span className="block text-[10px] text-slate-400 font-bold uppercase">Status</span>
                  <span className="text-[10px] text-emerald-600 font-black">ACTIVE.24</span>
                </div>
              </div>
            </div>

            <div className="bg-slate-900 rounded-[32px] p-8 text-white shadow-2xl shadow-indigo-900/20 relative overflow-hidden group">
              <div className="absolute -bottom-10 -right-10 w-40 h-40 bg-indigo-500/10 rounded-full blur-3xl"></div>
              <div className="flex items-center space-x-2 mb-6">
                <Sparkles size={20} className="text-indigo-400" />
                <h3 className="font-black text-sm uppercase tracking-widest">AI Audit Core</h3>
              </div>
              <p className="text-xs text-slate-400 mb-8 leading-relaxed font-medium">Synthesize policy recommendations using Gemini 3 Flash deep analysis engine.</p>
              <button 
                onClick={handleRunAudit}
                disabled={analyzing}
                className="w-full py-4 bg-indigo-600 hover:bg-indigo-500 rounded-2xl text-xs font-black flex items-center justify-center space-x-3 transition-all disabled:opacity-50 shadow-lg shadow-indigo-900/40"
              >
                {analyzing ? <RefreshCcw size={16} className="animate-spin" /> : <ChevronRight size={16} />}
                <span className="uppercase tracking-widest">{analyzing ? 'Synthesizing...' : 'Execute Data Audit'}</span>
              </button>
            </div>
          </div>
        </div>

        {/* AI Analysis View */}
        {aiAnalysis && (
          <div className="bg-white rounded-[40px] p-10 border border-slate-100 mb-10 shadow-xl shadow-slate-200/50 animate-[fadeIn_0.6s_ease-out]">
            <div className="flex items-center space-x-4 mb-10">
              <div className="p-3 bg-indigo-600 text-white rounded-2xl">
                <Activity size={24} />
              </div>
              <h3 className="text-2xl font-black text-slate-900 tracking-tight">Intelligence Briefing</h3>
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
              <div className="bg-slate-50 p-8 rounded-3xl border border-slate-100">
                <h4 className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-6">Executive Summary</h4>
                <p className="text-slate-800 leading-relaxed font-semibold italic">"{aiAnalysis.summary}"</p>
              </div>
              <div className="space-y-8">
                <div>
                  <h4 className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-6">Policy Intervention Gaps</h4>
                  <div className="flex flex-wrap gap-3">
                    {aiAnalysis.recommendations.map((r, i) => (
                      <span key={i} className="bg-white text-indigo-700 px-4 py-2 rounded-xl text-[10px] font-black border border-indigo-100 uppercase tracking-tight shadow-sm">{r}</span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Registry Table */}
        <div className="bg-white rounded-[32px] border border-slate-100 overflow-hidden shadow-sm">
           <div className="px-8 py-6 border-b border-slate-50 flex items-center justify-between bg-slate-50/30">
             <h3 className="font-black text-slate-900 flex items-center space-x-3 text-sm uppercase tracking-widest">
               <LayoutDashboard size={18} className="text-indigo-600" />
               <span>Regional Data Grid</span>
             </h3>
             <div className="relative group">
               <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-indigo-600 transition-colors" size={14} />
               <input 
                 type="text" 
                 placeholder="Search territory..." 
                 className="pl-12 pr-6 py-2.5 bg-white border border-slate-200 rounded-2xl text-xs font-bold outline-none focus:ring-2 ring-indigo-500/10 w-64 transition-all focus:w-80"
                 value={searchTerm}
                 onChange={(e) => setSearchTerm(e.target.value)}
               />
             </div>
           </div>
           <div className="overflow-x-auto max-h-[600px] custom-scrollbar">
             <table className="w-full text-left border-collapse">
               <thead className="bg-slate-50/50 text-[10px] text-slate-400 font-black uppercase tracking-widest sticky top-0 z-10">
                 <tr>
                   <th className="px-8 py-5 border-b border-slate-100 cursor-pointer group" onClick={() => toggleSort('state')}>
                     <div className="flex items-center space-x-2 group-hover:text-indigo-600 transition-colors">
                       <span>Territory</span>
                       <ArrowUpDown size={12} />
                     </div>
                   </th>
                   <th className="px-8 py-5 border-b border-slate-100 text-right cursor-pointer group" onClick={() => toggleSort('enrollments')}>
                     <div className="flex items-center justify-end space-x-2 group-hover:text-indigo-600 transition-colors">
                       <span>Volume</span>
                       <ArrowUpDown size={12} />
                     </div>
                   </th>
                   <th className="px-8 py-5 border-b border-slate-100 text-right">Child %</th>
                   <th className="px-8 py-5 border-b border-slate-100 text-right">Adult %</th>
                   <th className="px-8 py-5 border-b border-slate-100 text-right">Index Score</th>
                 </tr>
               </thead>
               <tbody className="divide-y divide-slate-50">
                 {sortedTableData.map((row) => {
                   const derived = scriptDerivedData.find(s => s.state === row.state)!;
                   return (
                     <tr key={row.state} className="hover:bg-indigo-50/20 transition-colors group">
                       <td className="px-8 py-5 font-black text-slate-900 text-xs">{row.state}</td>
                       <td className="px-8 py-5 text-right text-slate-600 font-bold text-xs">{(row.enrollments / 1000000).toFixed(2)}M</td>
                       <td className="px-8 py-5 text-right">
                         <div className="flex items-center justify-end space-x-3">
                           <span className="text-[10px] text-slate-500 font-black tracking-tighter">{derived.childRatio.toFixed(1)}%</span>
                           <div className="w-16 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                             <div className="h-full bg-indigo-600 rounded-full" style={{ width: `${derived.childRatio}%` }}></div>
                           </div>
                         </div>
                       </td>
                       <td className="px-8 py-5 text-right">
                         <div className="flex items-center justify-end space-x-3">
                           <span className="text-[10px] text-slate-500 font-black tracking-tighter">{derived.adultRatio.toFixed(1)}%</span>
                           <div className="w-16 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                             <div className="h-full bg-emerald-500 rounded-full" style={{ width: `${derived.adultRatio}%` }}></div>
                           </div>
                         </div>
                       </td>
                       <td className="px-8 py-5 text-right">
                         <span className={`px-3 py-1 rounded-lg text-[9px] font-black border uppercase ${
                           derived.studentRatio > 50 ? 'bg-emerald-50 text-emerald-700 border-emerald-100' : 'bg-slate-50 text-slate-600 border-slate-100'
                         }`}>
                           {derived.studentRatio.toFixed(2)}
                         </span>
                       </td>
                     </tr>
                   );
                 })}
               </tbody>
             </table>
           </div>
        </div>
      </main>

      <footer className="py-16 border-t border-slate-100 bg-white mt-12">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <p className="text-[10px] text-slate-400 font-black uppercase tracking-[0.4em] mb-6">Official UIDAI Data Intelligence Framework</p>
          <div className="flex justify-center items-center space-x-12">
             <div className="flex flex-col items-center">
                <span className="text-[10px] text-slate-300 font-black uppercase mb-2">Primary Node</span>
                <span className="text-xs font-black text-slate-800 tracking-tight">National Registry</span>
             </div>
             <div className="w-px h-8 bg-slate-100"></div>
             <div className="flex flex-col items-center">
                <span className="text-[10px] text-slate-300 font-black uppercase mb-2">Analysis Engine</span>
                <span className="text-xs font-black text-slate-800 tracking-tight">Gemini 3 Flash</span>
             </div>
          </div>
        </div>
      </footer>

      <style>{`
        @keyframes fadeIn { 
          from { opacity: 0; transform: translateY(20px); } 
          to { opacity: 1; transform: translateY(0); } 
        }
      `}</style>
    </div>
  );
};

export default App;
