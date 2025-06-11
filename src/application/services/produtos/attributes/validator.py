""" Attribute validator based on category. """

from .....infrastructure.database.models.produtos import Product
from .....infrastructure.api.mercadolivre.auth import AuthResponse
from .....infrastructure.api.mercadolivre.category import CategoryManager
from .models import AttributesValidatorResponse


class AttributesValidator:
    def __init__(self):
        self.cat_manager = CategoryManager()
    
    def validate(self, product: Product, attributes: list[dict], token: AuthResponse) -> AttributesValidatorResponse:
        """
        Validate if some oblied category is missing.
        Args:
            product (Product): Produtos dataclass table.
            attributes (list[dict]): Product attributes list.
            token (AuthResponse): Token to get the category attributes.
        Returns:
            list[str]: A list alert messages about the missing category attributes. (If everything ok, returns a empty list).
        """
        category_attributes = self.cat_manager.get_category_attributes(product.category.categoria, token.data.access_token)
        
        if not category_attributes.success:
            return AttributesValidatorResponse(
                is_valid=False,
                causes=[f"Falha no processo de obtenção de atributos da categoria: {category_attributes.error}"]
            )
        
        misses: list = self._verify_misses(attributes, category_attributes.data)
        
        if misses: # If something is missing
            return AttributesValidatorResponse(
                is_valid=False,
                causes=misses
            )
        
        return AttributesValidatorResponse(
            is_valid=True
        )
    
    def _verify_misses(self, attributes: list[dict], category_attributes: list[dict]) -> list[str]:
        """
        Verify if exists missing required category attributes.
        Args:
            attributes (list[dict]): Product attributes list.
            category_attributes (list[dict]): Category attributes.
        Returns:
            list: A alert list of messages about the missing category attributes. (If everything ok, returns a empty list).
        """
        attributes_ids: list[str] = [attr["id"] for attr in attributes]
        missing: list = []
        
        for cat_attr in category_attributes:
            if cat_attr.get("tags", {}).get("required"): # If it's a required attribute
                if not cat_attr.get("id") in attributes_ids: # Verify if the attribute already is inside the created attributes list
                    missing.append(self._build_message(cat_attr))
        return missing
    
    def _build_message(self, cat_attr: dict) -> str:
        """
        Build a friendly message for user.
        Args:
            cat_attr (dict): Category attribute.
        Returns:
            str: A message with the ID, Name of attribute and the hint e tooltip if they exists.
        Example:
            >>> _build_message(cat_attr)
            "GTIN (Código universal de produto) | hint: Pode ser um EAN, UPC ou outro GTIN | tooltip: Como posso encontrar o código?..."
        """
        attr_id: str = cat_attr.get("id")
        attr_name: str = cat_attr.get("name")
        message: str = f"{attr_id} ({attr_name})"
        
        if hint := cat_attr.get("hint"):
            message += f" | {hint}"
        elif tooltip := cat_attr.get("tooltip"):
            message += f" | {tooltip}"
        
        return message
