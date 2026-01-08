class NotFoundError(Exception):
    pass

class ProdutoNotFoundError(NotFoundError):
    """Erro lançado quando um produto não é encontrado."""
    pass

class CategoriaNotFoundError(NotFoundError):
    """Erro lançado quando uma categoria não é encontrada."""
    pass