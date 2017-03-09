import click
from datetime import timedelta

from valohai_cli.api import request
from valohai_cli.consts import execution_statuses
from valohai_cli.ctx import get_project
from valohai_cli.messages import print_table


@click.command()
@click.option(
    '--status',
    multiple=True,
    help='Filter by status (default: all)',
    type=click.Choice(sorted(execution_statuses | {'incomplete'}))
)
def list(status):
    """
    Show a list of executions for the project.
    """
    project = get_project(require=True)
    params = {
        'project': project.id,
        'count': 9001,
        'ordering': 'counter',
    }
    if status:
        params['status'] = set(status)
    executions = request('get', '/api/v0/executions/', params=params).json()['results']
    for exec in executions:
        exec['url'] = exec['urls']['display']
        exec['duration'] = str(timedelta(seconds=round(exec['duration'])) if exec['duration'] else '').rjust(10)

    print_table(
        executions,
        columns=['counter', 'status', 'step', 'duration', 'url'],
        headers=['#', 'Status', 'Step', 'Duration', 'URL'],
    )
