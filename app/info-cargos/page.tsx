import { Navbar } from "@/components/navbar"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"

export default function InfoCargosPage() {
  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />
      <main className="flex-1 container py-10">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold tracking-tighter mb-6">Información de Cargos</h1>

          <p className="text-muted-foreground mb-6">
            Conoce los diferentes cargos disponibles en la junta directiva capitular de ANEIAP, sus responsabilidades y
            requisitos.
          </p>

          <Tabs defaultValue="dca" className="w-full">
            <TabsList className="grid w-full grid-cols-2 sm:grid-cols-4 lg:grid-cols-8">
              <TabsTrigger value="dca">DCA</TabsTrigger>
              <TabsTrigger value="dcc">DCC</TabsTrigger>
              <TabsTrigger value="dcd">DCD</TabsTrigger>
              <TabsTrigger value="dcf">DCF</TabsTrigger>
              <TabsTrigger value="dcm">DCM</TabsTrigger>
              <TabsTrigger value="pc">PC</TabsTrigger>
              <TabsTrigger value="ccp">CCP</TabsTrigger>
              <TabsTrigger value="ic">IC</TabsTrigger>
            </TabsList>

            <TabsContent value="dca">
              <Card>
                <CardHeader>
                  <CardTitle>Director(a) Capitular Académico (DCA)</CardTitle>
                  <CardDescription>Lidera la gestión académica y formativa del capítulo</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <h3 className="font-bold text-lg text-primary mb-2">Áreas de responsabilidad:</h3>
                    <ul className="list-disc pl-5 space-y-1">
                      <li>Diseño académico y planificación de programas formativos</li>
                      <li>Innovación e investigación en metodologías educativas</li>
                      <li>Formación y capacitación de asociados</li>
                      <li>Gestión de recursos académicos y materiales didácticos</li>
                      <li>Evaluación y seguimiento del impacto formativo</li>
                    </ul>
                  </div>

                  <div>
                    <h3 className="font-bold text-lg text-primary mb-2">Competencias clave:</h3>
                    <ul className="list-disc pl-5 space-y-1">
                      <li>Capacidad pedagógica y diseño de programas educativos</li>
                      <li>Gestión de proyectos académicos y de investigación</li>
                      <li>Habilidades de comunicación y facilitación</li>
                      <li>Conocimiento en metodologías de enseñanza-aprendizaje</li>
                      <li>Planificación y organización de eventos académicos</li>
                    </ul>
                  </div>

                  <div>
                    <h3 className="font-bold text-lg text-primary mb-2">Consejos para el cargo:</h3>
                    <ul className="list-disc pl-5 space-y-1">
                      <li>Desarrolla capacidades pedagógicas para diseñar programas de formación académica</li>
                      <li>Domina herramientas de investigación para generar contenido relevante y actualizado</li>
                      <li>Fomenta la integración del entorno académico con los objetivos de ANEIAP</li>
                      <li>Aprende a coordinar eventos académicos de alto impacto como talleres y olimpiadas</li>
                      <li>Fortalece tus conocimientos en innovación educativa y herramientas tecnológicas</li>
                    </ul>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="dcc">
              <Card>
                <CardHeader>
                  <CardTitle>Director(a) Capitular de Comunicaciones (DCC)</CardTitle>
                  <CardDescription>Gestiona la estrategia comunicativa y la imagen del capítulo</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <h3 className="font-bold text-lg text-primary mb-2">Áreas de responsabilidad:</h3>
                    <ul className="list-disc pl-5 space-y-1">
                      <li>Estrategia de comunicación interna y externa</li>
                      <li>Producción audiovisual y gestión de contenidos</li>
                      <li>Gestión documental y archivo</li>
                      <li>Manejo de redes sociales y plataformas digitales</li>
                      <li>Desarrollo de campañas comunicativas</li>
                    </ul>
                  </div>

                  <div>
                    <h3 className="font-bold text-lg text-primary mb-2">Competencias clave:</h3>
                    <ul className="list-disc pl-5 space-y-1">
                      <li>Habilidades en diseño gráfico y producción multimedia</li>
                      <li>Gestión de redes sociales y marketing digital</li>
                      <li>Redacción y edición de contenidos</li>
                      <li>Planificación de campañas comunicativas</li>
                      <li>Manejo de herramientas de diseño y edición</li>
                    </ul>
                  </div>

                  <div>
                    <h3 className="font-bold text-lg text-primary mb-2">Consejos para el cargo:</h3>
                    <ul className="list-disc pl-5 space-y-1">
                      <li>
                        Aprende a diseñar estrategias de comunicación eficaces para captar la atención de asociados y
                        externos
                      </li>
                      <li>
                        Domina herramientas de diseño gráfico y edición audiovisual para generar contenido atractivo
                      </li>
                      <li>Fomenta la interacción digital mediante plataformas sociales y blogs</li>
                      <li>Desarrolla habilidades de redacción y storytelling para fortalecer la marca ANEIAP</li>
                      <li>Gestiona relaciones públicas para ampliar la visibilidad de los proyectos capitulares</li>
                    </ul>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="dcd">
              <Card>
                <CardHeader>
                  <CardTitle>Director(a) Capitular de Desarrollo (DCD)</CardTitle>
                  <CardDescription>Fortalece la integración y el impacto social del capítulo</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <h3 className="font-bold text-lg text-primary mb-2">Áreas de responsabilidad:</h3>
                    <ul className="list-disc pl-5 space-y-1">
                      <li>Gestión de asociados y procesos de reclutamiento</li>
                      <li>Integración y bienestar de los miembros</li>
                      <li>Sostenimiento y responsabilidad social</li>
                      <li>Organización de eventos de integración</li>
                      <li>Desarrollo de programas de retención</li>
                    </ul>
                  </div>

                  <div>
                    <h3 className="font-bold text-lg text-primary mb-2">Competencias clave:</h3>
                    <ul className="list-disc pl-5 space-y-1">
                      <li>Habilidades interpersonales y empatía</li>
                      <li>Gestión de clima organizacional</li>
                      <li>Planificación de eventos y actividades</li>
                      <li>Diseño de estrategias de retención</li>
                      <li>Responsabilidad social y ambiental</li>
                    </ul>
                  </div>

                  <div>
                    <h3 className="font-bold text-lg text-primary mb-2">Consejos para el cargo:</h3>
                    <ul className="list-disc pl-5 space-y-1">
                      <li>Fomenta la integración y permanencia de los asociados mediante eventos y actividades</li>
                      <li>Aprende a diseñar planes de reclutamiento y retención efectivos</li>
                      <li>Implementa sistemas de reconocimiento como incentivos y galas de premios</li>
                      <li>Domina las herramientas de gestión de clima organizacional</li>
                      <li>Fortalece tus habilidades en la organización de eventos de integración</li>
                    </ul>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="dcf">
              <Card>
                <CardHeader>
                  <CardTitle>Director(a) Capitular de Finanzas (DCF)</CardTitle>
                  <CardDescription>Administra los recursos económicos y la sostenibilidad financiera</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <h3 className="font-bold text-lg text-primary mb-2">Áreas de responsabilidad:</h3>
                    <ul className="list-disc pl-5 space-y-1">
                      <li>Gestión financiera y presupuestaria</li>
                      <li>Sostenibilidad económica y diversificación de ingresos</li>
                      <li>Análisis financiero y transparencia</li>
                      <li>Control de flujos de caja y tesorería</li>
                      <li>Elaboración de informes financieros</li>
                    </ul>
                  </div>

                  <div>
                    <h3 className="font-bold text-lg text-primary mb-2">Competencias clave:</h3>
                    <ul className="list-disc pl-5 space-y-1">
                      <li>Conocimientos contables y financieros</li>
                      <li>Planificación presupuestaria</li>
                      <li>Análisis de costos y proyecciones</li>
                      <li>Gestión de recursos económicos</li>
                      <li>Transparencia y ética financiera</li>
                    </ul>
                  </div>

                  <div>
                    <h3 className="font-bold text-lg text-primary mb-2">Consejos para el cargo:</h3>
                    <ul className="list-disc pl-5 space-y-1">
                      <li>Aprende a diseñar presupuestos y controlar el flujo de caja del capítulo</li>
                      <li>Domina la elaboración de informes financieros claros y precisos</li>
                      <li>Gestiona actividades de obtención de recursos de manera eficiente</li>
                      <li>Fortalece tus conocimientos en análisis financiero y proyecciones económicas</li>
                      <li>Implementa sistemas para la gestión de cuentas por pagar y cobrar</li>
                    </ul>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="dcm">
              <Card>
                <CardHeader>
                  <CardTitle>Director(a) Capitular de Mercadeo (DCM)</CardTitle>
                  <CardDescription>Gestiona la estrategia de marca y promoción del capítulo</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <h3 className="font-bold text-lg text-primary mb-2">Áreas de responsabilidad:</h3>
                    <ul className="list-disc pl-5 space-y-1">
                      <li>Estrategias de branding y posicionamiento</li>
                      <li>Promoción y visibilidad de actividades</li>
                      <li>Gestión comercial y alianzas estratégicas</li>
                      <li>Desarrollo de productos y servicios</li>
                      <li>Análisis de mercado y tendencias</li>
                    </ul>
                  </div>

                  <div>
                    <h3 className="font-bold text-lg text-primary mb-2">Competencias clave:</h3>
                    <ul className="list-disc pl-5 space-y-1">
                      <li>Creatividad y diseño de estrategias de marketing</li>
                      <li>Gestión de marca y posicionamiento</li>
                      <li>Análisis de mercado y segmentación</li>
                      <li>Planificación de campañas promocionales</li>
                      <li>Negociación y gestión de alianzas</li>
                    </ul>
                  </div>

                  <div>
                    <h3 className="font-bold text-lg text-primary mb-2">Consejos para el cargo:</h3>
                    <ul className="list-disc pl-5 space-y-1">
                      <li>Aprende a diseñar estrategias de branding para posicionar la marca ANEIAP</li>
                      <li>Domina herramientas de análisis de mercado para identificar necesidades de los asociados</li>
                      <li>Crea planes de fidelización para mantener asociados comprometidos</li>
                      <li>Implementa sistemas de CRM para gestionar relaciones con asociados y aliados</li>
                      <li>Fomenta la innovación en productos y servicios ofrecidos por el capítulo</li>
                    </ul>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="pc">
              <Card>
                <CardHeader>
                  <CardTitle>Presidencia Capitular (PC)</CardTitle>
                  <CardDescription>Lidera y representa al capítulo ante instancias internas y externas</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <h3 className="font-bold text-lg text-primary mb-2">Áreas de responsabilidad:</h3>
                    <ul className="list-disc pl-5 space-y-1">
                      <li>Liderazgo y estrategia organizacional</li>
                      <li>Gestión organizacional y administrativa</li>
                      <li>Relaciones y representación institucional</li>
                      <li>Toma de decisiones estratégicas</li>
                      <li>Coordinación de equipos directivos</li>
                    </ul>
                  </div>

                  <div>
                    <h3 className="font-bold text-lg text-primary mb-2">Competencias clave:</h3>
                    <ul className="list-disc pl-5 space-y-1">
                      <li>Liderazgo transformacional y adaptativo</li>
                      <li>Comunicación efectiva y asertiva</li>
                      <li>Pensamiento estratégico y visión global</li>
                      <li>Resolución de conflictos y negociación</li>
                      <li>Gestión del cambio y desarrollo organizacional</li>
                    </ul>
                  </div>

                  <div>
                    <h3 className="font-bold text-lg text-primary mb-2">Consejos para el cargo:</h3>
                    <ul className="list-disc pl-5 space-y-1">
                      <li>
                        Desarrolla habilidades intrapersonales como autogestión emocional y disciplina para liderar de
                        forma efectiva
                      </li>
                      <li>
                        Fomenta el liderazgo y la comunicación asertiva para relacionarte eficientemente con las
                        instancias internas y externas
                      </li>
                      <li>Conoce y comprende a fondo los procesos operativos y normativos de ANEIAP</li>
                      <li>
                        Fortalece tus habilidades en planeación estratégica para dirigir proyectos y alcanzar objetivos
                      </li>
                      <li>
                        Aprende a gestionar recursos de manera eficiente para asegurar la sostenibilidad del capítulo
                      </li>
                    </ul>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="ccp">
              <Card>
                <CardHeader>
                  <CardTitle>Coordinación Capitular de Proyectos (CCP)</CardTitle>
                  <CardDescription>Gestiona el desarrollo e implementación de proyectos del capítulo</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <h3 className="font-bold text-lg text-primary mb-2">Áreas de responsabilidad:</h3>
                    <ul className="list-disc pl-5 space-y-1">
                      <li>Gestión de proyectos y planificación</li>
                      <li>Innovación y creatividad en iniciativas</li>
                      <li>Colaboración estratégica con aliados</li>
                      <li>Seguimiento y evaluación de resultados</li>
                      <li>Formación de equipos multidisciplinarios</li>
                    </ul>
                  </div>

                  <div>
                    <h3 className="font-bold text-lg text-primary mb-2">Competencias clave:</h3>
                    <ul className="list-disc pl-5 space-y-1">
                      <li>Metodologías de gestión de proyectos</li>
                      <li>Pensamiento creativo y resolución de problemas</li>
                      <li>Trabajo en equipo y liderazgo colaborativo</li>
                      <li>Planificación y organización de recursos</li>
                      <li>Evaluación de riesgos y oportunidades</li>
                    </ul>
                  </div>

                  <div>
                    <h3 className="font-bold text-lg text-primary mb-2">Consejos para el cargo:</h3>
                    <ul className="list-disc pl-5 space-y-1">
                      <li>
                        Domina las metodologías de gestión de proyectos para asegurar la correcta ejecución de los
                        mismos
                      </li>
                      <li>Identifica y prioriza objetivos de innovación en los proyectos para aumentar su impacto</li>
                      <li>
                        Desarrolla habilidades en la formación de equipos multidisciplinarios para proyectos complejos
                      </li>
                      <li>Aprende a identificar y mitigar riesgos asociados a los proyectos</li>
                      <li>Fortalece la creación de alianzas estratégicas con patrocinadores y socios</li>
                    </ul>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="ic">
              <Card>
                <CardHeader>
                  <CardTitle>Interventoría Capitular (IC)</CardTitle>
                  <CardDescription>Supervisa y controla los procesos y la transparencia del capítulo</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <h3 className="font-bold text-lg text-primary mb-2">Áreas de responsabilidad:</h3>
                    <ul className="list-disc pl-5 space-y-1">
                      <li>Auditoría y control de procesos</li>
                      <li>Normativa y transparencia organizacional</li>
                      <li>Seguimiento y evaluación de proyectos</li>
                      <li>Verificación del cumplimiento de objetivos</li>
                      <li>Asesoría en temas normativos y procedimentales</li>
                    </ul>
                  </div>

                  <div>
                    <h3 className="font-bold text-lg text-primary mb-2">Competencias clave:</h3>
                    <ul className="list-disc pl-5 space-y-1">
                      <li>Conocimiento de normativas y procedimientos</li>
                      <li>Análisis crítico y objetivo</li>
                      <li>Ética y transparencia en la gestión</li>
                      <li>Habilidades de evaluación y seguimiento</li>
                      <li>Comunicación clara y asertiva</li>
                    </ul>
                  </div>

                  <div>
                    <h3 className="font-bold text-lg text-primary mb-2">Consejos para el cargo:</h3>
                    <ul className="list-disc pl-5 space-y-1">
                      <li>
                        Domina las funciones de veeduría, asesoría y control interno en los proyectos del capítulo
                      </li>
                      <li>Fortalece tu capacidad para analizar e interpretar normativas asociativas</li>
                      <li>Aprende a utilizar herramientas de auditoría y evaluación de proyectos</li>
                      <li>
                        Desarrolla habilidades para emitir conceptos imparciales y objetivos sobre situaciones complejas
                      </li>
                      <li>Fomenta la transparencia en todos los procesos de la asociación</li>
                    </ul>
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

