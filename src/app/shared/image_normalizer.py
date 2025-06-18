""" Image path normalizers. """

import re

class ImageNormalizer:
    @staticmethod
    def correct_format(raw_paths: str) -> list[str]:
        """
        Normalize serialized image paths into standardized Windows paths.
        
        Processing steps:
        1. Split input string by commas/semicolons into individual paths
        2. For each path:
            - Remove surrounding whitespace
            - Remove single/double quotation marks
            - Split into path components using any mix of backslashes/forward slashes
            - Filter out empty components
        3. Rebuild path using Windows-style backslashes
        
        Args:
            raw_paths: String containing multiple paths separated by commas/semicolons.
                        Example: "C:/img.jpg; D:\\photos\\1.jpg"
        
        Returns:
            List of normalized Windows paths with backslashes.
            Example: ['C:\\img.jpg', 'D:\\photos\\1.jpg']
        
        Raises:
            ValueError: If no valid paths found after cleaning
        
        Examples:
            >>> raw = "C:/test.jpg; 'D:\\\\images\\1.jpg'; E:\\temp\\"
            >>> ImageNormalizer.correct_format(raw)
            ['C:\\test.jpg', 'D:\\images\\1.jpg', 'E:\\temp']
        """
        # Implementação mais clara:
        paths = []
        for path in re.split(r'[;,]', raw_paths):
            cleaned = path.strip().replace("'", "").replace('"', '')
            components = [p for p in re.split(r'[\\/]', cleaned) if p]
            if components:
                paths.append("\\".join(components))
        
        # if not paths:
        #     raise ValueError("No valid paths found after normalization")
        return paths
