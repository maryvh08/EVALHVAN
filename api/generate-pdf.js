import { PDFDocument, rgb, StandardFonts } from 'pdf-lib';
import fs from 'node:fs/promises'

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).end(); // Método no permitido
  }

  try {
    const pdfDoc = await PDFDocument.create();
    const page = pdfDoc.addPage();
    const font = await pdfDoc.embedFont(StandardFonts.Helvetica);
    const text = req.body.text || 'Hola, este es un PDF generado en Vercel!'; // Recibe el texto del frontend
    const fontSize = 30;
    const textWidth = font.widthOfTextAtSize(text, fontSize);

    page.drawText(text, {
      x: page.getWidth() / 2 - textWidth / 2,
      y: page.getHeight() / 2 + fontSize / 2,
      size: fontSize,
      font,
      color: rgb(0, 0, 0),
    });

    const pdfBytes = await pdfDoc.save();
    
    res.setHeader('Content-Type', 'application/pdf');
    res.setHeader('Content-Disposition', 'attachment; filename=reporte.pdf');
    res.send(pdfBytes);

  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Error al generar el PDF' });
  }
}
