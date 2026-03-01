from app.models.pagamento import FormaPagamento
from .base import BaseRepository

class FormaPagamentoRepository(BaseRepository[FormaPagamento]):
    def __init__(self):
        super().__init__(FormaPagamento)