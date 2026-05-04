import re
from typing import Optional, Tuple, Union

import numpy as np

BASE_COLORS: dict[str, str] = {
    'b': '#1f77b4',  # blue (tab10 C0)
    'g': '#2ca02c',  # green (tab10 C1)
    'r': '#d62728',  # red (tab10 C2)
    'c': '#17becf',  # cyan (tab10 C3)
    'm': '#9467bd',  # magenta (tab10 C4)
    'y': '#bcbd22',  # yellow (tab10 C5)
    'k': '#000000',  # black
    'w': '#ffffff',  # white
}

CSS4_COLORS: dict[str, str] = {
    'aliceblue': '#F0F8FF',
    'antiquewhite': '#FAEBD7',
    'aqua': '#00FFFF',
    'aquamarine': '#7FFFD4',
    'azure': '#F0FFFF',
    'beige': '#F5F5DC',
    'bisque': '#FFE4C4',
    'black': '#000000',
    'blanchedalmond': '#FFEBCD',
    'blue': '#0000FF',
    'blueviolet': '#8A2BE2',
    'brown': '#A52A2A',
    'burlywood': '#DEB887',
    'cadetblue': '#5F9EA0',
    'chartreuse': '#7FFF00',
    'chocolate': '#D2691E',
    'coral': '#FF7F50',
    'cornflowerblue': '#6495ED',
    'cornsilk': '#FFF8DC',
    'crimson': '#DC143C',
    'cyan': '#00FFFF',
    'darkblue': '#00008B',
    'darkcyan': '#008B8B',
    'darkgoldenrod': '#B8860B',
    'darkgray': '#A9A9A9',
    'darkgreen': '#006400',
    'darkgrey': '#A9A9A9',
    'darkkhaki': '#BDB76B',
    'darkmagenta': '#8B008B',
    'darkolivegreen': '#556B2F',
    'darkorange': '#FF8C00',
    'darkorchid': '#9932CC',
    'darkred': '#8B0000',
    'darksalmon': '#E9967A',
    'darkseagreen': '#8FBC8F',
    'darkslateblue': '#483D8B',
    'darkslategray': '#2F4F4F',
    'darkslategrey': '#2F4F4F',
    'darkturquoise': '#00CED1',
    'darkviolet': '#9400D3',
    'deeppink': '#FF1493',
    'deepskyblue': '#00BFFF',
    'dimgray': '#696969',
    'dimgrey': '#696969',
    'dodgerblue': '#1E90FF',
    'firebrick': '#B22222',
    'floralwhite': '#FFFAF0',
    'forestgreen': '#228B22',
    'fuchsia': '#FF00FF',
    'gainsboro': '#DCDCDC',
    'ghostwhite': '#F8F8FF',
    'gold': '#FFD700',
    'goldenrod': '#DAA520',
    'gray': '#808080',
    'green': '#008000',
    'greenyellow': '#ADFF2F',
    'grey': '#808080',
    'honeydew': '#F0FFF0',
    'hotpink': '#FF69B4',
    'indianred': '#CD5C5C',
    'indigo': '#4B0082',
    'ivory': '#FFFFF0',
    'khaki': '#F0E68C',
    'lavender': '#E6E6FA',
    'lavenderblush': '#FFF0F5',
    'lawngreen': '#7CFC00',
    'lemonchiffon': '#FFFACD',
    'lightblue': '#ADD8E6',
    'lightcoral': '#F08080',
    'lightcyan': '#E0FFFF',
    'lightgoldenrodyellow': '#FAFAD2',
    'lightgray': '#D3D3D3',
    'lightgreen': '#90EE90',
    'lightgrey': '#D3D3D3',
    'lightpink': '#FFB6C1',
    'lightsalmon': '#FFA07A',
    'lightseagreen': '#20B2AA',
    'lightskyblue': '#87CEFA',
    'lightslategray': '#778899',
    'lightslategrey': '#778899',
    'lightsteelblue': '#B0C4DE',
    'lightyellow': '#FFFFE0',
    'lime': '#00FF00',
    'limegreen': '#32CD32',
    'linen': '#FAF0E6',
    'magenta': '#FF00FF',
    'maroon': '#800000',
    'mediumaquamarine': '#66CDAA',
    'mediumblue': '#0000CD',
    'mediumorchid': '#BA55D3',
    'mediumpurple': '#9370DB',
    'mediumseagreen': '#3CB371',
    'mediumslateblue': '#7B68EE',
    'mediumspringgreen': '#00FA9A',
    'mediumturquoise': '#48D1CC',
    'mediumvioletred': '#C71585',
    'midnightblue': '#191970',
    'mintcream': '#F5FFFA',
    'mistyrose': '#FFE4E1',
    'moccasin': '#FFE4B5',
    'navajowhite': '#FFDEAD',
    'navy': '#000080',
    'oldlace': '#FDF5E6',
    'olive': '#808000',
    'olivedrab': '#6B8E23',
    'orange': '#FFA500',
    'orangered': '#FF4500',
    'orchid': '#DA70D6',
    'palegoldenrod': '#EEE8AA',
    'palegreen': '#98FB98',
    'paleturquoise': '#AFEEEE',
    'palevioletred': '#DB7093',
    'papayawhip': '#FFEFD5',
    'peachpuff': '#FFDAB9',
    'peru': '#CD853F',
    'pink': '#FFC0CB',
    'plum': '#DDA0DD',
    'powderblue': '#B0E0E6',
    'purple': '#800080',
    'rebeccapurple': '#663399',
    'red': '#FF0000',
    'rosybrown': '#BC8F8F',
    'royalblue': '#4169E1',
    'saddlebrown': '#8B4513',
    'salmon': '#FA8072',
    'sandybrown': '#FAA460',
    'seagreen': '#2E8B57',
    'seashell': '#FFF5EE',
    'sienna': '#A0522D',
    'silver': '#C0C0C0',
    'skyblue': '#87CEEB',
    'slateblue': '#6A5ACD',
    'slategray': '#708090',
    'slategrey': '#708090',
    'snow': '#FFFAFA',
    'springgreen': '#00FF7F',
    'steelblue': '#4682B4',
    'tan': '#D2B48C',
    'teal': '#008080',
    'thistle': '#D8BFD8',
    'tomato': '#FF6347',
    'turquoise': '#40E0D0',
    'violet': '#EE82EE',
    'wheat': '#F5DEB3',
    'white': '#FFFFFF',
    'whitesmoke': '#F5F5F5',
    'yellow': '#FFFF00',
    'yellowgreen': '#9ACD32',
}

