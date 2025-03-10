"use client"

import type React from "react"

import { useState } from "react"
import { FileUp, Upload } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Navbar } from "@/components/navbar"

export default function EvaluacionDescriptivaPage() {
  const [fileName, setFileName] = useState<string>("")
  const [isUploading, setIsUploading] = useState<boolean>(false)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFileName(e.target.files[0].name)
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setIsUploading(true)

    // Simulación de carga
    setTimeout(() => {
      setIsUploading(false)
      // Aquí iría la lógica para generar el reporte
    }, 2000)
  }

  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />
      <main className="flex-1 container py-10">
        <div className="max-w-2xl mx-auto">
          <Card>
            <CardHeader>
              <CardTitle className="text-2xl">Evaluador Descriptivo</CardTitle>
              <CardDescription>
                Sube la hoja de vida en formato PDF para realizar la evaluación descriptiva detallada
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="space-y-2">
                  <label htmlFor="nombre" className="text-sm font-medium">
                    Nombre del candidato:
                  </label>
                  <Input id="nombre" placeholder="Ingrese el nombre completo" required />
                </div>

                <div className="space-y-2">
                  <label className="text-sm font-medium">Sube tu hoja de vida ANEIAP en formato PDF</label>
                  <div className="border-2 border-dashed rounded-lg p-6 flex flex-col items-center justify-center bg-muted/50">
                    <div className="flex flex-col items-center justify-center gap-2">
                      <FileUp className="h-10 w-10 text-muted-foreground" />
                      <p className="text-sm text-muted-foreground">Drag and drop file here</p>
                      <p className="text-xs text-muted-foreground">Limit 20MB por file • PDF</p>
                      {fileName && <p className="text-sm font-medium text-primary mt-2">{fileName}</p>}
                    </div>
                    <Input
                      id="file-upload"
                      type="file"
                      accept=".pdf"
                      className="hidden"
                      onChange={handleFileChange}
                      required
                    />
                    <Button
                      type="button"
                      variant="outline"
                      size="sm"
                      className="mt-4"
                      onClick={() => document.getElementById("file-upload")?.click()}
                    >
                      Browse files
                    </Button>
                  </div>
                </div>

                <div className="space-y-2">
                  <label htmlFor="cargo" className="text-sm font-medium">
                    Selecciona el cargo al que aspiras:
                  </label>
                  <Select required>
                    <SelectTrigger>
                      <SelectValue placeholder="Selecciona un cargo" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="dca">DCA</SelectItem>
                      <SelectItem value="dcc">DCC</SelectItem>
                      <SelectItem value="dcd">DCD</SelectItem>
                      <SelectItem value="dcf">DCF</SelectItem>
                      <SelectItem value="dcm">DCM</SelectItem>
                      <SelectItem value="pc">PC</SelectItem>
                      <SelectItem value="ccp">CCP</SelectItem>
                      <SelectItem value="ic">IC</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <label htmlFor="capitulo" className="text-sm font-medium">
                    Selecciona el Capítulo al que perteneces:
                  </label>
                  <Select required>
                    <SelectTrigger>
                      <SelectValue placeholder="Selecciona un capítulo" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="uniguajira">UNIGUAJIRA</SelectItem>
                      <SelectItem value="unimagdalena">UNIMAGDALENA</SelectItem>
                      <SelectItem value="uninorte">UNINORTE</SelectItem>
                      <SelectItem value="uniatlantico">UNIATLÁNTICO</SelectItem>
                      <SelectItem value="cuc">CUC</SelectItem>
                      <SelectItem value="unisimon">UNISIMÓN</SelectItem>
                      <SelectItem value="librequilla">LIBREQUILLA</SelectItem>
                      <SelectItem value="utb">UTB</SelectItem>
                      <SelectItem value="ufps">UFPS</SelectItem>
                      <SelectItem value="unalmed">UNALMED</SelectItem>
                      <SelectItem value="upbmed">UPBMED</SelectItem>
                      <SelectItem value="udea">UDEA</SelectItem>
                      <SelectItem value="utp">UTP</SelectItem>
                      <SelectItem value="unalma">UNALMA</SelectItem>
                      <SelectItem value="librecali">LIBRECALI</SelectItem>
                      <SelectItem value="univalle">UNIVALLE</SelectItem>
                      <SelectItem value="icesi">ICESI</SelectItem>
                      <SelectItem value="usc">USC</SelectItem>
                      <SelectItem value="udistrital">UDISTRITAL</SelectItem>
                      <SelectItem value="unalbog">UNALBOG</SelectItem>
                      <SelectItem value="upbmonteria">UPBMONTERÍA</SelectItem>
                      <SelectItem value="areandina">AREANDINA</SelectItem>
                      <SelectItem value="unicordoba">UNICÓRDOBA</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </form>
            </CardContent>
            <CardFooter>
              <Button type="submit" className="w-full" disabled={isUploading || !fileName} onClick={handleSubmit}>
                {isUploading ? (
                  <>
                    <Upload className="mr-2 h-4 w-4 animate-spin" />
                    Procesando...
                  </>
                ) : (
                  "Generar Reporte PDF"
                )}
              </Button>
            </CardFooter>
          </Card>
        </div>
      </main>
    </div>
  )
}

