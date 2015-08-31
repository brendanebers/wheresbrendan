import mock
import unittest

from app.tasks import basic_geo


class BasicGeoTestCase(unittest.TestCase):

    def testCalculateDistance(self):
        distance = basic_geo.CalculateDistance((0, 0), (0, 0))
        self.assertEqual(distance, 0)

    def testCalculateBearing(self):
        bearing = basic_geo.CalculateBearing((0, 0), (1, 1))
        # Floats and spheres are weird
        self.assertAlmostEqual(bearing, 45, places=2)

    def testReadableBearing(self):
        compass = basic_geo.ReadableBearing(45)
        self.assertEqual(compass, 'NE')

    def testStoreDistanceTraversed(self):
        # TODO: Write these tests.
        patcher = mock.patch.multiple(
            basic_geo.model, GetLastPositions=mock.DEFAULT,
            GetPositionsByIds=mock.DEFAULT, autospec=True)
        patcher.start()
        self.addCleanup(patcher.stop)


_POS_1 = {'latitude': 0, 'longitude': 0, 'epoch': 0}
_POS_2 = {'latitude': 0, 'longitude': 0.8983153, 'epoch': 600}


class DeltasTestCase(unittest.TestCase):

    def testDelta_BasicInfo(self):
        delta = basic_geo._Deltas(_POS_1, _POS_2)
        self.assertAlmostEqual(delta.meters, 100000, places=2)
        self.assertEqual(delta.time, 600)
        self.assertAlmostEqual(delta.rate, 100000.0/600, places=2)

    def testDelta_UpdateRow(self):
        pos = _POS_2.copy()
        delta = basic_geo._Deltas(_POS_1, pos)
        delta.UpdateRow(pos)
        self.assertAlmostEqual(pos['distance_from_prev'], 100000, places=2)
        self.assertEqual(pos['time_from_prev'], 600)
        self.assertAlmostEqual(pos['speed_from_prev'], 100000.0/600, places=2)
