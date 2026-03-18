class CalcularCostoRecetasUseCase:

    def __init__(self, service):
        self.service = service

    def execute(self):
        return self.service.ejecutar()