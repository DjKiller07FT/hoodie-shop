"""
Funciones auxiliares reutilizables.
Formateo de moneda, validaciones, etc.
"""

import os
from werkzeug.utils import secure_filename
from flask import current_app


def formato_moneda_cop(valor):
    """
    Formatea un valor numérico como moneda colombiana (COP).
    
    Args:
        valor (float): Valor a formatear
        
    Returns:
        str: Valor formateado (ej: $120.000)
    """
    try:
        return f"${valor:,.0f}".replace(",", ".")
    except (ValueError, TypeError):
        return "$0"


def allowed_file(filename):
    """
    Verifica si un archivo tiene una extensión permitida.
    
    Args:
        filename (str): Nombre del archivo
        
    Returns:
        bool: True si la extensión es permitida
    """
    allowed = current_app.config.get('ALLOWED_EXTENSIONS', {'png', 'jpg', 'jpeg', 'gif', 'webp'})
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed


def save_image(file, upload_folder=None):
    """
    Guarda una imagen subida de forma segura.
    
    Args:
        file: Archivo de la request
        upload_folder (str): Carpeta destino (opcional)
        
    Returns:
        str: Ruta relativa de la imagen guardada o None si hay error
    """
    if not file or not allowed_file(file.filename):
        return None
    
    filename = secure_filename(file.filename)
    
    # Generar nombre único si ya existe
    upload_path = upload_folder or current_app.config['UPLOAD_FOLDER']
    filepath = os.path.join(upload_path, filename)
    
    if os.path.exists(filepath):
        name, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(filepath):
            filename = f"{name}_{counter}{ext}"
            filepath = os.path.join(upload_path, filename)
            counter += 1
    
    try:
        file.save(filepath)
        # Retornar ruta relativa para guardar en BD
        return f"/static/uploads/{filename}"
    except Exception as e:
        current_app.logger.error(f"Error guardando imagen: {e}")
        return None


def validar_email(email):
    """
    Validación básica de formato de email.
    
    Args:
        email (str): Email a validar
        
    Returns:
        bool: True si el formato es válido
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validar_telefono(telefono):
    """
    Validación básica de teléfono colombiano.
    
    Args:
        telefono (str): Teléfono a validar
        
    Returns:
        bool: True si tiene formato válido (10 dígitos)
    """
    import re
    # Acepta formatos: 3001234567 o 300-123-4567 o 300 123 4567
    telefono_limpio = re.sub(r'[\s\-\(\)]', '', telefono)
    return len(telefono_limpio) == 10 and telefono_limpio.isdigit()


def paginar(items, page, per_page):
    """
    Pagina una lista de items.
    
    Args:
        items (list): Lista de items a paginar
        page (int): Número de página actual (1-indexed)
        per_page (int): Items por página
        
    Returns:
        dict: {
            'items': lista paginada,
            'total': total de items,
            'page': página actual,
            'pages': total de páginas,
            'has_prev': bool,
            'has_next': bool
        }
    """
    total = len(items)
    pages = (total + per_page - 1) // per_page  # Redondeo hacia arriba
    
    start = (page - 1) * per_page
    end = start + per_page
    
    return {
        'items': items[start:end],
        'total': total,
        'page': page,
        'pages': pages,
        'has_prev': page > 1,
        'has_next': page < pages
    }