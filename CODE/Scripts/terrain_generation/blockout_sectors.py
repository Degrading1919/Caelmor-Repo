"""Partition the planning sheet artwork on its existing metre grid."""
import base64
from copy import deepcopy
import csv
from dataclasses import dataclass
from functools import lru_cache
from io import BytesIO, StringIO
import math
import re
from xml.etree import ElementTree as ET

from matplotlib.path import Path as GeometryPath
from matplotlib.transforms import Bbox
import numpy as np
from PIL import Image
from resvg_py import svg_to_bytes


SVG = "http://www.w3.org/2000/svg"
XLINK = "http://www.w3.org/1999/xlink"
ET.register_namespace("", SVG)
ET.register_namespace("xlink", XLINK)
ET.register_namespace("inkscape", "http://www.inkscape.org/namespaces/inkscape")
GEOGRAPHIC_LAYERS = (
    "L01_terrain_base", "L02_planning_regions", "L03_landuse", "L04_envelopes", "L05_water",
    "L06_routes", "L07_capacity", "L08_grid", "L09_structures", "L10_conflicts", "L11_labels",
)
NUMBER = re.compile(r"-?\d+(?:\.\d+)?")
GRID_LINE = re.compile(r"M(\d+),(-?\d+) ([VH])(-?\d+)")


def tag(name):
    return f"{{{SVG}}}{name}"


@dataclass(frozen=True)
class Sector:
    column: int
    row: int
    size: int

    @property
    def id(self):
        return f"{chr(ord('A') + self.column)}{self.row + 1:02d}"

    @property
    def bounds(self):
        x, y = self.column * self.size, self.row * self.size
        return x, y, x + self.size, y + self.size

    @property
    def svg_bounds(self):
        west, south, east, north = self.bounds
        return west, -north, east, -south

    def pixels(self, height):
        west, south, east, north = self.bounds
        return west, height - north, east, height - south


def image_root(artwork, bounds):
    west, top, east, bottom = bounds
    width, height = east - west, bottom - top
    root = ET.Element(tag("svg"), width=str(width), height=str(height),
                      viewBox=f"{west} {top} {width} {height}", overflow="hidden")
    root.extend(artwork)
    return root


def in_frame(element, bounds):
    """Conservatively cull whole objects while preserving lines and dash phases."""
    if "transform" in element.attrib:
        return True
    kind = element.tag
    def attr(name, default=0):
        return float(element.get(name, default))

    if kind in (tag("circle"), tag("ellipse")):
        x, y = attr("cx"), attr("cy")
        rx, ry = (attr("r"), attr("r")) if kind == tag("circle") else (attr("rx"), attr("ry"))
        box = (x - rx, y - ry, x + rx, y + ry)
    elif kind == tag("rect"):
        x, y = attr("x"), attr("y")
        box = (x, y, x + attr("width"), y + attr("height"))
    elif kind in (tag("polyline"), tag("polygon")):
        return path_in_frame(element.get("points"), bounds, 4 * attr("stroke-width"), kind == tag("polygon"))
    elif kind == tag("text"):
        x, y, size = attr("x"), attr("y"), attr("font-size")
        # A generous font-independent bound keeps the original halo and glyphs.
        extent = size * (len(element.text or "") + 2)
        left = x if element.get("text-anchor") == "start" else x - extent
        right = x if element.get("text-anchor") == "end" else x + extent
        box = (left - size, y - 2 * size, right + size, y + size)
    else:
        return True
    return Bbox.from_extents(*bounds).padded(attr("stroke-width")).overlaps(Bbox.from_extents(*box))


def path_in_frame(coords, bounds, margin, filled=False):
    points = np.array([float(n) for n in NUMBER.findall(coords)]).reshape(-1, 2)
    return bool(GeometryPath(points).intersects_bbox(Bbox.from_extents(*bounds).padded(margin), filled=filled))


