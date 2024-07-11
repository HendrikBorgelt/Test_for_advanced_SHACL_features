import rdflib

g = rdflib.Graph()
g.parse(".\\Ontology_tests\\data_for_query3.ttl", format="turtle")
with open(".\\Ontology_tests\\knownQuery8.ttl", "r") as file:
    known_query1 = file.read()

qres = g.query(known_query1)

for row1 in qres:
    print(f"Experimental Reaction: {row1.experimentalReaction}, Ideal Reaction: {row1.idealReaction}")
