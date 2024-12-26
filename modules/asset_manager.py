import pygame

from modules.utils import load_sprite_sheets


class AssetManager:
    """Centralized Asset Manager for loading and caching assets."""

    _assets = {}  # Dictionary to cache all assets

    @classmethod
    def load_sprites(cls, folder, name, width, height, is_alpha=True):
        """
        Load and cache sprite sheets.
        :param folder: Folder name containing the assets.
        :param name: File name of the sprite sheet.
        :param width: Width of each sprite in the sheet.
        :param height: Height of each sprite in the sheet.
        :param is_alpha: Whether the sprite has transparency.
        :return: A dictionary of sprites.
        """
        key = (folder, name)  # Unique key for caching
        if key not in cls._assets:  # Check if sprites are already loaded
            cls._assets[key] = load_sprite_sheets(folder, name, width, height, is_alpha)
        return cls._assets[key]

    @classmethod
    def load_sound(cls, path):
        """Load and cache sound assets."""
        if path not in cls._assets:
            cls._assets[path] = pygame.mixer.Sound(path)
        return cls._assets[path]

    @classmethod
    def load_image(cls, path):
        """Load and cache single image assets."""
        if path not in cls._assets:
            cls._assets[path] = pygame.image.load(path).convert_alpha()
        return cls._assets[path]

    @classmethod
    def unload(cls, key=None):
        """
        Unload specific assets or all assets.
        :param key: The key of the asset to unload. If None, unloads all assets.
        """
        if key:
            if key in cls._assets:
                del cls._assets[key]
        else:
            cls._assets.clear()

    @classmethod
    def preload_assets(cls, assets):
        """
        Preload a list of assets into the cache.
        :param assets: A list of tuples in the format (type, args), where type is
                       'image', 'sound', or 'sprites', and args are the arguments for the respective load method.
        """
        for asset_type, args in assets:
            if asset_type == 'image':
                cls.load_image(*args)
            elif asset_type == 'sound':
                cls.load_sound(*args)
            elif asset_type == 'sprites':
                cls.load_sprites(*args)
