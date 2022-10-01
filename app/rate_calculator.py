import networkx as nx
from networkx.algorithms.shortest_paths.generic import shortest_path
from networkx.classes.function import path_weight

from collections import Counter


def calc_distance_to_cabinet(source, target, graph):
    """Calculate the distance between two points in network"""
    path = shortest_path(graph, source=source, target=target, weight="length")
    path_length = path_weight(graph, path, weight="length")

    return path_length


def calc_network(rate_card, file):
    """Calculate Network Cost by rate card"""
    G = nx.read_graphml(file)

    #  Use the Edge data to calculate the trench costs
    trench_costs = []
    for node1, node2, data in G.edges(data=True):
        trench_cost = rate_card[data['material']] * data['length']
        trench_costs.append(trench_cost)

    #  Use the Node data to count the number
    #  of items and identify the Pots and Cabinet
    items = []
    pots = []
    for node in G.nodes(data=True):
        items.append(node[1]['type'])
        if node[1]['type'] == 'Pot':
            pots.append(node[0])
        if node[1]['type'] == 'Cabinet':
            cabinet_id = node[0]

    item_count = Counter(items)

    #  Calculate the total chamber and cabinet cost
    total_cabinet_cost = item_count['Cabinet'] * rate_card['Cabinet']
    total_chamber_cost = item_count['Chamber'] * rate_card['Chamber']

    #  Check if the pot cost is fixed or based
    #  on distance to cabinet then calculate costs
    if rate_card['fixed_pot']:
        total_pot_cost = item_count['Pot'] * rate_card['Pot']
    else:
        pot_costs = []
        for pot in pots:
            dist_to_cab = calc_distance_to_cabinet(cabinet_id, pot, G)
            pot_cost = dist_to_cab * rate_card['Pot']
            pot_costs.append(pot_cost)
            total_pot_cost = sum(pot_costs)

    #  Calculate total items costs and sum with trench costs to give total cost
    item_costs = [total_cabinet_cost, total_chamber_cost, total_pot_cost]
    total_cost = sum(item_costs) + sum(trench_costs)

    return total_cost


if __name__ == "__main__":

    graph_file = 'files/problem.graphml'
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

    total_network_cost_a = calc_network(rate_card_a, graph_file)
    total_network_cost_b = calc_network(rate_card_b, graph_file)

    print('Total Network Cost (Rate Card A): £{:,.2f}'
            .format(total_network_cost_a))
    print('')
    print('Total Network Cost (Rate Card B): £{:,.2f}'
            .format(total_network_cost_b))
