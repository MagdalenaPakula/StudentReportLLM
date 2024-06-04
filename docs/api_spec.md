# API Specification

## Introduction

This document outlines the API endpoints for the LLM Grading System. The API allows users to upload student reports, set grading criteria, and retrieve grading results.

## Base URL
http://StudentReportGrader/api/

## Endpoints

### 1. Upload Report

**Endpoint:** `/upload`

**Method:** `POST`

**Description:** Uploads a student report for grading.

**Request:**

- **Headers:**
  - `Content-Type: multipart/form-data`
- **Body:**
  - `file`: The report file to be uploaded (PDF, Word, LaTeX).

**Response:**

- **Success (200):**
  ```json
  {
    "message": "Report uploaded successfully.",
    "report_id": "<report_id>"
  }
  
- **Error (400/500):**
  ```json
  {
    "error": "Description of the error."
  }

### 2. Set Grading Criteria
**Endpoint:** `/criteria`

**Method:** `POST`

**Description:** Sets the grading criteria for evaluating reports.

**Request:**
- **Headers:**
  - `Content-Type: application/json`
- **Body:**
  ```json
  {
      "criteria": [
    {
      "name": "Criterion 1",
      "weight": 0.5
    },
    {
      "name": "Criterion 2",
      "weight": 0.5
    }
  ]
  }
  
**Response:**
- **Success (200):**
  ```json
  {
    "message": "Criteria set successfully."
  }
  
- **Error (400/500):**
  ```json
  {
    "error": "Description of the error."
  }

### 3. Retrieve grading results
**Endpoint:** `/results/<report_id>`

**Method:** `GET`

**Description:** Retrieves the grading results for a specific report.

**Response:**
- **Success (200):**
  ```json
  {
    "report_id": "<report_id>",
    "grading": {
      "quality": 85,
      "compliance": 90,
      "originality": 95,
      "overall": 90
    }
  }
  
- **Error (400/500):**
  ```json
  {
    "error": "Description of the error."
  }

### 3. Error codes
Common Errors
- 400 Bad Request: The request could not be understood or was missing required parameters.
- 401 Unauthorized: Authentication failed or user does not have permissions for the requested operation.
- 404 Not Found: The requested resource could not be found.
- 500 Internal Server Error: An error occurred on the server.


