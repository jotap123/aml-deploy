import importlib
import logging

import click

logger = logging.getLogger(__name__)

try:
    import colored_traceback

    colored_traceback.add_hook()
except ModuleNotFoundError:
    pass


@click.group()
def run():
    pass


@run.command("task")
@click.argument("dag")
@click.argument("task")
def task(dag, task):
    try:
        mod = importlib.import_module(f"dags.{dag}")
    except ModuleNotFoundError as ex:
        if "dag" not in ex.args[0]:
            raise
        click.secho(f"ERROR: Dag not found '{dag}'")
        logger.exception(ex)
        raise SystemExit(1)

    mod.run_dag(task)


if __name__ == "__main__":
    from dags import logs

    logs.init()
    run()
