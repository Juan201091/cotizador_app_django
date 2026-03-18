from abc import ABC, abstractmethod
from typing import List, Dict

# Puerto para leer XLSX (Carnes y Pescados)
class LeerXLSPort(ABC):
    @abstractmethod
    def leer(self, path: str) -> List[Dict]:
        """
        Lee el archivo Excel y devuelve una lista de diccionarios con los datos necesarios.
        Cada diccionario representa un ingrediente con nombre y precio.
        """
        pass

# Puerto para leer PDF (Verdulería)
class LeerPDFPort(ABC):
    @abstractmethod
    def leer(self, path: str) -> List[Dict]:
        """
        Lee el PDF y devuelve una lista de diccionarios con los datos necesarios.
        Cada diccionario representa un ingrediente con nombre y precio.
        """
        pass

# Puerto para leer Markdown (Recetas)
class LeerMDPort(ABC):
    @abstractmethod
    def leer(self, path: str) -> List[Dict]:
        """
        Lee el archivo MD y devuelve una lista de diccionarios.
        Cada diccionario representa una receta con:
          - nombre
          - instrucciones
          - lista de ingredientes con cantidades
        """
        pass