from core.infrastructure.extractores.xls_extractor import LeerXLSImpl
from core.infrastructure.extractores.pdf_extractor import LeerPDFImpl
from core.infrastructure.extractores.md_extractor import LeerMDImpl
from core.aplication.services.receta_service import RecetaService
from core.aplication.services.cotizador_service import CotizadorService
from core.aplication.use_cases.calcular_costo_receta_use_case import CalcularCostoRecetasUseCase
from core.aplication.use_cases.recetas_use_case import ObtenerRecetasUseCase


def get_recetas_use_case():
    service = RecetaService(
        LeerXLSImpl(),
        LeerPDFImpl(),
        LeerMDImpl(),
    )
    return ObtenerRecetasUseCase(service)

def get_calcular_costo_use_case():
    cotizador_service = CotizadorService()
    return CalcularCostoRecetasUseCase(cotizador_service)