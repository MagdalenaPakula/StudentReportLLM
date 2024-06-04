# Usage Guide for LLM Grading System

This guide provides step-by-step instructions on how to use the LLM Grading System to upload student reports, set grading criteria, and retrieve grading results.

## Prerequisites

Make sure you have followed the setup guide and have the application running. The application should be launched using:

```bash
    python src/gui/__init__.py
```

## Using the Application
### 1. Uploading a Student Report
- **Open the Application**: Ensure the LLM Grading System GUI is running.

- **Upload Report**:
  - Click on the "Upload" button in the main window.
  - Select the report file (PDF, Word, or LaTeX) from your local system.
  - Click "Open" to upload the file.

- **Confirmation**:
  - A confirmation message will appear indicating the report was uploaded successfully.
  - Note the report_id provided, as it will be used for further operations.

### 2. Setting Grading Criteria
- **Open Criteria Dialog**:
  - Click on the "Set Criteria" button in the main window.

- **Define Criteria**:
  - Enter the criteria for grading. Each criterion should have a name and a weight.
  - Example:
    ```json
    {
      "criteria": [
        {
          "name": "Content Quality",
          "weight": 0.5
        },
        {
          "name": "Compliance with Guidelines",
          "weight": 0.3
        },
        {
          "name": "Originality",
          "weight": 0.2
        }
      ]
    }
    ```
    

- **Save Criteria**:
  - Click the "Save" button to apply the criteria.
  - A confirmation message will appear indicating the criteria were set successfully.

### 3. Retrieving Grading Results
- **Check Results**:
  - Click on the "Check Results" button in the main window.
  - Enter the `report_id` of the report you want to retrieve results for.

- **View Results**:
  - The results will be displayed, showing scores for quality, compliance, and originality.
  - Example results format:
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
    ```

- **Detailed Analysis**:
  - For a detailed breakdown, you can click on each criterion to see specific feedback and areas of improvement.

### Additional Features

#### Analyzing Common Errors

- The system provides an analysis of common errors across all reports.
- Click on the "Analyze Errors" button to view frequently occurring mistakes and suggestions for improvement.

#### Exporting Results

- You can export the grading results to a CSV or JSON file for further analysis.
- Click on the "Export Results" button and choose the desired format.

### Troubleshooting

#### Common Issues

- **File Upload Errors**:
  - Ensure the file format is supported (PDF, Word, LaTeX).
  - Check your internet connection and try again.

- **Criteria Not Saving**:
  - Ensure all criteria have valid names and weights.
  - Check for any error messages and correct the input accordingly.

- **No Results Found**:
  - Verify the `report_id` is correct.
  - Ensure the report has been graded before attempting to retrieve results.
