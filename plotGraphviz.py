import IPython.display
import pydotplus as pydot
import os
import csv

# How To Plot Unix Directory Structure Using Python Graphviz
# https://www.nbshare.io/notebook/745848606/How-To-Plot-Unix-Directory-Structure-Using-Python-Graphviz/
from IPython.core.display import Image
from IPython.core.display_functions import display


def plot_dirs_example():
    rootdir = "E:\\prog\\python\\plot-tree-data\\share\\man"
    # rootdir = "/Users/daniel.alonso/ecedago/scripts/batch-decrypter"

    G = pydot.Dot(graph_type="digraph")
    node = pydot.Node(rootdir, label=rootdir.split("/")[-1], style="filled", fillcolor="green")
    G.add_node(node)
    for root, dirs, files in os.walk(rootdir):
        node = pydot.Node(root, label=root.split("/")[-1], style="filled", fillcolor="green")
        G.add_node(node)
        for subdir in dirs:
            nodeId = root+os.sep+subdir
            # print("{}\t\t\t{}\t\t\t{}".format(nodeId, root, subdir))
            node = pydot.Node(nodeId, label=subdir, style="filled", fillcolor="green")
            G.add_node(node)
            edge = pydot.Edge(root, nodeId)
            G.add_edge(edge)

        for file in files:
            nodeId = root + os.sep + subdir + os.sep + file
            # print("{}\t\t\t{}\t\t\t{}".format(nodeId, from_node, file))
            node = pydot.Node(nodeId, label=file, style="filled", fillcolor="yellow")
            G.add_node(node)
            edge = pydot.Edge(root, nodeId)
            G.add_edge(edge)

    img = Image(G.create_png())
    display(img)

    G.write("output_example.png", format='png')


def read_csv(graph, csvDatfile):
    with open(csvDatfile, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            # print("line_count:{}".format(line_count))
            type = row["type"]
            name = row["name"].lower()
            path = row["path_with_namespace"].lower()
            archived = row["archived"]
            #            print(f'\t{type} | {path} | {name} | {archived} ')
            #            if path.split("/")[-2] != "sqa":
            if path not in graph.obj_dict['nodes'].keys():
                if type == 'G':
                    fillcolor = 'green'
                else:
                    fillcolor = 'yellow'
                node = pydot.Node(path, label=name, style="filled", fillcolor=fillcolor)
                graph.add_node(node)
                from_node = '/'.join(path.split("/")[:-1])
                edge = pydot.Edge(from_node, path)
                graph.add_edge(edge)
            line_count += 1
        print(f'Processed {line_count} lines.')


def create_base_graph():
    G = pydot.Dot(graph_type="digraph")
    G.add_node(pydot.Node("eurobits", label="eurobits", style="filled", fillcolor="cyan"))
    fillcolor = "green"

    G.add_node(pydot.Node("eurobits/aggregation", label="aggregation", style="filled", fillcolor=fillcolor))
    G.add_edge(pydot.Edge("eurobits", "eurobits/aggregation"))

    G.add_node(pydot.Node("eurobits/api-gobernance", label="api-gobernance", style="filled", fillcolor=fillcolor))
    G.add_edge(pydot.Edge("eurobits", "eurobits/api-gobernance"))

    G.add_node(pydot.Node("eurobits/banconet", label="banconet", style="filled", fillcolor=fillcolor))
    G.add_edge(pydot.Edge("eurobits", "eurobits/banconet"))

    G.add_node(pydot.Node("eurobits/categorize", label="categorize", style="filled", fillcolor=fillcolor))
    G.add_edge(pydot.Edge("eurobits", "eurobits/categorize"))

    G.add_node(pydot.Node("eurobits/common", label="common", style="filled", fillcolor=fillcolor))
    G.add_edge(pydot.Edge("eurobits", "eurobits/common"))

    G.add_node(pydot.Node("eurobits/equanimus", label="equanimus", style="filled", fillcolor=fillcolor))
    G.add_edge(pydot.Edge("eurobits", "eurobits/equanimus"))

    G.add_node(pydot.Node("eurobits/payments", label="payments", style="filled", fillcolor=fillcolor))
    G.add_edge(pydot.Edge("eurobits", "eurobits/payments"))

    G.add_node(pydot.Node("eurobits/sqa", label="sqa", style="filled", fillcolor=fillcolor))
    G.add_edge(pydot.Edge("eurobits", "eurobits/sqa"))

    G.add_node(pydot.Node("eurobits/sysadm", label="sysadm", style="filled", fillcolor=fillcolor))
    G.add_edge(pydot.Edge("eurobits", "eurobits/sysadm"))

    G.add_node(pydot.Node("eurobits/tools", label="tools", style="filled", fillcolor=fillcolor))
    G.add_edge(pydot.Edge("eurobits", "eurobits/tools"))

    return G

# Directory plot
plot_dirs_example()

# Tree handmade built
G = create_base_graph()
G.write("output_root.svg", format='svg')
G.write("output_root.png", format='png')

# Tree plot from csvs with data from gitlab projects and groups
csvDatafile = "E:\prog\python\plot-tree-data\gitlab_scripts\gitlab_eurobits_groups.csv"
# csvDatafile = "/Users/daniel.alonso/ecedago/scripts/gitlab/gitlab_eurobits_groups.csv"
G = pydot.Dot(graph_type="digraph")
G.add_node(pydot.Node("eurobits", label="eurobits", style="filled", fillcolor="cyan"))
read_csv(G, csvDatafile)
G.write("output_group.svg", format='svg')
G.write("output_group.png", format='png')

csvDatafile = "E:\prog\python\plot-tree-data\gitlab_scripts\gitlab_eurobits_groups_projects.csv"
# csvDatafile = "/Users/daniel.alonso/ecedago/scripts/gitlab/gitlab_eurobits_groups_projects.csv"
G = pydot.Dot(graph_type="digraph")
G.add_node(pydot.Node("eurobits", label="eurobits", style="filled", fillcolor="cyan"))
read_csv(G, csvDatafile)
G.write("output_full.svg", format='svg')
G.write("output_full.png", format='png')
