import unittest
from collections import Counter

from servers import ListServer, Product, Client, MapServer, TooManyProductsFoundError

server_types = (ListServer, MapServer)


class ServerTest(unittest.TestCase):

    def test_get_entries_returns_proper_entries(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual(Counter([products[2], products[1]]), Counter(entries))

    def test_sorted(self):
        products_sort = [Product('aa11', 1), Product('aa13', 3), Product('aa12', 2)]
        for server_type in server_types:
            server = server_type(products_sort)
            entries = server.get_entries(2)
            self.assertEqual(products_sort[0].price, entries[0].price)
            self.assertEqual(products_sort[2].price, entries[1].price)
            self.assertEqual(products_sort[1].price, entries[2].price)

    def test_sorted2(self):
        products_sort = [Product('aa11', 1), Product('aa13', 3), Product('aa12', 2)]
        for server_type in server_types:
            server = server_type(products_sort)
            entries = server.get_entries(2)
            self.assertListEqual([products_sort[0], products_sort[2], products_sort[1]], entries)

    def test_error(self):
        products = [Product('aa11', 1), Product('aa13', 3), Product('aa12', 2), Product('aa15', 5), Product('aa14', 4)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual([], entries)


class ClientTest(unittest.TestCase):
    def test_total_price_for_normal_execution(self):
        products = [Product('PP234', 2), Product('PP235', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(5, client.get_total_price(2))

    def test_price_error(self):
        products = [Product('aa11', 1), Product('aa13', 3), Product('aa12', 2), Product('aa15', 5), Product('aa14', 4)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(None, client.get_total_price(2))

    def test_price_not_found(self):
        products = [Product('aa11', 1), Product('aa13', 3), Product('aa12', 2)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(None, client.get_total_price(3))

    def test_get_total_price(self):
        products = [Product('PP234', 2), Product('PP235', 3), Product('PP236', 4), Product('PP237', 5)]
        client = Client(ListServer(products))
        self.assertEqual(client.get_total_price(2), None)
        client1 = Client(ListServer(products[:3]))
        self.assertEqual(client1.get_total_price(2), 9)
        client3 = Client(ListServer([Product('A12', 2), Product('ab1', 3), Product('Ab1234', 4)]))
        self.assertEqual(client3.get_total_price(2), None)


if __name__ == '__main__':
    unittest.main()