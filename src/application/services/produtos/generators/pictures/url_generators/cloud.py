""" A interface to CloudinaryManager what adapte it for Meli operations. """

from .......config import AppConfigManager
from .......infrastructure.database.repositories import CloudinaryReposity
from .......infrastructure.api.cloudinary import CloudinaryManager

app_config = AppConfigManager()
cloud_user = app_config.get_cloud_user()
cloud_repo = CloudinaryReposity()

credentials = cloud_repo.get.user_credentials(cloud_user)

class CloudinaryManagerForMeli(CloudinaryManager):
    def __init__(self):
        super().__init__(
            cloud_name=credentials.cloud_name, 
            api_key=credentials.api_key,
            api_secret=credentials.api_secret
        )
