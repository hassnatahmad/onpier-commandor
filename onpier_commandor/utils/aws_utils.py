import subprocess
from rich.console import Console
from rich.table import Table


def get_profiles():
    output = subprocess.check_output(['aws', 'configure', 'list-profiles'])
    profiles = output.decode('utf-8').strip().split('\n')
    return profiles


def aws_sso_login(profile_name):
    cmd = ['aws', 'sso', 'login', '--profile', profile_name, '--region', 'eu-central-1']
    subprocess.run(cmd)


def get_eks_clusters(profile_name: str, console_: Console):
    cmd = ['aws', 'eks', 'list-clusters', '--region', 'eu-central-1', '--profile', profile_name, '--output', 'text',
           '--query', 'clusters[*]']
    output = subprocess.check_output(cmd)
    found_clusters = output.decode('utf-8').strip().split('\n')

    clusters = []
    table = Table('Profile', 'Cluster', 'Region', show_header=True, header_style="bold magenta")
    for cluster in found_clusters:
        if not cluster or cluster == '':
            continue
        clusters.append(cluster)
        table.add_row(profile_name, cluster, 'eu-central-1')
    if len(clusters) > 0:
        console_.print(table)
    return clusters


def update_kubeconfig(profile_name, cluster):
    subprocess.run(
        ['aws', 'eks', 'update-kubeconfig', '--region', 'eu-central-1', '--profile', profile_name, '--name',
         cluster])


# @app.command()
def eks_update(console_: Console):
    profiles = get_profiles()
    aws_sso_login(profiles[0])
    for profile_name in profiles:
        clusters = get_eks_clusters(profile_name, console_=console_)

        if not clusters:
            console_.print(f"No clusters found for profile: {profile_name}")
        else:
            for cluster in clusters:
                # console_.print(f"Updating kubeconfig for cluster: {cluster}")
                update_kubeconfig(profile_name, cluster)

    console_.print("Updated .kube/config:")


if __name__ == "__main__":
    console = Console()
    eks_update(console_=console)
