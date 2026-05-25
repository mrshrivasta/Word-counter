from flask import Blueprint, request, jsonify, send_file
from app.analysis.metrics import get_basic_stats
from app.analysis.readability import get_readability_stats
from app.analysis.seo import get_seo_analysis
from app.analysis.semantics import analyze_semantics
from app.analysis.structure import analyze_structure
from app.analysis.geo_aeo import analyze_geo_aeo
from werkzeug.utils import secure_filename
import os
from docx import Document
from reportlab.pdfgen import canvas
from io import BytesIO
import time

api_bp = Blueprint('api', __name__)

@api_bp.route('/analyze', methods=['POST'])
def analyze():
    start_time = time.time()
    data = request.json
    text = data.get('text', '')

    stats = get_basic_stats(text)
    readability = get_readability_stats(text)
    seo = get_seo_analysis(text)
    semantics = analyze_semantics(text)
    structure = analyze_structure(text)
    geo_aeo = analyze_geo_aeo(text)

    processing_time = (time.time() - start_time) * 1000 # ms

    return jsonify({
        'stats': stats,
        'readability': readability,
        'seo': seo,
        'semantics': semantics,
        'structure': structure,
        'geo_aeo': geo_aeo,
        'advanced': {
            'geo_score': geo_aeo.get('geo_authority_score', 0),
            'aeo_score': geo_aeo.get('aeo_relevance', 0),
            'aio_score': 100 - semantics.get('filler_density', 0) * 5,
            'sxo_score': structure.get('variety_score', 0)
        },
        'processing_time': round(processing_time, 2)
    })

@api_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    upload_folder = 'static/uploads'
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)

    content = ""
    if filename.endswith('.txt'):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    elif filename.endswith('.docx'):
        doc = Document(filepath)
        content = "\n".join([para.text for para in doc.paragraphs])

    return jsonify({'content': content})

@api_bp.route('/export/<format>', methods=['POST'])
def export_file(format):
    data = request.json
    text = data.get('text', '')

    if format == 'txt':
        buffer = BytesIO()
        buffer.write(text.encode('utf-8'))
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name='export.txt', mimetype='text/plain')

    elif format == 'pdf':
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 800, "Text Export")
        y = 780
        for line in text.split('\n'):
            # simple wrap
            words = line.split()
            current_line = []
            for word in words:
                current_line.append(word)
                if len(' '.join(current_line)) > 80:
                    p.drawString(100, y, ' '.join(current_line))
                    y -= 15
                    current_line = []
            if current_line:
                p.drawString(100, y, ' '.join(current_line))
                y -= 15
            if y < 50:
                p.showPage()
                y = 800
        p.save()
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name='export.pdf', mimetype='application/pdf')

    elif format == 'docx':
        doc = Document()
        doc.add_paragraph(text)
        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name='export.docx', mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

    return jsonify({'error': 'Invalid format'}), 400
