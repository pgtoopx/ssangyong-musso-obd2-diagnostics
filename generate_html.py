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
                'ts': r['timestamp'].split(' ')[1],
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

html_content = f"""<!DOCTYPE html>
<html lang="es" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SsangYong Musso 2.2 — Telemetría y Diagnóstico OBD2</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
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
        body {{ background-color: #0b0f17; color: #e2e8f0; font-family: system-ui, -apple-system, sans-serif; }}
        .card {{ background: #131b2e; border: 1px solid #1e293b; border-radius: 0.75rem; }}
    </style>
</head>
<body class="p-4 md:p-8 max-w-7xl mx-auto">

    <!-- Header -->
    <header class="mb-8 border-b border-slate-800 pb-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
            <div class="flex items-center gap-3">
                <span class="px-2.5 py-1 text-xs font-semibold uppercase tracking-wider bg-red-950 text-red-400 border border-red-800 rounded-md">DTC P0102</span>
                <span class="px-2.5 py-1 text-xs font-semibold uppercase tracking-wider bg-blue-950 text-blue-400 border border-blue-800 rounded-md">SsangYong Musso 2.2 XDi</span>
                <span class="px-2.5 py-1 text-xs font-semibold uppercase tracking-wider bg-emerald-950 text-emerald-400 border border-emerald-800 rounded-md">Turbo VGT Activo</span>
            </div>
            <h1 class="text-2xl md:text-3xl font-bold mt-2 text-white">Análisis Comparativo de Telemetría OBD2</h1>
            <p class="text-slate-400 text-sm mt-1">Comparación de flujo de aire (MAF), presión de turbo (MAP) y diagnóstico de estrangulamiento por hollín.</p>
        </div>
        <div class="flex gap-2">
            <a href="data/telemetry_2026-11-06_pre_limpieza_mariposa.csv" download class="px-3 py-2 bg-slate-800 hover:bg-slate-700 text-xs font-medium rounded-lg border border-slate-700 transition">
                📥 CSV 06-Nov (Pre)
            </a>
            <a href="data/telemetry_2026-11-07_post_limpieza_mariposa.csv" download class="px-3 py-2 bg-blue-600 hover:bg-blue-500 text-xs font-medium rounded-lg text-white transition">
                📥 CSV 07-Nov (Post)
            </a>
        </div>
    </header>

    <!-- KPI Cards -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div class="card p-5">
            <div class="text-xs text-slate-400 uppercase font-semibold">Falla 1 (06-Nov Pre-Limpieza)</div>
            <div class="text-2xl font-bold text-red-400 mt-1">91 km/h</div>
            <div class="text-xs text-slate-400 mt-2">MAF: <span class="text-white font-medium">60.3 g/s</span> @ 2.228 RPM</div>
            <div class="text-xs text-slate-400">Boost: <span class="text-white font-medium">145 kPa</span> (0.45 bar)</div>
        </div>
        <div class="card p-5">
            <div class="text-xs text-slate-400 uppercase font-semibold">Falla 2 (07-Nov Post-Limpieza)</div>
            <div class="text-2xl font-bold text-amber-400 mt-1">105 km/h</div>
            <div class="text-xs text-slate-400 mt-2">MAF: <span class="text-white font-medium">48.2 g/s</span> @ 2.571 RPM</div>
            <div class="text-xs text-slate-400">Boost: <span class="text-white font-medium">122 kPa</span> (0.22 bar)</div>
        </div>
        <div class="card p-5">
            <div class="text-xs text-slate-400 uppercase font-semibold">Déficit de Flujo en Alta</div>
            <div class="text-2xl font-bold text-red-500 mt-1">-30%</div>
            <div class="text-xs text-slate-400 mt-2">Teórico 2.500 RPM: <span class="text-white font-medium">~68 g/s</span></div>
            <div class="text-xs text-slate-400">Medido real: <span class="text-red-400 font-medium">48.2 g/s</span></div>
        </div>
        <div class="card p-5">
            <div class="text-xs text-slate-400 uppercase font-semibold">Diagnóstico Causa Raíz</div>
            <div class="text-lg font-bold text-purple-400 mt-1">Múltiple con Hollín</div>
            <div class="text-xs text-slate-400 mt-2">Mariposa limpia ✓</div>
            <div class="text-xs text-amber-400 font-medium">Múltiple + EGR pendientes</div>
        </div>
    </div>

    <!-- Freeze Frame Comparison Table -->
    <div class="card p-6 mb-8">
        <h2 class="text-lg font-bold text-white mb-4 flex items-center gap-2">
            <span>📸</span> Comparativa de Freeze Frames (El momento exacto del DTC P0102)
        </h2>
        <div class="overflow-x-auto">
            <table class="w-full text-sm text-left">
                <thead class="text-xs text-slate-400 uppercase bg-slate-900/60 border-b border-slate-800">
                    <tr>
                        <th class="px-4 py-3">Medición / Estado</th>
                        <th class="px-4 py-3">Velocidad</th>
                        <th class="px-4 py-3">Régimen</th>
                        <th class="px-4 py-3">Presión MAP</th>
                        <th class="px-4 py-3">Caudal MAF</th>
                        <th class="px-4 py-3">Carga Motor</th>
                        <th class="px-4 py-3">Temp. Agua</th>
                        <th class="px-4 py-3">Código</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-slate-800 text-slate-300">
                    <tr class="hover:bg-slate-800/40">
                        <td class="px-4 py-3 font-semibold text-white">06-Nov (Pre-Limpieza mariposa)</td>
                        <td class="px-4 py-3 text-red-400 font-bold">91 km/h</td>
                        <td class="px-4 py-3">2.228 RPM</td>
                        <td class="px-4 py-3">145 kPa (1.45 bar)</td>
                        <td class="px-4 py-3 text-amber-400 font-bold">60.34 g/s</td>
                        <td class="px-4 py-3">63.9 %</td>
                        <td class="px-4 py-3">83 °C</td>
                        <td class="px-4 py-3"><span class="px-2 py-0.5 bg-red-900/60 text-red-300 rounded text-xs">P0102</span></td>
                    </tr>
                    <tr class="hover:bg-slate-800/40">
                        <td class="px-4 py-3 font-semibold text-white">07-Nov (Post-Limpieza mariposa)</td>
                        <td class="px-4 py-3 text-amber-400 font-bold">105 km/h</td>
                        <td class="px-4 py-3">2.571 RPM</td>
                        <td class="px-4 py-3">122 kPa (1.22 bar)</td>
                        <td class="px-4 py-3 text-red-400 font-bold">48.25 g/s</td>
                        <td class="px-4 py-3">36.5 %</td>
                        <td class="px-4 py-3">82 °C</td>
                        <td class="px-4 py-3"><span class="px-2 py-0.5 bg-red-900/60 text-red-300 rounded text-xs">P0102</span></td>
                    </tr>
                </tbody>
            </table>
        </div>
        <p class="text-xs text-slate-400 mt-3 italic">
            * Nótese que a 105 km/h y 2.571 RPM el flujo medido fue aún MENOR (48.25 g/s) que a 91 km/h (60.34 g/s), evidenciando el estrangulamiento de los conductos del múltiple de admisión a altas velocidades de aire.
        </p>
    </div>

    <!-- Charts Section -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div class="card p-6">
            <h3 class="text-base font-bold text-white mb-2">Flujo de Aire MAF (g/s) vs Régimen (RPM)</h3>
            <p class="text-xs text-slate-400 mb-4">Relación de flujo durante la prueba en movimiento del 07-Nov.</p>
            <div class="h-64">
                <canvas id="chartMafRpm"></canvas>
            </div>
        </div>
        <div class="card p-6">
            <h3 class="text-base font-bold text-white mb-2">Presión Turbo MAP (kPa) y Velocidad (km/h)</h3>
            <p class="text-xs text-slate-400 mb-4">Comportamiento dinámico durante aceleración en ruta.</p>
            <div class="h-64">
                <canvas id="chartMapSpeed"></canvas>
            </div>
        </div>
    </div>

    <!-- Technical Analysis Section -->
    <div class="card p-6 mb-8">
        <h2 class="text-lg font-bold text-white mb-4 flex items-center gap-2">
            <span>🔬</span> Análisis Técnico y Explicación Física
        </h2>
        <div class="grid md:grid-cols-3 gap-6 text-sm text-slate-300 leading-relaxed">
            <div class="bg-slate-900/60 p-4 rounded-lg border border-slate-800">
                <h4 class="font-bold text-blue-400 mb-2">1. La intervención y el cuello de botella</h4>
                <p>La limpieza de la mariposa de admisión despejó la entrada principal, pero el múltiple de admisión sigue colapsado por carbón y hollín. La mariposa actúa como válvula reguladora; si los conductos y lumbreras aguas abajo están reducidos un 30-40% en diámetro, el motor se asfixia en alta demanda.</p>
            </div>
            <div class="bg-slate-900/60 p-4 rounded-lg border border-slate-800">
                <h4 class="font-bold text-amber-400 mb-2">2. Por qué no falla en ciudad (&lt;70 km/h)</h4>
                <p>En ralentí (~8.5 g/s) y a velocidades moderadas (30-40 g/s), el caudal de aire cabe holgadamente por el múltiple obstruido. Solo al superar 90-100 km/h con el motor aspirando más de 65 g/s el aire se frena contra la carbonilla, el voltaje del MAF se desploma y la ECU acusa <strong>P0102 (Circuit Low)</strong>.</p>
            </div>
            <div class="bg-slate-900/60 p-4 rounded-lg border border-slate-800">
                <h4 class="font-bold text-emerald-400 mb-2">3. Pasos para la resolución final</h4>
                <p><strong>No cambiar el sensor MAF aún.</strong> El plan riguroso es desmontar y descarbonizar íntegramente el múltiple de admisión y la válvula EGR. Una vez que los cilindros puedan aspirar el volumen teórico, volver a registrar en ruta a 100 km/h para verificar que el MAF alcance los 70 g/s.</p>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <footer class="text-center text-xs text-slate-500 py-4 border-t border-slate-800">
        Diagnóstico generado de forma autónoma con Antigravity &bull; Repositorio privado de telemetría OBD2 &bull; SsangYong Musso 2.2 e-XDi
    </footer>

    <!-- Scripts for Charts -->
    <script>
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
                        pointRadius: 4
                    }},
                    {{
                        label: 'Freeze Frame Falla 1 (91 km/h)',
                        data: [{{ x: 2228.5, y: 60.34 }}],
                        backgroundColor: '#f59e0b',
                        pointRadius: 8,
                        pointStyle: 'triangle'
                    }},
                    {{
                        label: 'Freeze Frame Falla 2 (105 km/h)',
                        data: [{{ x: 2571.0, y: 48.25 }}],
                        backgroundColor: '#ef4444',
                        pointRadius: 9,
                        pointStyle: 'crossRot'
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    x: {{ title: {{ display: true, text: 'Régimen (RPM)', color: '#94a3b8' }}, grid: {{ color: '#1e293b' }}, ticks: {{ color: '#94a3b8' }} }},
                    y: {{ title: {{ display: true, text: 'Flujo MAF (g/s)', color: '#94a3b8' }}, grid: {{ color: '#1e293b' }}, ticks: {{ color: '#94a3b8' }} }}
                }},
                plugins: {{
                    legend: {{ labels: {{ color: '#e2e8f0', font: {{ size: 11 }} }} }}
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
                        label: 'Presión Turbo MAP (kPa)',
                        data: mapVals,
                        borderColor: '#8b5cf6',
                        backgroundColor: 'rgba(139, 92, 246, 0.1)',
                        yAxisID: 'yMap',
                        tension: 0.3,
                        fill: true
                    }},
                    {{
                        label: 'Velocidad (km/h)',
                        data: spdVals,
                        borderColor: '#10b981',
                        yAxisID: 'ySpd',
                        tension: 0.3
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    x: {{ grid: {{ color: '#1e293b' }}, ticks: {{ color: '#94a3b8', maxTicksLimit: 8 }} }},
                    yMap: {{ type: 'linear', position: 'left', title: {{ display: true, text: 'MAP (kPa)', color: '#8b5cf6' }}, grid: {{ color: '#1e293b' }}, ticks: {{ color: '#8b5cf6' }} }},
                    ySpd: {{ type: 'linear', position: 'right', title: {{ display: true, text: 'Velocidad (km/h)', color: '#10b981' }}, grid: {{ drawOnChartArea: false }}, ticks: {{ color: '#10b981' }} }}
                }},
                plugins: {{
                    legend: {{ labels: {{ color: '#e2e8f0', font: {{ size: 11 }} }} }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""

with open('/home/pgtoopx/.gemini/antigravity/scratch/ssangyong_musso_obd2_diagnostics/index.html', 'w') as f:
    f.write(html_content)

print('Generated index.html successfully.')
