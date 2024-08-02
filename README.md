# AML-Deploy - Azure Machine Learning Model Deployment
*Documentation under construction*

## Introduction

This project demonstrates how to deploy a machine learning model using Azure Machine Learning (AML). The setup leverages Azure's scalable cloud resources for training, deploying, and managing machine learning models efficiently. This repository contains scripts and configuration files necessary for deploying a model to AML and setting up continuous integration and continuous deployment (CI/CD) pipelines.

## Prerequisites

Before starting, ensure you have the following:

- **Azure Account**: You'll need an active Azure subscription.
- **Azure Machine Learning Workspace**: Set up an AML workspace in the Azure portal.
- **Azure CLI**: The Azure Command-Line Interface (CLI) is necessary for interacting with Azure services. You can install it via terminal using `pip install azure-cli` or from [here](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli).
- **Python**: Python 3.8 or later.
- **Git**: Version control tool to clone this repository.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/jotap123/aml-deploy.git
cd aml-deploy
```

### 2. Configure Azure Machine Learning

- **Login to Azure**:

    ```bash
    az login
    ```

- **Set up AML Workspace**: Follow the instructions in the Azure documentation to set up your AML workspace [here](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-manage-workspace).

- **Configure Workspace in Code**: Modify the provided configuration files to point to your Azure Machine Learning workspace.

### 3. Environment Setup

- **Create a Virtual Environment**:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

- **Install Required Python Packages**:

    ```bash
    pip install -r requirements.txt
    ```

## Deployment Instructions

### 1. Train and Register Model

Use the provided training script to train your machine learning model and register it to your AML workspace.

```bash
python train.py
```

### 2. Deploy Model

Deploy the registered model to an Azure container instance or Azure Kubernetes Service (AKS).

```bash
python deploy.py
```

### 3. Monitor and Manage

Use the Azure portal or the Azure CLI to monitor your deployed model, track usage, and manage scaling.

**Usage**
After deployment, interact with the model through the provided API endpoint. Use the API to make predictions by sending data in the appropriate format.

**Troubleshooting**
- **Authentication Issues**: Ensure you are logged in to the Azure CLI and have the necessary permissions.
- **Deployment Failures**: Check the logs for errors in deployment scripts or model configuration.
- **API Errors**: Validate the input data format and ensure the model is correctly deployed.

**Contributing**
Contributions are welcome! Please fork the repository, create a new branch, and submit a pull request with your changes. Ensure your code follows the project's coding standards and includes appropriate tests.

**License**
This project is licensed under the MIT License - see the LICENSE file for details.
