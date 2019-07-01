import numpy as np
import pygeos
from pygeos import \
    LineString, LinearRing, Polygon, MultiPoint, MultiLineString,\
    MultiPolygon, GeometryCollection, box
import pytest

point_polygon_testdata = pygeos.points(np.arange(6), np.arange(6)), box(2, 2, 4, 4)

point = pygeos.points(2, 2)
line_string = LineString([[0, 0], [1, 0], [1, 1]])
linear_ring = LinearRing(((0, 0), (0, 1), (1, 1), (1, 0)))
polygon = Polygon(((0., 0.), (0., 2.), (2., 2.), (2., 0.), (0., 0.)))
multi_point = MultiPoint([[0.0, 0.0], [1.0, 2.0]])
multi_line_string = MultiLineString([[[0.0, 0.0], [1.0, 2.0]]])
multi_polygon = MultiPolygon([
        Polygon(((0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0))),
        Polygon(((0.1, 0.1), (0.1, 0.2), (0.2, 0.2), (0.2, 0.1))),
    ])
geometry_collection = GeometryCollection(
    [pygeos.points(51, -1), LineString([(52, -1), (49, 2)])]
)
point_z = pygeos.points(1.0, 1.0, 1.0)

# Y_b


def test_has_z():
    actual = pygeos.has_z([point, point_z])
    expected = [False, True]
    np.testing.assert_equal(actual, expected)

# YY_b


def test_disjoint():
    actual = pygeos.disjoint(*point_polygon_testdata)
    expected = [True, True, False, False, False, True]
    np.testing.assert_equal(actual, expected)


def test_touches():
    actual = pygeos.touches(*point_polygon_testdata)
    expected = [False, False, True, False, True, False]
    np.testing.assert_equal(actual, expected)


def test_intersects():
    actual = pygeos.intersects(*point_polygon_testdata)
    expected = [False, False, True, True, True, False]
    np.testing.assert_equal(actual, expected)


def test_within():
    actual = pygeos.within(*point_polygon_testdata)
    expected = [False, False, False, True, False, False]
    np.testing.assert_equal(actual, expected)


def test_contains():
    actual = pygeos.contains(*reversed(point_polygon_testdata))
    expected = [False, False, False, True, False, False]
    np.testing.assert_equal(actual, expected)

# Y_Y


def test_get_centroid():
    actual = pygeos.get_centroid(polygon)
    assert pygeos.equals(actual, pygeos.points(1, 1))


# Yi_Y


def test_get_point_n():
    actual = pygeos.get_point_n(line_string, np.int16(1))
    assert pygeos.equals(actual, pygeos.points(1, 0))


# Yd_Y


def test_simplify():
    line = LineString([[0, 0], [0.1, 1], [0, 2]])
    actual = pygeos.simplify(line, [0, 1.])
    assert pygeos.get_num_points(actual).tolist() == [3, 2]

# YY_Y


def test_intersection():
    poly1, poly2 = box(0, 0, 10, 10), box(5, 5, 20, 20)
    actual = pygeos.intersection(poly1, poly2)
    expected = box(5, 5, 10, 10)
    assert pygeos.equals(actual, expected)


def test_union():
    poly1, poly2 = box(0, 0, 10, 10), box(10, 0, 20, 10)
    actual = pygeos.union(poly1, poly2)
    expected = box(0, 0, 20, 10)
    assert pygeos.equals(actual, expected)

# Y_d


def test_area():
    assert pygeos.area(polygon) == 4.

# Y_B


def test_geom_type_id():
    all_types = (
        point,
        line_string,
        linear_ring,
        polygon,
        multi_point,
        multi_line_string,
        multi_polygon,
        geometry_collection,
    )
    assert pygeos.geom_type_id(all_types).tolist() == list(range(8))

# Y_i


def test_get_num_points():
    assert pygeos.get_num_points(line_string) == 3


# YY_d


def test_distance():
    actual = pygeos.distance(*point_polygon_testdata)
    expected = [2 * 2**0.5, 2**0.5, 0, 0, 0, 2**0.5]
    np.testing.assert_allclose(actual, expected)

# YY_d_2


def test_project():
    line = LineString([[0, 0], [1, 1], [2, 2]])
    points = pygeos.points([1, 3], [0, 3])
    actual = pygeos.project(line, points)
    expected = [0.5 * 2**0.5, 2 * 2**0.5]
    np.testing.assert_allclose(actual, expected)


# specials


def test_buffer():
    radii = np.array([1., 2.])
    actual = pygeos.buffer(point, radii, np.int16(16))
    assert pygeos.area(actual) == pytest.approx(np.pi * radii**2, rel=0.01)


def test_snap():
    line = LineString([[0, 0], [1, 0], [2, 0]])
    points = pygeos.points([0, 1], [1, 0.1])
    actual = pygeos.snap(points, line, 0.5)
    expected = pygeos.points([0, 1], [1, 0])
    assert pygeos.equals(actual, expected).all()


def test_equals_exact():
    point1 = pygeos.points(0, 0)
    point2 = pygeos.points(0, 0.1)
    actual = pygeos.equals_exact(point1, point2, [0.01, 1.])
    expected = [False, True]
    np.testing.assert_equal(actual, expected)


# construction

def test_construct_from_tuples():
    actual = pygeos.points([[0, 0], [2, 2]])
    assert pygeos.equals(actual[1], point)


def test_construct_point():
    actual = pygeos.points(2, [0, 1, 2])
    assert pygeos.equals(actual[2], point)


def test_construct_point_z():
    actual = pygeos.points(1, 1, [0, 1, 2])
    assert pygeos.equals(actual[1], point_z)


def test_construct_point_invalid_dim():
    with pytest.raises(RuntimeError):
        pygeos.points([0, 1, 2, 3])
