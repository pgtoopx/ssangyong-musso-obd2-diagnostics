# SsangYong Musso 2.2 e-XDi — Diagnóstico y Telemetría OBD2 (P0102 / P00AF)

Repositorio de análisis forense y registro de telemetría en tiempo real sobre vehículo **SsangYong Musso 2.2 Turbo Diesel**, enfocado en la resolución de fallas de sobrealimentación y restricción de flujo de aire (**DTC P0102 / P00AF / P0299**).

---

## 📌 Contexto e Historial del Vehículo

1. **Fallo Inicial (Turbo VGT Desactivado):**
   * En pruebas previas, el actuador electrónico de geometría variable quedó atascado (`P00AF(2A)` y `P0299`).
   * La presión de admisión (MAP) no superaba los **96.0 kPa** (presión atmosférica, turbo inoperante).
2. **Intervención 1 (Limpieza de MAF):**
   * Se desconectó y roció el sensor de masa de aire (MAF) con limpiacontactos sin silicona (*Senfineco*).
3. **Intervención 2 (Limpieza de Mariposa de Admisión):**
   * Se retiró una gruesa capa de hollín y carbonilla acumulada sobre la mariposa de admisión / válvula anti-shudder.
   * **El múltiple de admisión aún no ha sido desmontado ni descarbonizado.**

---

## 📊 Comparativa de Mediciones (Telemetría en Vivo)

El repositorio incluye dos capturas completas en formato CSV dentro de la carpeta [`data/`](data/):

* [`telemetry_2026-11-06_pre_limpieza_mariposa.csv`](data/telemetry_2026-11-06_pre_limpieza_mariposa.csv): Captura antes de la limpieza de la mariposa.
* [`telemetry_2026-11-07_post_limpieza_mariposa.csv`](data/telemetry_2026-11-07_post_limpieza_mariposa.csv): Captura en marcha (44 a 71 km/h) tras limpiar la mariposa.

### Comparativa de "Freeze Frames" (El momento exacto del fallo P0102)

| Parámetro | Medición 1 (06-Nov Pre-Limpieza) | Medición 2 (07-Nov Post-Limpieza) | Diferencia / Tendencia |
| :--- | :--- | :--- | :--- |
| **Velocidad del vehículo** | **91 km/h** | **105 km/h** | Falla exclusivamente en ruta (>90 km/h) |
| **Régimen del motor** | **2.228 RPM** | **2.571 RPM** | Régimen medio-alto de crucero |
| **Presión del turbo (MAP)** | **145 kPa** (1.45 bar abs) | **122 kPa** (1.22 bar abs) | El turbo está soplando correctamente |
| **Carga de motor** | **63.9 %** | **36.5 %** | Carga media en autopista |
| **Temperatura refrigerante**| **83 °C** | **82 °C** | Temperatura óptima de trabajo |
| **Caudal registrado (MAF)** | **60.34 g/s** | **48.25 g/s** | **-20% menor a mayor velocidad** |
| **Código disparado** | **`P0102`** (*Circuit Low*) | **`P0102`** (*Circuit Low*) | Mismo DTC recurrente |

---

## 🔬 Diagnóstico Técnico de la Causa Raíz

### 1. La paradoja del flujo decreciente
A 105 km/h y 2.571 RPM, el motor aspiró **menos aire** (48.25 g/s) que a 91 km/h y 2.228 RPM (60.34 g/s).
Para un motor 2.2L a 2.571 RPM con 1.22 bar de presión absoluta, el consumo volumétrico teórico de aire fresco es de aproximadamente **65 a 70 g/s**. El sensor registró un **déficit del 30%**.

### 2. El cuello de botella (Efecto "Arterias Tapadas")
Limpiar la mariposa despejó la boca de entrada, pero al dejar el múltiple de admisión sin descarbonizar:
* En ralentí (~8.5 g/s) y en ciudad (&lt;70 km/h), el aire requerido es poco y cabe holgadamente por los conductos reducidos.
* A velocidad de autopista (>90 km/h), el motor demanda masa de aire masiva. El aire presurizado por el turbo choca contra el tapón de carbón en las lumbreras y corredores del múltiple. La velocidad del flujo en la admisión colapsa y el MAF cae por debajo de la tabla mínima permitida por la ECU, disparando **`P0102`**.

### 3. Fuga en la válvula EGR
Con semejante nivel de acumulación de carbonilla, es probable que la válvula EGR no logre un sellado hermético al 100%, permitiendo que gases quemados ingresen a la admisión en régimen de crucero y desplacen masa de aire fresco proveniente del filtro.

---

## 🛠️ Plan de Acción Recomendado

1. **NO reemplazar el sensor MAF preventivamente:** El sensor responde de forma continua y proporcional; el problema actual es físico/aerodinámico por restricción de paso.
2. **Desmontaje y descarbonización química/mecánica del múltiple de admisión.**
3. **Limpieza e inspección del sellado de la válvula EGR.**
4. **Verificación de prueba dinámica:** Repetir la captura en ruta a 100 km/h; con el múltiple limpio, el caudalímetro debe alcanzar 65–70 g/s sin encender Check Engine.

---

## 📈 Dashboard Interactivo

El repositorio cuenta con [`index.html`](index.html), un panel interactivo desarrollado con Chart.js y Tailwind CSS para visualizar las curvas de telemetría, comparar los puntos de fallo y descargar los datos en crudo.
