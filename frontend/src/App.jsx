import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import {
  Satellite, LayoutDashboard, Globe, Scan, MessageSquare,
  Settings, Droplets, Thermometer, Wind, Zap,
  ChevronRight, Search, Trash2, Send, Download
} from 'lucide-react';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, AreaChart, Area
} from 'recharts';
import { motion, AnimatePresence } from 'framer-motion';

const API_BASE = 'http://localhost:8002/api';

const App = () => {
  const [telemetry, setTelemetry] = useState({
    temperature: 25, humidity: 60, ph: 6.5, nitrogen: 2.0, phosphorus: 1.8, potassium: 2.2
  });
  const [market, setMarket] = useState({});
  const [chat, setChat] = useState([{ role: 'SYS', content: 'ESTABLISHING SECULAR UPLINK V21.0...' }]);
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const [geo, setGeo] = useState({ country: 'India', state: 'Tamil Nadu', place: 'Coimbatore', soil_type: 'Alluvial', season: 'August' });
  const [intel, setIntel] = useState('');

  const chatEndRef = useRef(null);

  useEffect(() => {
    const poll = setInterval(async () => {
      try {
        const res = await axios.get(`${API_BASE}/live-data`);
        setTelemetry(res.data.telemetry);
        setMarket(res.data.market);
      } catch (err) { console.error("Poll Link Error"); }
    }, 3000);
    return () => clearInterval(poll);
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chat]);

  const handleAutocomplete = async (val) => {
    setGeo({ ...geo, place: val });
    if (val.length < 3) { setSuggestions([]); return; }
    try {
      const res = await axios.get(`https://nominatim.openstreetmap.org/search?q=${val}&format=json&addressdetails=1&limit=5`, {
        headers: { 'User-Agent': 'AgriCommand/1.0' }
      });
      setSuggestions(res.data);
    } catch (err) { console.error("OSM Error"); }
  };

  const selectPlace = (s) => {
    const addr = s.address || {};
    const place = addr.city || addr.town || addr.village || addr.suburb || s.display_name.split(',')[0];
    setGeo({ ...geo, place, state: addr.state || '', country: addr.country || '' });
    setSuggestions([]);
  };

  const analyzeGI = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/geographic-intelligence`, { ...geo, ...telemetry });
      setIntel(res.data.intelligence);
      setChat(prev => [...prev, { role: 'SYS', content: `GEOGRAPHIC INTEL SYNCED FOR ${geo.place.toUpperCase()}` }]);
    } catch (err) { console.error("GI Error"); }
    setLoading(false);
  };

  const sendChat = async () => {
    if (!query.trim()) return;
    const userMsg = { role: 'user', content: query };
    setChat(prev => [...prev, userMsg]);
    setQuery('');
    setLoading(true);
    try {
      const res = await axios.post(`${API_BASE}/chat`, {
        message: query,
        context_data: { ...telemetry, ...geo },
        language: 'English',
        history: chat.slice(-10)
      });
      setChat(prev => [...prev, { role: 'assistant', content: res.data.answer }]);
    } catch (err) { setChat(prev => [...prev, { role: 'SYS', content: 'Neural Uplink Failure.' }]); }
    setLoading(false);
  };

  return (
    <div className="flex bg-[#05070a] text-[#e6edf3] min-h-screen">
      {/* SIDEBAR */}
      <aside className="w-80 h-screen bg-[#0c1117] border-r border-[#30363d] p-5 flex flex-col gap-6 fixed overflow-y-auto">
        <div className="flex items-center gap-3 text-[#00d4ff]">
          <Satellite size={24} />
          <h1 className="text-xl font-bold tracking-tight">AGRI-COMMAND V21.0</h1>
        </div>

        <section className="flex flex-col gap-4">
          <div className="text-xs font-bold text-[#8b949e] uppercase tracking-wider">Geographic Intelligence</div>
          <div className="relative">
            <input
              className="w-full bg-[#0d1117] border border-[#30363d] p-2 rounded text-sm"
              placeholder="Country" value={geo.country} onChange={(e) => setGeo({ ...geo, country: e.target.value })}
            />
          </div>
          <div className="relative">
            <input
              className="w-full bg-[#0d1117] border border-[#30363d] p-2 rounded text-sm"
              placeholder="State" value={geo.state} onChange={(e) => setGeo({ ...geo, state: e.target.value })}
            />
          </div>
          <div className="relative">
            <input
              className="w-full bg-[#0d1117] border border-[#30363d] p-2 rounded text-sm"
              placeholder="Place" value={geo.place} onChange={(e) => handleAutocomplete(e.target.value)}
            />
            <AnimatePresence>
              {suggestions.length > 0 && (
                <motion.ul
                  initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0 }}
                  className="absolute left-0 right-0 bg-[#161b22] border border-[#30363d] mt-1 rounded shadow-xl z-50 max-h-40 overflow-y-auto"
                >
                  {suggestions.map((s, i) => (
                    <li key={i} onClick={() => selectPlace(s)} className="p-2 text-xs hover:bg-[#30363d] cursor-pointer">
                      {s.display_name}
                    </li>
                  ))}
                </motion.ul>
              )}
            </AnimatePresence>
          </div>
          <button onClick={analyzeGI} className="w-full bg-[#00d4ff] text-black font-bold py-2 rounded text-sm hover:opacity-90">
            ANALYZE LOCATION
          </button>
        </section>

        <section className="flex flex-col gap-4">
          <div className="text-xs font-bold text-[#8b949e] uppercase tracking-wider">Bio-Scan Uplink</div>
          <div className="h-32 bg-[#0d1117] border border-[#30363d] rounded flex items-center justify-center text-xs text-[#8b949e]">
            [ NO IMAGE LOADED ]
          </div>
          <button className="w-full bg-[#21262d] border border-[#30363d] text-white py-2 rounded text-sm">SCAN LEAF DATA</button>
        </section>
      </aside>

      {/* MAIN CONTENT */}
      <main className="ml-80 flex-1 p-6 flex flex-col gap-6">
        <header className="flex justify-between items-center bg-[#0c1117] p-4 border border-[#30363d] rounded-xl glass-panel">
          <div className="flex items-center gap-4">
            <div className="pulsing-dot"></div>
            <div className="text-sm font-bold">SYSTEM STATUS: OPTIMAL</div>
          </div>
          <div className="flex items-center gap-4">
            <select className="bg-transparent text-xs outline-none">
              <option>English</option>
              <option>Tamil</option>
            </select>
            <LayoutDashboard className="text-[#00d4ff]" size={20} />
          </div>
        </header>

        {/* TELEMETRY CARDS */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {[
            { label: 'Soil Temperature', val: `${telemetry.temperature}°C`, icon: <Thermometer className="text-[#f85149]" /> },
            { label: 'Hydration Level', val: `${telemetry.humidity}%`, icon: <Droplets className="text-[#00d4ff]" /> },
            { label: 'Soil Ph Factor', val: telemetry.ph, icon: <Zap className="text-[#d29922]" /> }
          ].map((s, i) => (
            <motion.div whileHover={{ scale: 1.02 }} key={i} className="p-4 bg-[#0c1117] border border-[#30363d] rounded-xl flex justify-between items-center glass-panel">
              <div>
                <div className="text-[10px] uppercase text-[#8b949e] font-bold">{s.label}</div>
                <div className="text-2xl font-bold">{s.val}</div>
              </div>
              {s.icon}
            </motion.div>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* ANALYTICS */}
          <section className="p-6 bg-[#0c1117] border border-[#30363d] rounded-xl glass-panel flex flex-col gap-4">
            <h2 className="text-lg font-bold flex items-center gap-2">
              <Zap size={20} className="text-[#d29922]" /> CROP STABILITY MATRIX
            </h2>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={[{ n: telemetry.nitrogen, p: telemetry.phosphorus, k: telemetry.potassium }]}>
                  <defs>
                    <linearGradient id="colorN" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#3fb950" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#3fb950" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <Tooltip contentStyle={{ backgroundColor: '#0d1117', border: '1px solid #30363d' }} />
                  <Area type="monotone" dataKey="n" stroke="#3fb950" fillOpacity={1} fill="url(#colorN)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </section>

          {/* CHAT / STRATEGIST */}
          <section className="p-6 bg-[#0c1117] border border-[#30363d] rounded-xl glass-panel flex flex-col gap-4 h-[500px]">
            <h2 className="text-lg font-bold flex items-center gap-2 text-[#00d4ff]">
              <MessageSquare size={20} /> TACTICAL STRATEGIST V21.0
            </h2>
            <div className="flex-1 overflow-y-auto pr-2 space-y-4">
              {chat.map((m, i) => (
                <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`p-3 rounded-xl max-w-[85%] text-xs ${m.role === 'user' ? 'bg-[#00d4ff] text-black font-semibold' : 'bg-[#161b22] text-[#e6edf3] border border-[#30363d]'
                    }`}>
                    {m.content}
                  </div>
                </div>
              ))}
              <div ref={chatEndRef} />
            </div>
            <div className="flex gap-2">
              <input
                className="flex-1 bg-[#0d1117] border border-[#30363d] p-3 rounded-lg text-sm"
                placeholder="Message Strategist..."
                value={query} onChange={(e) => setQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && sendChat()}
              />
              <button
                onClick={sendChat}
                className="bg-[#00d4ff] text-black p-3 rounded-lg hover:opacity-90 transition-opacity"
              >
                <Send size={18} />
              </button>
            </div>
          </section>
        </div>

        {/* INTEL DISPLAY */}
        <AnimatePresence>
          {intel && (
            <motion.div
              initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
              className="p-6 bg-[#0c1117] border border-[#30363d] rounded-xl glass-panel"
            >
              <h2 className="text-lg font-bold mb-4 flex items-center gap-2">
                <Globe size={20} className="text-[#00d4ff]" /> REGIONAL INTELLIGENCE REPORT
              </h2>
              <div className="text-sm leading-relaxed text-[#8b949e]">
                {intel.split('\n').map((line, i) => <p key={i} className="mb-2">{line}</p>)}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </main>
    </div>
  );
};

export default App;
