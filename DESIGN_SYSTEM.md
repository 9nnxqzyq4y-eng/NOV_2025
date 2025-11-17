    # Abaco Design System

    ## Commercial Deck - Reglas de Diseño y Presentación

    _Última actualización: Enero 2025_

    ---

    ## 📋 Tabla de Contenidos

    - [Identidad Visual](#identidad-visual)
    - [Paleta de Colores](#paleta-de-colores)
    - [Tipografía](#tipografía)
    - [Efectos Visuales](#efectos-visuales)
    - [Componentes](#componentes)
    - [Layout y Espaciado](#layout-y-espaciado)
    - [Formato de Datos](#formato-de-datos)
    - [Idioma y Estilo](#idioma-y-estilo)
    - [Mejores Prácticas](#mejores-prácticas)


    ## 🎨 Identidad Visual

    ### Principios de Diseño

    1. **Glassmorphism**: Uso de efectos de vidrio esmerilado con transparencias
    2. **Gradientes oscuros**: Fondos con degradados para profundidad
    3. **Acentos de color**: Colores brillantes sobre fondos oscuros para jerarquía
    4. **Minimalismo**: Espacios en blanco y diseño limpio
    5. **Legibilidad**: Contraste alto para texto sobre fondos oscuros

    ### Estilo Visual

    - **Tema**: Dark mode profesional con acentos vibrantes
    - **Mood**: Tecnológico, moderno, confiable, data-driven
    - **Target audience**: Inversores, ejecutivos, equipos comerciales


    ## 🎨 Paleta de Colores

    ### Colores Principales

    ```css
    /* Backgrounds - Gradientes principales */
    .bg-primary {
      background: linear-gradient(
        to bottom right,
        rgb(15, 23, 42),
        /* slate-900 */ rgb(30, 58, 138),
        /* blue-900 */ rgb(15, 23, 42) /* slate-900 */
      );
    }

    .bg-secondary {
        rgb(17, 24, 39),
        /* gray-900 */ rgb(88, 28, 135),
        /* purple-900 */ rgb(17, 24, 39) /* gray-900 */
    ```

    ### Colores de Acento por Categoría

    | Color      | Uso                          | Hex       | Tailwind             |
    | ---------- | ---------------------------- | --------- | -------------------- |
    | **Purple** | KPIs principales, highlights | `#C1A6FF` | `purple-300/400/500` |
    | **Blue**   | Canales digitales, Meta      | `#60A5FA` | `blue-300/400/500`   |
    | **Green**  | Success, growth, positivo    | `#34D399` | `green-300/400`      |
    | **Pink**   | Digital small, social media  | `#F472B6` | `pink-300/400`       |
    | **Yellow** | Anchors, alertas             | `#FCD34D` | `yellow-300`         |
    | **Red**    | Risk, warnings               | `#F87171` | `red-300/500`        |

    ### Colores de Texto

    ```javascript
    // Jerarquía de texto
    const textColors  {
      primary: "text-white", // Títulos principales, números importantes
      secondary: "text-gray-300", // Body text, descripciones
      tertiary: "text-gray-400", // Subtítulos, labels
      muted: "text-gray-500", // Footer, notas, timestamps

      // Highlights semánticos
      success: "text-green-400", // Métricas positivas, objetivos cumplidos
      warning: "text-yellow-300", // Alertas, atención
      error: "text-red-400", // Errores, riesgos
      info: "text-blue-400", // Información, datos neutrales
      accent: "text-purple-400", // KPIs destacados, números clave
    };

    ### Bordes y Divisores

    // Bordes con transparencia
    border - purple - 500 / 20; // Sutil, para cards normales
    border - purple - 400 / 30; // Más visible, para highlights
    border - white / 10; // Divisores internos muy sutiles
    border - white / 20; // Divisores más visibles


    ## ✍️ Tipografía

    ### Fuentes

    // Fuentes principales (Google Fonts)
    const fonts  {
      titles: "Lato", // Títulos, headers, labels
      numbers: "Poppins", // Números, KPIs, datos
      body: "Lato", // Texto corrido, descripciones

    // Pesos de fuente
    const fontWeights  {
      regular: 400,
      semibold: 600,
      bold: 700,

    ### Escala Tipográfica

    | Elemento                  | Tamaño  | Peso     | Clase Tailwind                    |
    | ------------------------- | ------- | -------- | --------------------------------- |
    | **H1** (Números grandes)  | 36-48px | Bold     | `text-4xl` o `text-5xl font-bold` |
    | **H2** (Títulos de slide) | 24px    | Bold     | `text-2xl font-bold`              |
    | **H3** (Secciones)        | 12px    | Semibold | `text-xs font-semibold`           |
    | **Body** (Texto normal)   | 12px    | Regular  | `text-xs`                         |
    | **Small** (Detalles)      | 10px    | Regular  | `text-[10px]`                     |
    | **Tiny** (Footer, notas)  | 9-8px   | Regular  | `text-[9px]` o `text-[8px]`       |

    ### Jerarquía Visual

    ```jsx
    // Ejemplo de jerarquía en un KPI card

        {" "}
        {/* Label */}
        AUM (Live Portfolio)

        {/* Número principal */}
        $7.28M

        {/* Contexto */}
        As of Oct-2025


    ### Line Height y Spacing

    // Interlineado por tipo de texto
    const lineHeight  {
      tight: "leading-tight", // Títulos grandes (1.25)
      normal: "leading-normal", // Body text (1.5)
      relaxed: "leading-relaxed", // Texto largo (1.625)


    ## ✨ Efectos Visuales

    ### Glassmorphism (Efecto de Vidrio)

    // Card básica con efecto glassmorphism

      {/* Contenido */}

    // Desglose de propiedades:
    // bg-white/5         → Fondo blanco al 5% de opacidad
    // backdrop-blur-sm   → Desenfoque del fondo (small)
    // rounded-lg         → Bordes redondeados (8px)
    // border             → Borde sólido 1px
    // border-purple-500/20 → Color de borde al 20% de opacidad

    ### Variaciones de Cards

    // Card normal (información general)
    className
      "bg-white/5 backdrop-blur-sm rounded-lg p-3 border border-purple-500/20";

    // Card destacada (KPIs importantes)
      "bg-gradient-to-r from-purple-900/30 to-blue-900/30 backdrop-blur-sm rounded-lg p-3 border border-purple-400/30";

    // Card de alerta/warning
      "bg-white/5 backdrop-blur-sm rounded-lg p-3 border border-yellow-500/20";

    // Card de riesgo
      "bg-white/5 backdrop-blur-sm rounded-lg p-3 border border-red-500/20";

    // Card de éxito
      "bg-gradient-to-r from-green-900/30 to-blue-900/30 backdrop-blur-sm rounded-lg p-3 border border-green-400/30";

    ### Gradientes para Highlights

    // Gradiente purple-blue (más común)
    className  "bg-gradient-to-r from-purple-900/30 to-blue-900/30";

    // Gradiente green-blue (success)
    className  "bg-gradient-to-r from-green-900/30 to-blue-900/30";

    // Gradiente completo de fondo
    className  "bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900";

    ### Sombras y Profundidad

    // No usamos box-shadow tradicional
    // La profundidad se logra con:
    // 1. Glassmorphism (backdrop-blur)
    // 2. Bordes semitransparentes
    // 3. Gradientes sutiles
    // 4. Opacidades estratégicas


    ## 🧩 Componentes

    ### 1. KPI Card

    // Componente reutilizable para mostrar métricas

      {/* Label/Título */}
      Label del KPI

      {/* Valor principal */}

          • Métrica: Valor

          • Otra métrica:{" "}
          Otro valor

      {/* Nota al pie (opcional) */}
      Contexto o explicación


    ### 2. Highlighted Box

    // Box con gradiente para destacar información crítica

        Título destacado

        Texto importante con{" "}
        númerosy{" "}
        highlights.


    ### 3. List Item con Bullet

    // Lista con bullets personalizados

        • Item 1: valor destacado

        • Item 2: métrica positiva

        • Item 3:{" "}
        dato importante


    ### 4. Metric Row (Key-Value)

    // Fila de métrica con label y valor alineados

      Label de la métrica:
      $320k


    ### 5. Section Divider

    // Divisor entre secciones

      {/* Contenido después del divisor */}

    // O divisor inferior

      {/* Contenido antes del divisor */}


    ### 6. Grid de Cards (2 o 3 columnas)

    // Grid 2 columnas

        {/* Card 1 */}

        {/* Card 2 */}

    // Grid 3 columnas

      {/* 3 cards */}



    ## 📐 Layout y Espaciado

    ### Estructura de Slide (Template)

    // Estructura estándar de un slide
    div
      className"h-screen w-full bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900
                    flex flex-col justify-between p-8 overflow-hidden"
    
      {/* Header - Siempre centrado */}

        Título del Slide
        Subtítulo o contexto

      {/* Content - Grid de 2 columnas, scrollable */}

        {/* Columna izquierda */}
        {/* Cards */}

        {/* Columna derecha */}

      {/* Footer - Nota al pie */}

          Nota informativa | Fecha | Contexto


    ### Sistema de Espaciado

    | Uso                          | Clase       | Valor (px) |
    | ---------------------------- | ----------- | ---------- |
    | Padding contenedor principal | `p-8`       | 32px       |
    | Gap entre columnas           | `gap-4`     | 16px       |
    | Gap entre cards pequeñas     | `gap-3`     | 12px       |
    | Margin bottom sección        | `mb-4`      | 16px       |
    | Margin bottom pequeño        | `mb-2`      | 8px        |
    | Space-y entre items          | `space-y-1` | 4px        |
    | Space-y entre items          | `space-y-2` | 8px        |
    | Space-y entre cards          | `space-y-3` | 12px       |
    | Padding interno card         | `p-3`       | 12px       |
    | Padding interno card grande  | `p-4`       | 16px       |

    ### Responsive Considerations

    // Aunque el deck es para presentaciones (no responsive),
    // las proporciones están optimizadas para 16:9
    const aspectRatio  "16:9";
    const resolution  "1920x1080"; // Full HD estándar

    // El contenido usa overflow-y-auto para manejar exceso de contenido
    // en lugar de reducir tamaños de fuente


    ## 🔢 Formato de Datos

    ### Números y Moneda

    // Formato de moneda USD
    const formatCurrency  (value, decimals  2)  {
      if (value  1000000) {
        return `$${(value / 1000000).toFixed(decimals)}M`;
      }
      if (value  1000) {
        return `$${(value / 1000).toFixed(0)}k`;
      return `$${value.toLocaleString("en-US")}`;

    // Ejemplos:
    // $7,368,000 → "$7.37M"
    // $620,000 → "$620k"
    // $16,276,000 → "$16.276M" (cuando se necesita precisión)
    // $320,000 → "$320k"

    ### Porcentajes

    // Formato de porcentajes
    "37.4%"; // Con decimal para precisión
    "~20%"; // Aproximado (usar tilde ~)
    "≥96%"; // Mayor o igual
    "≤4%"; // Menor o igual
    "12%"; // Menor que (usar &lt; en JSX)
    "$50k"; // Mayor que (usar &gt; en JSX)

    // Cambios y objetivos
    "93.6% → ≥96%"; // Estado actual → Objetivo
    "15.6% → 12%"; // Mejora esperada

    ### Rangos

    // Rangos numéricos
    "$620–700k"; // Usar em dash (–), no guión (-)
    "10–16 clients"; // Rango de cantidad
    "$50–150k"; // Rango de montos
    "20–30k views"; // Vistas o impresiones

    ### Multiplicadores y Ratios

    "3.6×"; // Rotación de portafolio (usar ×, no x)
    "≥3×"; // Pipeline coverage
    "~4.5×/yr"; // Por año

    ### Fechas

    // Formato de fechas
    "Oct-25"; // Mes-Año (formato corto)
    "Oct-2025"; // Mes-Año (formato largo)
    "Oct 17, 2025"; // Fecha completa (en contexto)
    "Q4-2025"; // Quarter-Año
    "H1-26"; // Half (semestre)-Año corto
    "Dec-2026"; // Mes-Año objetivo

    // Rangos de fechas
    "Oct-25 → Dec-26"; // Período completo
    "Q4-25 → H1-26"; // Quarters/Halfs


    ## 🗣️ Idioma y Estilo

    ### Regla de Spanglish

    **Principio**: Mezclar español e inglés de forma natural según el contexto técnico y la audiencia.

    // ✅ Usar inglés para:
    const englishTerms  [
      "AUM",
      "KPI",
      "KAM",
      "funnel",
      "leads",
      "pipeline",
      "close rate",
      "churn",
      "default",
      "ROI",
      "CAC",
      "LTV",
      "SQL",
      "MQL",
      "SLA",
      "API",
      "CPL",
      "ER",
      "DPD",
    ];

    // ✅ Usar español para:
    const spanishPhrases  [
      "Objetivo & Oportunidad",
      "Estrategia por canal",
      "Cartera viva",
      "Líneas de crédito",
      "Flujo de caja",
      "Desembolsos",
      "Cobranza",

    // ✅ Mezclar naturalmente:
    ("Pipeline coverage: ≥3× (3 anchors futuros por cada cierre mensual)");
    ("Meta Q4-2025: 100–160k impresiones → 225–305 leads");
    ("Convierte tus facturas en cash en 48h");

    ### Tono y Voz

    | Contexto          | Tono                    | Ejemplo                          |
    | ----------------- | ----------------------- | -------------------------------- |
    | **Títulos**       | Directo, técnico        | "4 KAMs Strategy"                |
    | **KPIs**          | Preciso, cuantitativo   | "AUM (live): $7.28M"             |
    | **Descripciones** | Claro, conciso          | "After runoff/default allowance" |
    | **Objetivos**     | Aspiracional, concreto  | "Target (Dec-2026): $16.276M"    |
    | **Notas**         | Informativo, contextual | "Risk-adjusted path to $16.276M" |

    ### Símbolos y Caracteres Especiales

    // Símbolos matemáticos y lógicos
    "≥"; // Mayor o igual (ALT + 242)
    "≤"; // Menor o igual (ALT + 243)
    "≈"; // Aproximadamente (ALT + 247)
    "~"; // Aproximado (tilde)
    "±"; // Más/menos (ALT + 241)
    "×"; // Multiplicación (ALT + 0215)

    // Flechas y direcciones
    "→"; // Flecha derecha (indica cambio, progreso)
    "⇒"; // Flecha doble (indica resultado, consecuencia)

    // Bullets y separadores
    "•"; // Bullet point (ALT + 0149)
    "–"; // Em dash para rangos (ALT + 0150)
    "|"; // Pipe para separar (barra vertical)
    "/"; // Slash para fracciones o "por"

    // En JSX, usar HTML entities:
    "&lt;"; // 
    "&gt;"; // 
    "&amp;"; // &


    ## ✅ Mejores Prácticas

    ### 1. Jerarquía Visual

    // Orden de importancia visual (de mayor a menor)
    // 1. Número principal (text-4xl, text-white, font-bold)
    // 2. Label del número (text-xs, text-purple-300, font-semibold)
    // 3. Contexto/fecha (text-[10px], text-gray-400)
    // 4. Notas al pie (text-[8px], text-gray-500)

    // ✅ Bueno - Clara jerarquía

      AUM Target
      $16.276M
      Dec-2026

    // ❌ Malo - Sin jerarquía clara

      AUM Target: $16.276M (Dec-2026)


    ### 2. Uso de Color con Propósito

    // ✅ Bueno - Color indica significado
    +$8.908M  // Crecimiento
    DPD15: 15.6%         // Riesgo
    Meta/WA Only         // Canal
    $620–700k/mo       // KPI destacado

    // ❌ Malo - Color sin significado
    Total clients        // Color aleatorio

    ### 3. Consistencia en Formato

    // ✅ Bueno - Formato consistente en todo el deck
    "$7.28M"  →  "$16.276M"   // Siempre $ antes, M mayúscula
    "Oct-25"  →  "Dec-26"     // Siempre formato corto
    "~$320k/mo"               // Siempre /mo para mensual

    // ❌ Malo - Formatos mezclados
    "7.28M$"  →  "$16.276 M"  // Inconsistente
    "Oct-25"  →  "December 2026"  // Formatos diferentes

    ### 4. Espaciado Consistente

    // ✅ Bueno - Espaciado predecible
      {/* Siempre space-y-3 entre cards */}

    // ❌ Malo - Espaciado irregular

        {/* Espacios mezclados */}


    ### 5. Contenido Editable

    // Agregar interactividad para edición
    h2
      className"text-2xl font-bold text-white mb-2 cursor-pointer hover:text-purple-300"
      onClick{()  setEditing(true)}
      {editing ?  : title}


    ### 6. Responsive Content (Scroll)

    // ✅ Bueno - Scroll cuando hay overflow

      {/* Mucho contenido */}

    // ❌ Malo - Contenido cortado

      {/* Contenido se sale del slide */}


    ### 7. HTML Entities en JSX

    // ✅ Bueno - Usar entities para caracteres especiales
    Target: &lt;$10k
    Pipeline: &gt;3×
    Efficiency: &gt;96%

    // ❌ Malo - Causa errores de compilación
    Target:      // ❌ JSX error
    Pipeline: 3×     // ❌ JSX error


    ## 📊 Ejemplos Completos

    ### Ejemplo 1: KPI Card Completa


      {/* Header */}

        Current Base (Oct-2025)

      {/* Métricas principales */}

          • AUM (live): $7.28M

          • Active clients: 188

          • Target (Dec-2026):{" "}
          $16.276M

        {/* Contexto adicional */}

          +$8.908M net (~$0.636M/month avg)


    ### Ejemplo 2: Highlighted Summary Box

      className"bg-gradient-to-r from-purple-900/30 to-blue-900/30
                    backdrop-blur-sm rounded-lg p-3 border border-purple-400/30"
      {/* Título */}

        Total Monthly Growth Composition

      {/* Lista de métricas */}

        {/* Rows con key-value */}

          Anchors (KAM):
          $320k

          Mid (Inbound+KAM):
          $180–220k

          Digital Small (Meta/WA):
          $120–160k

        {/* Divisor */}

          Total Net Lift:
          $620–700k/mo

        {/* Nota al pie */}

          Cubre trayectoria a $16.276M (Dec-2026)


    ### Ejemplo 3: Section con Subsecciones


        Line Buckets by Channel (Monthly)

      {/* Subsección 1 */}

          Anchors (&gt;$50–150k) - KAM Only

            • Target: ≥1 new client/KAM/month

            • Ticket: $75–125k

            • Net AUM contrib:{" "}
            ~$320k/mo

      {/* Subsección 2 */}

          Mid ($10–50k) - Inbound + KAM

            • Target: 8–12 new clients/month

            ~$180–220k/mo

      {/* Subsección 3 (última, sin border-b) */}

          Digital Small (≤$10k) - Meta/WA Only

            • Target: 20–30 new clients/month

            ~$120–160k/mo



    ## 🚀 Quick Reference

    ### Colores por Categoría

    | Categoría         | Color Primary | Border                 | Uso               |
    | ----------------- | ------------- | ---------------------- | ----------------- |
    | General           | Purple        | `border-purple-500/20` | Default, KPIs     |
    | Canales digitales | Blue          | `border-blue-500/20`   | Meta, LinkedIn    |
    | Crecimiento       | Green         | `border-green-500/20`  | Success, targets  |
    | Social media      | Pink          | `border-pink-500/20`   | Small tickets     |
    | Alerts            | Yellow        | `border-yellow-500/20` | Anchors, warnings |
    | Risk              | Red           | `border-red-500/20`    | Riesgos, DPD      |

    ### Tamaños de Fuente por Elemento

    | Elemento             | Clase                                   |
    | -------------------- | --------------------------------------- |
    | Número KPI principal | `text-4xl font-bold text-white`         |
    | Título slide         | `text-2xl font-bold text-white`         |
    | Label sección        | `text-xs font-semibold text-purple-300` |
    | Body text            | `text-xs text-gray-300`                 |
    | Small details        | `text-[10px] text-gray-400`             |
    | Footer notes         | `text-[9px] text-gray-500`              |

    ### Espaciado Común

    | Uso                    | Clase       |
    | ---------------------- | ----------- |
    | Container padding      | `p-8`       |
    | Card padding           | `p-3`       |
    | Grid gap (2 cols)      | `gap-4`     |
    | Grid gap (3 cols)      | `gap-3`     |
    | Vertical spacing cards | `space-y-3` |
    | Vertical spacing items | `space-y-1` |
    | Margin bottom section  | `mb-4`      |


    ## 📝 Checklist de Diseño

    Antes de finalizar un slide, verificar:

    - [ ] Fondo con gradiente oscuro (`bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900`)
    - [ ] Header centrado con título H2 y subtítulo
    - [ ] Content en grid 2 columnas con `overflow-y-auto`
    - [ ] Cards con glassmorphism (`bg-white/5 backdrop-blur-sm`)
    - [ ] Bordes semitransparentes (`border border-purple-500/20`)
    - [ ] Jerarquía clara de texto (tamaños y colores)
    - [ ] Números formateados consistentemente (`$X.XXM`, `XX%`)
    - [ ] Spanglish natural (términos técnicos en inglés)
    - [ ] Espaciado consistente (`space-y-3` entre cards)
    - [ ] Footer con nota informativa pequeña
    - [ ] HTML entities para `` (`&lt;`, `&gt;`)
    - [ ] Colores semánticos (greensuccess, redrisk, etc.)


    _Documento vivo - actualizar según evolucione el design system_
