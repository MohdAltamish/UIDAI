
import React from 'react';

interface StatCardProps {
  label: string;
  value: string | number;
  icon: React.ReactNode;
  color: string;
  trend?: string;
}

const StatCard: React.FC<StatCardProps> = ({ label, value, icon, color, trend }) => {
  return (
    <div className="bg-white p-5 rounded-2xl shadow-sm border border-slate-100 flex flex-col justify-between hover:shadow-md transition-shadow group">
      <div className="flex items-center justify-between mb-4">
        <div className={`p-3 rounded-xl ${color} transition-transform group-hover:scale-110`}>
          {icon}
        </div>
        {trend && (
          <span className="text-[10px] font-bold px-2 py-1 bg-emerald-50 text-emerald-600 rounded-full border border-emerald-100">
            {trend}
          </span>
        )}
      </div>
      <div>
        <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">{label}</p>
        <h3 className="text-2xl font-black text-slate-900 mt-1">{value}</h3>
      </div>
    </div>
  );
};

export default StatCard;
