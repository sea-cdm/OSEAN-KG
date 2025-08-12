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

Before you begin, ensure you have the following installed:

* **Python 3.6 or higher:** Required to run the Python scripts.
* **Neo4j Graph Database:** You need a running instance of Neo4j.
* **Neo4j Python Driver:** This project uses the official Neo4j Python driver. You can install it using pip:
    ```bash
    pip install neo4j
    ```
* **dotenv:** For managing environment variables. Install using pip:
    ```bash
    pip install python-dotenv
    ```
* **Neosemantics (n10s):** This Neo4j extension is used for importing the OWL ontology.

## Installation

1.  **Clone the repository (if you have the code in a repository):**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

## Configuration

### .env File Configuration

This project uses a `.env` file to store sensitive information like your Neo4j connection URI, username, and password.

1.  **Create a `.env` file** in the root directory of your project.
2.  **Add your Neo4j connection details** to the `.env` file. Replace the placeholders with your actual credentials:
    ```dotenv
    URI=bolt://localhost:7687  # Replace with your Neo4j URI
    USERNAME=neo4j             # Replace with your Neo4j username
    PASSWORD=your_password     # Replace with your Neo4j password
    ```

### Neosemantics (n10s) Configuration

To enable the import of the OWL ontology, you need to configure Neosemantics in your Neo4j instance. Follow these steps:

1.  **Download Neosemantics:** Download the latest stable release JAR file of Neosemantics from the official GitHub releases page: [https://github.com/neo4j-labs/neosemantics/releases](https://github.com/neo4j-labs/neosemantics/releases). Look for a file named something like `neosemantics-{version}.jar`.

2.  **Place the JAR file in the `plugins` directory:** Locate your Neo4j installation directory. Inside it, you will find a `plugins` directory. Copy the downloaded Neosemantics JAR file into this directory.

3.  **Configure `neo4j.conf`:** Open the `neo4j.conf` file located in the `conf` directory of your Neo4j installation.

4.  **Add the following lines to the `neo4j.conf` file:**

    * **Enable unmanaged extensions for Neosemantics:**
        ```
        dbms.unmanaged_extension_classes=n10s.extension=/rdf
        ```
    * **Set the import directory:** This allows Neo4j to access files in the specified import directory. While this project imports from a remote URL, it's a good practice to configure it.
        ```
        dbms.directories.import=import
        ```
        **Note:** Ensure that the `import` directory exists within your Neo4j installation directory. You might need to create it if it doesn't exist.

5.  **Restart Neo4j:** After making these changes, you need to restart your Neo4j server for the configuration to take effect.

## Usage

1.  **Activate your Python environment (if applicable):** If you are working within a virtual environment, make sure to activate it. For example, if you used `venv`:
    ```bash
    source neo4j-env/Scripts/activate  # On Windows
    source neo4j-env/bin/activate    # On macOS and Linux
    ```
    (This step is also mentioned in the code comments).

2.  **Run the main script (`__main__.py` if you structure your project that way, or directly run the provided script):** Execute the 2 Python scripts to start the import and mapping process.
    ```bash
    python import_to_neo4j.py
    ```
    and then
    ```bash
    python ontology_mapping.py
    ```