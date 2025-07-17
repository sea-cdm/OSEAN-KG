from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables
URI = os.getenv("URI")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
# environment: neo4j-env\Scripts\activate  

# CSV file path prefix
CSV_PATH = "file:///"

def import_ontology_complete(driver):
    """
    Import the Vaccine Ontology (VO) from a remote GitHub URL into a Neo4j graph database.

    This function performs the following key steps:
    1. Creates a unique constraint for Resource nodes
    2. Resets previous graph configuration
    3. Configures n10s (Neosemantics) for RDF import
    4. Fetches and imports the OWL ontology from a GitHub URL
    5. Handles potential errors during the import process

    Args:
        driver (GraphDatabase.driver): An active Neo4j database driver connection

    Raises:
        Exception: If there are issues with constraint creation, graph configuration, or ontology import
    """
    with driver.session() as session:
        try:
            # Create the required constraint if it doesn't exist
            print("Creating required constraint for n10s...")
            try:
                session.run("CREATE CONSTRAINT n10s_unique_uri FOR (r:Resource) REQUIRE r.uri IS UNIQUE")
                print("Constraint created")
            except Exception as constraint_error:
                # If constraint already exists, this will fail, which is fine
                print(f"Note: {str(constraint_error)}")
                print("Constraint may already exist, continuing...")

            # Reset any previous graph config
            session.run("MATCH (n:_GraphConfig) DELETE n")
            print("Cleared previous graph config")

            # Configure n10s properly
            session.run("""
                CALL n10s.graphconfig.init({
                  handleVocabUris: 'MAP',
                  handleMultipleRelsPerType: 'OVERWRITE',
                  handleRDFTypes: 'NODES'
                })
            """)
            print("n10s configured successfully")

            # Import from the GitHub URL
            owl_url = "https://raw.githubusercontent.com/vaccineontology/VO/v2025-02-26/vo.owl"

            print(f"Importing ontology from URL: {owl_url}")
            import_result = session.run(
                "CALL n10s.rdf.import.fetch($url, 'RDF/XML') YIELD triplesParsed RETURN triplesParsed",
                {"url": owl_url}
            )

            for record in import_result:
                print(f"Import result: {record['triplesParsed']} triples parsed")

            # Check what was imported
            count_result = session.run("MATCH (n:Resource) RETURN count(n) as resourceCount")
            for record in count_result:
                print(f"Imported {record['resourceCount']} Resource nodes")

        except Exception as e:
            print(f"Error during ontology import: {str(e)}")
            import traceback
            print(traceback.format_exc())

