from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

# Load environment variables to securely manage database credentials
load_dotenv()

# Database connection parameters retrieved from environment variables
URI = os.getenv("URI")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# Prefix for CSV file paths to enable local file loading in Neo4j
CSV_PATH = "file:///"

# Queries to create constraints for each node type
CONSTRAINT_QUERIES = {
    "Assay": """
        CREATE CONSTRAINT IF NOT EXISTS FOR (n:Assay) REQUIRE n.assay_id IS UNIQUE;
    """,
    "Analysis": """
        CREATE CONSTRAINT IF NOT EXISTS FOR (n:Analysis) REQUIRE n.analysis_id IS UNIQUE;
    """,
    "Documentation": """
        CREATE CONSTRAINT IF NOT EXISTS FOR (n:Documentation) REQUIRE n.documentation_id IS UNIQUE;
    """,
    "Experiment": """
        CREATE CONSTRAINT IF NOT EXISTS FOR (n:Experiment) REQUIRE n.experiment_id IS UNIQUE;
    """,
    "Group": """
        CREATE CONSTRAINT IF NOT EXISTS FOR (n:Group) REQUIRE n.group_id IS UNIQUE;
    """,
    "Intervention": """
        CREATE CONSTRAINT IF NOT EXISTS FOR (n:Intervention) REQUIRE n.intervention_id IS UNIQUE;
    """,
    "Material": """
        CREATE CONSTRAINT IF NOT EXISTS FOR (n:Material) REQUIRE n.material_id IS UNIQUE;
    """,
    "Organism": """
        CREATE CONSTRAINT IF NOT EXISTS FOR (n:Organism) REQUIRE n.organism_id IS UNIQUE;
    """,
    "Study": """
        CREATE CONSTRAINT IF NOT EXISTS FOR (n:Study) REQUIRE n.study_id IS UNIQUE;
    """,
    "Sample": """
        CREATE CONSTRAINT IF NOT EXISTS FOR (n:Sample) REQUIRE n.sample_id IS UNIQUE;
    """,
    "Result": """
        CREATE CONSTRAINT IF NOT EXISTS FOR (n:Result) REQUIRE n.results_id IS UNIQUE;
    """,
}