def select_artwork(element, bounds):
    if not in_frame(element, bounds):
        return None
    copy = ET.Element(element.tag, element.attrib)
    copy.text = element.text
    if element.tag == tag("defs"):
        return deepcopy(element)
    if element.tag == tag("image"):
        return crop_hillshade(copy, bounds)
    if element.get("data-elev-m") is not None:
        parts = element.get("d").split("M")[1:]
        visible = [part for part in parts if path_in_frame(part, bounds, 4)]
        if not visible:
            return None
        copy.set("d", " ".join("M" + part.strip() for part in visible))
    for child in element:
        selected = select_artwork(child, bounds)
        if selected is not None:
            copy.append(selected)
    # Keep the layer objects for editing, even where a layer has no feature.
    if element.tag == tag("g") and not len(copy) and element.get("id") not in GEOGRAPHIC_LAYERS:
        return None
    return copy


@lru_cache(maxsize=1)
def decoded_png(data):
    return Image.open(BytesIO(base64.b64decode(data.removeprefix("data:image/png;base64,"))))


def crop_hillshade(element, bounds):
    """Retain source texels at their exact coordinates, including a sampling halo."""
    key = f"{{{XLINK}}}href"
    image = decoded_png(element.get(key))
    x, y = float(element.get("x")), float(element.get("y"))
    dx = float(element.get("width")) / image.width
    dy = float(element.get("height")) / image.height
    west, top, east, bottom = bounds
    # Leave two texels for interpolation at the viewport edges.
    x0, y0 = max(0, math.floor((west - x) / dx) - 2), max(0, math.floor((top - y) / dy) - 2)
    x1 = min(image.width, math.ceil((east - x) / dx) + 2)
    y1 = min(image.height, math.ceil((bottom - y) / dy) + 2)
    element.set("x", str(x + x0 * dx))
    element.set("y", str(y + y0 * dy))
    element.set("width", str((x1 - x0) * dx))
    element.set("height", str((y1 - y0) * dy))
    data = base64.b64encode(png_bytes(image.crop((x0, y0, x1, y1)))).decode("ascii")
    element.set(key, f"data:image/png;base64,{data}")
    return element


def rasterize(svg):
    return Image.open(BytesIO(svg_to_bytes(svg_string=svg, background="#ffffff"))).convert("RGB")


def png_bytes(image):
    stream = BytesIO()
    image.save(stream, format="PNG", optimize=True)
    return stream.getvalue()


def artwork_layers(sheet):
    root = ET.fromstring(sheet)
    layers = {child.get("id"): child for child in root}
    return [root.find(tag("defs")), *(layers[name] for name in GEOGRAPHIC_LAYERS), layers["L12_frame"]]


def validate_quadrants(grid_layer, sector, quadrant, width, height):
    cells = grid_layer.find(f".//*[@id='grid_cells_{quadrant}m']")
    major = grid_layer.find(f".//*[@id='grid_sectors_{sector.size}m']")
    west, top, east, bottom = sector.svg_bounds
    for element, step, internal_only in ((cells, quadrant, True), (major, sector.size, False)):
        lines = {(int(x), int(y), axis, int(end)) for x, y, axis, end in GRID_LINE.findall(element.get("d"))}
        for x in range(west, east + 1, step):
            if (internal_only and x % sector.size) or (not internal_only and 0 < x < width):
                if not any(start == x and axis == "V" and y >= bottom and end <= top
                           for start, y, axis, end in lines):
                    raise ValueError(f"Missing {step} m vertical grid line in {sector.id}.")
        for y in range(top, bottom + 1, step):
            if (internal_only and y % sector.size) or (not internal_only and -height < y < 0):
                if not any(start == y and axis == "H" and x <= west and end >= east
                           for x, start, axis, end in lines):
                    raise ValueError(f"Missing {step} m horizontal grid line in {sector.id}.")