def add_id_prefixes(driver):
    """
    Add prefixes to various ID fields in the Neo4j database.
    
    This function adds meaningful prefixes to ID fields to make them more descriptive:
    - organism_id: gets 'org_' prefix
    - experiment_id: gets 'exp_' prefix
    - intervention_id: gets 'int_' prefix
    - material_id: gets 'mat_' prefix
    - sample_id: gets 'sample_' prefix
    - Add more mappings as needed for your specific use case
    
    Args:
        driver (GraphDatabase.driver): An active Neo4j database driver connection
    """
    with driver.session() as session:
        try:
            print("Adding prefixes to ID fields...")
            
            # Define prefix mappings: field_name -> prefix
            prefix_mappings = {
                'organism_id': 'org_',
                'experiment_id': 'exp_',
                'intervention_id': 'int_',
                'material_id': 'mat_',
                'sample_id': 'sam_',
                'assay_id': 'asy_',
                'analysis_id': 'ana_',
            }
            
            # Apply prefixes to Organism nodes
            for field, prefix in prefix_mappings.items():
                # Update organisms
                result = session.run(f"""
                    MATCH (o:Organism)
                    WHERE o.{field} IS NOT NULL AND o.{field} <> '' 
                    AND NOT o.{field} STARTS WITH '{prefix}'
                    SET o.{field} = '{prefix}' + toString(o.{field})
                    RETURN count(o) as updatedCount
                """)
                count = result.single()['updatedCount']
                if count > 0:
                    print(f"Added '{prefix}' prefix to {count} Organism nodes for field '{field}'")

                # Update sample
                result = session.run(f"""
                    MATCH (sam:Sample)
                    WHERE sam.{field} IS NOT NULL AND sam.{field} <> '' 
                    AND NOT sam.{field} STARTS WITH '{prefix}'
                    SET sam.{field} = '{prefix}' + toString(sam.{field})
                    RETURN count(sam) as updatedCount
                """)
                count = result.single()['updatedCount']
                if count > 0:
                    print(f"Added '{prefix}' prefix to {count} Sample nodes for field '{field}'")

                # Update sample
                result = session.run(f"""
                    MATCH (a:Analysis)
                    WHERE a.{field} IS NOT NULL AND a.{field} <> '' 
                    AND NOT a.{field} STARTS WITH '{prefix}'
                    SET a.{field} = '{prefix}' + toString(a.{field})
                    RETURN count(a) as updatedCount
                """)
                count = result.single()['updatedCount']
                if count > 0:
                    print(f"Added '{prefix}' prefix to {count} Analysis nodes for field '{field}'")

                # Update assay
                result = session.run(f"""
                    MATCH (a:Assay)
                    WHERE a.{field} IS NOT NULL AND a.{field} <> '' 
                    AND NOT a.{field} STARTS WITH '{prefix}'
                    SET a.{field} = '{prefix}' + toString(a.{field})
                    RETURN count(a) as updatedCount
                """)
                count = result.single()['updatedCount']
                if count > 0:
                    print(f"Added '{prefix}' prefix to {count} Analysis nodes for field '{field}'")
                
                # Update experiments
                result = session.run(f"""
                    MATCH (e:Experiment)
                    WHERE e.{field} IS NOT NULL AND e.{field} <> '' 
                    AND NOT e.{field} STARTS WITH '{prefix}'
                    SET e.{field} = '{prefix}' + toString(e.{field})
                    RETURN count(e) as updatedCount
                """)
                count = result.single()['updatedCount']
                if count > 0:
                    print(f"Added '{prefix}' prefix to {count} Experiment nodes for field '{field}'")
                
                # Update interventions
                result = session.run(f"""
                    MATCH (i:Intervention)
                    WHERE i.{field} IS NOT NULL AND i.{field} <> '' 
                    AND NOT i.{field} STARTS WITH '{prefix}'
                    SET i.{field} = '{prefix}' + toString(i.{field})
                    RETURN count(i) as updatedCount
                """)
                count = result.single()['updatedCount']
                if count > 0:
                    print(f"Added '{prefix}' prefix to {count} Intervention nodes for field '{field}'")
                
                # Update materials
                result = session.run(f"""
                    MATCH (m:Material)
                    WHERE m.{field} IS NOT NULL AND m.{field} <> '' 
                    AND NOT m.{field} STARTS WITH '{prefix}'
                    SET m.{field} = '{prefix}' + toString(m.{field})
                    RETURN count(m) as updatedCount
                """)
                count = result.single()['updatedCount']
                if count > 0:
                    print(f"Added '{prefix}' prefix to {count} Material nodes for field '{field}'")
            
            print("Prefix addition completed successfully")
            
        except Exception as e:
            print(f"Error during prefix addition: {str(e)}")
            import traceback
            print(traceback.format_exc())

def map_ontology(driver):
    """
    Map imported ontology nodes to domain-specific nodes with proper ontological relationships.

    This function performs domain-specific node mapping:
    1. Verifies the number of imported Resource nodes
    2. Maps Vaccine, Pathogen, and potentially other domain-specific nodes
    3. Provides detailed logging of mapping processes

    Args:
        driver (GraphDatabase.driver): An active Neo4j database driver connection

    Raises:
        Exception: If there are issues during the ontology mapping process
    """
    with driver.session() as session:
        try:
            # Check what was imported
            count_result = session.run("MATCH (n:Resource) RETURN count(n) as resourceCount")
            for record in count_result:
                print(f"Imported {record['resourceCount']} Resource nodes")

            # Execute node mapping queries
            print("\nMapping domain nodes to ontology...")

            # map_vaccine_nodes(session) # Map Vaccine nodes
            map_experiment_nodes(session) # Map Analysis nodes
            map_intervention_nodes(session) # Map Intervention nodes
            map_material_nodes(session) # Map Material nodes
            map_organism_nodes(session) # Map Organism nodes

            print("\nNode mapping completed successfully, starting relationship mapping...")

            print("\nMapping completed successfully")

        except Exception as e:
            print(f"Error during ontology import: {str(e)}")
            import traceback
            print(traceback.format_exc())


