import Link from "next/link"
import { Facebook, Instagram, Globe } from "lucide-react"

export function Footer() {
  return (
    <footer className="border-t py-6">
      <div className="container flex flex-col items-center justify-between gap-4 md:h-24 md:flex-row">
        <p className="text-center text-sm leading-loose text-muted-foreground md:text-left">
          © 2025 ANEIAP. Todos los derechos reservados.
        </p>
        <div className="flex items-center gap-6">
          <Link
            href="https://www.instagram.com/aneiap/"
            target="_blank"
            rel="noopener noreferrer"
            className="text-muted-foreground hover:text-primary transition-colors"
            aria-label="Instagram de ANEIAP"
          >
            <Instagram className="h-5 w-5" />
            <span className="sr-only">Instagram</span>
          </Link>
          <Link
            href="https://www.facebook.com/ANEIAP/"
            target="_blank"
            rel="noopener noreferrer"
            className="text-muted-foreground hover:text-primary transition-colors"
            aria-label="Facebook de ANEIAP"
          >
            <Facebook className="h-5 w-5" />
            <span className="sr-only">Facebook</span>
          </Link>
          <Link
            href="https://aneiap.co/"
            target="_blank"
            rel="noopener noreferrer"
            className="text-muted-foreground hover:text-primary transition-colors"
            aria-label="Sitio web de ANEIAP"
          >
            <Globe className="h-5 w-5" />
            <span className="sr-only">Sitio web</span>
          </Link>
        </div>
      </div>
    </footer>
  )
}

