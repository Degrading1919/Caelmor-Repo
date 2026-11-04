"""Dependency-free sweep for planar, tapered, hewn rectangular members."""

import math


_EPS = 1e-9


def _vector(value, label):
    try:
        result = tuple(float(component) for component in value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be a finite 3D vector") from exc
    if len(result) != 3 or not all(math.isfinite(component) for component in result):
        raise ValueError(f"{label} must be a finite 3D vector")
    return result


def _dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0])


def _sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def _unit(vector, label):
    length = math.sqrt(_dot(vector, vector))
    if length <= _EPS:
        raise ValueError(f"{label} must have nonzero length")
    return tuple(component / length for component in vector)


def _dimensions(values, label, count):
    try:
        result = tuple(float(value) for value in values)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must contain one finite positive value per center") from exc
    if (len(result) != count or
            not all(math.isfinite(value) and value > _EPS for value in result)):
        raise ValueError(f"{label} must contain one finite positive value per center")
    return result


def sweep_member(buffer, centers, side, widths, depths, chamfer=0.12):
    """Append a closed octagonal swept member to ``buffer`` and return it.

    ``side`` is the constant plane normal and width direction. Widths and
    depths are full section dimensions at each exact center. ``chamfer`` is
    the clipped corner size as a fraction of the smaller section dimension.
    Center points must form a nondegenerate planar path perpendicular to side.
    """
    try:
        points = tuple(_vector(point, f"centers[{i}]") for i, point in enumerate(centers))
    except TypeError as exc:
        raise ValueError("centers must contain at least two finite 3D points") from exc
    if len(points) < 2:
        raise ValueError("centers must contain at least two finite 3D points")
    normal = _unit(_vector(side, "side"), "side")
    width_values = _dimensions(widths, "widths", len(points))
    depth_values = _dimensions(depths, "depths", len(points))
    try:
        chamfer = float(chamfer)
    except (TypeError, ValueError) as exc:
        raise ValueError("chamfer must be a finite fraction in (0, 0.5)") from exc
    if not math.isfinite(chamfer) or not 0.0 < chamfer < 0.5:
        raise ValueError("chamfer must be a finite fraction in (0, 0.5)")
    if any(math.sqrt(_dot(_sub(points[i + 1], points[i]),
                          _sub(points[i + 1], points[i]))) <= _EPS
           for i in range(len(points) - 1)):
        raise ValueError("consecutive centers must be distinct")

    span = max(math.sqrt(_dot(_sub(point, points[0]), _sub(point, points[0])))
               for point in points)
    planar_tolerance = max(1e-7, span * 1e-7)
    if any(abs(_dot(_sub(point, points[0]), normal)) > planar_tolerance
           for point in points[1:]):
        raise ValueError("centers must lie in the plane perpendicular to side")

    tangents = []
    for i in range(len(points)):
        if i == 0:
            delta = _sub(points[1], points[0])
        elif i == len(points) - 1:
            delta = _sub(points[-1], points[-2])
        else:
            delta = _sub(points[i + 1], points[i - 1])
        tangents.append(_unit(delta, f"centerline tangent at section {i}"))

    rings = []
    for center, tangent, width, depth in zip(points, tangents, width_values, depth_values):
        # This basis obeys side x depth_axis = tangent, so the section polygon
        # below is counterclockwise as viewed along the path direction.
        depth_axis = _unit(_cross(tangent, normal), "in-plane depth axis")
        half_width, half_depth = width * 0.5, depth * 0.5
        cut = chamfer * min(width, depth)
        section = ((-half_width + cut, -half_depth),
                   ( half_width - cut, -half_depth),
                   ( half_width, -half_depth + cut),
                   ( half_width,  half_depth - cut),
                   ( half_width - cut,  half_depth),
                   (-half_width + cut,  half_depth),
                   (-half_width,  half_depth - cut),
                   (-half_width, -half_depth + cut))
        ring = []
        for along_side, along_depth in section:
            ring.append(tuple(center[k] + normal[k] * along_side
                              + depth_axis[k] * along_depth for k in range(3)))
        rings.append(ring)

    vertices = [point for ring in rings for point in ring]
    faces = [tuple(reversed(range(8))), tuple(range((len(rings) - 1) * 8, len(rings) * 8))]
    for section_index in range(len(rings) - 1):
        start, end = section_index * 8, (section_index + 1) * 8
        for corner in range(8):
            following = (corner + 1) % 8
            faces.append((start + corner, start + following,
                          end + following, end + corner))
    buffer.indexed(vertices, faces)
    return buffer


__all__ = ["sweep_member"]