# Queries to load data into Neo4j
CREATE_QUERIES = {
    "Assay": f"""
        LOAD CSV WITH HEADERS FROM '{CSV_PATH}assay.csv' AS row
        MERGE (a:Assay {{assay_id: row.assay_id}})
        SET a.assay_name = row.assay_name,
            a.documentation_id = row.documentation_id,
            a.assay_type = row.assay_type,
            a.assay_type_id = row.assay_type_id,
            a.organism = row.organism,
            a.reagents = row.reagents,
            a.platform = row.platform,
            a.comments = row.comments
    """,
    "Analysis": f"""
    LOAD CSV WITH HEADERS FROM '{CSV_PATH}analysis.csv' AS row
    MERGE (a:Analysis {{analysis_id: row.analysis_id}})
    SET a.documentation_id     = row.documentation_id,
        a.group_id             = row.group_id,
        a.analysis_name        = row.analysis_name,
        a.analysis_name_id     = row.analysis_name_id,
        a.input_data           = row.input_data,
        a.input_data_id        = row.input_data_id,
        a.reference_id         = row.reference_id,
        a.reference_source     = row.reference_source,
        a.comments             = row.comments,
        a.assay_name           = row.assay_name,
        a.assay_type           = row.assay_type,
        a.assay_type_id        = row.assay_type_id,
        a.organism             = row.organism,
        a.reagents             = row.reagents,
        a.platform             = row.platform
    """,
    "Documentation": f"""
        LOAD CSV WITH HEADERS FROM '{CSV_PATH}documentation.csv' AS row
        MERGE (d:Documentation {{documentation_id: row.documentation_id}})
        SET d.study_id = row.study_id,
            d.document_name = row.document_name,
            d.document_type = row.document_type,
            d.document_type_id = row.document_type_id,
            d.documentation_source = row.documentation_source,
            d.source_id = row.source_id,
            d.reference_source = row.reference_source,
            d.citation = row.citation,
            d.citation_style = row.citation_style,
            d.person_id = row.person_id,
            d.person_id_type = row.person_id_type,
            d.honorific = row.honorific,
            d.first_name = row.first_name,
            d.middle_name = row.middle_name,
            d.last_name = row.last_name,
            d.person_role = row.person_role,
            d.comments = row.comments
    """,
    "Experiment": f"""
        LOAD CSV WITH HEADERS FROM '{CSV_PATH}experiment.csv' AS row
        MERGE (e:Experiment {{experiment_id: row.experiment_id}})
        SET e.study_id = row.study_id,
            e.experiment_type = row.experiment_type,
            e.experiment_type_id = row.experiment_type_id,
            e.experiment_control = row.experiment_control,
            e.source_id = row.source_id,
            e.reference_source = row.reference_source,
            e.comments = row.comments,
            e.experiment_name = row.experiment_name
    """,
    "Group": f"""
        LOAD CSV WITH HEADERS FROM '{CSV_PATH}group.csv' AS row
        MERGE (g:Group {{group_id: row.group_id}})
        SET g.experiment_id = row.experiment_id,
            g.group_type = row.group_type,
            g.group_size = row.group_size,
            g.reference_id = row.reference_id,
            g.reference_source = row.reference_source,
            g.max_age = row.max_age,
            g.min_age = row.min_age,
            g.comments = row.comments
    """,
    "Intervention": f"""
        LOAD CSV WITH HEADERS FROM '{CSV_PATH}intervention.csv' AS row
        MERGE (i:Intervention {{intervention_id: row.intervention_id}})
        SET i.experiment_id = row.experiment_id,
            i.organism_id = row.organism_id,
            i.material = row.material,
            i.material_id = row.material_id,
            i.dosage = row.dosage,
            i.dosage_unit = row.dosage_unit,
            i.dosage_unit_id = row.dosage_unit_id,
            i.intervention_type = row.intervention_type,
            i.intervention_type_id = row.intervention_type_id,
            i.intervention_route = row.intervention_route,
            i.intervention_route_id = row.intervention_route_id,
            i.T0_defintion = row.T0_defintion,
            i.intervention_time = row.intervention_time,
            i.intervention_unit = row.intervention_unit,
            i.intervention_time_unit_id = row.intervention_time_unit_id,
            i.source_id = row.source_id,
            i.reference_source = row.reference_source,
            i.comments = row.comments,
            i.T0_definition = row.T0_definition
    """,
    "Material": f"""
        LOAD CSV WITH HEADERS FROM '{CSV_PATH}material.csv' AS row
        MERGE (m:Material {{material_id: row.material_id}})
        SET m.material_name = row.material_name,
            m.material_name_id = row.material_name_id,
            m.organization = row.organization,
            m.reference_id = row.reference_id,
            m.reference_source = row.reference_source,
            m.comments = row.comments,
            m.reference = row.reference
    """,
    "Organism": f"""
        LOAD CSV WITH HEADERS FROM '{CSV_PATH}organism.csv' AS row
        MERGE (o:Organism {{organism_id: row.organism_id}})
        SET o.group_id = row.group_id,
            o.experiment_id = row.experiment_id,
            o.species = row.species,
            o.species_id = row.species_id,
            o.type = row.type,
            o.type_id = row.type_id,
            o.age = row.age,
            o.age_unit = row.age_unit,
            o.age_unit_id = row.age_unit_id,
            o.sex = row.sex,
            o.sex_id = row.sex_id,
            o.reference_id = row.reference_id,
            o.reference_source = row.reference_source,
            o.comments = row.comments
    """,
    "Study": f"""
        LOAD CSV WITH HEADERS FROM '{CSV_PATH}study.csv' AS row
        MERGE (s:Study {{study_id: row.study_id}})
        SET s.study_type = row.study_type,
            s.study_type_id = row.study_type_id,
            s.study_name = row.study_name,
            s.study_description = row.study_description,
            s.reference_id = row.reference_id,
            s.reference_source = row.reference_source,
            s.comments = row.comments
    """,
    "Sample": f"""
        LOAD CSV WITH HEADERS FROM '{CSV_PATH}sample.csv' AS row
        MERGE (s:Sample {{sample_id: row.sample_id}})
        SET s.group_id = row.group_id,
            s.organism_id = row.organism_id,
            s.collection = row.collection,
            s.collection_id = row.collection_id,
            s.collection_time = row.collection_time,
            s.collection_time_unit = row.collection_time_unit,
            s.collection_time_unit_id = row.collection_time_unit_id,
            s.T0_definitionexpsample_type = row.T0_definitionexpsample_type,
            s.expsample_type_id = row.expsample_type_id,
            s.expsample_reference_id = row.expsample_reference_id,
            s.expsample_reference_name = row.expsample_reference_name,
            s.biosample_type = row.biosample_type,
            s.biosample_type_id = row.biosample_type_id,
            s.biosample_reference_id = row.biosample_reference_id,
            s.biosample_reference_name = row.biosample_reference_name,
            s.replicates = row.replicates,
            s.expsample_type = row.expsample_type,
            s.expsample_source = row.expsample_source
    """,
    "Result": f"""
        LOAD CSV WITH HEADERS FROM '{CSV_PATH}result.csv' AS row
        MERGE (r:Result {{results_id: row.results_id}})
        SET r.experiment_id = row.experiment_id,
            r.group_id = row.group_id,
            r.sample_id = row.sample_id,
            r.analysis_name = row.analysis_name,
            r.analysis_id = row.analysis_id,
            r.original_assay_type = row.original_assay_type,
            r.assay_id = row.assay_id,
            r.analysis_type = row.analysis_type,
            r.datatype = row.datatype,
            r.datatype_id = row.datatype_id,
            r.file_access = row.file_access,
            r.file_type = row.file_type,
            r.replications = row.replications,
            r.comments = row.comments,
            r.document_id = row.document_id,
            r.original_assay_type_id = row.original_assay_type_id
    """
}

