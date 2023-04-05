import typer
from rich.console import Console
from cli.enums import DocDbClustersEnum, DocDbClusterActionsEnum
from cli.k8s.k8s_pods import aws_docdb_py_status
from cli.utils.aws_utils import eks_update

app = typer.Typer()
console = Console()


@app.command()
def docdb(action: DocDbClusterActionsEnum = DocDbClusterActionsEnum.status,
          env: DocDbClustersEnum = DocDbClustersEnum.all):
    if action == DocDbClusterActionsEnum.status:
        aws_docdb_py_status(cluster_name=env.value)
    elif action == DocDbClusterActionsEnum.create:
        pass
    elif action == DocDbClusterActionsEnum.delete:
        pass
    elif action == DocDbClusterActionsEnum.update:
        pass
    else:
        typer.echo(f"Unknown action: {action.value}")


@app.command()
def eks():
    eks_update(console_=console)


@app.command()
def msk(action: DocDbClusterActionsEnum = DocDbClusterActionsEnum.status,
        env: DocDbClustersEnum = DocDbClustersEnum.all):
    typer.echo(f"Hello from docdb env: {env.value} action: {action.value}")


if __name__ == "__main__":
    app()
