#!/usr/bin/env python3
import csv
import json

def load_data(path):
    with open(path) as f:
        rows = list(csv.DictReader(f))
    clean = []
    for r in rows:
        if r['status'] == 'RECORDING':
            clean.append({
                'ts': r['timestamp'].split(' ')[1][:8], # HH:MM:SS
                'rpm': float(r['rpm']) if r['rpm'] else None,
                'spd': float(r['speed_kmh']) if r['speed_kmh'] else None,
                'maf': float(r['maf_gps']) if r['maf_gps'] else None,
                'map': float(r['map_kpa']) if r['map_kpa'] else None,
                'load': float(r['engine_load_pct']) if r['engine_load_pct'] else None,
                'temp': float(r['coolant_c']) if r['coolant_c'] else None,
                'volt': float(r['voltage_v']) if r['voltage_v'] else None,
                'dtc': r['dtc_list'] or 'Ninguno'
            })
    return clean

s1 = load_data('/home/pgtoopx/.gemini/antigravity/scratch/ssangyong_musso_obd2_diagnostics/data/telemetry_2026-11-06_pre_limpieza_mariposa.csv')
s2 = load_data('/home/pgtoopx/.gemini/antigravity/scratch/ssangyong_musso_obd2_diagnostics/data/telemetry_2026-11-07_post_limpieza_mariposa.csv')

with open('/home/pgtoopx/.gemini/antigravity/scratch/ssangyong_musso_obd2_diagnostics/README.md') as f:
    readme_md = f.read()

