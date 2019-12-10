# Joanna Reszka 302907
# Sabina Psarska 302903
#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Optional, List, Dict
from abc import ABC, abstractmethod
from typing import TypeVar


class Product:

    def __init__(self, name: str, price: float) -> None:
        self.name = name
        self.price = price

    def __hash__(self):
        return hash((self.name, self.price))

    def __eq__(self, other):
        return self.name == other.name and self.price == other.price


class TooManyProductsFoundError(Exception):
    pass


class Server(ABC):
    n_max_returned_entries = 3

    def get_entries(self, n_letters: int = 1) -> List[Product]:
        try:
            result = []
            for product in self._get_all_products():

                act_letters = 0
                act_numbers = 0

                for s in product.name:
                    act_letters += 1
                    if s in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                        act_letters -= 1
                        act_numbers += 1

                if act_letters == n_letters and 2 <= act_numbers <= 3:
                    result.append(product)

            if len(result) > self.n_max_returned_entries:
                raise TooManyProductsFoundError

            result = sorted(result, key=lambda prod: prod.price)
            return result
        except TooManyProductsFoundError:
            return []

    @abstractmethod
    def _get_all_products(self) -> List[Product]:
        raise NotImplementedError()


class ListServer(Server):

    def __init__(self, products: List[Product], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.products = products

    def _get_all_products(self) -> List[Product]:
        return self.products


class MapServer(Server):

    def __init__(self, products: List[Product], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        dict_products = {}
        for product in products:
            dict_products[product.name] = product
        self.products = dict_products

    def _get_all_products(self) -> List[Product]:
        products_list = []

        for name, product in self.products.items():
            products_list.append(product)

        return products_list


EveryServer = TypeVar('EveryServer', bound=Server)


class Client:

    def __init__(self, client_server: EveryServer):
        super().__init__()
        self.client_server = client_server

    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        products = self.client_server.get_entries(n_letters)
        if not products:
            return None
        sum_of_prices = 0
        for one_product in products:
            sum_of_prices += one_product.price
        return sum_of_prices
