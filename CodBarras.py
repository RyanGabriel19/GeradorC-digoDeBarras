from flask import Flask, render_template, request, send_file
from reportlab.graphics.barcode import code128
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gerar_pdf', methods=['POST'])
def gerar_pdf():
    # Coleta os dados dos produtos enviados
    codigos_produto = request.form.getlist('codigo_produto[]')
    descricoes = request.form.getlist('descricao[]')
    codigos_barras = request.form.getlist('codigo_barras[]')
    
    produtos = zip(codigos_produto, descricoes, codigos_barras)
    
    # Criar o PDF com os dados dos produtos
    pdf_filename = "CodigoDeBarras_produtos.pdf"
    
    pdf = canvas.Canvas(pdf_filename, pagesize=letter)
    y_position = 750

    for produto in produtos:
        codigo_produto, descricao, codigo_barras = produto

        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y_position, "Código:")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(100, y_position, codigo_produto)

        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y_position - 20, "Descrição:")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(117, y_position - 20, descricao)

        pdf.setFont("Helvetica", 10)
        pdf.drawCentredString(130, y_position - 120, codigo_barras)

        barcode = code128.Code128(codigo_barras, barHeight=60, barWidth=1.6)
        barcode.drawOn(pdf, 32, y_position - 100)

        y_position -= 180
        if y_position < 100:
            pdf.showPage()
            y_position = 750

    pdf.save()

    # Enviar o PDF gerado para download
    return send_file(pdf_filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