html_content = f"""<!DOCTYPE html>
<html lang="es" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
    <title>SsangYong Musso 2.2 — Telemetría y Diagnóstico OBD2</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    colors: {{
                        brand: {{
                            50: '#eff6ff',
                            500: '#3b82f6',
                            600: '#2563eb',
                            700: '#1d4ed8'
                        }}
                    }}
                }}
            }}
        }}
    </script>
    <style>
        body {{ 
            background-color: #0b0f17; 
            color: #e2e8f0; 
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            -webkit-tap-highlight-color: transparent;
        }}
        .card {{ 
            background: #131b2e; 
            border: 1px solid #1e293b; 
            border-radius: 0.75rem; 
        }}
        
        /* Mobile scroll styling */
        .touch-scroll {{
            -webkit-overflow-scrolling: touch;
        }}
        
        /* Markdown mobile friendly rendering */
        .prose-dark h1 {{ font-size: 1.5rem; font-weight: 800; color: #ffffff; margin-top: 1.25rem; margin-bottom: 0.75rem; border-bottom: 1px solid #1e293b; padding-bottom: 0.5rem; }}
        .prose-dark h2 {{ font-size: 1.25rem; font-weight: 700; color: #60a5fa; margin-top: 1.5rem; margin-bottom: 0.75rem; border-bottom: 1px solid #1e293b; padding-bottom: 0.4rem; }}
        .prose-dark h3 {{ font-size: 1.1rem; font-weight: 600; color: #93c5fd; margin-top: 1rem; margin-bottom: 0.5rem; }}
        .prose-dark p {{ margin-bottom: 0.85rem; line-height: 1.65; color: #cbd5e1; font-size: 0.925rem; }}
        .prose-dark ul {{ list-style-type: disc; padding-left: 1.25rem; margin-bottom: 0.85rem; color: #cbd5e1; font-size: 0.925rem; }}
        .prose-dark ol {{ list-style-type: decimal; padding-left: 1.25rem; margin-bottom: 0.85rem; color: #cbd5e1; font-size: 0.925rem; }}
        .prose-dark li {{ margin-bottom: 0.35rem; }}
        .prose-dark hr {{ border-color: #1e293b; margin: 1.5rem 0; }}
        .prose-dark strong {{ color: #ffffff; }}
        
        /* Ensure tables in Markdown don't overflow the screen on mobile */
        .prose-dark table {{ 
            display: block; 
            width: 100%; 
            overflow-x: auto; 
            -webkit-overflow-scrolling: touch;
            border-collapse: collapse; 
            margin-top: 0.75rem; 
            margin-bottom: 1.25rem; 
            font-size: 0.8rem; 
            border-radius: 0.5rem;
        }}
        .prose-dark th {{ 
            background-color: #0f172a; 
            padding: 0.6rem 0.75rem; 
            text-align: left; 
            border: 1px solid #1e293b; 
            color: #94a3b8; 
            font-weight: 600; 
            text-transform: uppercase; 
            font-size: 0.7rem; 
            white-space: nowrap;
        }}
        .prose-dark td {{ 
            padding: 0.6rem 0.75rem; 
            border: 1px solid #1e293b; 
            color: #e2e8f0; 
            white-space: nowrap;
        }}
        .prose-dark tr:hover td {{ background-color: rgba(30, 41, 59, 0.4); }}
        .prose-dark a {{ color: #38bdf8; text-decoration: underline; }}
        .prose-dark code {{ background: #1e293b; color: #f472b6; padding: 0.15rem 0.35rem; border-radius: 0.25rem; font-size: 0.825em; }}
    </style>
</head>
<body class="p-3 sm:p-6 md:p-8 max-w-7xl mx-auto">

    <!-- Header (Mobile Optimized) -->
    <header class="mb-6 border-b border-slate-800 pb-5">
        <div class="flex flex-col gap-3">
            <!-- Badges wrap cleanly on any screen width -->
            <div class="flex flex-wrap items-center gap-1.5 sm:gap-2">
                <span class="px-2 py-0.5 text-[11px] font-bold uppercase tracking-wider bg-red-950/80 text-red-400 border border-red-800 rounded">DTC P0102</span>
                <span class="px-2 py-0.5 text-[11px] font-bold uppercase tracking-wider bg-blue-950/80 text-blue-400 border border-blue-800 rounded">SsangYong Musso 2.2</span>
                <span class="px-2 py-0.5 text-[11px] font-bold uppercase tracking-wider bg-emerald-950/80 text-emerald-400 border border-emerald-800 rounded">Turbo VGT Activo</span>
            </div>

            <div>
                <h1 class="text-xl sm:text-2xl md:text-3xl font-extrabold text-white leading-tight">Telemetría y Diagnóstico OBD2</h1>
                <p class="text-slate-400 text-xs sm:text-sm mt-1">Análisis de flujo de aire (MAF), turbo (MAP) y restricción por hollín.</p>
            </div>

            <!-- Action buttons: wrap and full-width on mobile -->
            <div class="flex flex-wrap items-center gap-2 pt-1">
                <a href="https://github.com/pgtoopx/ssangyong-musso-obd2-diagnostics" target="_blank" class="flex-1 sm:flex-none justify-center px-3 py-2 bg-slate-800 hover:bg-slate-700 text-xs font-semibold rounded-lg border border-slate-700 transition flex items-center gap-1.5 text-white min-h-[40px]">
                    <svg class="w-4 h-4 fill-current shrink-0" viewBox="0 0 24 24"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
                    <span>GitHub</span>
                </a>
                <a href="data/telemetry_2026-11-06_pre_limpieza_mariposa.csv" download class="flex-1 sm:flex-none justify-center px-3 py-2 bg-slate-800 hover:bg-slate-700 text-xs font-semibold rounded-lg border border-slate-700 transition flex items-center gap-1 text-slate-200 min-h-[40px]">
                    <span>📥 CSV 06-Nov</span>
                </a>
                <a href="data/telemetry_2026-11-07_post_limpieza_mariposa.csv" download class="flex-1 sm:flex-none justify-center px-3 py-2 bg-blue-600 hover:bg-blue-500 text-xs font-semibold rounded-lg text-white transition flex items-center gap-1 min-h-[40px]">
                    <span>📥 CSV 07-Nov</span>
                </a>
            </div>
        </div>
    </header>

    <!-- Navigation Tabs (Touch Friendly) -->
    <div class="grid grid-cols-2 border-b border-slate-800 mb-6 gap-1">
        <button id="tabDashboardBtn" onclick="switchTab('dashboard')" class="py-3 px-2 text-xs sm:text-sm font-bold text-center text-blue-400 border-b-2 border-blue-500 transition flex items-center justify-center gap-1.5 min-h-[44px]">
            <span>📊</span> <span>Dashboard</span>
        </button>
        <button id="tabReadmeBtn" onclick="switchTab('readme')" class="py-3 px-2 text-xs sm:text-sm font-bold text-center text-slate-400 hover:text-slate-200 border-b-2 border-transparent transition flex items-center justify-center gap-1.5 min-h-[44px]">
            <span>📖</span> <span>Informe (README)</span>
        </button>
    </div>

    <!-- TAB 1: DASHBOARD -->
    <div id="tabDashboard">
        <!-- KPI Cards (2 cols on mobile, 4 on desktop) -->
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-2.5 sm:gap-4 mb-6">
            <div class="card p-3.5 sm:p-5">
                <div class="text-[10px] sm:text-xs text-slate-400 uppercase font-bold tracking-wider">Falla 1 (06-Nov)</div>
                <div class="text-xl sm:text-2xl font-black text-red-400 mt-1">91 km/h</div>
                <div class="text-[11px] sm:text-xs text-slate-400 mt-1.5 leading-snug">MAF: <span class="text-white font-medium">60.3 g/s</span></div>
                <div class="text-[11px] sm:text-xs text-slate-400">Boost: <span class="text-white font-medium">145 kPa</span></div>
            </div>
            <div class="card p-3.5 sm:p-5">
                <div class="text-[10px] sm:text-xs text-slate-400 uppercase font-bold tracking-wider">Falla 2 (07-Nov)</div>
                <div class="text-xl sm:text-2xl font-black text-amber-400 mt-1">105 km/h</div>
                <div class="text-[11px] sm:text-xs text-slate-400 mt-1.5 leading-snug">MAF: <span class="text-white font-medium">48.2 g/s</span></div>
                <div class="text-[11px] sm:text-xs text-slate-400">Boost: <span class="text-white font-medium">122 kPa</span></div>
            </div>
            <div class="card p-3.5 sm:p-5">
                <div class="text-[10px] sm:text-xs text-slate-400 uppercase font-bold tracking-wider">Déficit de Flujo</div>
                <div class="text-xl sm:text-2xl font-black text-red-500 mt-1">-30%</div>
                <div class="text-[11px] sm:text-xs text-slate-400 mt-1.5 leading-snug">Teórico: <span class="text-white font-medium">~68 g/s</span></div>
                <div class="text-[11px] sm:text-xs text-red-400">Medido: 48.2 g/s</div>
            </div>
            <div class="card p-3.5 sm:p-5">
                <div class="text-[10px] sm:text-xs text-slate-400 uppercase font-bold tracking-wider">Diagnóstico Raíz</div>
                <div class="text-sm sm:text-lg font-black text-purple-400 mt-1 truncate">Múltiple con Hollín</div>
                <div class="text-[11px] sm:text-xs text-slate-400 mt-1.5 leading-snug">Mariposa limpia ✓</div>
                <div class="text-[11px] sm:text-xs text-amber-400 font-medium">Múltiple pendiente</div>
            </div>
        </div>

        <!-- Freeze Frame Comparison Table -->
        <div class="card p-4 sm:p-6 mb-6">
            <div class="flex items-center justify-between mb-3">
                <h2 class="text-sm sm:text-base font-bold text-white flex items-center gap-1.5">
                    <span>📸</span> Freeze Frames (DTC P0102)
                </h2>
                <span class="text-[10px] text-slate-500 sm:hidden">← Desliza tabla →</span>
            </div>
            <div class="overflow-x-auto touch-scroll -mx-4 sm:mx-0 px-4 sm:px-0">
                <table class="w-full text-xs sm:text-sm text-left">
                    <thead class="text-[10px] sm:text-xs text-slate-400 uppercase bg-slate-900/60 border-b border-slate-800">
                        <tr>
                            <th class="py-2.5 px-3">Estado</th>
                            <th class="py-2.5 px-3">Velocidad</th>
                            <th class="py-2.5 px-3">Régimen</th>
                            <th class="py-2.5 px-3">MAP</th>
                            <th class="py-2.5 px-3">MAF</th>
                            <th class="py-2.5 px-3">Carga</th>
                            <th class="py-2.5 px-3">Agua</th>
                            <th class="py-2.5 px-3">DTC</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-800 text-slate-300">
                        <tr class="hover:bg-slate-800/40">
                            <td class="py-2.5 px-3 font-semibold text-white whitespace-nowrap">06-Nov (Pre-Limpieza)</td>
                            <td class="py-2.5 px-3 text-red-400 font-bold whitespace-nowrap">91 km/h</td>
                            <td class="py-2.5 px-3 whitespace-nowrap">2.228 RPM</td>
                            <td class="py-2.5 px-3 whitespace-nowrap">145 kPa</td>
                            <td class="py-2.5 px-3 text-amber-400 font-bold whitespace-nowrap">60.3 g/s</td>
                            <td class="py-2.5 px-3 whitespace-nowrap">63.9 %</td>
                            <td class="py-2.5 px-3 whitespace-nowrap">83 °C</td>
                            <td class="py-2.5 px-3 whitespace-nowrap"><span class="px-1.5 py-0.5 bg-red-900/60 text-red-300 rounded text-[10px]">P0102</span></td>
                        </tr>
                        <tr class="hover:bg-slate-800/40">
                            <td class="py-2.5 px-3 font-semibold text-white whitespace-nowrap">07-Nov (Post-Limpieza)</td>
                            <td class="py-2.5 px-3 text-amber-400 font-bold whitespace-nowrap">105 km/h</td>
                            <td class="py-2.5 px-3 whitespace-nowrap">2.571 RPM</td>
                            <td class="py-2.5 px-3 whitespace-nowrap">122 kPa</td>
                            <td class="py-2.5 px-3 text-red-400 font-bold whitespace-nowrap">48.2 g/s</td>
                            <td class="py-2.5 px-3 whitespace-nowrap">36.5 %</td>
                            <td class="py-2.5 px-3 whitespace-nowrap">82 °C</td>
                            <td class="py-2.5 px-3 whitespace-nowrap"><span class="px-1.5 py-0.5 bg-red-900/60 text-red-300 rounded text-[10px]">P0102</span></td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <p class="text-[11px] sm:text-xs text-slate-400 mt-2.5 italic">
                * A 105 km/h y 2.571 RPM el flujo medido cayó a 48.2 g/s (vs 60.3 g/s antes), confirmando el estrangulamiento del múltiple en alta velocidad.
            </p>
        </div>

        <!-- Charts Section (Stacked on mobile) -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 sm:gap-6 mb-6">
            <div class="card p-3.5 sm:p-6">
                <h3 class="text-xs sm:text-sm font-bold text-white mb-1">Flujo MAF (g/s) vs RPM</h3>
                <p class="text-[11px] text-slate-400 mb-3">Dispersión durante la prueba en ruta del 07-Nov.</p>
                <div class="h-56 sm:h-64 relative">
                    <canvas id="chartMafRpm"></canvas>
                </div>
            </div>
            <div class="card p-3.5 sm:p-6">
                <h3 class="text-xs sm:text-sm font-bold text-white mb-1">Presión Turbo MAP (kPa) y Velocidad (km/h)</h3>
                <p class="text-[11px] text-slate-400 mb-3">Evolución en marcha.</p>
                <div class="h-56 sm:h-64 relative">
                    <canvas id="chartMapSpeed"></canvas>
                </div>
            </div>
        </div>

        <!-- Technical Analysis Section -->
        <div class="card p-4 sm:p-6 mb-6">
            <h2 class="text-sm sm:text-base font-bold text-white mb-3 flex items-center gap-1.5">
                <span>🔬</span> Resumen Técnico
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-3 sm:gap-4 text-xs sm:text-sm text-slate-300">
                <div class="bg-slate-900/70 p-3.5 rounded-lg border border-slate-800">
                    <h4 class="font-bold text-blue-400 mb-1.5">1. El cuello de botella</h4>
                    <p class="leading-relaxed">Limpiar la mariposa abrió la entrada, pero los corredores del múltiple siguen reducidos 30-40% en diámetro por carbonilla de la EGR.</p>
                </div>
                <div class="bg-slate-900/70 p-3.5 rounded-lg border border-slate-800">
                    <h4 class="font-bold text-amber-400 mb-1.5">2. Por qué no falla en ciudad</h4>
                    <p class="leading-relaxed">A &lt;70 km/h la demanda es de 20-35 g/s y cabe bien. A &gt;90 km/h el motor pide tragar 68 g/s y se ahoga contra el carbón.</p>
                </div>
                <div class="bg-slate-900/70 p-3.5 rounded-lg border border-slate-800">
                    <h4 class="font-bold text-emerald-400 mb-1.5">3. Solución definitiva</h4>
                    <p class="leading-relaxed"><strong>No cambiar el sensor MAF aún.</strong> Descarbonizar el múltiple de admisión y la EGR para restituir el diámetro original.</p>
                </div>
            </div>
        </div>
    </div>

    <!-- TAB 2: README.MD VIEWER (Full touch scrollable) -->
    <div id="tabReadme" class="hidden">
        <div class="card p-4 sm:p-8 md:p-10 mb-6">
            <div id="readmeContent" class="prose-dark max-w-none"></div>
        </div>
    </div>

    <!-- Footer -->
    <footer class="text-center text-[11px] sm:text-xs text-slate-500 py-6 border-t border-slate-800">
        Diagnóstico OBD2 &bull; SsangYong Musso 2.2 e-XDi &bull; Optimizado para móviles y escritorio
    </footer>

    <!-- Scripts -->
    <script>
        // Tab switching
        function switchTab(tab) {{
            const dashTab = document.getElementById('tabDashboard');
            const readmeTab = document.getElementById('tabReadme');
            const dashBtn = document.getElementById('tabDashboardBtn');
            const readmeBtn = document.getElementById('tabReadmeBtn');

            if (tab === 'dashboard') {{
                dashTab.classList.remove('hidden');
                readmeTab.classList.add('hidden');
                dashBtn.className = 'py-3 px-2 text-xs sm:text-sm font-bold text-center text-blue-400 border-b-2 border-blue-500 transition flex items-center justify-center gap-1.5 min-h-[44px]';
                readmeBtn.className = 'py-3 px-2 text-xs sm:text-sm font-bold text-center text-slate-400 hover:text-slate-200 border-b-2 border-transparent transition flex items-center justify-center gap-1.5 min-h-[44px]';
            }} else {{
                dashTab.classList.add('hidden');
                readmeTab.classList.remove('hidden');
                readmeBtn.className = 'py-3 px-2 text-xs sm:text-sm font-bold text-center text-blue-400 border-b-2 border-blue-500 transition flex items-center justify-center gap-1.5 min-h-[44px]';
                dashBtn.className = 'py-3 px-2 text-xs sm:text-sm font-bold text-center text-slate-400 hover:text-slate-200 border-b-2 border-transparent transition flex items-center justify-center gap-1.5 min-h-[44px]';
            }}
        }}

        // Render embedded README Markdown
        const rawReadme = {json.dumps(readme_md)};
        document.getElementById('readmeContent').innerHTML = marked.parse(rawReadme);

        // Charts configuration with touch / mobile friendliness
        const s2Data = {json.dumps(s2)};
        
        // Chart 1: MAF vs RPM
        const scatterData = s2Data.map(d => ({{ x: d.rpm, y: d.maf }})).filter(d => d.x && d.y);
        new Chart(document.getElementById('chartMafRpm'), {{
            type: 'scatter',
            data: {{
                datasets: [
                    {{
                        label: 'Prueba en Marcha (07-Nov)',
                        data: scatterData,
                        backgroundColor: '#3b82f6',
                        pointRadius: 4,
                        pointHoverRadius: 6
                    }},
                    {{
                        label: 'Freeze Frame 1 (91 km/h)',
                        data: [{{ x: 2228.5, y: 60.34 }}],
                        backgroundColor: '#f59e0b',
                        pointRadius: 7,
                        pointStyle: 'triangle'
                    }},
                    {{
                        label: 'Freeze Frame 2 (105 km/h)',
                        data: [{{ x: 2571.0, y: 48.25 }}],
                        backgroundColor: '#ef4444',
                        pointRadius: 8,
                        pointStyle: 'crossRot'
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                interaction: {{
                    mode: 'nearest',
                    intersect: false
                }},
                scales: {{
                    x: {{ 
                        title: {{ display: true, text: 'RPM', color: '#94a3b8', font: {{ size: 10 }} }}, 
                        grid: {{ color: '#1e293b' }}, 
                        ticks: {{ color: '#94a3b8', font: {{ size: 10 }} }} 
                    }},
                    y: {{ 
                        title: {{ display: true, text: 'MAF (g/s)', color: '#94a3b8', font: {{ size: 10 }} }}, 
                        grid: {{ color: '#1e293b' }}, 
                        ticks: {{ color: '#94a3b8', font: {{ size: 10 }} }} 
                    }}
                }},
                plugins: {{
                    legend: {{ 
                        position: 'top',
                        labels: {{ 
                            color: '#e2e8f0', 
                            boxWidth: 10,
                            padding: 8,
                            font: {{ size: 10 }} 
                        }} 
                    }}
                }}
            }}
        }});

        // Chart 2: MAP & Speed Timeline
        const labels = s2Data.map(d => d.ts);
        const mapVals = s2Data.map(d => d.map);
        const spdVals = s2Data.map(d => d.spd);

        new Chart(document.getElementById('chartMapSpeed'), {{
            type: 'line',
            data: {{
                labels: labels,
                datasets: [
                    {{
                        label: 'MAP (kPa)',
                        data: mapVals,
                        borderColor: '#8b5cf6',
                        backgroundColor: 'rgba(139, 92, 246, 0.1)',
                        yAxisID: 'yMap',
                        tension: 0.3,
                        pointRadius: 2,
                        fill: true
                    }},
                    {{
                        label: 'Velocidad (km/h)',
                        data: spdVals,
                        borderColor: '#10b981',
                        yAxisID: 'ySpd',
                        tension: 0.3,
                        pointRadius: 2
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                interaction: {{
                    mode: 'index',
                    intersect: false
                }},
                scales: {{
                    x: {{ 
                        grid: {{ color: '#1e293b' }}, 
                        ticks: {{ color: '#94a3b8', font: {{ size: 9 }}, maxTicksLimit: 6 }} 
                    }},
                    yMap: {{ 
                        type: 'linear', 
                        position: 'left', 
                        title: {{ display: false }}, 
                        grid: {{ color: '#1e293b' }}, 
                        ticks: {{ color: '#8b5cf6', font: {{ size: 9 }} }} 
                    }},
                    ySpd: {{ 
                        type: 'linear', 
                        position: 'right', 
                        title: {{ display: false }}, 
                        grid: {{ drawOnChartArea: false }}, 
                        ticks: {{ color: '#10b981', font: {{ size: 9 }} }} 
                    }}
                }},
                plugins: {{
                    legend: {{ 
                        position: 'top',
                        labels: {{ 
                            color: '#e2e8f0', 
                            boxWidth: 10,
                            padding: 8,
                            font: {{ size: 10 }} 
                        }} 
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""

with open('/home/pgtoopx/.gemini/antigravity/scratch/ssangyong_musso_obd2_diagnostics/index.html', 'w') as f:
    f.write(html_content)

print('Generated mobile-optimized index.html successfully.')
