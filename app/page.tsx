import Link from "next/link"
import { Download, FileText, Search, Settings } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Navbar } from "@/components/navbar"

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />
      <main className="flex-1">
        <section className="w-full py-12 md:py-24 lg:py-32 bg-gradient-to-b from-background to-muted">
          <div className="container px-4 md:px-6">
            <div className="grid gap-6 lg:grid-cols-[1fr_400px] lg:gap-12 xl:grid-cols-[1fr_600px]">
              <div className="flex flex-col justify-center space-y-4">
                <div className="space-y-2">
                  <h1 className="text-3xl font-bold tracking-tighter sm:text-5xl xl:text-6xl/none">
                    Bienvenido a EvalHVAN
                  </h1>
                  <p className="max-w-[600px] text-muted-foreground md:text-xl">
                    ¿Qué tan listo estás para asumir un cargo de junta directiva Capitular? Descúbrelo aquí ⚙️
                  </p>
                </div>
                <div className="flex flex-col gap-2 min-[400px]:flex-row">
                  <Button asChild size="lg">
                    <Link href="/evaluacion">
                      <FileText className="mr-2 h-4 w-4" />
                      Evaluar Hoja de Vida
                    </Link>
                  </Button>
                  <Button asChild variant="outline" size="lg">
                    <Link href="/subir-hv">
                      <Download className="mr-2 h-4 w-4" />
                      Descargar Formato HV
                    </Link>
                  </Button>
                </div>
              </div>
              <div className="flex items-center justify-center">
                <Card className="w-full max-w-md">
                  <CardHeader>
                    <CardTitle className="text-2xl">Evaluador de Hoja de Vida ANEIAP</CardTitle>
                    <CardDescription>Herramienta para análisis de hojas de vida</CardDescription>
                  </CardHeader>
                  <CardContent className="grid gap-4">
                    <div className="flex items-center gap-4">
                      <div className="relative h-20 w-20 shrink-0 overflow-hidden rounded-xl flex items-center justify-center bg-muted">
                        <Settings className="h-10 w-10 text-primary" />
                      </div>
                      <div className="grid gap-1">
                        <h3 className="font-semibold">EvalHVAN</h3>
                        <p className="text-sm text-muted-foreground">
                          Esta herramienta analiza el contenido de la hoja de vida ANEIAP, comparándola con las
                          funciones y perfil del cargo al que aspira.
                        </p>
                      </div>
                    </div>
                  </CardContent>
                  <CardFooter>
                    <Button asChild className="w-full">
                      <Link href="/evaluacion">
                        <Search className="mr-2 h-4 w-4" />
                        Comenzar Evaluación
                      </Link>
                    </Button>
                  </CardFooter>
                </Card>
              </div>
            </div>
          </div>
        </section>
        <section className="w-full py-12 md:py-24 lg:py-32 bg-background">
          <div className="container px-4 md:px-6">
            <div className="mx-auto grid max-w-5xl items-center gap-6 py-12 lg:grid-cols-2 lg:gap-12">
              <div className="space-y-4">
                <div className="inline-block rounded-lg bg-secondary px-3 py-1 text-sm">Beneficios Clave</div>
                <h2 className="text-3xl font-bold tracking-tighter md:text-4xl/tight">
                  Optimiza el proceso de selección
                </h2>
                <p className="max-w-[600px] text-muted-foreground md:text-xl/relaxed lg:text-base/relaxed xl:text-xl/relaxed">
                  EvalHVAN te permite evaluar candidatos de manera eficiente y estandarizada, asegurando que los mejores
                  talentos sean seleccionados.
                </p>
              </div>
              <div className="grid gap-6">
                <div className="grid gap-1">
                  <h3 className="text-xl font-bold">Optimización del Reclutamiento</h3>
                  <p className="text-muted-foreground">Proceso digitalizado y eficiente para evaluar postulantes.</p>
                </div>
                <div className="grid gap-1">
                  <h3 className="text-xl font-bold">Centralización de Datos</h3>
                  <p className="text-muted-foreground">
                    Acceso organizado a perfiles de candidatos y procesos en curso.
                  </p>
                </div>
                <div className="grid gap-1">
                  <h3 className="text-xl font-bold">Evaluaciones Estandarizadas</h3>
                  <p className="text-muted-foreground">
                    Formatos predefinidos para evaluar competencias y habilidades.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  )
}

