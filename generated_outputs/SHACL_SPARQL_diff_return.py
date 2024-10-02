from pyshacl import Validator
from rdflib import Graph
from rdflib.compare import to_isomorphic, graph_diff


def gen_dif_and_ext_graph(data_g, shape_g):
    val_0 = Validator(data_g, options={"advanced": True, "inference": "rdfs"})
    conforms_data, report_g_data, report_text_data = val_0.run()
    inferred_base_graph_1 = val_0.target_graph
    val_1 = Validator(data_g, shacl_graph=shape_g, options={"advanced": True, "inference": "rdfs"})
    conforms_expanded, report_g_expanded, report_text_expanded = val_1.run()
    expanded_g = val_1.target_graph
    is0_1, is0_2 = to_isomorphic(inferred_base_graph_1), to_isomorphic(expanded_g)
    both, diff_g1, diff_g2 = graph_diff(is0_1, is0_2)
    conforms_sum = f'baseshape: \n{conforms_data}\nexpanded graph: \n{conforms_expanded}'
    dict_of_report_g = {'baseshape_report_graph': report_g_data, 'expanded_report_graph': report_g_expanded}
    report_text_sum = f'baseshape: \n{report_text_data}\nexpanded graph: \n{report_text_expanded}'
    return expanded_g, diff_g2, conforms_sum, dict_of_report_g, report_text_sum


path_to_data = "D:/Users/smhhborg(D_Laufwerk)/Documents/GitHub/Test_for_advanced_SHACL_features/shacl_sparql_test_data.ttl"
path_to_shapes = "D:/Users/smhhborg(D_Laufwerk)/Documents/GitHub/Test_for_advanced_SHACL_features/shacl_sparql_test_shape.ttl"

data_graph = Graph()
data_graph.parse(path_to_data, format="ttl")

shape_graph = Graph()
shape_graph.parse(path_to_shapes, format="ttl")

expanded_graph, diff_graph, conforms, report_graph_dict, report_text = gen_dif_and_ext_graph(data_graph, shape_graph)
expanded_graph.serialize(destination='./expanded_graph.ttl', format='turtle')
diff_graph.serialize(destination='./diff_graph.ttl', format='turtle')


