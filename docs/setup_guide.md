# Setup Guide for LLM Grading System

This guide will walk you through the steps necessary to set up and run the LLM Grading System on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.12
- Git
- Virtualenv (optional but recommended)

## Step 1: Clone the Repository

Start by cloning the repository from GitHub:
```bash
    git clone https://github.com/magdalenpakula/yourproject.git
    cd yourproject
```

## Step 2: Set Up a Virtual Environment
It is recommended to use a virtual environment to manage dependencies. You can create one using virtualenv:
 
```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
```

## Step 3: Install Dependencies
Install the required Python packages using pip:

```bash
    pip install -r requirements.txt
```

## Step 4: Set Up MongoDB and Qdrant
 - MongoDB: Ensure MongoDB is installed and running on your local machine or remote server. You can find installation instructions on the official MongoDB website.

 - Qdrant: Install and start Qdrant using Docker.
 - 
```bash
    docker pull qdrant/qdrant
    docker run -p 6333:6333 qdrant/qdrant
```

## Step 5: Configure the Application
Create a .env file in the root directory and add the following configurations:
```bash
    MONGO_URI=mongodb://localhost:27017
    QDRANT_HOST=localhost
    QDRANT_PORT=6333
```
Adjust the values as necessary based on your environment setup.

## Step 6: Running the Application
To start the application, run the following command:
```bash
    python services/gui/main.py
```
This will launch the GUI for the LLM Grading System.

##  Step 7: Running Tests
To ensure everything is set up correctly, run the unit tests
```bash
    pytest services/tests/
```

## Additional Setup (Optional)
### Installing LaTeX (For LaTeX File Processing)
For processing LaTeX files, you may need to install a LaTeX distribution.