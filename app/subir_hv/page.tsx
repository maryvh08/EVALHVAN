import Link from "next/link"
import Image from "next/image"
import { Download, FileText } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Navbar } from "@/components/navbar"

export default function SubirHVPage() {
  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />
      <main className="flex-1 container py-10">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold tracking-tighter mb-6">Plantilla HV ANEIAP</h1>

          <Card className="mb-8">
            <CardHeader>
              <CardTitle>Formato Oficial de Hoja de Vida ANEIAP</CardTitle>
              <CardDescription>
                Descarga el formato oficial para presentar tu hoja de vida en los procesos de selección
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid md:grid-cols-2 gap-6">
                <div className="relative h-[400px] w-full rounded-xl overflow-hidden border">
                  <Image
                    src="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/PLANTILLA%20PROPUESTA%20HV%20ANEIAP.jpg-bMoeT4834N4HRAxnIiPM3U3VdDZnaq.jpeg"
                    alt="Plantilla de Hoja de Vida ANEIAP"
                    fill
                    className="object-contain"
                  />
                </div>
                <div className="space-y-4">
                  <h3 className="text-xl font-bold">Instrucciones de uso</h3>
                  <p className="text-muted-foreground">
                    Esta plantilla está diseñada para estandarizar la presentación de información en los procesos de
                    selección de ANEIAP. Asegúrate de completar todas las secciones relevantes:
                  </p>
                  <ul className="list-disc pl-5 space-y-2">
                    <li>
                      <span className="font-semibold">Perfil:</span> Breve descripción de tus habilidades y
                      aspiraciones.
                    </li>
                    <li>
                      <span className="font-semibold">Estudios Realizados:</span> Formación académica formal.
                    </li>
                    <li>
                      <span className="font-semibold">Asistencia a Eventos ANEIAP:</span> Participación en eventos de la
                      asociación.
                    </li>
                    <li>
                      <span className="font-semibold">Actualización Profesional:</span> Cursos, certificaciones y
                      formación complementaria.
                    </li>
                    <li>
                      <span className="font-semibold">Experiencia en ANEIAP:</span> Detalle de cargos y
                      responsabilidades dentro de la asociación.
                    </li>
                    <li>
                      <span className="font-semibold">Reconocimientos:</span> Logros y distinciones recibidas.
                    </li>
                    <li>
                      <span className="font-semibold">Eventos Organizados:</span> Participación en la organización de
                      eventos.
                    </li>
                  </ul>
                </div>
              </div>

              <div className="mt-6 border-t pt-6">
                <h3 className="text-xl font-bold mb-4">Recomendaciones para completar tu HV</h3>
                <div className="grid md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <h4 className="font-semibold">Para evaluación simplificada:</h4>
                    <ul className="list-disc pl-5 space-y-1 text-sm">
                      <li>Mantén el formato original sin modificaciones.</li>
                      <li>Enumera claramente tu experiencia en ANEIAP.</li>
                      <li>Separa adecuadamente las secciones con subtítulos.</li>
                      <li>Evita usar tablas para la sección de experiencia.</li>
                    </ul>
                  </div>
                  <div className="space-y-2">
                    <h4 className="font-semibold">Para evaluación descriptiva:</h4>
                    <ul className="list-disc pl-5 space-y-1 text-sm">
                      <li>Organiza la HV en formato descriptivo para cada cargo.</li>
                      <li>Utiliza negrita para identificar la experiencia.</li>
                      <li>Usa guiones para detallar las acciones realizadas.</li>
                      <li>Incluye métricas o resultados cuando sea posible.</li>
                    </ul>
                  </div>
                </div>
              </div>
            </CardContent>
            <CardFooter className="flex justify-center">
              <Button className="w-full md:w-auto" asChild>
                <a
                  href="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/plantilla-hv-aneiap-2025.docx"
                  download
                >
                  <Download className="mr-2 h-4 w-4" />
                  Descargar Plantilla
                </a>
              </Button>
            </CardFooter>
          </Card>

          <div className="flex justify-center gap-4">
            <Button asChild variant="outline">
              <Link href="/evaluacion">
                <FileText className="mr-2 h-4 w-4" />
                Ir a Evaluación
              </Link>
            </Button>
            <Button asChild variant="secondary">
              <Link href="/">Volver al Inicio</Link>
            </Button>
          </div>
        </div>
      </main>
    </div>
  )
}

