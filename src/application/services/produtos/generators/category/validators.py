""" Validators for a category based on a Product line. """

from typing import Any

from src.infrastructure.database.models.produtos import Product
from .models import ValidationResponse, CategoryValidateProtocol


class IsLeaf(CategoryValidateProtocol):
    """ Valida se é uma categoria folha """
    def validate(self, produto: Product, category_data: list[str, Any]):
        if category_data.get("children_categories") != []:
            return ValidationResponse(reason=f"Apenas categorias sem subcategorias são permitidas.")
        return ValidationResponse(True)


class BuyingModes(CategoryValidateProtocol):
    """ Valida se o modo de venda do produto está dentro do permitido pela categoria """
    def validate(self, produto: Product, category_data: list[str, Any]):
        buying_modes: list = category_data["settings"]["buying_modes"]
        if produto.sale.modo_compra not in buying_modes:
            return ValidationResponse(reason=f"Apenas os modos de venda ({buying_modes}) são aceitos")
        return ValidationResponse(True)


class ItemConditions(CategoryValidateProtocol):
    """ Valida se a condição do produto é permitida pela categoria """
    def validate(self, produto: Product, category_data: list[str, Any]):
        item_conditions: list = category_data["settings"]["item_conditions"]
        if produto.sale.modo_compra not in item_conditions:
            return ValidationResponse(reason=f"Apenas as condições ({item_conditions}) são permitidas")
        return ValidationResponse(True)


class MaxDescriptionLength(CategoryValidateProtocol):
    """ Valida se o tamanho da descrição está dentro do permitido """
    def validate(self, produto: Product, category_data: list[str, Any]):
        max_description_length: int = category_data["settings"]["max_description_length"]
        if len(produto.sale.descricao) > max_description_length:
            return ValidationResponse(reason=f"Tamanho da descrição excede o máximo permitido ({max_description_length})")
        return ValidationResponse(True)


class MaxPicturesPerItem(CategoryValidateProtocol):
    """ Valida se a quantidade de imagens está dentro do permitido """
    def validate(self, produto: Product, category_data: list[str, Any]):
        max_pictures_per_item: int = category_data["settings"]["max_pictures_per_item"]
        
        if not max_pictures_per_item:
            return ValidationResponse(True)
        
        if  len(produto.sale.imagens) > max_pictures_per_item:
            return ValidationResponse(reason=f"Quantidade de imagens excede o máximo permitido ({max_pictures_per_item})")
        return ValidationResponse(True)


class TitleLength(CategoryValidateProtocol):
    """ Valida se o tamanho do título está dentro do permitido """
    def validate(self, produto: Product, category_data: list[str, Any]):
        max_title_length: int = category_data["settings"]["max_title_length"]
        if not max_title_length:
            return ValidationResponse(True)
        if len(produto.sale.titulo) > max_title_length:
            return ValidationResponse(reason=f"Tamanho do título excede o máximo permitido ({max_title_length})")
        return ValidationResponse(True)


class MaximumPrice(CategoryValidateProtocol):
    """ Eu tenho que ter cuidado, se isso returnar "null" eu preciso pular a validação e retornar verdadeiro logo de cara. """
    def validate(self, produto: Product, category_data: list[str, Any]):
        maximum_price: int = category_data["settings"]["maximum_price"]
        if not maximum_price:
            return ValidationResponse(True)
        if produto.sale.preco > maximum_price:
            return ValidationResponse(reason=f"Preço excede o máximo permitido ({maximum_price})")
        return ValidationResponse(True)


class MinimumPrice(CategoryValidateProtocol):
    """ Valida se o preço do produto corresponde ao valor mínimo da categoria """
    def validate(self, produto: Product, category_data: list[str, Any]):
        minimum_price: int = category_data["settings"]["minimum_price"]
        if not minimum_price:
            return ValidationResponse(True)
        if produto.sale.preco < minimum_price:
            return ValidationResponse(reason=f"Preço é menor que o mínimo permitido ({minimum_price})")
        return ValidationResponse(True)


class Price(CategoryValidateProtocol):
    """ Valida se a categoria exige um preço """
    def validate(self, produto: Product, category_data: list[str, Any]):
        price: int = category_data["settings"]["price"]
        if price != "required":
            return ValidationResponse(True)
        if not produto.sale.preco:
            return ValidationResponse(reason=f"Preço não informado ({price})")
        return ValidationResponse(True)


class ShippingOptions(CategoryValidateProtocol):
    """ Valida se o modo de entrega é compatível com a categoria """
    def validate(self, produto: Product, category_data: list[str, Any]):
        shipping_options: list = category_data["settings"]["shipping_options"]
        if produto.shippiment.modo_envio not in shipping_options:
            return ValidationResponse(reason=f"Apenas os modos de envio ({shipping_options}) são aceitos")
        return ValidationResponse(True)


class Status:
    """ Eu suspeito seriamente que isso diz respeito ao estado da categoria, se ainda está ativa ou não, se for o caso é um valor super importante. No exemplo de json que eu peguei está como "enabled" """
    def validate(self, produto: Product, category_data: list[str, Any]):
        status = category_data["settings"]["status"]
        if status != "enabled":
            return ValidationResponse(reason=f"Categoria descontinuada pelo mercado livre")
        return ValidationResponse(True)


validators: list[CategoryValidateProtocol] = [
    IsLeaf(),
    BuyingModes(),
    ItemConditions(),
    MaxDescriptionLength(),
    MaxDescriptionLength(),
    MaxPicturesPerItem(),
    TitleLength(),
    MaximumPrice(),
    MinimumPrice(),
    Price(),
    ShippingOptions(),
    Status()
]


# def validar(product=produto, category_data=cat_data):
#     causes: list = []
#     for validator in validators:
#         response = validator.validate(product, category_data)
#         if not response.is_valid:
#             causes.append(response.reason)
    
#     if causes:
#         return ValidationResponse(causes=causes)
    
#     return ValidationResponse(True)

# print(validar(product=produto, category_data=cat_data))
