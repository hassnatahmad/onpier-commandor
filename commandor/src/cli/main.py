import typer
from rich.console import Console

from cli.enums import DocDbClustersEnum, DocDbClusterActionsEnum
from cli.k8s.k8s_pods import aws_docdb_status, aws_docdb_delete, aws_docdb_update
from cli.utils.aws_utils import eks_update

app = typer.Typer()
console = Console()


@app.command()
def docdb(action: DocDbClusterActionsEnum = DocDbClusterActionsEnum.status,
          env: DocDbClustersEnum = DocDbClustersEnum.all):
    if action == DocDbClusterActionsEnum.status:
        aws_docdb_status(cluster_name=env.value)
    elif action == DocDbClusterActionsEnum.delete:
        aws_docdb_delete(cluster_name=env.value)
    elif action == DocDbClusterActionsEnum.update:
        aws_docdb_update(cluster_name=env.value)
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