def centerlines(elements):
    """Identity and unshifted source points for seam-relevant linework."""
    for layer in elements:
        identity = layer.get("id")
        if identity == "L01_terrain_base":
            for path in layer.iter(tag("path")):
                for component in path.get("d").split("M")[1:]:
                    yield identity, path.get("data-elev-m"), component.strip()
        elif identity in ("L03_landuse", "L05_water", "L06_routes"):
            for line in layer.iter(tag("polyline")):
                yield identity, line.get("id"), line.get("points")


def validate_seams(artwork, sector_lines, size, columns, rows):
    lines = [(key, GeometryPath(np.array([float(n) for n in NUMBER.findall(key[2])]).reshape(-1, 2)))
             for key in set(centerlines(artwork))]
    count = 0
    crossing_count = 0
    for row in range(rows):
        for column in range(columns):
            a = Sector(column, row, size)
            west, top, east, bottom = a.svg_bounds
            neighbors = []
            if column + 1 < columns:
                neighbors.append((Sector(column + 1, row, size), (east, top, east, bottom)))
            if row + 1 < rows:
                neighbors.append((Sector(column, row + 1, size), (west, top, east, top)))
            for b, edge in neighbors:
                border = Bbox.from_extents(*edge).padded(1e-6)
                expected = {key for key, line in lines if line.intersects_bbox(border, filled=False)}
                if not expected.issubset(sector_lines[a.id] & sector_lines[b.id]):
                    raise ValueError(f"Source linework changed along the {a.id}/{b.id} seam.")
                count += 1
                crossing_count += len(expected)
    return count, crossing_count


def index_row(sector, controls, verification, regions, labels, svg):
    west, south, east, north = sector.bounds
    width = controls["world"]["width_m"]
    height = controls["world"]["height_m"]
    ids = {node.get("id", "") for node in svg.iter()}
    sites = []
    for site in controls["settlements"]:
        if f'envelope_{site["id"]}' in ids:
            sites.append(site["name"])
    named_points = [(labels[site["id"]][2], (site["xy"][0] * width, site["xy"][1] * height))
                    for site in controls["landmark_anchors"] if labels[site["id"]][2]]
    node_names = {"hollow_lock_inlet": "Hollow Lock", "weir_up": "Bramblelock Weir / Relief Cut mouth",
                  "mill_forebay": "Drowsebank wheel drop", "uphill_canal_foot": "Uphill Canal foot pool",
                  "uphill_canal_cistern": "Uphill Canal cistern"}
    named_points.extend((node_names[node["id"]], (node["xy"][0] * width, node["xy"][1] * height))
                        for node in controls["hydrology"]["nodes"] if node["id"] in node_names)
    named_points.extend((f'Unbuilt {route["id"].replace("_", " ")} crossing ({crossing["reach"].replace("_", " ")})', crossing["xy_m"])
                        for route in verification["routes"] for crossing in route["crossings"])
    anchors = [name for name, (x, y) in named_points if west <= x <= east and south <= y <= north]
    reaches = [reach["id"].replace("_", " ") for reach in controls["hydrology"]["reaches"]
               if f'reach_{reach["id"]}' in ids]
    routes = [route["id"].replace("_", " ") for route in controls["routes"] if f'route_{route["id"]}' in ids]
    region_names = [key + " " + name for key, name, *_ in regions if f"region_{key}" in ids]
    if any(reach.startswith("relief cut ") for reach in reaches):
        region_names.append("E Relief Cut Engineering Line")
    overlays = [name for identity, name in (("stillwater_fen", "Stillwater Fen"),
                   ("floodplain_orchards", "Floodplain Orchards"), ("orchard_drainage_apron", "Orchard drainage apron"))
                if identity in ids]
    conflicts = sorted(node.get("id")[4:] for node in svg.iter(tag("g"))
                       if node.get("id", "").startswith("tag_") and node.find(tag("rect")) is not None)
    return {
        "sector_id": sector.id, "column": chr(ord("A") + sector.column), "row": f"{sector.row + 1:02d}",
        "x_min_m": west, "y_min_m": south, "x_max_m": east, "y_max_m": north,
        "width_m": sector.size, "height_m": sector.size,
        "center_x_m": (west + east) / 2, "center_y_m": (south + north) / 2,
        "planning_regions": " | ".join(region_names), "settlement_envelopes": " | ".join(sites),
        "named_points": " | ".join(anchors), "water_reaches": " | ".join(reaches),
        "routes": " | ".join(routes), "overlays": " | ".join(overlays), "conflict_tags": " | ".join(conflicts),
    }