RELATIONSHIP_QUERIES = {
    # Connects Experiments to the Study they are part of.
    "StudyExperiment": """
        MATCH (s:Study), (e:Experiment)
        WHERE s.study_id = e.study_id
        MERGE (s)-[:HAS_EXPERIMENT]->(e);
    """,

    # Connects Documentation to the Study it belongs to.
    "StudyDocumentation": """
        MATCH (s:Study), (d:Documentation)
        WHERE s.study_id = d.study_id
        MERGE (s)-[:PROVIDES_DOCUMENTATION]->(d);
    """,

    # Connects Groups to the Experiment they are part of.
    "ExperimentGroup": """
        MATCH (e:Experiment), (g:Group)
        WHERE e.experiment_id = g.experiment_id
        MERGE (e)-[:CONTAINS_GROUP]->(g);
    """,

    # Connects Organisms directly to an Experiment.
    "ExperimentOrganism": """
        MATCH (e:Experiment), (o:Organism)
        WHERE e.experiment_id = o.experiment_id
        MERGE (e)-[:INVOLVES_ORGANISM]->(o);
    """,

    # Connects Interventions to their respective Experiment.
    "ExperimentIntervention": """
        MATCH (e:Experiment), (i:Intervention)
        WHERE e.experiment_id = i.experiment_id
        MERGE (e)-[:HAS_INTERVENTION]->(i);
    """,

    # Connects Results to the Experiment that produced them.
    "ExperimentResult": """
        MATCH (e:Experiment), (r:Result)
        WHERE e.experiment_id = r.experiment_id
        MERGE (e)-[:YIELDS_RESULT]->(r);
    """,

    # Connects Organisms to the Group they belong to.
    "GroupOrganism": """
        MATCH (g:Group), (o:Organism)
        WHERE g.group_id = o.group_id
        MERGE (g)-[:COMPOSED_OF]->(o);
    """,

    # Connects Samples to the Group they were taken from.
    "GroupSample": """
        MATCH (g:Group), (s:Sample)
        WHERE g.group_id = s.group_id
        MERGE (g)-[:PROVIDES_SAMPLE]->(s);
    """,
    
    # Connects Results to the Group they are associated with.
    "GroupResult": """
        MATCH (g:Group), (r:Result)
        WHERE g.group_id = r.group_id
        MERGE (g)-[:ASSOCIATED_WITH_RESULT]->(r);
    """,

    # Connects Samples to their source Organism.
    "OrganismSample": """
        MATCH (o:Organism), (s:Sample)
        WHERE o.organism_id = s.organism_id
        MERGE (o)-[:IS_SOURCE_OF]->(s);
    """,

    # Connects Interventions to the Organism that received them.
    "OrganismIntervention": """
        MATCH (i:Intervention), (o:Organism)
        WHERE i.organism_id = o.organism_id
        MERGE (o)-[:UNDERGOES]->(i);
    """,

    # Connects Results to the Sample they were generated from.
    "SampleResult": """
        MATCH (s:Sample), (r:Result)
        WHERE s.sample_id = r.sample_id
        MERGE (s)-[:GENERATES_RESULT]->(r);
    """,

    # Connects Interventions to the Material used.
    "InterventionMaterial": """
        MATCH (i:Intervention), (m:Material)
        WHERE i.material_id = m.material_id
        MERGE (i)-[:APPLIES_MATERIAL]->(m);
    """,

    # Connects an Analysis to the Assay it was derived from using the assay name.
    "AnalysisAssay": """
        MATCH (an:Analysis), (a:Assay)
        WHERE an.assay_name = a.assay_name
        MERGE (an)-[:ANALYZES_ASSAY]->(a);
    """,

    # Connects an Analysis to the Result it produced.
    "AnalysisResult": """
        MATCH (an:Analysis), (r:Result)
        WHERE an.analysis_id = r.analysis_id
        MERGE (an)-[:PRODUCED_RESULT]->(r);
    """,
    
    # Connects Documentation to the Assay it describes.
    "DocumentationAssay": """
        MATCH (d:Documentation), (a:Assay)
        WHERE d.documentation_id = a.documentation_id
        MERGE (d)-[:DESCRIBES]->(a);
    """,

    # Connects Documentation to the Analysis it describes.
    "DocumentationAnalysis": """
        MATCH (d:Documentation), (an:Analysis)
        WHERE d.documentation_id = an.documentation_id
        MERGE (d)-[:DESCRIBES]->(an);
    """,
    
    # Connects Documentation to the Result it describes.
    "DocumentationResult": """
        MATCH (d:Documentation), (r:Result)
        WHERE d.documentation_id = r.document_id
        MERGE (d)-[:DESCRIBES]->(r);
    """,

    # NEW: Connects Intervention to Material based on a reference ID (like a VO ID).
    "InterventionReferencesMaterial": """
        MATCH (i:Intervention), (m:Material)
        WHERE i.material_id = m.reference_id
        MERGE (i)-[:REFERENCES_MATERIAL]->(m);
    """,

    # NEW: Connects a Result directly to the Assay it was derived from.
    "ResultFromAssay": """
        MATCH (r:Result), (a:Assay)
        WHERE r.assay_id = a.platform
        MERGE (r)-[:DERIVED_FROM_ASSAY]->(a);
    """
}

