import xml.etree.ElementTree as ET
from collections import Counter

import networkx as nx
from networkx.algorithms.shortest_paths.generic import shortest_path
from networkx.classes.function import path_weight


def calc_distance_to_cabinet(source, target):
    """Calculate the distance between two points in network"""
    G = nx.read_graphml(file)

    path = shortest_path(G, source=source, target=target, weight="length")
    path_length = path_weight(G, path, weight="length")

    return path_length

def calc_network(rate_card, file):
    """Takes in a rate card and GraphML XML file and returns the total cost of network"""
    tree = ET.parse(file)
    root = tree.getroot()

    nodes = {}
    for element in root.iter('node'):
        type = element.find('data').text
        id = element.attrib['id']
        nodes[id] = type
    # print(items)

    trench_data = []
    trench_costs = []
    for element in root.iter('edge'):
        source_id = element.attrib['source']
        target_id = element.attrib['target']
        source_name = nodes[source_id]
        target_name = nodes[target_id]
        for data in element.iter('data'):
            if data.attrib['key'] == 'material':
                material = data.text
            elif data.attrib['key'] == 'length':
                length = data.text

        trench_cost = rate_card[material] * int(length)
        trench_costs.append(trench_cost)

        branch = {
                'source_id': source_id,
                'source_name': source_name,
                'target_id': target_id,
                'target_name': target_name,
                'material': material,
                'length': length,
                'cost': trench_cost
                }

        trench_data.append(branch)

    # Append distance from pots to cabinet
    for trench in trench_data:
        if trench['source_name'] == 'Cabinet':
            cab_id = trench['source_id']

    for trench in trench_data:
        if trench['source_name'] == 'Pot':
            cab_dist = calc_distance_to_cabinet(trench['source_id'],  cab_id)
            trench['dist_to_cab'] = cab_dist

    # print(trench_data)

    # Fixed Item Costs
    item_count = Counter(nodes.values())
    total_cabinet_cost = item_count['Cabinet'] * rate_card['Cabinet']
    total_chamber_cost = item_count['Chamber'] * rate_card['Chamber']
    if rate_card['fixed_pot'] == True:
        total_pot_cost = item_count['Pot'] * rate_card['Pot']
    else:
        pot_costs = []
        for trench in trench_data:
            if trench['source_name'] == 'Pot':
                pot_cost = trench['dist_to_cab'] * rate_card['Pot']
                pot_costs.append(pot_cost)
        total_pot_cost = sum(pot_costs)

    item_costs = [total_cabinet_cost, total_chamber_cost, total_pot_cost]
    # print(item_costs)
    # print(trench_costs)
    total_cost = sum(item_costs) + sum(trench_costs)

    return total_cost


if __name__ == "__main__":

    file = 'problem.graphml'
    rate_card_a = {
        'Cabinet': 1000,
        'verge': 50,
        'road': 100,
        'Chamber': 200,
        'Pot': 100,
        'fixed_pot': True,
    }

    rate_card_b = {
        'Cabinet': 1200,
        'verge': 40,
        'road': 80,
        'Chamber': 200,
        'Pot': 20,
        'fixed_pot': False,
    }

    total_network_cost_a = calc_network(rate_card_a, file)
    total_network_cost_b = calc_network(rate_card_b, file)

    print(f'Total Network Cost (Rate Card A):', total_network_cost_a)
    print('')
    print(f'Total Network Cost (Rate Card B):', total_network_cost_b)
