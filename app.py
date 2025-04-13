<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ANEIAP - Evaluador de Hojas de Vida</title>
  <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@5.15.4/css/all.min.css" rel="stylesheet">
  <style>
    :root {
      --aneiap-blue: #0D62AD;
      --aneiap-light-green: #A8CF45;
      --aneiap-dark-green: #76C04E;
    }
    
    body {
      font-family: 'Century Gothic', Arial, sans-serif;
      color: #333;
      background-color: #f9f9f9;
    }
    
    .bg-aneiap-blue {
      background-color: var(--aneiap-blue);
    }
    
    .bg-aneiap-light-green {
      background-color: var(--aneiap-light-green);
    }
    
    .bg-aneiap-dark-green {
      background-color: var(--aneiap-dark-green);
    }
    
    .text-aneiap-blue {
      color: var(--aneiap-blue);
    }
    
    .text-aneiap-light-green {
      color: var(--aneiap-light-green);
    }
    
    .text-aneiap-dark-green {
      color: var(--aneiap-dark-green);
    }
    
    .border-aneiap-blue {
      border-color: var(--aneiap-blue);
    }
    
    .border-aneiap-light-green {
      border-color: var(--aneiap-light-green);
    }
    
    .btn-aneiap-blue {
      background-color: var(--aneiap-blue);
      color: white;
      transition: all 0.3s ease;
    }
    
    .btn-aneiap-blue:hover {
      background-color: #0A4D8A;
      transform: translateY(-2px);
    }
    
    .btn-aneiap-green {
      background-color: var(--aneiap-light-green);
      color: white;
      transition: all 0.3s ease;
    }
    
    .btn-aneiap-green:hover {
      background-color: var(--aneiap-dark-green);
      transform: translateY(-2px);
    }
    
    .section {
      display: none;
    }
    
    .section.active {
      display: block;
    }
    
    .card {
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
      transition: all 0.3s ease;
    }
    
    .card:hover {
      box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
      transform: translateY(-5px);
    }
    
    .placeholder-aneiap::placeholder {
      color: #aaa;
      opacity: 1;
    }
    
    .custom-file-input {
      position: relative;
    }
    
    .custom-file-input::before {
      content: 'Seleccionar archivo';
      position: absolute;
      top: 0;
      right: 0;
      bottom: 0;
      left: 0;
      background-color: var(--aneiap-blue);
      color: white;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 0.25rem;
      cursor: pointer;
    }
    
    .custom-file-label {
      margin-top: 5px;
      font-size: 0.875rem;
      color: #666;
    }
    
    .navbar {
      backdrop-filter: blur(10px);
      -webkit-backdrop-filter: blur(10px);
    }
    
    .disclaimer {
      background-color: rgba(255, 240, 240, 0.9);
      border-left: 5px solid #ff5252;
    }
  </style>
