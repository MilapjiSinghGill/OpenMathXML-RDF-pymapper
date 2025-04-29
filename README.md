# OpenMath to RDF Mapping

This repository contains a Python-based converter that transforms OpenMath expressions encoded in XML into RDF (Turtle) format, using explicit `rdf:List` structures for function arguments.

## ✨ Purpose

The goal of this project is to enable the semantic integration and querying of mathematical expressions within knowledge graphs. The input is a standard OpenMath XML structure, and the output is a corresponding RDF graph with correct handling of nested applications and argument ordering.

## 🧩 Problem Statement

OpenMath expressions often involve deeply nested mathematical structures such as function applications with multiple arguments, combinations of operators, and recursive subterms. Generic RDF mapping tools like RML cannot natively handle these recursive structures or generate valid `rdf:List` encodings. Therefore, a custom Python mapping is used to traverse and transform the tree structure into a semantically correct RDF representation.

## ⚙️ Features

- Supports `OMV`, `OMS`, `OMA`, `OMI`, and `OMF` OpenMath elements.
- Generates `om:Application`, `om:Variable`, `om:Symbol`, and RDF lists using `rdf:first`, `rdf:rest`, and `rdf:nil`.
- Handles arbitrary nesting through recursive traversal of the OpenMath XML tree.
- Uses UUID-based URIs to uniquely identify function applications.

## 🔧 Requirements

- Python 3.7+
- `rdflib` library (`pip install rdflib`)

## ▶️ Usage

Place your OpenMath XML files in the project directory. Run the converter script:

```bash
python OMtoRDF_BN.py