def update_resource_properties(session):
    """
    Update Resource nodes by transforming complex IAO and UBPROP codes to human-readable properties.

    This function performs two key operations:
    1. Creates new, more readable property keys from existing IAO and UBPROP coded properties
    2. Optionally removes the original coded properties to clean up the graph

    Key transformations include:
    - IAO_0000111 → editor_preferred_label
    - IAO_0000115 → definition
    - VO_0003099 → trade_name
    And many more similar transformations

    Args:
        session (neo4j.Session): An active Neo4j database session

    Raises:
        Exception: If there are issues during property transformation
    """
    print("Updating Resource node properties to human-readable labels...")
    try:
        # Copy values from IAO properties to new human-readable keys
        session.run("""
            MATCH (r:Resource)
            SET r.editor_preferred_label = r.IAO_0000111,
                r.example_of_usage = r.IAO_0000112,
                r.has_curation_status = r.IAO_0000114,
                r.definition = r.IAO_0000115,
                r.editor_note = r.IAO_0000116,
                r.term_editor = r.IAO_0000117,
                r.alternative_term = r.IAO_0000118,
                r.definition_source = r.IAO_0000119,
                r.curator_note = r.IAO_0000232,
                r.term_tracker_item = r.IAO_0000233,
                r.imported_from = r.IAO_0000412,
                r.violin_vaccine_id = r.VO_0001818,
                r.trade_name = r.VO_0003099,
                r.fda_vaccine_indications = r.VO_0003160,
                r.vaccine_package_insert_pdf_url = r.VO_0003161,
                r.vaccine_stn = r.VO_0003162,
                r.taxon_notes = r.UBPROP_0000008,
                r.external_definition = r.UBPROP_0000001,
                r.axiom_lost_from_external_ontology = r.UBPROP_0000002,
                r.homology_notes = r.UBPROP_0000003
        """)
        # Optionally remove the original IAO properties if they are no longer needed
        session.run("""
            MATCH (r:Resource)
            REMOVE r.IAO_0000111, r.IAO_0000112, r.IAO_0000114, r.IAO_0000115,
                   r.IAO_0000116, r.IAO_0000117, r.IAO_0000118, r.IAO_0000119,
                   r.IAO_0000232, r.IAO_0000233, r.IAO_0000412,
                   r.VO_0001818, r.VO_0003099, r.VO_0003160, r.VO_0003161, r.VO_0003162,
                   r.UBPROP_0000008, r.UBPROP_0000001, r.UBPROP_0000002, r.UBPROP_0000003
        """)
        print("Resource node properties updated successfully.")
    except Exception as e:
        print(f"Error updating Resource node properties: {str(e)}")

