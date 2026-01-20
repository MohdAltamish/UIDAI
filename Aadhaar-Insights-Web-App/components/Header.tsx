
import React from 'react';
import { Database, Bell, User, Search, Fingerprint } from 'lucide-react';

const Header: React.FC = () => {
  return (
    <header className="sticky top-0 z-50 bg-white/90 backdrop-blur-md border-b border-slate-200 px-6 py-3 flex items-center justify-between shadow-sm">
      <div className="flex items-center space-x-3">
        <div className="w-10 h-10 bg-indigo-600 rounded-xl flex items-center justify-center text-white shadow-lg shadow-indigo-200">
          <Fingerprint size={24} />
        </div>
        <div>
          <h1 className="text-xl font-extrabold text-slate-900 tracking-tight leading-none">Aadhaar Insights</h1>
          <p className="text-[10px] text-slate-500 font-bold uppercase tracking-widest mt-1">Official Analytics Hub</p>
        </div>
      </div>

      <div className="hidden lg:flex items-center bg-slate-100/80 px-4 py-2 rounded-xl border border-slate-200 w-full max-w-md transition-all focus-within:ring-2 focus-within:ring-indigo-500/20 focus-within:bg-white">
        <Search size={16} className="text-slate-400" />
        <input 
          type="text" 
          placeholder="Global database query..." 
          className="bg-transparent border-none outline-none text-xs ml-3 w-full text-slate-600 font-medium"
        />
      </div>

      <div className="flex items-center space-x-5">
        <button className="relative p-2 text-slate-500 hover:bg-slate-100 rounded-full transition-all group">
          <Bell size={18} />
          <span className="absolute top-2 right-2 w-2 h-2 bg-red-500 border-2 border-white rounded-full group-hover:scale-125 transition-transform"></span>
        </button>
        <div className="flex items-center space-x-3 border-l pl-5 border-slate-200">
          <div className="text-right hidden sm:block">
            <p className="text-xs font-bold text-slate-800 leading-none">Command Center</p>
            <p className="text-[10px] text-indigo-600 font-bold uppercase mt-1">Authorized Access</p>
          </div>
          <div className="w-9 h-9 bg-gradient-to-tr from-slate-200 to-slate-100 rounded-full border border-slate-200 flex items-center justify-center text-slate-500">
            <User size={18} />
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
