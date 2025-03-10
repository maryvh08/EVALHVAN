"use client"

import Link from "next/link"
import Image from "next/image"
import { usePathname } from "next/navigation"
import { FileText, Home, Upload, Settings, Users, Menu } from "lucide-react"

import { cn } from "@/lib/utils"
import { ModeToggle } from "@/components/mode-toggle"
import { Button } from "@/components/ui/button"
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"

export function Navbar() {
  const pathname = usePathname()

  const routes = [
    {
      href: "/",
      label: "Inicio",
      icon: Home,
      active: pathname === "/",
    },
    {
      href: "/evaluacion",
      label: "Evaluación",
      icon: FileText,
      active: pathname === "/evaluacion" || pathname.startsWith("/evaluacion/"),
    },
    {
      href: "/subir-hv",
      label: "Plantilla HV",
      icon: Upload,
      active: pathname === "/subir-hv",
    },
    {
      href: "/info-cargos",
      label: "Info Cargos",
      icon: Users,
      active: pathname === "/info-cargos",
    },
    {
      href: "/info-indicadores",
      label: "Info Indicadores",
      icon: Settings,
      active: pathname === "/info-indicadores",
    },
  ]

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between">
        <div className="flex items-center gap-2">
          <Link href="/" className="flex items-center gap-2">
            <div className="relative h-8 w-8 sm:h-10 sm:w-36">
              <Image
                src="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/ISOLOGO%20C%20A%20COLOR-ZMU3GLlzToBZNRmZzvuQ1AdYeuwVuR.png"
                alt="ANEIAP Logo"
                fill
                className="object-contain dark:hidden"
              />
              <Image
                src="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/ISOLOGO%20C%20BLANCO-gt7UBVFzSA2IkpxwrYmbFRR4NGuOnc.png"
                alt="ANEIAP Logo"
                fill
                className="object-contain hidden dark:block"
              />
            </div>
            <span className="text-xl font-bold hidden sm:inline-block">EvalHVAN</span>
          </Link>
        </div>

        {/* Navegación para pantallas medianas y grandes */}
        <nav className="hidden md:flex items-center gap-6">
          {routes.map((route) => (
            <Link
              key={route.href}
              href={route.href}
              className={cn(
                "text-sm font-medium transition-colors hover:text-primary flex items-center gap-1",
                route.active ? "text-primary" : "text-muted-foreground",
              )}
            >
              <route.icon className="h-4 w-4" />
              {route.label}
            </Link>
          ))}
        </nav>

        <div className="flex items-center gap-2">
          <ModeToggle />
          <Button asChild variant="default" size="sm" className="hidden sm:flex">
            <Link href="/evaluacion">Evaluar HV</Link>
          </Button>

          {/* Menú móvil */}
          <Sheet>
            <SheetTrigger asChild>
              <Button variant="outline" size="icon" className="md:hidden">
                <Menu className="h-5 w-5" />
                <span className="sr-only">Menú</span>
              </Button>
            </SheetTrigger>
            <SheetContent side="right" className="w-[80%] sm:w-[385px]">
              <nav className="flex flex-col gap-4 mt-8">
                {routes.map((route) => (
                  <Link
                    key={route.href}
                    href={route.href}
                    className={cn(
                      "text-base font-medium transition-colors hover:text-primary flex items-center gap-2 p-2 rounded-md",
                      route.active ? "bg-muted text-primary" : "text-muted-foreground",
                    )}
                  >
                    <route.icon className="h-5 w-5" />
                    {route.label}
                  </Link>
                ))}
                <Button asChild className="mt-4">
                  <Link href="/evaluacion">Evaluar Hoja de Vida</Link>
                </Button>
              </nav>
            </SheetContent>
          </Sheet>
        </div>
      </div>
    </header>
  )
}

