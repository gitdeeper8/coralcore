"""
🪸 CORAL-CORE: Biomineralization Dynamics & Reef Hydro-Acoustic Buffering Framework
Version: 1.0.0 | DOI: 10.5281/zenodo.18913829

Pure Python implementation - لا يحتاج إلى numpy أو أي مكتبات خارجية
"""

__version__ = "1.0.0"
__doi__ = "10.5281/zenodo.18913829"
__author__ = "Samir Baladi"
__email__ = "gitdeeper@gmail.com"

# استيراد كسول - يتم الاستيراد عند الحاجة فقط
def get_calcification():
    """Get calcification module."""
    from coralcore.parameters.calcification import calcification_rate, get_species_constant
    return {'rate': calcification_rate, 'constants': get_species_constant}

def get_rhi():
    """Get RHI module."""
    from coralcore.rhi.composite import ReefHealthIndex, RHI_WEIGHTS
    return {'calculator': ReefHealthIndex, 'weights': RHI_WEIGHTS}

def get_alert():
    """Get alert module."""
    from coralcore.rhi.alert import AlertManager, AlertLevel, AlertChannel
    return {'manager': AlertManager, 'levels': AlertLevel, 'channels': AlertChannel}

# قائمة بالوحدات المتاحة
__all__ = [
    'get_calcification',
    'get_rhi',
    'get_alert',
    '__version__',
    '__doi__',
]
