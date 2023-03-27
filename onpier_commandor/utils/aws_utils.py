import subprocess
from rich.console import Console
from rich.table import Table


def port_forward_list():
    profiles = get_profiles()
    # sort profiles by name
    profiles.sort()
    services = []
    for ind, profile_name in enumerate(profiles):
        services.append(
            {
                'profile': profile_name,
                'services': [
                    {
                        "host": f"{profile_name}.vault.127.0.0.1.nip.io",
                        'namespace': 'vault',
                        'service': 'vault',
                        'port': 8200,
                        'local_port': 8200 + ind,
                        'process_id': None,
                    },
                    {
                        "host": f"{profile_name}.docdb.127.0.0.1.nip.io",
                        'namespace': 'default',
                        'service': 'aws-documentdb',
                        'port': 8081,
                        'local_port': 8300 + ind,
                        'process_id': None,
                    },
                    {
                        "host": f"{profile_name}.msk.127.0.0.1.nip.io",
                        'namespace': 'default',
                        'service': 'aws-msk',
                        'port': 9092,
                        'local_port': 9000 + ind,
                        'process_id': None,
                    },
                ]
            }
        )
    return services


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


def start_port_forward_background(namespace: str, service: str, port: int, local_port: int, console_: Console):
    # check if port is already forwarded on local_port. if so, kill it,start new port forward
    existing_port_forwards = subprocess.check_output(['lsof', '-i', f':{local_port}'])
    existing_port_forwards = existing_port_forwards.decode('utf-8').strip().split('\n')
    for existing_port_forward in existing_port_forwards:
        if existing_port_forward.startswith('kubectl'):
            existing_port_forward = existing_port_forward.split(' ')
            existing_port_forward = [x for x in existing_port_forward if x]
            process_id = existing_port_forward[1]
            stop_port_forward(process_id, console_=console_)
    console_.print(f"Starting port forward: {namespace} {service} {port} {local_port}", style="bold yellow")
    nohup_cmd = ['nohup', 'kubectl', 'port-forward', '-n', namespace, service, f'{local_port}:{port}', '&']
    process_id = subprocess.check_output(nohup_cmd)
    process_id = process_id.decode('utf-8').strip()
    console_.print(f"Started port forward: {process_id} {namespace} {service} {port} {local_port}", style="bold green")
    return process_id


def stop_port_forward(process_id: str, console_: Console):
    console_.print(f"Stopping port forward: {process_id}", style="bold red")
    subprocess.run(['kill', '-9', process_id])


def export_service_map_to_csv(port_forward_list_: list, console_: Console):
    with open('service_map.csv', 'w') as f:
        f.write('profile,namespace,service,port,local_port,host,process_id\n')
        for profile in port_forward_list_:
            profile_name = profile['profile']
            for service in profile['services']:
                f.write(
                    f'{profile_name},{service["namespace"]},{service["service"]},{service["port"]},{service["local_port"]},{service["host"]},{service["process_id"]}\n')


def start_port_forwards(console_: Console):
    port_forward_list_ = port_forward_list()
    table = Table('Profile', 'Namespace', 'Service', 'Port', 'Local Port', 'Host', 'Process ID', show_header=True,
                  header_style="bold magenta")
    for ind,profile in enumerate(port_forward_list_):
        profile_name = profile['profile']
        aws_sso_login(profile_name)
        for ind_,service in enumerate(profile['services']):
            process_id = start_port_forward_background(service['namespace'], service['service'], service['port'],
                                                       service['local_port'],
                                                       console_=console_)
            port_forward_list_[ind]['services'][ind_]['process_id'] = process_id
            table.add_row(profile_name, service['namespace'], service['service'], service['port'],
                          service['local_port'], service['host'], process_id)
    console_.print(table)
    export_service_map_to_csv(port_forward_list_=port_forward_list_, console_=console_)


def stop_port_forwards(console_: Console):
    port_forward_list_ = port_forward_list()
    table = Table('Profile', 'Namespace', 'Service', 'Port', 'Local Port', 'Host', 'Process ID', show_header=True,
                  header_style="bold magenta")
    for ind,profile in enumerate(port_forward_list_):
        profile_name = profile['profile']
        aws_sso_login(profile_name)
        for ind_,service in enumerate(profile['services']):
            process_id = service['process_id']
            stop_port_forward(process_id, console_=console_)
            table.add_row(profile_name, service['namespace'], service['service'], service['port'],
                          service['local_port'], service['host'], process_id)
    console_.print(table)

if __name__ == "__main__":
    console = Console()
    eks_update(console_=console)
