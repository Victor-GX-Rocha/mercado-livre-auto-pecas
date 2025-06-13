""" Image corretors. """

from PIL import Image

class CorretImageProperties:
    """ Provides image corret methods. """
    def corret(self, imagem_path: str) -> str:
        """
        Correct the image dimensions and format.
        - Resize if less than 500x500.
        - Convert to ['JPEG', 'JPG', 'PNG'] if diferent. 
        Args:
            imagem_path (str):
        Returns:
            str: Temp image path.
        """
        temp_path: str = f"{imagem_path}_temp.jpg"
        
        img = Image.open(imagem_path)
        img = self.corret_dimensions(img)
        img = self.corret_format(img)
        img.save(temp_path, optimize=True, quality=85)
        
        return temp_path
    
    def corret_dimensions(self, img):
        """
        Resize the image if less than 500x500.
        Args:
            img (Image.ImageFile.ImageFile):
        Returns:
            (Image.ImageFile.ImageFile): 
        """
        largura, altura = img.size
        if largura < 500 or altura < 500:
            img = img.resize((500, 500))
        return img
    
    def corret_format(self, img):
        """
        Convert to ['JPEG', 'JPG', 'PNG'] if it's in a diferent format. 
        Args:
            img (Image.ImageFile.ImageFile):
        Returns:
            (Image.ImageFile.ImageFile): 
        """
        if img.format not in ['JPEG', 'JPG', 'PNG']:
            img = img.convert('RGB')
        return img