TAB10_COLORS = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
    '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
    '#bcbd22', '#17becf',
]


def _hex_to_rgba(hex_color: str, alpha: float = 1.0) -> Tuple[int, int, int, int]:
    """Convert hex color to RGBA tuple with alpha in 0-255 range."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join(c * 2 for c in hex_color)
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    a = int(alpha * 255) if alpha <= 1.0 else int(min(alpha, 255))
    return (r, g, b, a)


_color_cycle_index: int = 0


def _reset_color_cycle() -> None:
    global _color_cycle_index
    _color_cycle_index = 0


def _next_color() -> str:
    global _color_cycle_index
    c = TAB10_COLORS[_color_cycle_index % len(TAB10_COLORS)]
    _color_cycle_index += 1
    return c


def resolve_color(
    spec: Union[str, Tuple[float, ...], None],
    alpha: Optional[float] = 1.0,
) -> Tuple[int, int, int, int]:
    """
    Resolve a matplotlib-style color specification to RGBA.

    Returns RGBA tuple with all values in 0-255 range (compatible with QColor).

    Supported formats:
    - Single letter: 'b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'
    - CSS4 color name: 'blue', 'red', 'darkorange', etc.
    - Hex: '#RRGGBB', '#RGB'
    - RGB tuple: (r, g, b) each in [0, 1]
    - None: returns the next color from the tab10 cycle
    """
    if alpha is None:
        alpha = 1.0
    a = int(alpha * 255) if alpha <= 1.0 else int(min(alpha, 255))

    # Handle C0-C9 color cycle codes
    if isinstance(spec, str) and len(spec) == 2 and spec[0] == 'C' and spec[1].isdigit():
        idx = int(spec[1])
        return _hex_to_rgba(TAB10_COLORS[idx % len(TAB10_COLORS)], alpha)
    if spec is None:
        return _hex_to_rgba(_next_color(), alpha)

    if isinstance(spec, (list, np.ndarray)):
        # Handle list/array: take first element
        if len(spec) > 0:
            spec = spec[0]
        else:
            spec = None

    if isinstance(spec, tuple):
        if len(spec) == 3:
            return (int(spec[0] * 255), int(spec[1] * 255), int(spec[2] * 255), a)
        elif len(spec) == 4:
            return (int(spec[0] * 255), int(spec[1] * 255), int(spec[2] * 255),
                    int(spec[3] * 255) if spec[3] <= 1.0 else int(min(spec[3], 255)))

    spec_lower = spec.lower().strip()

    if spec_lower in BASE_COLORS:
        return _hex_to_rgba(BASE_COLORS[spec_lower], alpha)

    if spec_lower in CSS4_COLORS:
        return _hex_to_rgba(CSS4_COLORS[spec_lower], alpha)

    if re.match(r'^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$', spec_lower):
        return _hex_to_rgba(spec_lower, alpha)

    return _hex_to_rgba(_next_color(), alpha)
