# Architecture Overview

## Introduction

The LLM Grading System is designed to automate the assessment of student reports using advanced language models. The system evaluates the quality of content and compliance with project guidelines, providing an objective and precise tool to support the educational process.

## System Components

### 1. Converters

The Converters module handles the conversion of various document formats (PDF, Word, LaTeX) to plain text for analysis.


### 2. Grading

The Grading module evaluates the content quality and compliance with guidelines using pre-trained language models.

### 3. Database

The Database module manages the storage and retrieval of data.

### 4. API

The API module provides endpoints for interaction with the system.

### 5. Utils

The Utils module contains utility functions for file handling and text processing.

### 6. GUI

The GUI module provides a graphical user interface for user interaction.

### 7. Tests

The Tests module contains unit and integration tests for the system components.

## Data Flow

1. **Document Upload**: Users upload student reports via the GUI or API.
2. **Conversion**: The Converters module transforms documents into plain text.
3. **Grading**: The Grading module evaluates the text based on predefined criteria and checks for originality.
4. **Storage**: Grading results are stored in MongoDB, and vector data is managed by Qdrant.
5. **Retrieval**: Users can retrieve grading results and analyses through the GUI or API.