def execute_queries(driver, queries):
    """
    Execute a collection of Cypher queries in a single Neo4j session.

    This helper function runs multiple Cypher queries sequentially, providing 
    progress tracking and error-tolerant execution. It's useful for batch 
    operations like creating constraints, importing data, or establishing 
    relationships.

    Args:
        driver (GraphDatabase.driver): Active Neo4j database driver
        queries (dict): Dictionary of query names and their corresponding Cypher queries

    Raises:
        Exception: If a query fails during execution
    """    """Helper function to execute a dictionary of Cypher queries."""
    with driver.session() as session:
        for key, query in queries.items():
            print(f"Executing: {key}")
            session.run(query)

# Function to execute queries
def import_data():
    """
    Orchestrate the complete data import process for the Neo4j graph database.

    This function manages the entire import workflow:
    1. Establish database connection
    2. Create node constraints
    3. Import CSV data into nodes
    4. Establish relationships between nodes

    Raises:
        Exception: If any stage of the import process fails
    """
    driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

    # Step 1: Create Constraints
    execute_queries(driver, CONSTRAINT_QUERIES)
    print("Constraints created.")
    
    # Step 2: Import CSV Data into Nodes
    execute_queries(driver, CREATE_QUERIES)
    print("CSV data imported into nodes.")

    # Step 3: Establish Relationships
    execute_queries(driver, RELATIONSHIP_QUERIES)
    print("Relationships created.")

    driver.close()

# Run the import function
if __name__ == "__main__":
    import_data()