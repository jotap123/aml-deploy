import os

import dotenv
from azureml.core import Environment, Workspace
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.core.runconfig import RunConfiguration
from azureml.pipeline.core import Pipeline, PipelineEndpoint
from azureml.pipeline.steps import PythonScriptStep

dotenv.load_dotenv()


def deploy_to_aml(
    pipeline_name=None,
    script_path="",
):

    tenant_id = os.environ.get("AZURE_TENANT_ID")
    client_id = os.environ.get("AZURE_CLIENT_ID")
    secret = os.environ.get("AZURE_CLIENT_SECRET")

    spa_auth = ServicePrincipalAuthentication(
        tenant_id=tenant_id,
        service_principal_id=client_id,
        service_principal_password=secret,
    )

    try:
        ws = Workspace.get(
            name="aml-pae2",
            subscription_id="283a9cc8-19c4-42d7-b65e-f6e5705695e0",
            resource_group="rg-mlopaes",
            auth=spa_auth,
        )
    except:
        ws = Workspace.get(
            name="aml-pae2",
            subscription_id="283a9cc8-19c4-42d7-b65e-f6e5705695e0",
            resource_group="rg-mlopaes",
        )

    env_dict = {
        "AZURE_CLIENT_ID": client_id,
        "AZURE_CLIENT_SECRET": secret,
        "AZURE_TENANT_ID": tenant_id,
    }

    test_env = Environment.from_pip_requirements("env", "./requirements.txt")
    run_config = RunConfiguration()
    run_config.environment = test_env
    run_config.environment_variables = env_dict

    step = PythonScriptStep(
        name=pipeline_name,
        script_name=script_path,
        source_directory=".",
        runconfig=run_config,
        compute_target="compaeting",
    )

    az_pipeline = Pipeline(ws, steps=[step])
    published_pipeline = az_pipeline.publish(
        name=pipeline_name, description=pipeline_name
    )

    try:
        pipeline_endpoint = PipelineEndpoint.publish(
            workspace=ws,
            name="TestEndpoint",
            pipeline=published_pipeline,
            description="Publish pipeline endpoint for test",
        )
    except:
        pipeline_endpoint = PipelineEndpoint.get(workspace=ws, name="TestEndpoint")

    pipeline_endpoint.add_default(published_pipeline)


if __name__ == "__main__":
    deploy_to_aml(
        pipeline_name="model_test",
        script_path="dags/pipeline.py",
    )
