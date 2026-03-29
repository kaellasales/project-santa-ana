from pydantic import BaseModel, model_validator
from typing import List
from app.schemas.turno import TurnoSync
from app.schemas.venda import VendaSync


class SyncPayload(BaseModel):
    turno: TurnoSync
    vendas: List[VendaSync] = []

    @model_validator(mode="after")
    def validar_fechamento(self):
        turno = self.turno
        if turno.data_fechamento and turno.valor_informado is None:
            raise ValueError("valor_informado é obrigatório quando data_fechamento está presente")
        return self


class SyncResponse(BaseModel):
    status: str
    turno_id: int
    vendas_sincronizadas: int
    conflitos: List[dict] = []