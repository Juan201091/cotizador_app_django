class ObtenerRecetasUseCase:
    def __init__(self, receta_service):
        self.receta_service = receta_service

    def ejecutar(self):
        platos, precios = self.receta_service.ejecutar()
        return platos, precios