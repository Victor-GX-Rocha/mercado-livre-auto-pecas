"""  """

from PIL import Image

class CorretImageDimentions:
    """  """
    def corret(self, imagem_path: str):
        """
        
        Args:
            imagem_path (str):
        """
        temp_path: str = f"{imagem_path}_temp.jpg"
        
        img = Image.open(imagem_path)
        img: Image.ImageFile.ImageFile = self.corret_dimensions(img)
        img: Image.ImageFile.ImageFile = self.corret_format(img)
        img.save(imagem_path, optimize=True, quality=85)
    
    def corret_dimensions(self, img: Image.ImageFile) -> Image.ImageFile.ImageFile:
        """
        
        Args:
            img (Image.ImageFile.ImageFile):
        Returns:
            (Image.ImageFile.ImageFile): 
        """
        largura, altura = img.size
        if largura < 500 or altura < 500:
            img = img.resize((500, 500))
        return img
    
    def corret_format(self, img: Image.ImageFile.ImageFile) -> Image.ImageFile.ImageFile:
        """
        
        Args:
            img (Image.ImageFile.ImageFile):
        Returns:
            (Image.ImageFile.ImageFile): 
        """
        if img.format not in ['JPEG', 'JPG', 'PNG']:
            img = img.convert('RGB')
        return img
