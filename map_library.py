"""Versioned, explicit authored arenas; none is a verified DX reconstruction.

Geometry uses lane center-lines, not wall-fill pixels. Rendering and collision
consume the same cells. Map edits are data edits, independent of presentation.
"""
from dataclasses import dataclass
from functools import lru_cache
import json
from pathlib import Path


@dataclass(frozen=True)
class MapSpec:
    id: str
    revision: int
    name: str
    accent: tuple
    cols: int
    rows: int
    lanes: frozenset
    entries: tuple
    spawns: tuple
    portals: tuple
    den: tuple
    provenance: str


def parse_catalog(document):
    """Reject malformed geometry before it can enter a playable match."""
    if document.get('schema_version') != 1:
        raise ValueError('Unsupported map catalog schema')
    specs = []
    ids = set()
    for raw in document.get('maps', []):
        ident = raw['id']
        if not ident or ident in ids:
            raise ValueError('Map IDs must be unique and nonempty')
        ids.add(ident)
        grid = raw['lane_rows']
        cols, rows = raw['cols'], raw['rows']
        if cols < 3 or rows < 3 or len(grid) != rows or any(len(row) != cols for row in grid):
            raise ValueError(f'{ident}: invalid grid dimensions')
        if any(ch not in '#.' for row in grid for ch in row):
            raise ValueError(f'{ident}: unsupported lane glyph')
        lanes = frozenset((x, y) for y, row in enumerate(grid) for x, ch in enumerate(row) if ch == '.')
        entries = tuple(tuple(c) for c in raw['entries'])
        spawns = tuple(tuple(c) for c in raw['spawns'])
        portals = tuple(raw['portals'])
        if len(entries) != 8 or len(spawns) != 8 or len(set(spawns)) != 8:
            raise ValueError(f'{ident}: must have eight distinct stations')
        if len(set(entries)) != 8 or not set(entries) <= lanes or set(spawns) & lanes:
            raise ValueError(f'{ident}: invalid station entry')
        for entry, spawn in zip(entries, spawns):
            if len(entry) != 2 or len(spawn) != 2 or any(type(n) is not int for n in entry + spawn):
                raise ValueError(f'{ident}: invalid station coordinate')
            if not (0 <= spawn[0] < cols and spawn[1] in (0, rows - 1)):
                raise ValueError(f'{ident}: station must be on top/bottom border')
            if abs(entry[0] - spawn[0]) + abs(entry[1] - spawn[1]) != 1:
                raise ValueError(f'{ident}: station must touch its entry')
        if len(portals) != len(set(portals)) or any(type(y) is not int or not 0 < y < rows-1 for y in portals):
            raise ValueError(f'{ident}: invalid portal row')
        if any((0, y) not in lanes or (cols-1, y) not in lanes for y in portals):
            raise ValueError(f'{ident}: unpaired tunnel')
        if any(y in (0, rows-1) or (x in (0, cols-1) and y not in portals) for x, y in lanes):
            raise ValueError(f'{ident}: undeclared border exit')
        seen, todo = {entries[0]}, [entries[0]]
        while todo:
            x, y = todo.pop()
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nxt = (x + dx, y + dy)
                if y in portals and nxt[0] in (-1, cols):
                    nxt = (nxt[0] % cols, y)
                if nxt in lanes and nxt not in seen:
                    seen.add(nxt)
                    todo.append(nxt)
        if seen != lanes:
            raise ValueError(f'{ident}: disconnected lane graph')
        if any({(x+1, y), (x, y+1), (x+1, y+1)} <= lanes for x, y in lanes):
            raise ValueError(f'{ident}: multiple parallel dot lanes in open square')
        for x, y in lanes:
            neighbors = {(x, y-1), (x, y+1), (x-1, y), (x+1, y)}
            if y in portals and x in (0, cols-1):
                neighbors.add(((x-1) % cols if x == 0 else (x+1) % cols, y))
            if len(neighbors & lanes) < 2:
                raise ValueError(f'{ident}: unintended corridor dead end')
        den = tuple(raw['den'])
        if len(den) != 4 or any(type(n) is not int for n in den):
            raise ValueError(f'{ident}: invalid ghost house')
        x, y, width, height = den
        if width < 1 or height < 1 or x < 0 or y < 0 or x+width > cols or y+height > rows:
            raise ValueError(f'{ident}: ghost house outside field')
        if any((xx, yy) in lanes for xx in range(x, x+width) for yy in range(y, y+height)):
            raise ValueError(f'{ident}: ghost house overlaps public lanes')
        # Each authored map promises a playable one-line route around its house.
        # This prevents new layouts from recreating the cyan merged-wall defect.
        # The two-cell inset is our geometry convention, not a recovered DX size.
        left, right, top, bottom = x-2, x+width+1, y-2, y+height+1
        perimeter = ({(xx, yy) for xx in (left, right) for yy in range(top, bottom+1)} |
                     {(xx, yy) for xx in range(left, right+1) for yy in (top, bottom)})
        if not perimeter <= lanes:
            raise ValueError(f'{ident}: incomplete ghost-house perimeter route')
        accent = tuple(raw['accent'])
        if len(accent) != 3 or any(type(v) is not int or not 0 <= v <= 255 for v in accent):
            raise ValueError(f'{ident}: invalid accent')
        specs.append(MapSpec(ident, raw['revision'], raw['name'], accent, cols, rows,
                             lanes, entries, spawns, portals, den, raw['provenance']))
    if not specs:
        raise ValueError('Empty map catalog')
    return tuple(specs)


@lru_cache(maxsize=1)
def catalog():
    return parse_catalog(json.loads(Path(__file__).with_name('maps.json').read_text(encoding='utf-8')))


def get_map(index):
    return catalog()[index % len(catalog())]


def next_map_index(current, mode='cycle', rng=None):
    """Configurable adaptation policies, not asserted commercial progression."""
    count = len(catalog())
    if mode == 'repeat':
        return current % count
    if mode == 'cycle':
        return (current + 1) % count
    if mode == 'random':
        if rng is None:
            raise ValueError('Random progression requires the match seeded RNG')
        return rng.randrange(count)
    raise ValueError(f'Unknown progression mode: {mode}')