</head>
<body>
  <!-- Barra de navegación -->
  <nav class="navbar fixed w-full bg-white bg-opacity-90 shadow-md z-50">
    <div class="container mx-auto px-4 py-2 flex justify-between items-center">
      <div class="flex items-center">
        <img src="ISOLOGO C A COLOR.png">
      </div>
      <div class="space-x-4 hidden md:flex">
        <button onclick="showSection('home')" class="nav-link px-3 py-2 rounded hover:bg-gray-100 text-aneiap-blue font-bold">Inicio</button>
        <button onclick="showSection('simplified')" class="nav-link px-3 py-2 rounded hover:bg-gray-100 text-aneiap-blue">Evaluador Simplificado</button>
        <button onclick="showSection('descriptive')" class="nav-link px-3 py-2 rounded hover:bg-gray-100 text-aneiap-blue">Evaluador Descriptivo</button>
      </div>
      <div class="md:hidden">
        <button id="menu-toggle" class="text-aneiap-blue">
          <i class="fas fa-bars text-2xl"></i>
        </button>
      </div>
    </div>
    <!-- Menú móvil -->
    <div id="mobile-menu" class="hidden bg-white w-full py-2 px-4 shadow-md">
      <div class="flex flex-col space-y-2">
        <button onclick="showSection('home')" class="nav-link py-2 text-left text-aneiap-blue hover:bg-gray-100 px-2 rounded">Inicio</button>
        <button onclick="showSection('simplified')" class="nav-link py-2 text-left text-aneiap-blue hover:bg-gray-100 px-2 rounded">Evaluador Simplificado</button>
        <button onclick="showSection('descriptive')" class="nav-link py-2 text-left text-aneiap-blue hover:bg-gray-100 px-2 rounded">Evaluador Descriptivo</button>
      </div>
    </div>
  </nav>

  <div class="container mx-auto px-4 pt-20 pb-10">
    <!-- Sección de Inicio -->
    <section id="home" class="section active space-y-8">
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-aneiap-blue mb-2">Bienvenido a EvalHVAN</h1>
        <p class="text-xl font-semibold text-gray-700">¿Qué tan listo estás para asumir un cargo de junta directiva Capitular? Descúbrelo aquí 🦁</p>
      </div>
      
      <div class="bg-white rounded-lg shadow-lg overflow-hidden">
        <img src="https://i.imgur.com/6tJ8HAO.jpg" alt="Evaluador Hoja de Vida ANEIAP" class="w-full object-cover h-64 md:h-96">
        <div class="p-6">
          <p class="text-gray-700 mb-4">
            Esta herramienta analiza el contenido de la hoja de vida ANEIAP, comparándola con las funciones y perfil del cargo al que aspira, evaluando por medio de indicadores los aspectos puntuales en los cuales se hace necesario el aspirante enfatice para asegurar que este se encuentre preparado.
          </p>
          <p class="text-gray-700 mb-4">
            Esta fue diseñada para apoyar en el proceso de convocatoria a los evaluadores para calificar las hojas de vida de los aspirantes.
          </p>
          <p class="text-gray-700 mb-4">
            Como resultado de este análisis se generará un reporte PDF descargable.
          </p>
        </div>
      </div>
      
      <div class="my-10">
        <h2 class="text-2xl font-bold text-center text-aneiap-blue mb-8">🔍 Selecciona el tipo de evaluación de Hoja de Vida</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <!-- Versión Simplificada -->
          <div class="card bg-white rounded-lg overflow-hidden">
            <div class="p-6">
              <h3 class="text-xl font-bold text-aneiap-blue mb-2">▶️ Versión Simplificada</h3>
              <p class="text-gray-700 mb-4">Esta versión analiza la hoja de vida de forma mucho más rápida evaluando cada una de las experiencias como listado.</p>
              <img src="https://i.imgur.com/Nh2ysAK.jpg" alt="Split actual" class="w-full h-48 object-cover rounded-lg mb-4">
              
              <div class="bg-blue-50 p-4 rounded-lg mb-4">
                <h4 class="font-bold text-aneiap-blue mb-2">Recomendaciones a tener en cuenta ✅</h4>
                <ul class="list-disc pl-5 text-gray-700 space-y-1">
                  <li>Es preferible que la HV no haya sido cambiada de formato varias veces, ya que esto puede complicar la lectura y extracción del texto.</li>
                  <li>La EXPERIENCIA EN ANEIAP debe estar enumerada para facilitar el análisis de la misma.</li>
                  <li>El análisis puede presentar inconsistencias si la HV no está debidamente separada en subtítulos.</li>
                  <li>Si la sección de EXPERIENCIA EN ANEIAP está dispuesta como tabla, la herramienta puede fallar.</li>
                </ul>
              </div>
              
              <button onclick="showSection('simplified')" class="btn-aneiap-blue w-full py-3 px-4 rounded-lg font-bold text-center">Ir a Evaluador Simplificado</button>
            </div>
          </div>
          
          <!-- Versión Descriptiva -->
          <div class="card bg-white rounded-lg overflow-hidden">
            <div class="p-6">
              <h3 class="text-xl font-bold text-aneiap-blue mb-2">⏩ Versión Descriptiva</h3>
              <p class="text-gray-700 mb-4">Esta versión es más cercana al entorno profesional permitiendo analizar la descripción de cada una de las experiencia de la hoja de vida</p>
              <img src="https://i.imgur.com/5jfmCPA.jpg" alt="Split descriptivo" class="w-full h-48 object-cover rounded-lg mb-4">
              
              <div class="bg-blue-50 p-4 rounded-lg mb-4">
                <h4 class="font-bold text-aneiap-blue mb-2">Recomendaciones a tener en cuenta ✅</h4>
                <ul class="list-disc pl-5 text-gray-700 space-y-1">
                  <li>Organiza tu HV en formato descriptivo para cada cargo o proyecto.</li>
                  <li>Utiliza negrita para identificar la experiencia.</li>
                  <li>Usa guiones para detallar las acciones realizadas en cada ítem.</li>
                  <li>Evita usar tablas para la sección de experiencia, ya que esto dificulta la extracción de datos.</li>
                </ul>
              </div>
              
              <button onclick="showSection('descriptive')" class="btn-aneiap-blue w-full py-3 px-4 rounded-lg font-bold text-center">Ir a Evaluador Descriptivo</button>
            </div>
          </div>
        </div>
      </div>
      
      <div class="mt-8 text-center">
        <h2 class="text-xl font-semibold text-gray-700 mb-4">ℹ️ Aquí puedes encontrar información si quieres saber un poco más</h2>
        
        <div class="flex justify-center space-x-4">
          <a href="https://drive.google.com/drive/folders/1hSUChvaYymUJ6g-IEfiY4hYqikePsQ9P?usp=drive_link" target="_blank" class="bg-orange-500 hover:bg-orange-600 text-white font-bold py-3 px-6 rounded-lg transition">
            Info cargos
          </a>
          <a href="https://docs.google.com/document/d/1BM07wuVaXEWcdurTRr8xBzjsB1fiWt6wGqOzLiyQBs8/edit?usp=drive_link" target="_blank" class="bg-orange-500 hover:bg-orange-600 text-white font-bold py-3 px-6 rounded-lg transition">
            Info indicadores
          </a>
        </div>
      </div>
      
      <div class="mt-10 py-4 border-t border-gray-200">
        <p class="text-center font-bold text-lg text-gray-700">
          La herramienta tiene disponible dos versiones, de modo que se pueda evaluar la HV con el formato actual y una propuesta para incluir descripciones de los proyectos/cargos ocupados.
        </p>
      </div>
    </section>

    <!-- Sección Simplificada -->
    <section id="simplified" class="section space-y-8">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-aneiap-blue mb-2">Evaluador de Hoja de Vida ANEIAP</h1>
        <img src="https://i.imgur.com/T4Vb5tL.jpg" alt="Analizador Versión Simplificada" class="max-w-full mx-auto my-4 rounded-lg shadow-lg">
        <h2 class="text-xl font-semibold text-gray-700">Versión Simplificada Hoja de Vida ANEIAP ▶️</h2>
        <p class="text-gray-600 mt-2">Sube tu hoja de vida ANEIAP (en formato PDF) para evaluar tu perfil.</p>
      </div>
      
      <div class="bg-white rounded-lg shadow-lg p-6 max-w-3xl mx-auto">
        <form id="simplified-form" class="space-y-6">
          <div>
            <label for="candidate-name-simple" class="block text-gray-700 font-semibold mb-2">Nombre del candidato:</label>
            <input type="text" id="candidate-name-simple" name="candidate_name" class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-aneiap-blue placeholder-aneiap" placeholder="Ej: Juan Pérez">
          </div>
          
          <div>
            <label for="resume-file-simple" class="block text-gray-700 font-semibold mb-2">Sube tu hoja de vida ANEIAP en formato PDF:</label>
            <div class="relative">
              <input type="file" id="resume-file-simple" name="resume_file" accept=".pdf" class="opacity-0 absolute top-0 left-0 w-full h-12 cursor-pointer">
              <div class="bg-aneiap-blue text-white px-4 py-3 rounded-md font-medium text-center cursor-pointer">
                Seleccionar archivo
              </div>
              <p id="file-name-simple" class="mt-2 text-sm text-gray-500">Ningún archivo seleccionado</p>
            </div>
          </div>
          
          <div>
            <label for="position-simple" class="block text-gray-700 font-semibold mb-2">Selecciona el cargo al que aspiras:</label>
            <select id="position-simple" name="position" class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-aneiap-blue">
              <option value="DCA">DCA</option>
              <option value="DCC">DCC</option>
              <option value="DCD">DCD</option>
              <option value="DCF">DCF</option>
              <option value="DCM">DCM</option>
              <option value="CCP">CCP</option>
              <option value="IC">IC</option>
              <option value="PC">PC</option>
            </select>
          </div>
          
          <div>
            <label for="chapter-simple" class="block text-gray-700 font-semibold mb-2">Selecciona el Capítulo al que perteneces:</label>
            <select id="chapter-simple" name="chapter" class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-aneiap-blue">
              <option value="UNIGUAJIRA">UNIGUAJIRA</option>
              <option value="UNIMAGDALENA">UNIMAGDALENA</option>
              <option value="UNINORTE">UNINORTE</option>
              <option value="UNIATLÁNTICO">UNIATLÁNTICO</option>
              <option value="CUC">CUC</option>
              <option value="UNISIMÓN">UNISIMÓN</option>
              <option value="LIBREQUILLA">LIBREQUILLA</option>
              <option value="UTB">UTB</option>
              <option value="UFPS">UFPS</option>
              <option value="UNALMED">UNALMED</option>
              <option value="UPBMED">UPBMED</option>
              <option value="UDEA">UDEA</option>
              <option value="UTP">UTP</option>
              <option value="UNALMA">UNALMA</option>
              <option value="LIBRECALI">LIBRECALI</option>
              <option value="UNIVALLE">UNIVALLE</option>
              <option value="ICESI">ICESI</option>
              <option value="USC">USC</option>
              <option value="UDISTRITAL">UDISTRITAL</option>
              <option value="UNALBOG">UNALBOG</option>
              <option value="UPBMONTERÍA">UPBMONTERÍA</option>
              <option value="AREANDINA">AREANDINA</option>
              <option value="UNICÓDOBA">UNICÓDOBA</option>
            </select>
          </div>
          
          <button type="button" id="generate-report-simple" class="btn-aneiap-blue w-full py-3 rounded-lg font-bold text-center">
            Generar Reporte PDF
          </button>
        </form>
      </div>
      
      <div id="report-preview-simple" class="hidden bg-white rounded-lg shadow-lg p-6 max-w-3xl mx-auto mt-8">
        <h3 class="text-xl font-bold text-aneiap-blue mb-4">Vista previa del reporte</h3>
        
        <div class="border border-gray-200 rounded-lg p-4 mb-4">
          <div class="bg-gray-100 p-4 rounded-lg mb-4">
            <h4 class="font-bold text-gray-700 mb-2">Análisis de perfil del aspirante</h4>
            <div class="flex justify-between mb-2">
              <span class="font-semibold">Concordancia con funciones:</span>
              <span id="profile-func-match" class="text-aneiap-blue font-bold">85%</span>
            </div>
            <div class="flex justify-between">
              <span class="font-semibold">Concordancia con perfil:</span>
              <span id="profile-profile-match" class="text-aneiap-blue font-bold">78%</span>
            </div>
          </div>
          
          <div class="bg-gray-100 p-4 rounded-lg mb-4">
            <h4 class="font-bold text-gray-700 mb-2">Evaluación de presentación</h4>
            <div class="grid grid-cols-2 gap-2">
              <div class="flex justify-between">
                <span>Ortografía:</span>
                <span class="text-aneiap-blue font-bold">4.5</span>
              </div>
              <div class="flex justify-between">
                <span>Coherencia:</span>
                <span class="text-aneiap-blue font-bold">4.2</span>
              </div>
              <div class="flex justify-between">
                <span>Gramática:</span>
                <span class="text-aneiap-blue font-bold">4.0</span>
              </div>
              <div class="flex justify-between">
                <span>Puntuación general:</span>
                <span class="text-aneiap-blue font-bold">4.3</span>
              </div>
            </div>
          </div>
          
          <div class="bg-gray-100 p-4 rounded-lg">
            <h4 class="font-bold text-gray-700 mb-2">Resultados globales</h4>
            <div class="flex justify-between mb-2">
              <span class="font-semibold">Puntaje total:</span>
              <span id="total-score" class="text-aneiap-blue font-bold">4.1</span>
            </div>
            <p class="text-sm text-gray-600 italic">El reporte completo estará disponible en el PDF generado.</p>
          </div>
        </div>
        
        <div class="text-center">
          <button id="download-report-simple" class="bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-lg transition">
            Descargar Reporte Completo
          </button>
        </div>
      </div>
      
      <div class="disclaimer p-4 rounded-lg text-red-800 max-w-3xl mx-auto mt-8">
        <p class="text-center font-bold text-lg">
          ⚠️ DISCLAIMER: LA INFORMACIÓN PROPORCIONADA POR ESTA HERRAMIENTA NO REPRESENTA NINGÚN TIPO DE DECISIÓN, SU FIN ES MERAMENTE ILUSTRATIVO
        </p>
      </div>
      
      <div class="text-center mt-6">
        <button onclick="showSection('home')" class="inline-flex items-center text-aneiap-blue hover:underline">
          <i class="fas fa-arrow-left mr-2"></i> Volver al Inicio
        </button>
      </div>
    </section>

    <!-- Sección Descriptiva -->
    <section id="descriptive" class="section space-y-8">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-aneiap-blue mb-2">Evaluador de Hoja de Vida ANEIAP</h1>
        <img src="https://i.imgur.com/K3cD8LS.jpg" alt="Analizador Versión Descriptiva" class="max-w-full mx-auto my-4 rounded-lg shadow-lg">
        <h2 class="text-xl font-semibold text-gray-700">Versión Descriptiva Hoja de Vida ANEIAP ⏩</h2>
        <p class="text-gray-600 mt-2">Sube tu hoja de vida ANEIAP (en formato PDF) para evaluar tu perfil.</p>
      </div>
      
      <div class="bg-white rounded-lg shadow-lg p-6 max-w-3xl mx-auto">
        <form id="descriptive-form" class="space-y-6">
          <div>
            <label for="candidate-name-desc" class="block text-gray-700 font-semibold mb-2">Nombre del candidato:</label>
            <input type="text" id="candidate-name-desc" name="candidate_name" class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-aneiap-blue placeholder-aneiap" placeholder="Ej: María Rodríguez">
          </div>
          
          <div>
            <label for="resume-file-desc" class="block text-gray-700 font-semibold mb-2">Sube tu hoja de vida ANEIAP en formato PDF:</label>
            <div class="relative">
              <input type="file" id="resume-file-desc" name="resume_file" accept=".pdf" class="opacity-0 absolute top-0 left-0 w-full h-12 cursor-pointer">
              <div class="bg-aneiap-blue text-white px-4 py-3 rounded-md font-medium text-center cursor-pointer">
                Seleccionar archivo
              </div>
              <p id="file-name-desc" class="mt-2 text-sm text-gray-500">Ningún archivo seleccionado</p>
            </div>
          </div>
          
          <div>
            <label for="position-desc" class="block text-gray-700 font-semibold mb-2">Selecciona el cargo al que aspiras:</label>
            <select id="position-desc" name="position" class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-aneiap-blue">
              <option value="DCA">DCA</option>
              <option value="DCC">DCC</option>
              <option value="DCD">DCD</option>
              <option value="DCF">DCF</option>
              <option value="DCM">DCM</option>
              <option value="CCP">CCP</option>
              <option value="IC">IC</option>
              <option value="PC">PC</option>
            </select>
          </div>
          
          <div>
            <label for="chapter-desc" class="block text-gray-700 font-semibold mb-2">Selecciona el Capítulo al que perteneces:</label>
            <select id="chapter-desc" name="chapter" class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-aneiap-blue">
              <option value="UNIGUAJIRA">UNIGUAJIRA</option>
              <option value="UNIMAGDALENA">UNIMAGDALENA</option>
              <option value="UNINORTE">UNINORTE</option>
              <option value="UNIATLÁNTICO">UNIATLÁNTICO</option>
              <option value="CUC">CUC</option>
              <option value="UNISIMÓN">UNISIMÓN</option>
              <option value="LIBREQUILLA">LIBREQUILLA</option>
              <option value="UTB">UTB</option>
              <option value="UFPS">UFPS</option>
              <option value="UNALMED">UNALMED</option>
              <option value="UPBMED">UPBMED</option>
              <option value="UDEA">UDEA</option>
              <option value="UTP">UTP</option>
              <option value="UNALMA">UNALMA</option>
              <option value="LIBRECALI">LIBRECALI</option>
              <option value="UNIVALLE">UNIVALLE</option>
              <option value="ICESI">ICESI</option>
              <option value="USC">USC</option>
              <option value="UDISTRITAL">UDISTRITAL</option>
              <option value="UNALBOG">UNALBOG</option>
              <option value="UPBMONTERÍA">UPBMONTERÍA</option>
              <option value="AREANDINA">AREANDINA</option>
              <option value="UNICÓDOBA">UNICÓDOBA</option>
            </select>
          </div>
          
          <button type="button" id="generate-report-desc" class="btn-aneiap-blue w-full py-3 rounded-lg font-bold text-center">
            Generar Reporte PDF
          </button>
        </form>
      </div>
      
      <div id="report-preview-desc" class="hidden bg-white rounded-lg shadow-lg p-6 max-w-3xl mx-auto mt-8">
        <h3 class="text-xl font-bold text-aneiap-blue mb-4">Vista previa del reporte descriptivo</h3>
        
        <div class="border border-gray-200 rounded-lg p-4 mb-4">
          <div class="bg-gray-100 p-4 rounded-lg mb-4">
            <h4 class="font-bold text-gray-700 mb-2">Análisis de experiencias descritas</h4>
            <div class="overflow-x-auto">
              <table class="min-w-full bg-white">
                <thead>
                  <tr>
                    <th class="py-2 px-4 bg-gray-50 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">
                      Experiencia
                    </th>
                    <th class="py-2 px-4 bg-gray-50 text-center text-xs font-semibold text-gray-700 uppercase tracking-wider">
                      Funciones (%)
                    </th>
                    <th class="py-2 px-4 bg-gray-50 text-center text-xs font-semibold text-gray-700 uppercase tracking-wider">
                      Perfil (%)
                    </th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-200">
                  <tr>
                    <td class="py-2 px-4 text-sm">Director Capitular de Académico 2023-2</td>
                    <td class="py-2 px-4 text-sm text-center text-aneiap-blue font-semibold">92%</td>
                    <td class="py-2 px-4 text-sm text-center text-aneiap-blue font-semibold">88%</td>
                  </tr>
                  <tr>
                    <td class="py-2 px-4 text-sm">Coordinador de Escuela de Formación 2023-1</td>
                    <td class="py-2 px-4 text-sm text-center text-aneiap-blue font-semibold">85%</td>
                    <td class="py-2 px-4 text-sm text-center text-aneiap-blue font-semibold">76%</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          
          <div class="bg-gray-100 p-4 rounded-lg mb-4">
            <h4 class="font-bold text-gray-700 mb-2">Indicadores de competencia</h4>
            <div class="space-y-2">
              <div>
                <div class="flex justify-between mb-1">
                  <span class="text-sm font-medium">Diseño académico</span>
                  <span class="text-sm font-medium text-aneiap-blue">85%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div class="bg-aneiap-blue h-2 rounded-full" style="width: 85%"></div>
                </div>
              </div>
              <div>
                <div class="flex justify-between mb-1">
                  <span class="text-sm font-medium">Innovación e investigación</span>
                  <span class="text-sm font-medium text-aneiap-blue">68%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div class="bg-aneiap-blue h-2 rounded-full" style="width: 68%"></div>
                </div>
              </div>
              <div>
                <div class="flex justify-between mb-1">
                  <span class="text-sm font-medium">Formación y capacitación</span>
                  <span class="text-sm font-medium text-aneiap-blue">92%</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2">
                  <div class="bg-aneiap-blue h-2 rounded-full" style="width: 92%"></div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="bg-gray-100 p-4 rounded-lg">
            <h4 class="font-bold text-gray-700 mb-2">Puntajes totales</h4>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <span class="font-semibold">Experiencia ANEIAP:</span>
                <span class="text-aneiap-blue font-bold">4.2</span>
              </div>
              <div>
                <span class="font-semibold">Asistencia a eventos:</span>
                <span class="text-aneiap-blue font-bold">3.8</span>
              </div>
              <div>
                <span class="font-semibold">Eventos organizados:</span>
                <span class="text-aneiap-blue font-bold">4.5</span>
              </div>
              <div>
                <span class="font-semibold">Perfil:</span>
                <span class="text-aneiap-blue font-bold">4.1</span>
              </div>
              <div>
                <span class="font-semibold">Presentación:</span>
                <span class="text-aneiap-blue font-bold">4.3</span>
              </div>
              <div>
                <span class="font-semibold">Puntaje global:</span>
                <span class="text-aneiap-blue font-bold">4.2</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="text-center">
          <button id="download-report-desc" class="bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-lg transition">
            Descargar Reporte Completo
          </button>
        </div>
      </div>
      
      <div class="bg-white rounded-lg shadow-lg p-6 max-w-3xl mx-auto mt-8">
        <h3 class="text-xl font-bold text-center text-aneiap-blue mb-4">Plantilla Propuesta HV 📑</h3>
        <img src="https://i.imgur.com/DwCXrQz.jpg" alt="PLANTILLA PROPUESTA HV ANEIAP" class="max-w-full mx-auto my-4 rounded-lg shadow-md">
        
        <div class="text-center mt-4">
          <a href="https://drive.google.com/drive/folders/16i35reQpBq9eC2EuZfy6E6Uul5XVDN8D?usp=sharing" target="_blank" class="inline-block bg-orange-500 hover:bg-orange-600 text-white font-bold py-3 px-6 rounded-lg transition">
            Explorar plantilla
          </a>
        </div>
      </div>
      
      <div class="disclaimer p-4 rounded-lg text-red-800 max-w-3xl mx-auto mt-8">
        <p class="text-center font-bold text-lg">
          ⚠️ DISCLAIMER: LA INFORMACIÓN PROPORCIONADA POR ESTA HERRAMIENTA NO REPRESENTA NINGÚN TIPO DE DECISIÓN, SU FIN ES MERAMENTE ILUSTRATIVO
        </p>
      </div>
      
      <div class="text-center mt-6">
        <button onclick="showSection('home')" class="inline-flex items-center text-aneiap-blue hover:underline">
          <i class="fas fa-arrow-left mr-2"></i> Volver al Inicio
        </button>
      </div>
    </section>
  </div>

  <footer class="bg-aneiap-blue text-white py-8">
    <div class="container mx-auto px-4">
      <div class="flex flex-col md:flex-row justify-between items-center">
        <div class="mb-6 md:mb-0">
          <img src="ISOLOGO C BLANCO.png">
        </div>
        <div class="text-center md:text-right">
          <p class="mb-2">© 2024 Asociación Nacional de Estudiantes de Ingeniería Industrial, Administrativa y de Producción</p>
          <p class="text-sm opacity-75">Herramienta desarrollada para uso interno de evaluación de hojas de vida</p>
        </div>
      </div>
    </div>
  </footer>

  <script>
    // Manejo de navegación entre secciones
    function showSection(sectionId) {
      // Ocultar todas las secciones
      document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
      });
      
      // Mostrar la sección seleccionada
      document.getElementById(sectionId).classList.add('active');
      
      // Desplazarse al inicio
      window.scrollTo(0, 0);
      
      // Cerrar menú móvil si está abierto
      document.getElementById('mobile-menu').classList.add('hidden');
    }
    
    // Manejar menú móvil
    document.getElementById('menu-toggle').addEventListener('click', function() {
      const mobileMenu = document.getElementById('mobile-menu');
      mobileMenu.classList.toggle('hidden');
    });
    
    // Mostrar nombre de archivo seleccionado (versión simplificada)
    document.getElementById('resume-file-simple').addEventListener('change', function(e) {
      const fileName = e.target.files[0] ? e.target.files[0].name : 'Ningún archivo seleccionado';
      document.getElementById('file-name-simple').textContent = fileName;
    });
    
    // Mostrar nombre de archivo seleccionado (versión descriptiva)
    document.getElementById('resume-file-desc').addEventListener('change', function(e) {
      const fileName = e.target.files[0] ? e.target.files[0].name : 'Ningún archivo seleccionado';
      document.getElementById('file-name-desc').textContent = fileName;
    });
    
    // Simulación de generación de reportes (versión simplificada)
    document.getElementById('generate-report-simple').addEventListener('click', function() {
      const candidateName = document.getElementById('candidate-name-simple').value;
      const resumeFile = document.getElementById('resume-file-simple').files[0];
      const position = document.getElementById('position-simple').value;
      const chapter = document.getElementById('chapter-simple').value;
      
      if (!candidateName || !resumeFile || !position || !chapter) {
        alert('Por favor, complete todos los campos para generar el reporte.');
        return;
      }
      
      // Simulación de procesamiento (en una aplicación real, esto sería una llamada a la API)
      document.getElementById('generate-report-simple').textContent = 'Procesando...';
      
      setTimeout(() => {
        document.getElementById('generate-report-simple').textContent = 'Generar Reporte PDF';
        document.getElementById('report-preview-simple').classList.remove('hidden');
        
        // Actualizar datos de la vista previa con valores aleatorios (simulación)
        const profileFuncMatch = (65 + Math.random() * 35).toFixed(2);
        const profileProfileMatch = (65 + Math.random() * 35).toFixed(2);
        const totalScore = (3 + Math.random() * 2).toFixed(1);
        
        document.getElementById('profile-func-match').textContent = `${profileFuncMatch}%`;
        document.getElementById('profile-profile-match').textContent = `${profileProfileMatch}%`;
        document.getElementById('total-score').textContent = totalScore;
        
        // Desplazarse a la vista previa
        document.getElementById('report-preview-simple').scrollIntoView({behavior: 'smooth'});
      }, 2000);
    });
    
    // Simulación de generación de reportes (versión descriptiva)
    document.getElementById('generate-report-desc').addEventListener('click', function() {
      const candidateName = document.getElementById('candidate-name-desc').value;
      const resumeFile = document.getElementById('resume-file-desc').files[0];
      const position = document.getElementById('position-desc').value;
      const chapter = document.getElementById('chapter-desc').value;
      
      if (!candidateName || !resumeFile || !position || !chapter) {
        alert('Por favor, complete todos los campos para generar el reporte.');
        return;
      }
      
      // Simulación de procesamiento (en una aplicación real, esto sería una llamada a la API)
      document.getElementById('generate-report-desc').textContent = 'Procesando...';
      
      setTimeout(() => {
        document.getElementById('generate-report-desc').textContent = 'Generar Reporte PDF';
        document.getElementById('report-preview-desc').classList.remove('hidden');
        
        // Desplazarse a la vista previa
        document.getElementById('report-preview-desc').scrollIntoView({behavior: 'smooth'});
      }, 2000);
    });
    
    // Simulación de descarga de reportes
    document.getElementById('download-report-simple').addEventListener('click', function() {
      alert('En una aplicación funcional, aquí se descargaría el reporte PDF generado');
    });
    
    document.getElementById('download-report-desc').addEventListener('click', function() {
      alert('En una aplicación funcional, aquí se descargaría el reporte PDF generado');
    });
  </script>
</body>
</html>
