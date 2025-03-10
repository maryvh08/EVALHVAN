import { Navbar } from "@/components/navbar"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

export default function InfoIndicadoresPage() {
  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />
      <main className="flex-1 container py-10">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold tracking-tighter mb-6">Información de Indicadores</h1>

          <p className="text-muted-foreground mb-6">
            Conoce los indicadores utilizados para evaluar las hojas de vida y el desempeño de los candidatos según su
            cargo.
          </p>

          <Tabs defaultValue="pc" className="w-full">
            <TabsList className="grid w-full grid-cols-2 sm:grid-cols-4 lg:grid-cols-8">
              <TabsTrigger value="pc">PC</TabsTrigger>
              <TabsTrigger value="ccp">CCP</TabsTrigger>
              <TabsTrigger value="ic">IC</TabsTrigger>
              <TabsTrigger value="dca">DCA</TabsTrigger>
              <TabsTrigger value="dcc">DCC</TabsTrigger>
              <TabsTrigger value="dcd">DCD</TabsTrigger>
              <TabsTrigger value="dcf">DCF</TabsTrigger>
              <TabsTrigger value="dcm">DCM</TabsTrigger>
            </TabsList>

            <TabsContent value="pc">
              <Card>
                <CardHeader>
                  <CardTitle>Presidencia Capitular (PC)</CardTitle>
                  <CardDescription>Se enfoca en el liderazgo y la representación externa</CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="grid md:grid-cols-3 gap-6">
                    <div className="space-y-3">
                      <h3 className="font-bold text-lg text-primary">Liderazgo y estrategia</h3>
                      <p className="text-sm text-muted-foreground">
                        Enfocado en la capacidad del presidente para liderar con visión estratégica y dirigir al equipo
                        hacia objetivos claros.
                      </p>
                      <div className="mt-2">
                        <h4 className="font-semibold text-sm">Palabras clave:</h4>
                        <p className="text-xs text-muted-foreground">
                          Presidencia, Estrategia, Liderazgo, Rendimiento, Decisiones, Supervisión, Transformación,
                          Gestión del cambio, Comunicación efectiva, Delegación estratégica, Desarrollo de equipos,
                          Pensamiento crítico
                        </p>
                      </div>
                    </div>

                    <div className="space-y-3">
                      <h3 className="font-bold text-lg text-primary">Gestión organizacional</h3>
                      <p className="text-sm text-muted-foreground">
                        Relacionado con la administración eficiente de recursos, planeación de actividades y resolución
                        de conflictos internos.
                      </p>
                      <div className="mt-2">
                        <h4 className="font-semibold text-sm">Palabras clave:</h4>
                        <p className="text-xs text-muted-foreground">
                          Directiva, Capítulo, Junta, Gestión, Coordinación, Procesos operativos, Gestión de riesgos,
                          Metodologías ágiles, Control de calidad, Normativa interna, Protocolos, Organización interna
                        </p>
                      </div>
                    </div>

                    <div className="space-y-3">
                      <h3 className="font-bold text-lg text-primary">Relaciones y representación</h3>
                      <p className="text-sm text-muted-foreground">
                        Incluye la representación de la organización ante terceros, fortaleciendo alianzas y mejorando
                        la imagen del capítulo.
                      </p>
                      <div className="mt-2">
                        <h4 className="font-semibold text-sm">Palabras clave:</h4>
                        <p className="text-xs text-muted-foreground">
                          Representante, Negociaciones, Relaciones públicas, Diplomacia, Visitas institucionales,
                          Acuerdos estratégicos, Representatividad, Relaciones externas, Gestión de imagen, Networking
                          estratégico
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="border-t pt-4">
                    <h3 className="font-bold text-lg text-primary mb-3">Consejos para destacar en este cargo:</h3>
                    <ol className="list-decimal pl-5 space-y-1">
                      <li>
                        Desarrolla habilidades intrapersonales como autogestión emocional y disciplina para liderar de
                        forma efectiva.
                      </li>
                      <li>
                        Fomenta el liderazgo y la comunicación asertiva para relacionarte eficientemente con las
                        instancias internas y externas.
                      </li>
                      <li>Conoce y comprende a fondo los procesos operativos y normativos de ANEIAP.</li>
                      <li>
                        Fortalece tus habilidades en planeación estratégica para dirigir proyectos y alcanzar objetivos.
                      </li>
                      <li>
                        Aprende a gestionar recursos de manera eficiente para asegurar la sostenibilidad del capítulo.
                      </li>
                    </ol>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="ccp">
              <Card>
                <CardHeader>
                  <CardTitle>Coordinación de Proyectos (CCP)</CardTitle>
                  <CardDescription>Está más orientado a la gestión de proyectos y la innovación</CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="grid md:grid-cols-3 gap-6">
                    <div className="space-y-3">
                      <h3 className="font-bold text-lg text-primary">Gestión de proyectos</h3>
                      <p className="text-sm text-muted-foreground">
                        Habilidades necesarias para planificar, ejecutar, y evaluar proyectos en función de los
                        objetivos del capítulo.
                      </p>
                      <div className="mt-2">
                        <h4 className="font-semibold text-sm">Palabras clave:</h4>
                        <p className="text-xs text-muted-foreground">
                          Proyecto, Asesor, Sponsor, Equipo, Manager, Gestión, Vida, Viabilidad, Planificación,
                          Implementación, Cronogramas, Recursos humanos, Stakeholders, Gestión de alcance
                        </p>
                      </div>
                    </div>

                    <div className="space-y-3">
                      <h3 className="font-bold text-lg text-primary">Innovación y creatividad</h3>
                      <p className="text-sm text-muted-foreground">
                        Promueve el desarrollo de ideas novedosas que aumenten el impacto y la relevancia de los
                        proyectos.
                      </p>
                      <div className="mt-2">
                        <h4 className="font-semibold text-sm">Palabras clave:</h4>
                        <p className="text-xs text-muted-foreground">
                          Innovación, Cambio, Reforma, Estructura, Modelo, Pensamiento lateral, Proyectos disruptivos,
                          Design thinking, Innovación abierta, Modelos de negocio, Colaboración creativa
                        </p>
                      </div>
                    </div>

                    <div className="space-y-3">
                      <h3 className="font-bold text-lg text-primary">Colaboración estratégica</h3>
                      <p className="text-sm text-muted-foreground">
                        Capacidad para trabajar en equipo y establecer alianzas clave con otras organizaciones o
                        capítulos.
                      </p>
                      <div className="mt-2">
                        <h4 className="font-semibold text-sm">Palabras clave:</h4>
                        <p className="text-xs text-muted-foreground">
                          CNI, GNP, Directiva, ECP, PEN, COEC, Capítulo, Fraternidad, Organización, Asesoramiento,
                          Indicadores, Colaboración, Sinergias, Alianzas público-privadas, Networking estratégico
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="border-t pt-4">
                    <h3 className="font-bold text-lg text-primary mb-3">Consejos para destacar en este cargo:</h3>
                    <ol className="list-decimal pl-5 space-y-1">
                      <li>
                        Domina las metodologías de gestión de proyectos para asegurar la correcta ejecución de los
                        mismos.
                      </li>
                      <li>Identifica y prioriza objetivos de innovación en los proyectos para aumentar su impacto.</li>
                      <li>
                        Desarrolla habilidades en la formación de equipos multidisciplinarios para proyectos complejos.
                      </li>
                      <li>Aprende a identificar y mitigar riesgos asociados a los proyectos.</li>
                      <li>Fortalece la creación de alianzas estratégicas con patrocinadores y socios.</li>
                    </ol>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="ic">
              <Card>
                <CardHeader>
                  <CardTitle>Interventoría Capitular (IC)</CardTitle>
                  <CardDescription>Resalta la importancia del control y la transparencia</CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="grid md:grid-cols-3 gap-6">
                    <div className="space-y-3">
                      <h3 className="font-bold text-lg text-primary">Auditoría y control</h3>
                      <p className="text-sm text-muted-foreground">
                        Enfocado en la supervisión de los procesos y la evaluación del cumplimiento de normativas
                        internas.
                      </p>
                      <div className="mt-2">
                        <h4 className="font-semibold text-sm">Palabras clave:</h4>
                        <p className="text-xs text-muted-foreground">
                          Interventoría, Normativa, Auditor, Interventor, Datos, Análisis, Ética, Revisión, Evaluación
                          de riesgos, Verificación, Procedimientos internos, Informes de control
                        </p>
                      </div>
                    </div>

                    <div className="space-y-3">
                      <h3 className="font-bold text-lg text-primary">Normativa y transparencia</h3>
                      <p className="text-sm text-muted-foreground">
                        Relacionado con la interpretación de políticas asociativas y la promoción de una cultura de
                        honestidad.
                      </p>
                      <div className="mt-2">
                        <h4 className="font-semibold text-sm">Palabras clave:</h4>
                        <p className="text-xs text-muted-foreground">
                          Transparencia, Análisis financiero, Veeduría, Reglas de compliance, Código de conducta,
                          Reportes públicos, Declaraciones, Ética normativa, Controles regulatorios
                        </p>
                      </div>
                    </div>

                    <div className="space-y-3">
                      <h3 className="font-bold text-lg text-primary">Seguimiento y evaluación</h3>
                      <p className="text-sm text-muted-foreground">
                        Habilidades para medir el desempeño de proyectos y procesos, asegurando su alineación con los
                        objetivos.
                      </p>
                      <div className="mt-2">
                        <h4 className="font-semibold text-sm">Palabras clave:</h4>
                        <p className="text-xs text-muted-foreground">
                          ECI, Directiva, IC, ENI, Capítulo, Rúbrica, Indicadores de desempeño, Seguimiento, KPIs,
                          Cuadros de mando, Feedback, Informe ejecutivo, Panel de control
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="border-t pt-4">
                    <h3 className="font-bold text-lg text-primary mb-3">Consejos para destacar en este cargo:</h3>
                    <ol className="list-decimal pl-5 space-y-1">
                      <li>
                        Domina las funciones de veeduría, asesoría y control interno en los proyectos del capítulo.
                      </li>
                      <li>Fortalece tu capacidad para analizar e interpretar normativas asociativas.</li>
                      <li>Aprende a utilizar herramientas de auditoría y evaluación de proyectos.</li>
                      <li>
                        Desarrolla habilidades para emitir conceptos imparciales y objetivos sobre situaciones
                        complejas.
                      </li>
                      <li>Fomenta la transparencia en todos los procesos de la asociación.</li>
                    </ol>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="dca">
              <Card>
                <CardHeader>
                  <CardTitle>Director Capitular Académico (DCA)</CardTitle>
                  <CardDescription>Destaca el diseño académico y la innovación educativa</CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="grid md:grid-cols-3 gap-6">
                    <div className="space-y-3">
                      <h3 className="font-bold text-lg text-primary">Diseño académico</h3>
                      <p className="text-sm text-muted-foreground">
                        Desarrollo de actividades educativas como talleres y cursos, con un enfoque en la formación
                        integral.
                      </p>
                      <div className="mt-2">
                        <h4 className="font-semibold text-sm">Palabras clave:</h4>
                        <p className="text-xs text-muted-foreground">
                          Académico, Conocimiento, Integral, Directiva, Capítulo, Habilidades, Estructura curricular,
                          Evaluaciones, Planificación académica, Proyectos interdisciplinarios
                        </p>
                      </div>
                    </div>

                    <div className="space-y-3">
                      <h3 className="font-bold text-lg text-primary">Innovación e investigación</h3>
                      <p className="text-sm text-muted-foreground">
                        Capacidad para integrar herramientas y metodologías modernas para la enseñanza y el aprendizaje.
                      </p>
                      <div className="mt-2">
                        <h4 className="font-semibold text-sm">Palabras clave:</h4>
                        <p className="text-xs text-muted-foreground">
                          I+D+I, Consultoria, Entorno, Innovación, Mentoría, Ciclo, Innovación tecnológica,
                          Investigación aplicada, Startups, Colaboración académica, Transferencia de conocimiento
                        </p>
                      </div>
                    </div>

                    <div className="space-y-3">
                      <h3 className="font-bold text-lg text-primary">Formación y capacitación</h3>
                      <p className="text-sm text-muted-foreground">
                        Relacionado con la planificación y ejecución de programas para fortalecer habilidades técnicas y
                        blandas.
                      </p>
                      <div className="mt-2">
                        <h4 className="font-semibold text-sm">Palabras clave:</h4>
                        <p className="text-xs text-muted-foreground">
                          Formación, Escuela, Liderazgo, Olimpiadas, Taller, FIC, Ingeolimpiadas, Capacitación,
                          Seminario, Entrenamiento, Cursos, Profesional, Aplicado
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="border-t pt-4">
                    <h3 className="font-bold text-lg text-primary mb-3">Consejos para destacar en este cargo:</h3>
                    <ol className="list-decimal pl-5 space-y-1">
                      <li>Desarrolla capacidades pedagógicas para diseñar programas de formación académica.</li>
                      <li>Domina herramientas de investigación para generar contenido relevante y actualizado.</li>
                      <li>Fomenta la integración del entorno académico con los objetivos de ANEIAP.</li>
                      <li>Aprende a coordinar eventos académicos de alto impacto como talleres y olimpiadas.</li>
                      <li>Fortalece tus conocimientos en innovación educativa y herramientas tecnológicas.</li>
                    </ol>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="dcc">
              <Card>
                <CardHeader>
                  <CardTitle>Director Capitular de Comunicaciones (DCC)</CardTitle>
                  <CardDescription>
                    Se centra en las comunicaciones y la producción de contenido multimedia
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="grid md:grid-cols-3 gap-6">
                    <div className="space-y-3">
                      <h3 className="font-bold text-lg text-primary">Estrategia de comunicación</h3>
                      <p className="text-sm text-muted-foreground">
                        Planificación de campañas comunicativas que fortalezcan la presencia del capítulo en medios
                        internos y externos.
                      </p>
                      <div className="mt-2">
                        <h4 className="font-semibold text-sm">Palabras clave:</h4>
                        <p className="text-xs text-muted-foreground">
                          Comunicaciones, Publicidad, MIC, Directiva, Capítulo, Journal, Boletín, Digital, Medios,
                          Información, Campañas, Interacción, Promoción
                        </p>
                      </div>
                    </div>

                    <div className="space-y-3">
                      <h3 className="font-bold text-lg text-primary">Producción audiovisual</h3>
                      <p className="text-sm text-muted-foreground">
                        Desarrollo de piezas gráficas y contenido multimedia para captar la atención del público
                        objetivo.
                      </p>
                      <div className="mt-2">
                        <h4 className="font-semibold text-sm">Palabras clave:</h4>
                        <p className="text-xs text-muted-foreground">
                          Redes, Youtube, Podcast, Induspod, Web, Diseño, Contenido, IGTV, Piezas, Tiktok, Audiovisual,
                          Diseño gráfico, Producción, Animaciones
                        </p>
                      </div>
                    </div>

                    <div className="space-y-3">
                      <h3 className="font-bold text-lg text-primary">Gestión documental</h3>
                      <p className="text-sm text-muted-foreground">
                        Competencias relacionadas con el manejo, organización y administración de documentos e
                        información.
                      </p>
                      <div className="mt-2">
                        <h4 className="font-semibold text-sm">Palabras clave:</h4>
                        <p className="text-xs text-muted-foreground">
                          Data, Documental, Biblioteca, Escuela, Documentación, Archivos digitales, Preservación de
                          datos, Control de versiones, Análisis documental, Metadatos
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="border-t pt-4">
                    <h3 className="font-bold text-lg text-primary mb-3">Consejos para destacar en este cargo:</h3>
                    <ol className="list-decimal pl-5 space-y-1">
                      <li>
                        Aprende a diseñar estrategias de comunicación eficaces para captar la atención de asociados y
                        externos.
                      </li>
                      <li>
                        Domina herramientas de diseño gráfico y edición audiovisual para generar contenido atractivo.
                      </li>
                      <li>Fomenta la interacción digital mediante plataformas sociales y blogs.</li>
                      <li>Desarrolla habilidades de redacción y storytelling para fortalecer la marca ANEIAP.</li>
                      <li>Gestiona relaciones públicas para ampliar la visibilidad de los proyectos capitulares.</li>
                    </ol>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="dcd">
              <Card>
                <CardHeader>
                  <CardTitle>Director Capitular de Desarrollo (DCD)</CardTitle>
                  <CardDescription>Fortalece la integración y el impacto social</CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="grid md:grid-cols-3 gap-6">
                    <div className="space-y-3">
                      <h3 className="font-bold text-lg text-primary">Gestión de asociados</h3>
                      <p className="text-sm text-muted-foreground">
                        Enfoque en la retención y reclutamiento de nuevos miembros, fomentando su compromiso con el
                        capítulo.
                      </p>
                      <div className="mt-2">
                        <h4 className="font-semibold text-sm">Palabras clave:</h4>
                        <p className="text-xs text-muted-foreground">
                          Desarrollo, Directiva, Capítulo, Expansión, Cultura, Reclutamiento, SÉ, SRA, Insignia,
                          Gestión, Equipos, Contacto, Retención, Inclusión
                        </p>
                      </div>
                    </div>

                    <div className="space-y-3">
                      <h3 className="font-bold text-lg text-primary">Integración y bienestar</h3>
                      <p className="text-sm text-muted-foreground">
                        Relacionado con la organización de actividades que promueven la cohesión y el bienestar del
                        grupo.
                      </p>
                      <div className="mt-2">
                        <h4 className="font-semibold text-sm">Palabras clave:</h4>
                        <p className="text-xs text-muted-foreground">
                          Relaciones, Gala, Integraciones, Premios, Cohesión, Personal, Interpersonal, Diversidad,
                          Inclusión social, Clima organizacional, Teambuilding
                        </p>
                      </div>
                    </div>

                    <div className="space-y-3">
                      <h3 className="font-bold text-lg text-primary">Sostenimiento y sociedad</h3>
                      <p className="text-sm text-muted-foreground">
                        Promoción de valores sociales a través de proyectos de responsabilidad comunitaria.
                      </p>
                      <div className="mt-2">
                        <h4 className="font-semibold text-sm">Palabras clave:</h4>
                        <p className="text-xs text-muted-foreground">
                          Responsabilidad, RSA, Social, Ambiental, Comunitario, Impacto social, Proyectos comunitarios,
                          Responsabilidad ambiental, Conciencia social
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="border-t pt-4">
                    <h3 className="font-bold text-lg text-primary mb-3">Consejos para destacar en este cargo:</h3>
                    <ol className="list-decimal pl-5 space-y-1">
                      <li>Fomenta la integración y permanencia de los asociados mediante eventos y actividades.</li>
                      <li>Aprende a diseñar planes de reclutamiento y retención efectivos.</li>
                      <li>Implementa sistemas de reconocimiento como incentivos y galas de premios.</li>
                      <li>Domina las herramientas de gestión de clima organizacional.</li>
                      <li>Fortalece tus habilidades en la organización de eventos de integración.</li>
                    </ol>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="dcf">
              <Card>
                <CardHeader>
                  <CardTitle>Director Capitular de Finanzas (DCF)</CardTitle>
                  <CardDescription>Prioriza la estabilidad económica y la transparencia</CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="grid md:grid-cols-3 gap-6">
                    <div className="space-y-3">
                      <h3 className="font-bold text-lg text-primary">Gestión financiera</h3>
                      <p className="text-sm text-muted-foreground">
                        Administración eficiente de recursos, creación de presupuestos y control de gastos del capítulo.
                      </p>
                      <div className="mt-2">
                        <h4 className="font-semibold text-sm">Palabras clave:</h4>
                        <p className="text-xs text-muted-foreground">
                          Finanzas, Financiero, Recursos, Fondos, Fuente, Gestión, Egreso, Ingreso, Ahorro, Dashboard,
                          Sustentable, Balance general
                        </p>
                      </div>
                    </div>

                    <div className="space-y-3">
                      <h3 className="font-bold text-lg text-primary">Sostenibilidad económica</h3>
                      <p className="text-sm text-muted-foreground">
                        Implementación de estrategias para diversificar ingresos y garantizar la estabilidad financiera.
                      </p>
                      <div className="mt-2">
                        <h4 className="font-semibold text-sm">Palabras clave:</h4>
                        <p className="text-xs text-muted-foreground">
                          Riqueza, Sostenibilidad, Obtención, Recaudación, Sostenimiento, Económica, Rentabilidad,
                          Proyectos rentables, Estrategia económica
                        </p>
                      </div>
                    </div>

                    <div className="space-y-3">
                      <h3 className="font-bold text-lg text-primary">Análisis y transparencia</h3>
                      <p className="text-sm text-muted-foreground">
                        Evaluación de informes financieros y promoción de prácticas transparentes en la gestión
                        económica.
                      </p>
                      <div className="mt-2">
                        <h4 className="font-semibold text-sm">Palabras clave:</h4>
                        <p className="text-xs text-muted-foreground">
                          Directiva, Capítulo, Donaciones, Ética financiera, Cumplimiento normativo, Indicadores clave,
                          Informes de impacto, Controles internos
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="border-t pt-4">
                    <h3 className="font-bold text-lg text-primary mb-3">Consejos para destacar en este cargo:</h3>
                    <ol className="list-decimal pl-5 space-y-1">
                      <li>Aprende a diseñar presupuestos y controlar el flujo de caja del capítulo.</li>
                      <li>Domina la elaboración de informes financieros claros y precisos.</li>
                      <li>Gestiona actividades de obtención de recursos de manera eficiente.</li>
                      <li>Fortalece tus conocimientos en análisis financiero y proyecciones económicas.</li>
                      <li>Implementa sistemas para la gestión de cuentas por pagar y cobrar.</li>
                    </ol>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="dcm">
              <Card>
                <CardHeader>
                  <CardTitle>Director Capitular de Mercadeo (DCM)</CardTitle>
                  <CardDescription>Enfatiza el branding y la comercialización</CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  <div className="grid md:grid-cols-3 gap-6">
                    <div className="space-y-3">
                      <h3 className="font-bold text-lg text-primary">Estrategias de branding</h3>
                      <p className="text-sm text-muted-foreground">
                        Creación de una identidad sólida para el capítulo que lo diferencie y lo haga atractivo.
                      </p>
                      <div className="mt-2">
                        <h4 className="font-semibold text-sm">Palabras clave:</h4>
                        <p className="text-xs text-muted-foreground">
                          Mercadeo, Branding, Negocio, Posicionamiento, Promoción, Plan, Campaña, Identidad corporativa,
                          Rebranding, Estrategia de marca
                        </p>
                      </div>
                    </div>

                    <div className="space-y-3">
                      <h3 className="font-bold text-lg text-primary">Promoción y visibilidad</h3>
                      <p className="text-sm text-muted-foreground">
                        Diseño de campañas que aumenten el alcance y la participación en las actividades del capítulo.
                      </p>
                      <div className="mt-2">
                        <h4 className="font-semibold text-sm">Palabras clave:</h4>
                        <p className="text-xs text-muted-foreground">
                          Buzón, Directiva, Capítulo, ANEIAPDAY, Relaciones, Visibilidad, Identidad, Visualización,
                          Estrategias promocionales, Publicidad segmentada
                        </p>
                      </div>
                    </div>

                    <div className="space-y-3">
                      <h3 className="font-bold text-lg text-primary">Gestión comercial</h3>
                      <p className="text-sm text-muted-foreground">
                        Administración de productos y alianzas estratégicas para generar ingresos y fortalecer la marca.
                      </p>
                      <div className="mt-2">
                        <h4 className="font-semibold text-sm">Palabras clave:</h4>
                        <p className="text-xs text-muted-foreground">
                          Tienda, Públicas, Cliente, Externo, Interno, Modelo, Servicio, Venta, Comercial, Propuestas de
                          valor, E-commerce, Negociación comercial
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="border-t pt-4">
                    <h3 className="font-bold text-lg text-primary mb-3">Consejos para destacar en este cargo:</h3>
                    <ol className="list-decimal pl-5 space-y-1">
                      <li>Aprende a diseñar estrategias de branding para posicionar la marca ANEIAP.</li>
                      <li>Domina herramientas de análisis de mercado para identificar necesidades de los asociados.</li>
                      <li>Crea planes de fidelización para mantener asociados comprometidos.</li>
                      <li>Implementa sistemas de CRM para gestionar relaciones con asociados y aliados.</li>
                      <li>Fomenta la innovación en productos y servicios ofrecidos por el capítulo.</li>
                    </ol>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      </main>
    </div>
  )
}

