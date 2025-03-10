import type React from "react"
import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "./globals.css"
import { ThemeProvider } from "@/components/theme-provider"
import { Footer } from "@/components/footer"

const inter = Inter({ subsets: ["latin"], variable: "--font-sans" })

export const metadata: Metadata = {
  title: "EvalHVAN - Sistema de Gestión de Talento ANEIAP",
  description: "Plataforma para la evaluación de hojas de vida y gestión de procesos de selección de ANEIAP",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="es" suppressHydrationWarning>
      <body className={`${inter.variable} font-sans flex flex-col min-h-screen`}>
        <ThemeProvider attribute="class" defaultTheme="light" storageKey="evalhvan-theme">
          <div className="flex-1 flex flex-col">{children}</div>
          <Footer />
        </ThemeProvider>
      </body>
    </html>
  )
}

