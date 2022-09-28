import xml.etree.ElementTree as ET
from collections import Counter

def calc_network(rate_card, file):
    tree = ET.parse(file)
    root = tree.getroot()

    items = {}
    for element in root.iter('node'):
        type = element.find('data').text
        id = element.attrib['id']
        items[id] = type

    # print(items)
    trench_data = []
    trench_costs = []
    for element in root.iter('edge'):
        source_id = element.attrib['source']
        target_id = element.attrib['target']
        source_name = items[source_id]
        target_name = items[target_id]
        for data in element.iter('data'):
            if data.attrib['key'] == 'material':
                material = data.text
            elif data.attrib['key'] == 'length':
                length = data.text

        trench_cost = rate_card[material] * int(length)
        trench_costs.append(trench_cost)

        data = {'source_id': source_id, 'source_name': source_name, 'target_id': target_id, 'target_name': target_name, 'material': material, 'length': length, 'cost': trench_cost}
        trench_data.append(data)

        #print(source_id, source_name, target_id, target_name, material, length, trench_cost)

    print(trench_data)

    # trench_data = calc_distance_to_cabinet(trench_data)

    item_count = Counter(items.values())
    cabinet_cost = item_count['Cabinet'] * rate_card['Cabinet']
    chamber_cost = item_count['Chamber'] * rate_card['Chamber']
    if rate_card['fixed_pot'] == True:
        pot_cost = item_count['Pot'] * rate_card['Pot']
    else:
        pot_cost = 0

    item_costs = [cabinet_cost, chamber_cost, pot_cost]
    print(trench_costs)
    print(item_costs)

    total_cost = sum(item_costs) + sum(trench_costs)

    return total_cost

# def calc_distance_to_cabinet(trench_data):

#     for data in trench_data:
#         if data['source_name'] == 'Chamber' and data['target_name'] == 'Chamber':

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

total_network_cost = calc_network(rate_card_a, file)

print(f'Total cost:', total_network_cost)
