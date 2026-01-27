class NotFoundError(Exception):
    pass


class ProdutoNotFoundError(NotFoundError):
    """Erro lançado quando um produto não é encontrado."""
    pass


class CategoriaNotFoundError(NotFoundError):
    """Erro lançado quando uma categoria não é encontrada."""
    pass


class EstoqueInsuficienteError(Exception):
    """Exceção levantada quando tenta-se vender mais do que o estoque permite."""
    def __init__(self, message="Estoque insuficiente para realizar a operação."):
        self.message = message
        super().__init__(self.message)

class VendaNotFoundError(Exception):
    pass

class UsuarioNotFoundError(Exception):
    pass

class ItemVendaNotFoundError(Exception):
    pass

