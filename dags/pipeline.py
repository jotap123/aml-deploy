from dags.models.train import train_model
from dags.visualization.inference import predictions


def run_dag(task):
    from dags.runner import run_task

    run_task(task)


def train():
    train_model()


def predict():
    predictions()


if __name__ == "__main__":
    train()
