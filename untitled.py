import json
import networkx as nx

# Read data from the JSON file
with open('output.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Create a directed graph
G = nx.DiGraph()

# Helper function to add a node if it doesn't exist
def add_node_if_not_exists(graph, node_name, label=None, pos=None):
    if node_name not in graph.nodes:
        graph.add_node(node_name, label=label, pos=pos)

# Add nodes and edges based on the data
for word, info in data.items():
    # Add English node
    add_node_if_not_exists(G, word, label="English")

    # Add Nepali node
    nepali_node_name = f"{word}"
    add_node_if_not_exists(G, nepali_node_name, label="Nepali")

    # Connect English to Nepali bidirectionally with label "translation"
    G.add_edge(word, nepali_node_name, label="translation")
    G.add_edge(nepali_node_name, word, label="translation")

    # Add edges for translations (bidirectional) with label "translation"
    for translation in info.get("translation", []):
        add_node_if_not_exists(G, translation, label="English")
        G.add_edge(word, translation, label="translation")
        G.add_edge(translation, word, label="translation")

    # Add edges for synonyms (bidirectional) with label "synonym"
    for synonym in info.get("synonym", []):
        add_node_if_not_exists(G, synonym, label="Nepali")
        G.add_edge(word, synonym, label="synonym")
        G.add_edge(synonym, word, label="synonym")

    # Add edges for pos (unidirectional) with label "pos"
    pos_values = info.get("pos", [])
    for pos_value in pos_values:
        pos_string = str(pos_value)
        add_node_if_not_exists(G, pos_string, label="POS")
        G.add_edge(word, pos_string, label="pos")

    # Add edges for category (unidirectional) with label "category"
    for category in info.get("category", []):
        add_node_if_not_exists(G, category, label="Nepali")
        G.add_edge(word, category, label="category")

# Convert node attributes to strings
for node, data in G.nodes(data=True):
    for key, value in data.items():
        data[key] = str(value)

# Write the graph to GraphML
nx.write_graphml(G, "output.graphml")
print("GraphML file created successfully.")
