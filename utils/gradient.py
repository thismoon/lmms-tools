def hex_to_rgb(hex):
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def interpolate(start_color, end_color, factor: float):
    return tuple(int(start + (end - start) * factor) for start, end in zip(start_color, end_color))

def generate_gradient(start_hex, end_hex, n):
    start_rgb = hex_to_rgb(start_hex)
    end_rgb = hex_to_rgb(end_hex)
    gradient = [rgb_to_hex(interpolate(start_rgb, end_rgb, i / (n - 1))) for i in range(n)]
    return gradient