import re

# Diccionario de equivalencias de vocales
VOCAL_PATTERNS = {
    'a': '[aáà]',
    'e': '[eéè]',
    'i': '[iíì]',
    'o': '[oóò]',
    'u': '[uúù]',
    'A': '[AÁÀ]',
    'E': '[EÉÈ]',
    'I': '[IÍÌ]',
    'O': '[OÓÒ]',
    'U': '[UÚÙ]'
}

def crear_patron_flexible(texto):
    """
    Convierte un texto en un patrón que acepta vocales con o sin tilde.
    
    Args:
        texto (str): Texto original
        
    Returns:
        str: Texto con patrones flexibles para vocales
    """
    if not texto:
        return None
        
    patron = ''
    # Itera cada carácter del texto
    for char in texto:
        # Si es vocal, obtiene su patrón del diccionario VOCAL_PATTERNS
        # Si no es vocal, escapa el carácter
        patron += VOCAL_PATTERNS.get(char, re.escape(char))
    return patron

def patron_coincidencia_exacta(value):
    """
    Crea patrón para coincidencias exactas tolerante a tildes.
    
    Example:
        >>> patron = patron_coincidencia_exacta("Angel")
        >>> patron.match("Ángel")  # Coincidirá
        >>> patron.match("Angel")  # Coincidirá
    """
    if not value:
        return None
    patron = crear_patron_flexible(value)
    return re.compile(f"^{patron}$", re.IGNORECASE)

def patron_coincidencia_parcial(value):
    """
    Crea patrón para coincidencias parciales tolerante a tildes.
    
    Example:
        >>> patron = patron_coincidencia_parcial("Angel")
        >>> patron.match("El Ángel")  # Coincidirá
        >>> patron.match("angeles")   # Coincidirá
    """
    if not value:
        return None
    patron = crear_patron_flexible(value)
    return re.compile(f".*{patron}.*", re.IGNORECASE)