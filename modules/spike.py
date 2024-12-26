from os.path import join

import pygame


def load_spikes(width, height):
    """
    Load the spike sprite (Idle.png) from the Traps/Spikes folder.
    """
    path = join("assets", "Traps", "Spikes", "Idle.png")
    spike_image = pygame.image.load(path).convert_alpha()

    # Scale the spike image to fit the block size
    spike_image = pygame.transform.scale(spike_image, (width, height))
    return spike_image