def export_sectors(sheet, controls, verification, regions, labels, destination, size, quadrant):
    width, height = (controls["world"][key] for key in ("width_m", "height_m"))
    artwork = artwork_layers(sheet)
    master = rasterize(sheet)
    west, top, *_ = map(int, ET.fromstring(sheet).get("viewBox").split())
    master_frame = master.crop((-west, -height - top, width - west, -top))

    artifacts, rows, sector_lines = {}, [], {}
    mosaic = Image.new("RGB", (width, height))
    max_changed_fraction = 0.0
    max_mean_error = 0.0
    for row in range(height // size):
        for column in range(width // size):
            sector = Sector(column, row, size)
            bounds = sector.svg_bounds
            selected = [element for item in artwork if (element := select_artwork(item, bounds)) is not None]
            root = image_root(selected, bounds)
            west, south, east, north = sector.bounds
            root.insert(0, ET.Element(tag("title")))
            root[0].text = f"Lowmark Vale {sector.id}"
            root.insert(1, ET.Element(tag("desc")))
            root[1].text = (f"World metres X {west}–{east}, Y {south}–{north}. SVG (X, −Y). "
                            f"SW offset ({west}, {south}). Quadrants {quadrant} m. North is up.")
            svg = ET.tostring(root, encoding="unicode")
            validate_quadrants(root.find("./*[@id='L08_grid']"), sector, quadrant, width, height)
            box = sector.pixels(height)
            pixels = master_frame.crop(box)
            rendered = rasterize(svg)
            if pixels.size != rendered.size or rendered.size != (size, size):
                raise ValueError(f"Invalid PNG or SVG dimensions for {sector.id}.")
            diff = np.abs(np.asarray(pixels, dtype=np.int16) - np.asarray(rendered, dtype=np.int16))
            changed = float(np.any(diff, axis=2).mean())
            mean_error = float(diff.mean())
            max_changed_fraction = max(max_changed_fraction, changed)
            max_mean_error = max(max_mean_error, mean_error)
            if changed > .025 or mean_error > .15:
                raise ValueError(f"Sector {sector.id} disagrees with the master artwork: "
                                 f"{changed:.3%} changed pixels, mean channel error {mean_error:.4f}.")
            artifacts[f"{sector.id}.svg"] = svg.encode("utf-8")
            artifacts[f"{sector.id}.png"] = png_bytes(pixels)
            mosaic.paste(Image.open(BytesIO(artifacts[f"{sector.id}.png"])), box[:2])
            rows.append(index_row(sector, controls, verification, regions, labels, root))
            sector_lines[sector.id] = set(centerlines(root))

    if mosaic.tobytes() != master_frame.tobytes():
        raise ValueError("PNG mosaic contains an altered or missing master map pixel.")
    seams, crossings = validate_seams(artwork, sector_lines, size, width // size, height // size)
    table = StringIO(newline="")
    writer = csv.DictWriter(table, fieldnames=rows[0], lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    artifacts["grid_index.csv"] = table.getvalue().encode("utf-8")
    destination.mkdir(parents=True, exist_ok=True)
    for name, data in artifacts.items():
        (destination / name).write_bytes(data)
    print(f"CAELMOR_BLOCKOUT_SECTORS_VERIFIED sectors={len(rows)} size_m={size} quadrant_m={quadrant} "
          f"mosaic={width}x{height} pixel_mismatches=0 seams={seams} matching_linework={crossings} "
          f"svg_max_changed_fraction={max_changed_fraction:.6f} svg_max_mean_channel_error={max_mean_error:.6f}")
