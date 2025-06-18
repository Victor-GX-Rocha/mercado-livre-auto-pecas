""" An interface to chose the url generator that will be used. """

from .cloud import CloudinaryImageUploader

class UrlGeneratorFactory:
    """ Interface to select a Url generator. """
    @staticmethod
    def chose(generator: str) -> object:
        """
        Returns to you a Url generator object.
        Args:
            generator (str): Generator name.
        Returns:
            CloudinaryManagerForMeli: Cloudinary manager interface adapted to meli operations.
        Raises:
            ValueError: If the generator name dosen't mach.
        """
        match generator.strip().lower():
            case "cloudinary":
                return CloudinaryImageUploader()
            case _:
                raise ValueError(f"{generator} não possui uma classe de geração de Url correspondente") 
