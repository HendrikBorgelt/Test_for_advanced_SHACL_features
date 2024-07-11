import rdflib

data = """
@prefix cml: <http://www.xml-cml.org/schema/cml2/core#> .
@prefix ro: <http://www.example.org/reaction-ontology#> .
@prefix ex: <http://www.example.org/chemicals#> .

# Define reactants and products with their chemical structures
ex:Reactant1 cml:chemicalStructure "SMILES:CCO" .  # Ethanol
ex:Reactant2 cml:chemicalStructure "SMILES:O=C=O" .  # Carbon dioxide
ex:Reactant3 cml:chemicalStructure "SMILES:CC(=O)O" .  # Acetic acid
ex:Reactant4 cml:chemicalStructure "SMILES:H2O" .  # Water
ex:Reactant5 cml:chemicalStructure "SMILES:O2" .  # Oxygen

ex:Product1 cml:chemicalStructure "SMILES:CCOCC(=O)O" .  # Ethyl acetate
ex:Product2 cml:chemicalStructure "SMILES:CCOCC" .  # Diethyl ether
ex:Product3 cml:chemicalStructure "SMILES:COO" .  # Formate
ex:Product4 cml:chemicalStructure "SMILES:CCOCO" .  # Ethylene glycol

# Idealized Reaction 1: Ethanol + Carbon dioxide -> Ethyl acetate
ex:IdealReaction1 a ro:Reaction ;
                  ro:type "idealized" ;
                  ro:hasReactant ex:Reactant1 , ex:Reactant2 ;
                  ro:hasProduct ex:Product1 .

# Idealized Reaction 2: Acetic acid -> Diethyl ether + Formate
ex:IdealReaction2 a ro:Reaction ;
                  ro:type "idealized" ;
                  ro:hasReactant ex:Reactant3 ;
                  ro:hasProduct ex:Product2 , ex:Product3 .

# Idealized Reaction 3: Ethanol -> Ethylene glycol
ex:IdealReaction3 a ro:Reaction ;
                  ro:type "idealized" ;
                  ro:hasReactant ex:Reactant1 ;
                  ro:hasProduct ex:Product4 .

# Experimental Reaction 1: Matches Idealized Reaction 1 exactly
ex:ExperimentReaction1 a ro:Reaction ;
                       ro:type "experimental" ;
                       ro:hasReactant ex:Reactant1 , ex:Reactant2 ;
                       ro:hasProduct ex:Product1 .

# Experimental Reaction 2: Matches Idealized Reaction 2 with an additional reactant (Water)
ex:ExperimentReaction2 a ro:Reaction ;
                       ro:type "experimental" ;
                       ro:hasReactant ex:Reactant3 , ex:Reactant4 ;  # Additional reactant (Water)
                       ro:hasProduct ex:Product2 , ex:Product3 .

# Experimental Reaction 3: More reactants but matches Idealized Reaction 1 in relevant reactants and products
ex:ExperimentReaction3 a ro:Reaction ;
                       ro:type "experimental" ;
                       ro:hasReactant ex:Reactant1 , ex:Reactant2 , ex:Reactant4 ;  # Additional reactant (Water)
                       ro:hasProduct ex:Product1 .

# Experimental Reaction 4: Correct reactants for Idealized Reaction 1 but incorrect product
ex:ExperimentReaction4 a ro:Reaction ;
                       ro:type "experimental" ;
                       ro:hasReactant ex:Reactant1 , ex:Reactant2 ;
                       ro:hasProduct ex:Product2 .  # Incorrect product

# Experimental Reaction 5: Matches Idealized Reaction 3 with an additional reactant (Oxygen)
ex:ExperimentReaction5 a ro:Reaction ;
                       ro:type "experimental" ;
                       ro:hasReactant ex:Reactant1 , ex:Reactant5 ;  # Additional reactant (Oxygen)
                       ro:hasProduct ex:Product4 .

# Experimental Reaction 6: Non-matching reaction with entirely different products
ex:ExperimentReaction6 a ro:Reaction ;
                       ro:type "experimental" ;
                       ro:hasReactant ex:Reactant2 , ex:Reactant4 ;  # Different set of reactants
                       ro:hasProduct ex:Product3 .  # Different product
"""

g = rdflib.Graph()
g.parse(data=data, format="turtle")

knows_query = """
PREFIX cml: <http://www.xml-cml.org/schema/cml2/core#>
PREFIX ro: <http://www.example.org/reaction-ontology#>

INSERT {?experimentReaction a ?idealReaction}
WHERE {
  # Idealized Reaction
  ?idealReaction a ro:Reaction ;
                 ro:type "idealized" .

  {
    SELECT  ?idealReaction  (GROUP_CONCAT(DISTINCT ?idealReactantStructure ; separator=",") AS ?idealReactantsList) 
                            (GROUP_CONCAT(DISTINCT ?idealProductStructure ; separator=",") AS ?idealProductsList)
    WHERE {
      ?idealReaction ro:hasReactant ?idealReactant .
      ?idealReactant cml:chemicalStructure ?idealReactantStructure .
      
      ?idealReaction ro:hasProduct ?idealProduct .
      ?idealProduct cml:chemicalStructure ?idealProductStructure .
    }
    GROUP BY ?idealReaction
  }

  # Experimental Reaction
  ?experimentReaction a ro:Reaction ;
                      ro:type "experimental" .

  {
    SELECT ?experimentReaction (GROUP_CONCAT(DISTINCT ?experimentReactantStructure ; separator=",") AS ?experimentReactantsList) (GROUP_CONCAT(DISTINCT ?experimentProductStructure ; separator=",") AS ?experimentProductsList)
    WHERE {
      ?experimentReaction ro:hasReactant ?experimentReactant .
      ?experimentReactant cml:chemicalStructure ?experimentReactantStructure .
      
      ?experimentReaction ro:hasProduct ?experimentProduct .
      ?experimentProduct cml:chemicalStructure ?experimentProductStructure .
    }
    GROUP BY ?experimentReaction
  }

  # Compare the product lists exactly
  FILTER (STR(?idealProductsList) = STR(?experimentProductsList))
  
  # Ensure all ideal reactants are in the experimental reactants list
  FILTER NOT EXISTS {
    # Iterate over each ideal reactant
    ?idealReaction ro:hasReactant ?idealReactant .
    ?idealReactant cml:chemicalStructure ?idealReactantStructure .
    
    # Check if this ideal reactant is missing in the experimental reaction's reactants
    FILTER NOT EXISTS {
      ?experimentReaction ro:hasReactant ?experimentReactant .
      ?experimentReactant cml:chemicalStructure ?idealReactantStructure .
    }
  }
}
"""

# qres = g.query(knows_query)
# for row in qres:
#     print(f"{row}")

qres = g.update(knows_query)
# for row in qres:
#     print(f"{row}")

g.serialize(destination='scratch_16.ttl', format='turtle')