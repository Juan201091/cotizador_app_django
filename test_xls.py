from core.aplication.services.receta_service import RecetaService
from core.aplication.use_cases.calculador_costo import CalcularCostoRecetasUseCase
from core.infrastructure.extractores.xls_extractor import LeerXLSImpl
from core.infrastructure.extractores.pdf_extractor import LeerPDFImpl
from core.infrastructure.extractores.md_extractor import LeerMDImpl


if __name__ == "__main__":
    # 1. Instanciar readers (infraestructura)
    excel_reader = LeerXLSImpl()
    pdf_reader = LeerPDFImpl()
    md_reader = LeerMDImpl()

    # 2. Inyectarlos en el service
    service = RecetaService(
        excel_reader=excel_reader, pdf_reader=pdf_reader, md_reader=md_reader
    )

    # 3. Inyectar service en use case
    use_case = CalcularCostoRecetasUseCase(service)

    # 4. Ejecutar
    resultado = use_case.execute()

    print(resultado)
