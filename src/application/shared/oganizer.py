""" Organizer dataclasses tables based on his columns """

import operator
from typing import Any

class GroupBy:
    @staticmethod
    def column(lines: list[Any], column_path: str) -> dict[Any, list[Any]]:
        """
        Agrupa objetos baseado em um caminho de atributos (suporta aninhamento)
        
        Args:
            lines: Lista de objetos (dataclasses ou objetos com atributos)
            column_path: Caminho do atributo (ex: "atributo" ou "subobjeto.coluna")
        
        Returns:
            Dicionário agrupado {valor_da_coluna: [objetos]}
        """
        if not isinstance(lines, list):
            raise TypeError(f"Tipo inválido! Esperado: list. Recebido: {type(lines)}")
        
        # Obtém a função de acesso ao atributo (otimizado com operator.attrgetter)
        try:
            attr_getter = operator.attrgetter(column_path)
        except AttributeError as e:
            raise ValueError(f"Caminho inválido: '{column_path}'") from e
        
        grouped = {}
        for line in lines:
            try:
                value = attr_getter(line)
            except AttributeError:
                value = None  # Atributo ausente é tratado como None
                # raise AttributeError(f"Caminho de atributos inválido: {column_path}")
            
            grouped.setdefault(value, []).append(line)
            
        return grouped
