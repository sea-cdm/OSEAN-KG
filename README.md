# OSEAN-KG
OSEAN_KG: OSEAN knowledge graph

OSEAN is a knowledge graph built on the ontology-supported SEA CDM through Python script to ingest various biological study data entities into a Neo4j graph database. It transforms raw data, creates distinct nodes for different entities (Studies, Experiments, Interventions, etc.), and enriches the graph by linking these nodes to formal ontology terms from resources like the Vaccine Ontology (VO).

---

## Overview

The primary goal of this script is to build a semantically rich and interconnected knowledge graph from disparate data sources. Instead of storing data in isolated tables, this approach creates a graph where the relationships between data points are as important as the data itself.

By linking entities to standard ontologies, we move from ambiguous free-text fields (e.g., "vaccination response") to standardized, machine-readable definitions (e.g., `VO_0000002`). This enhances data quality, enables powerful analytical queries, and ensures interoperability with other datasets.

---

## Key Features

- **Data Ingestion**: Parses various data formats (key-value and XML-like snippets) into structured Python dictionaries.
- **ID Transformation**: Programmatically converts raw numeric IDs from source files into globally unique, prefixed IDs (e.g., `785` becomes `exp_785`) before loading.
- **Multi-Entity Mapping**: Supports multiple biological entities:
    - Study
    - Experiment
    - Intervention
    - Material
    - Organism
    - Sample
- **Precise Ontology Linking**: Creates specific, named relationships (e.g., `:HAS_TYPE`, `:USES_MATERIAL`, `:IS_SPECIES`) to accurately model the connection between a data node and an ontology term.
- **Data Enrichment**: Copies relevant metadata (definitions, labels, synonyms) from the ontology nodes directly onto the data nodes, making the graph easier to explore and query.

---

## How It Works

The script operates in two main phases within a single run:

### 1. Data Ingestion and Transformation (import_to_neo4j.py)

- It reads raw data for each entity (Study, Experiment, etc.).
- The `parse_node_data` function converts the raw string data into a Python dictionary.
- **Crucially, it transforms the primary numeric ID into a prefixed string ID** (e.g., `organism_id: 13` becomes `organism_id: 'org_13'`).
- It then uses a `MERGE` query to create or update the corresponding node in Neo4j, ensuring no duplicates are created.

### 2. Ontology Mapping (ontology_mapping.py)

- After the data nodes are in the graph, a series of `map_*_nodes` functions are called.
- Each function targets a specific node label (e.g., `map_experiment_nodes` targets `:Experiment` nodes).
- It finds nodes that have a relevant ontology ID property (e.g., `experiment_type_id`).
- It then finds the corresponding `:Resource` node (from the imported ontology) by matching the ID with the resource's URI.
- Finally, it creates a relationship between the data node and the ontology resource node.

---

## Graph Data Model

The script generates the following primary nodes and relationships:

| Node Label | Identifier | Mapped By | Relationship Type | Ontology Properties Copied? |
| :--- | :--- | :--- | :--- | :--- |
| **Study** | `study_id` | `study_type_id` | `[:HAS_TYPE]` | Yes (as `ontology_*`) |
| **Experiment**| `experiment_id`| `experiment_type_id`| `[:VO_REPRESENTATION]`| Yes (as `vo_*`) |
| **Material** | `material_id` | `material_name_id` | `[:VO_REPRESENTATION]`| Yes (as `vo_*`) |
| **Intervention**| `intervention_id`| Multiple IDs | Multiple specific types | No |
| | | `intervention_type_id` | `[:HAS_TYPE]` | |
| | | `material_id` | `[:USES_MATERIAL]` | |
| | | `intervention_route_id`| `[:HAS_ROUTE]` | |
| | | `dosage_unit_id` | `[:HAS_DOSAGE_UNIT]`| |
| **Organism** | `organism_id` | `species_id` | `[:IS_SPECIES]` | No |
| **Sample** | `sample_id` | `sample_type_id` | `[:HAS_TYPE]` | No |

**Note on Relationship Types:**
- A generic `[:VO_REPRESENTATION]` is used when the ontology term defines *what the node is* (e.g., an Experiment, a Material).
- Specific relationships like `[:HAS_TYPE]` or `[:USES_MATERIAL]` are used when the ontology term defines a specific *aspect* or *attribute* of the node. This creates a more precise and queryable model.

---

## Prerequisites

- Python 3.x
- A running Neo4j Database instance (Community or Enterprise).
- The `neo4j` Python library.
- Neosemantics (n10s): This Neo4j extension is used for importing the OWL ontology.

---

## Setup and Usage

1.  **Install the Neo4j Library:**
    ```bash
    pip install neo4j
    ```

2.  **Load Ontologies into Neo4j:**
    Before running this script, ensure you have loaded the necessary ontologies (VO, OBI, etc.) into your Neo4j database. A common way to do this is with the `n10s` (Neosemantics) plugin for Neo4j. All ontology terms should be loaded as nodes with the label `:Resource`.

3.  **Configure the Database Connection:**
    Open the Python script and update the connection details in the `if __name__ == "__main__"` block to match your Neo4j instance:
    ```python
    # !!! IMPORTANT: Replace with your Neo4j database credentials !!!
    URI = "bolt://localhost:7687"
    AUTH = ("neo4j", "your_password")
    ```

4.  **Run the Script:**
    Execute the script from your terminal. It will connect to the database, load the sample data, and run all the mapping functions.
    ```bash
    python your_script_name.py
    ```