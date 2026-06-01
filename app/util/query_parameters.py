from enum import Enum

from pydantic import BaseModel

from app.core import ApiError

__all__ = [
    "parse_operator_and_value",
    "FieldQuery",
]


class QueyOperator(str, Enum):
    Nenhum = ""  # Nenhum ("")
    Igual = "eq"  # Igual (=)
    Diferente = "ne"  # Diferente (!=)
    Maior_que = "gt"  # Maior que (>)
    Maior_ou_igual = "ge"  # Maior ou igual (>=)
    Menor_que = "lt"  # Menor que (<)
    Menor_ou_igual = "le"  # Menor ou igual (<=)
    Contém = "lk"  # Contém (~)
    Intervalo = "in"  # Intervalo (|)


class SortOperator(str, Enum):
    Menor_para_Maior = "-"  # Igual (=)
    Maior_para_Menor = "+"  # Diferente (!=)


class FieldQuery(BaseModel):
    op: QueyOperator
    data: str


class FieldSort(BaseModel):
    op: SortOperator
    data: str


def parse_operator_and_value(query: str) -> FieldQuery:
    """
    Analisa uma string de consulta para separar operador e valor.

    Regras:
    - O operador deve ser composto de exatamente duas letras seguido de `:`.
    - Se não houver operador válido, assume-se o operador `eq` por padrão.

    :param query: A string de consulta no formato 'op:valor' ou apenas 'valor'.
    :return: Uma tupla (operador, valor).
    """
    try:
        if ":" in query and len(query.split(":", 1)[0]) == 2:
            # Tenta separar operador e valor
            op, data = query.split(":", 1)
            return FieldQuery(op=QueyOperator(op), data=data)
        else:
            # Se não houver operador valido, assume-se o operador `eq`
            return FieldQuery(op=QueyOperator.Igual, data=query)
    except ValueError as e:
        raise ApiError(
            status_code=422,
            loc=["body", data],
            msg=f'Operador inválido "{op}" no filtro para o campo "{data}". Valores permitidos: {list(QueyOperator)}',
            type="query.invalid_operator",
        )