def map_experiment_nodes(session):
    """
    Maps Experiment nodes to their corresponding Vaccine Ontology (VO) Resource representations in Neo4j.

    This function assumes:
    1. Your experiment data has been loaded into Neo4j with the label 'Experiment'.
    2. Experiment nodes have an 'experiment_type_id' property (e.g., 'VO_0000002').
    3. The Vaccine Ontology has been loaded as 'Resource' nodes where the URI's last part is the VO ID.

    The function will:
    1. Find Experiment nodes with a non-empty 'experiment_type_id'.
    2. Find corresponding Resource nodes by matching 'experiment_type_id' with the resource's URI.
    3. Copy properties from the Resource node to the Experiment node.
    4. Create a 'VO_REPRESENTATION' relationship between the Experiment and Resource nodes.
    """
    print("Mapping Experiment nodes by matching experiment_type_id with VO Resource URI...")
    try:
        # This query finds Experiment nodes and matches them to VO Resource nodes
        # using the direct VO identifier.
        result = session.run("""
            MATCH (e:Experiment)
            WHERE e.experiment_type_id IS NOT NULL AND e.experiment_type_id <> ''
            MATCH (resource:Resource)
            // Match the VO ID from the experiment with the last part of the resource URI
            // Handle prefixed IDs by removing the prefix before matching
            WHERE last(split(resource.uri, '/')) = 
                CASE 
                    WHEN e.experiment_type_id STARTS WITH 'exp_type_' THEN substring(e.experiment_type_id, 9)
                    ELSE e.experiment_type_id
                END
            WITH e, resource
            // Set properties on the experiment node, mirroring your vaccine mapping logic for consistency
            SET e.vo_representation_uri = resource.uri,
                e.vo_editor_preferred_label = resource.IAO_0000111,
                e.vo_example_of_usage = resource.IAO_0000112,
                e.vo_has_curation_status = resource.IAO_0000114,
                e.vo_definition = resource.IAO_0000115,
                e.vo_editor_note = resource.IAO_0000116,
                e.vo_term_editor = resource.IAO_0000117,
                e.vo_alternative_term = resource.IAO_0000118,
                e.vo_definition_source = resource.IAO_0000119,
                e.vo_curator_note = resource.IAO_0000232,
                e.vo_term_tracker_item = resource.IAO_0000233,
                e.vo_imported_from = resource.IAO_0000412,
                e.vo_violin_vaccine_id = resource.VO_0001818,
                e.vo_trade_name = resource.VO_0003099,
                e.vo_fda_vaccine_indications = resource.VO_0003160,
                e.vo_vaccine_package_insert_pdf_url = resource.VO_0003161,
                e.vo_vaccine_stn = resource.VO_0003162,
                e.vo_taxon_notes = resource.UBPROP_0000008,
                e.vo_external_definition = resource.UBPROP_0000001,
                e.vo_axiom_lost_from_external_ontology = resource.UBPROP_0000002,
                e.vo_homology_notes = resource.UBPROP_0000003
            // Create a relationship to the VO resource
            MERGE (e)-[:VO_REPRESENTATION]->(resource)
            RETURN count(e) as mappedCount
        """)
        mapped_count = result.single()['mappedCount']
        print(f"Mapped {mapped_count} Experiment nodes with remapped VO properties and created relationships.")

        # Log any unmapped nodes for review
        unmapped_result = session.run("""
            MATCH (e:Experiment)
            WHERE NOT (e)-[:VO_REPRESENTATION]->()
            RETURN count(e) as unmappedCount
        """)
        unmapped_count = unmapped_result.single()['unmappedCount']
        if unmapped_count > 0:
            print(f"Warning: {unmapped_count} Experiment nodes could not be mapped to a VO Resource.")

    except Exception as e:
        print(f"An error occurred during Experiment node mapping: {e}")


def map_intervention_nodes(session):
    """
    Maps Intervention nodes to Resource nodes based on various ontology IDs.
    This creates multiple, specific relationships for each type of mapping.
    """
    print("Mapping Intervention nodes to their corresponding Ontology Resources...")
    
    # Define the mappings: property name, relationship type, prefix to remove
    mappings = {
        "intervention_type_id": ("HAS_TYPE", "int_type_"),
        "material_id": ("USES_MATERIAL", "mat_"),
        "intervention_route_id": ("HAS_ROUTE", "route_"),
        "dosage_unit_id": ("HAS_DOSAGE_UNIT", "dosage_")
    }

    for prop_name, (rel_type, prefix) in mappings.items():
        try:
            query = f"""
                MATCH (i:Intervention)
                WHERE i.{prop_name} IS NOT NULL AND i.{prop_name} <> ''
                MATCH (resource:Resource)
                WHERE last(split(resource.uri, '/')) = 
                    CASE 
                        WHEN i.{prop_name} STARTS WITH '{prefix}' THEN substring(i.{prop_name}, {len(prefix) + 1})
                        ELSE i.{prop_name}
                    END
                MERGE (i)-[:{rel_type}]->(resource)
                RETURN count(i) as mappedCount
            """
            result = session.run(query)
            mapped_count = result.single()['mappedCount']
            if mapped_count > 0:
                print(f"-> Created {mapped_count} ':{rel_type}' relationships from Intervention nodes.")
        except Exception as e:
            print(f"An error occurred while mapping '{prop_name}' with relationship ':{rel_type}': {e}")


