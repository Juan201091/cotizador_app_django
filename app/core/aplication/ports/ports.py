from abc import ABC, abstractmethod
from typing import List, Dict

class LeerXLSPort(ABC):
    @abstractmethod
    def leer(self, path: str) -> List[Dict]:
        """
        Lee el archivo Excel y devuelve una lista de diccionarios con los datos necesarios.
        Cada diccionario representa un ingrediente con nombre y precio.
        """
        pass

class LeerPDFPort(ABC):
    @abstractmethod
    def leer(self, path: str) -> List[Dict]:
        """
        Lee el PDF y devuelve una lista de diccionarios con los datos necesarios.
        Cada diccionario representa un ingrediente con nombre y precio.
        """
        pass

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