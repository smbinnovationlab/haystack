# -*- coding:utf-8 -*-

import re


def find_best_match(products, condition):
    """
    find the product matches the condition best in the products list
    :param products: list of product information
    :param condition: product name
    :return: price of the product matched best
    """
    condition = condition.lower().split(' ')
    ranks = []
    i = 0
    for p in products:
        rank = [i, 0]
        for c in condition:
            if re.match(re.compile(r'.*' + c + r'.*'), p.get('name').lower()):
                rank[1] += 1
        ranks.append(rank)

    ranks.sort(key=lambda x: x[1], reverse=True)
    return products[ranks[0][0]]
