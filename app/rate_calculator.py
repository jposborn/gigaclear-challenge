import networkx as nx
from networkx.algorithms.shortest_paths.generic import shortest_path
from networkx.classes.function import path_weight
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout
from collections import Counter


def calc_distance_to_cabinet(source, target, g):
    """Calculate the distance between two points in network"""
    path = shortest_path(g, source=source, target=target, weight="length")
    path_length = path_weight(g, path, weight="length")

    return path_length


def calc_network(rate_card, file):
    """Calculate Network Cost by rate card"""
    G = nx.read_graphml(file)

    #  Use the Edge data to calculate the trench costs
    trench_costs = []
    for node1, node2, data in G.edges(data=True):
        trench_cost = rate_card[data['material'].lower()] * data['length']
        trench_costs.append(trench_cost)

    #  Use the Node data to count the number
    #  of items and identify the Pots and Cabinet
    items = []
    node_labels = {}
    pots = []
    node_colors = []
    for node in G.nodes(data=True):
        items.append(node[1]['type'])
        if node[1]['type'] == 'Pot':
            pots.append(node[0])
            node_colors.append('Yellow')
        if node[1]['type'] == 'Cabinet':
            cabinet_id = node[0]
            node_colors.append('Red')
        if node[1]['type'] == 'Chamber':
            node_colors.append('Blue')
        node_labels[node[0]] = node[1]['type'][0:3].upper()

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

    draw_diagram(G, node_labels, node_colors)

    return total_cost


def draw_diagram(g, node_labels, node_colors):
    pos = graphviz_layout(g, prog="dot")
    edge_label_length = nx.get_edge_attributes(g, 'length')
    edge_label_material = nx.get_edge_attributes(g, 'material')

    # # Build Edge Labels from material * length
    # edge_labels = {edge: (edge_label_material[edge] + '\n(' + str(edge_label_length[edge])) + 'm)'
    #                for edge in edge_label_material}

    edge_labels = {}
    edge_colors = []
    for edge in edge_label_material:
        label = edge_label_material[edge] + '\n(' + str(edge_label_length[edge]) + 'm)'
        if edge_label_material[edge] == 'verge':
            color = 'Green'
        else:
            color = "Black"
        edge_labels.update({edge: label})
        edge_colors.append(color)


    # node_labels = nx.get_node_attributes(g, 'type')
    #  nx.draw_networkx(g, pos, labels=node_labels, node_size=1000, node_color=node_colors)
    nx.draw_networkx_nodes(g, pos, node_size=1000, node_color=node_colors, edgecolors='Black')
    nx.draw_networkx_labels(g, pos, labels=node_labels)
    nx.draw_networkx_edges(g, pos, edge_color=edge_colors, width=3)
    nx.draw_networkx_edge_labels(g, pos, edge_labels=edge_labels)
    plt.show()
    return


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

    print(
        'Total Network Cost (Rate Card A): £{:,.2f}'
        .format(total_network_cost_a)
        )
    print('')
    print(
        'Total Network Cost (Rate Card B): £{:,.2f}'
        .format(total_network_cost_b)
        )

