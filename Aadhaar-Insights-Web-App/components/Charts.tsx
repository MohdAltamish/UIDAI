
import React from 'react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, LineChart, Line, Legend, AreaChart, Area,
  ScatterChart, Scatter, ZAxis
} from 'recharts';

const COLORS = ['#4f46e5', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#06b6d4'];

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-white p-3 border border-slate-100 shadow-xl rounded-xl">
        <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1">{label || payload[0].payload.state}</p>
        <p className="text-sm font-black text-slate-900">
          {(payload[0].value / 1000000).toFixed(2)}M Enrollments
        </p>
      </div>
    );
  }
  return null;
};

export const EnrollmentByState: React.FC<{ data: any[], title: string }> = ({ data, title }) => (
  <div className="bg-white p-6 rounded-3xl shadow-sm border border-slate-100 h-full min-h-[400px]">
    <h3 className="text-sm font-bold mb-6 text-slate-800 uppercase tracking-widest">{title}</h3>
    <ResponsiveContainer width="100%" height="90%">
      <BarChart data={data} layout="vertical" margin={{ left: 40, right: 20 }}>
        <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#f1f5f9" />
        <XAxis type="number" hide />
        <YAxis dataKey="state" type="category" width={100} tick={{ fontSize: 10, fontWeight: 600, fill: '#64748b' }} axisLine={false} />
        <Tooltip content={<CustomTooltip />} cursor={{fill: '#f8fafc'}} />
        <Bar dataKey="enrollments" fill="#4f46e5" radius={[0, 8, 8, 0]} barSize={20} />
      </BarChart>
    </ResponsiveContainer>
  </div>
);

export const IntensityScatter: React.FC<{ data: any[], xKey: string, yKey: string, title: string }> = ({ data, xKey, yKey, title }) => (
  <div className="bg-white p-6 rounded-3xl shadow-sm border border-slate-100 h-full min-h-[400px]">
    <h3 className="text-sm font-bold mb-6 text-slate-800 uppercase tracking-widest">{title}</h3>
    <ResponsiveContainer width="100%" height="90%">
      <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
        <XAxis type="number" dataKey={xKey} name="Population" unit="M" tick={{fontSize: 10}} axisLine={false} />
        <YAxis type="number" dataKey={yKey} name="Ratio" unit="%" tick={{fontSize: 10}} axisLine={false} />
        <ZAxis type="category" dataKey="state" name="State" />
        <Tooltip cursor={{ strokeDasharray: '3 3' }} />
        <Scatter name="States" data={data} fill="#4f46e5">
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} fillOpacity={0.6} strokeWidth={2} stroke={COLORS[index % COLORS.length]} />
          ))}
        </Scatter>
      </ScatterChart>
    </ResponsiveContainer>
  </div>
);

export const GrowthTrend: React.FC<{ data: any[] }> = ({ data }) => (
  <div className="bg-white p-6 rounded-3xl shadow-sm border border-slate-100 h-full min-h-[400px]">
    <h3 className="text-sm font-bold mb-6 text-slate-800 uppercase tracking-widest">National Adoption Timeline</h3>
    <ResponsiveContainer width="100%" height="90%">
      <AreaChart data={data}>
        <defs>
          <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#4f46e5" stopOpacity={0.1}/>
            <stop offset="95%" stopColor="#4f46e5" stopOpacity={0}/>
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
        <XAxis dataKey="year" axisLine={false} tickLine={false} tick={{fontSize: 10, fontWeight: 600}} />
        <YAxis tickFormatter={(val) => (val / 1000000000).toFixed(1) + 'B'} axisLine={false} tickLine={false} tick={{fontSize: 10}} />
        <Tooltip />
        <Area type="monotone" dataKey="count" stroke="#4f46e5" fill="url(#colorCount)" strokeWidth={3} dot={{r: 4, fill: '#4f46e5'}} activeDot={{r: 6}} />
      </AreaChart>
    </ResponsiveContainer>
  </div>
);
