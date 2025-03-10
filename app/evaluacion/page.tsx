import Link from "next/link"
import Image from "next/image"
import { Search } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Navbar } from "@/components/navbar"

export default function EvaluacionPage() {
  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />
      <main className="flex-1 container py-10">
        <div className="flex flex-col gap-6">
          <h1 className="text-3xl font-bold tracking-tighter">
            <Search className="inline-block mr-2 h-6 w-6" />
            Selecciona el tipo de evaluación de Hoja de Vida
          </h1>

          <Tabs defaultValue="simplificada" className="w-full">
            <TabsList className="grid w-full grid-cols-2">
              <TabsTrigger value="simplificada">Versión Simplificada</TabsTrigger>
              <TabsTrigger value="descriptiva">Versión Descriptiva</TabsTrigger>
            </TabsList>
            <TabsContent value="simplificada">
              <Card>
                <CardHeader>
                  <CardTitle>Versión Simplificada</CardTitle>
                  <CardDescription>
                    Esta versión analiza la hoja de vida de forma mucho más rápida evaluando cada una de las
                    experiencias como listado.
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex flex-col md:flex-row items-start md:items-center gap-4">
                    <div className="relative h-32 w-32 shrink-0 overflow-hidden rounded-xl">
                      <Image
                        src="/placeholder.svg?height=128&width=128"
                        alt="Ejemplo de formato simplificado"
                        width={128}
                        height={128}
                        className="aspect-square object-cover"
                      />
                    </div>
                    <div className="space-y-2">
                      <h3 className="font-semibold">Recomendaciones a tener en cuenta ✅</h3>
                      <ul className="list-disc pl-5 space-y-1 text-sm">
                        <li>
                          Es preferible que la HV no haya sido cambiada de formato varias veces, ya que puede complicar
                          la lectura y extracción del texto.
                        </li>
                        <li>La EXPERIENCIA EN ANEIAP debe estar enumerada para facilitar el análisis de la misma.</li>
                        <li>
                          El análisis puede presentar inconsistencias si la HV no está debidamente separada en
                          subtítulos.
                        </li>
                        <li>
                          Si la sección de EXPERIENCIA EN ANEIAP está dispuesta como tabla, la herramienta puede fallar.
                        </li>
                      </ul>
                    </div>
                  </div>
                </CardContent>
                <CardFooter>
                  <Button asChild className="w-full">
                    <Link href="/evaluacion/simplificada">Ir a Evaluador Simplificado</Link>
                  </Button>
                </CardFooter>
              </Card>
            </TabsContent>
            <TabsContent value="descriptiva">
              <Card>
                <CardHeader>
                  <CardTitle>Versión Descriptiva</CardTitle>
                  <CardDescription>
                    Esta versión es más cercana al entorno profesional permitiendo analizar la descripción de cada una
                    de las experiencias de la hoja de vida.
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex flex-col md:flex-row items-start md:items-center gap-4">
                    <div className="relative h-32 w-32 shrink-0 overflow-hidden rounded-xl">
                      <Image
                        src="/placeholder.svg?height=128&width=128"
                        alt="Ejemplo de formato descriptivo"
                        width={128}
                        height={128}
                        className="aspect-square object-cover"
                      />
                    </div>
                    <div className="space-y-2">
                      <h3 className="font-semibold">Recomendaciones a tener en cuenta ✅</h3>
                      <ul className="list-disc pl-5 space-y-1 text-sm">
                        <li>
                          Organiza la HV en formato <span className="font-bold text-primary">descriptivo</span> para
                          cada cargo o proyecto.
                        </li>
                        <li>
                          Utiliza <span className="font-bold">negrita</span> para identificar la experiencia.
                        </li>
                        <li>
                          Usa <span className="font-bold">guiones</span> para detallar las acciones realizadas en cada
                          ítem.
                        </li>
                        <li>
                          Evita usar tablas para la sección de experiencia, ya que esto dificulta la extracción de
                          datos.
                        </li>
                      </ul>
                    </div>
                  </div>
                </CardContent>
                <CardFooter>
                  <Button asChild className="w-full">
                    <Link href="/evaluacion/descriptiva">Ir a Evaluador Descriptivo</Link>
                  </Button>
                </CardFooter>
              </Card>
            </TabsContent>
          </Tabs>
        </div>
      </main>
    </div>
  )
}