def map_material_nodes(session):
    """
    Maps Material nodes to their corresponding Vaccine Ontology (VO) Resource representations in Neo4j.
    """
    print("Mapping Material nodes by matching material_name_id with VO Resource URI...")
    try:
        result = session.run("""
            MATCH (m:Material)
            WHERE m.material_name_id IS NOT NULL AND m.material_name_id <> ''
            MATCH (resource:Resource)
            WHERE last(split(resource.uri, '/')) = 
                CASE 
                    WHEN m.material_name_id STARTS WITH 'mat_name_' THEN substring(m.material_name_id, 10)
                    ELSE m.material_name_id
                END
            WITH m, resource
            // Set properties on the material node, copying from the ontology resource
            SET m.vo_representation_uri = resource.uri,
                m.vo_editor_preferred_label = resource.IAO_0000111,
                m.vo_example_of_usage = resource.IAO_0000112,
                m.vo_has_curation_status = resource.IAO_0000114,
                m.vo_definition = resource.IAO_0000115,
                m.vo_editor_note = resource.IAO_0000116,
                m.vo_term_editor = resource.IAO_0000117,
                m.vo_alternative_term = resource.IAO_0000118,
                m.vo_definition_source = resource.IAO_0000119,
                m.vo_curator_note = resource.IAO_0000232,
                m.vo_term_tracker_item = resource.IAO_0000233,
                m.vo_imported_from = resource.IAO_0000412,
                m.vo_violin_vaccine_id = resource.VO_0001818,
                m.vo_trade_name = resource.VO_0003099,
                m.vo_fda_vaccine_indications = resource.VO_0003160,
                m.vo_vaccine_package_insert_pdf_url = resource.VO_0003161,
                m.vo_vaccine_stn = resource.VO_0003162,
                m.vo_taxon_notes = resource.UBPROP_0000008,
                m.vo_external_definition = resource.UBPROP_0000001,
                m.vo_axiom_lost_from_external_ontology = resource.UBPROP_0000002,
                m.vo_homology_notes = resource.UBPROP_0000003
            MERGE (m)-[:VO_REPRESENTATION]->(resource)
            RETURN count(m) as mappedCount
        """)
        mapped_count = result.single()['mappedCount']
        print(f"Mapped {mapped_count} Material nodes with a VO_REPRESENTATION relationship.")

    except Exception as e:
        print(f"An error occurred during Material node mapping: {e}")


def map_organism_nodes(session):
    """
    Maps Organism nodes to Resource nodes based on various ontology IDs (e.g., PATO, NCBITaxon, UO).
    """
    print("Mapping Organism nodes to their corresponding Ontology Resources...")
    
    # Define the mappings: property name, relationship type, prefix to remove
    mappings = {
        "species_id": ("IS_SPECIES", "species_"),
    }

    for prop_name, (rel_type, prefix) in mappings.items():
        try:
            # The species_id from NCBITaxon might not have an underscore, so we replace it.
            # e.g., NCBITaxon_9606 becomes NCBITaxon:9606 in some ontology versions.
            # This query handles both cases gracefully.
            query = f"""
                MATCH (o:Organism)
                WHERE o.{prop_name} IS NOT NULL AND o.{prop_name} <> ''
                MATCH (resource:Resource)
                WHERE last(split(resource.uri, '/')) = 
                    CASE 
                        WHEN o.{prop_name} STARTS WITH '{prefix}' THEN substring(o.{prop_name}, {len(prefix) + 1})
                        ELSE o.{prop_name}
                    END
                   OR last(split(resource.uri, '/')) = 
                    CASE 
                        WHEN o.{prop_name} STARTS WITH '{prefix}' THEN replace(substring(o.{prop_name}, {len(prefix) + 1}), '_', ':')
                        ELSE replace(o.{prop_name}, '_', ':')
                    END
                MERGE (o)-[:{rel_type}]->(resource)
                RETURN count(o) as mappedCount
            """
            result = session.run(query)
            mapped_count = result.single()['mappedCount']
            if mapped_count > 0:
                print(f"-> Created {mapped_count} ':{rel_type}' relationships from Organism nodes.")
        except Exception as e:
            print(f"An error occurred while mapping '{prop_name}' with relationship ':{rel_type}': {e}")

def import_data():
    """
    Main orchestration function to import and map ontology data.

    This function:
    1. Establishes a Neo4j database connection
    2. Imports the complete ontology
    3. Adds prefixes to ID fields
    4. Maps domain-specific nodes
    5. Updates Resource node properties
    6. Handles any exceptions during the process

    Raises:
        Exception: If there are issues during the entire import process
    """
    driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
    try:        
        import_ontology_complete(driver)
        
        # Add prefixes to ID fields BEFORE mapping
        add_id_prefixes(driver)
        
        map_ontology(driver)
        with driver.session() as session:
            # Update Resource node properties to human-readable labels
            update_resource_properties(session)
    except Exception as e:
        print(f"Error in main execution: {str(e)}")

    driver.close()

# Run the import function
if __name__ == "__main__":
    import_data()