import unittest

from offers.models import Offer
from offers.parse import parse_capacity_tb, parse_kind, parse_form
from offers.sources import SampleSource


class ParseTests(unittest.TestCase):
    def test_capacity(self):
        self.assertEqual(parse_capacity_tb("Seagate 4TB"), 4)
        self.assertEqual(parse_capacity_tb("WD 500 GB"), 0.5)
        self.assertEqual(parse_capacity_tb("Disco 1,5 TB"), 1.5)
        self.assertIsNone(parse_capacity_tb("Cavo SATA"))

    def test_kind_form(self):
        self.assertEqual(parse_kind("Crucial P3 NVMe"), "SSD")
        self.assertEqual(parse_kind("WD Red Plus 6TB NAS"), "NAS")
        self.assertEqual(parse_form("WD Elements esterno"), "esterno")

    def test_derived_fields(self):
        d = Offer.build("x", "Disco 4TB", 80, "u", original_price=100).to_dict()
        self.assertEqual(d["price_per_tb"], 20.0)
        self.assertEqual(d["discount_pct"], 20.0)

    def test_sample_search(self):
        self.assertTrue(all("seagate" in o.title.lower() for o in SampleSource().search("seagate")))


if __name__ == "__main__":
    unittest.main()
