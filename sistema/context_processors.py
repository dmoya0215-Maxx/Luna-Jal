"""
Context Processor para pasar variables globales a los templates
"""

def global_context(request):
    """Agrega variables globales disponibles en todos los templates"""
    logueado = request.session.get("logueado", None)
    
    context = {
        'logueado': logueado,
    }
    
    return context
