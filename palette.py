import math

def generate_color_variations(base_hex, steps=15):
    """
    Generate color variations for a given base hex color.
    
    Args:
        base_hex (str): Base color in hex format
        steps (int): Number of color variations to generate
    
    Returns:
        list: List of color variations in hex format
    """
    # Convert hex to RGB
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    # Convert RGB to hex
    def rgb_to_hex(rgb):
        return '#{:02x}{:02x}{:02x}'.format(
            max(0, min(255, rgb[0])),
            max(0, min(255, rgb[1])),
            max(0, min(255, rgb[2]))
        )
    
    # Unpack RGB values
    r, g, b = hex_to_rgb(base_hex)
    
    # Generate variations
    variations = []
    for i in range(steps):
        # Use sine wave for natural color progression
        factor = (math.sin(math.pi * i / (steps - 1)) * 0.5 + 0.5)
        
        # Blend colors with a wave-like progression
        new_r = int(255 - math.pow(255 - r, 1 + factor * 0.8))
        new_g = int(255 - math.pow(255 - g, 1 + factor * 0.8))
        new_b = int(255 - math.pow(255 - b, 1 + factor * 0.8))
        
        variations.append(rgb_to_hex((new_r, new_g, new_b)))
    
    return variations

# Base colors
base_colors = [
    '#418c65',   # Muted green
    '#2c5e46',   # Deep forest green
    '#7bc4b4',   # Soft aqua
    '#134a3f',   # Dark teal
]

# Generate color variations
color_variations = [
    generate_color_variations(color) for color in base_colors
]

# Flatten the list of variations
all_color_variations = [color for color_set in color_variations for color in color_set]

if __name__ == '__main__':
    # Print the full list of color variations
    print("Color Variations:")
    for color in all_color_variations:
        print(color)
    
    # Optional: Print color variations grouped by base color
    print("\nColor Variations by Base Color:")
    for base_color, variations in zip(base_colors, color_variations):
        print(f"\n{base_color}:")
        for variation in variations:
            print(variation)