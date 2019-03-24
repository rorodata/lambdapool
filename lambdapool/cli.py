import sys
import click

from .function import LambdaPoolFunction
from . import utils
from tabulate import tabulate

from lambdapool import exceptions

@click.group()
def cli():
    pass

@cli.command()
@click.option('--requirements', '-r', type=click.Path(exists=True), help="Specifies the dependencies to be installed along with the function")
@click.option('--memory', type=click.INT, help="Sets the memory size of the function environment")
@click.option('--timeout', type=click.INT, help="Sets the timeout for the function in seconds")
@click.option('--layers', help="Sets the layers to be used when the function is ran. The Layers ARN's (a maximum of 5) should be specified.")
@click.argument('function_name', nargs=1)
@click.argument('paths', nargs=-1, type=click.Path(exists=True))
def create(function_name, paths, requirements, memory, timeout, layers):
    """Create a new function"""
    click.echo('=== Creating lambdapool function ===')

    try:
        func = LambdaPoolFunction(
            function_name=function_name,
            paths=paths,
            requirements=requirements,
            memory=memory,
            timeout=timeout,
            layers=layers.split(',') if layers else []
        )

        if func.exists():
            click.echo(f'lambdapool function {function_name} already exists')
            sys.exit(1)

        func.create()
    except exceptions.LambdaFunctionError as e:
        click.echo(f'ERROR: {e}')
        sys.exit(1)

    click.echo(f'=== Succesfully created lambdapool function {function_name} ===')

@cli.command()
def list():
    """List all deployed functions"""
    funcs = LambdaPoolFunction.list()
    funcs = sorted(funcs, key=lambda x: x['last_updated'], reverse=True)
    rows = []
    for func in funcs:
        rows.append(
            [
                func['function_name'],
                utils.convert_size(func['size']),
                utils.datestr(func['last_updated']),
                func['memory'],
                func['timeout']
            ]
        )
    click.echo(tabulate(rows, headers=['FUNCTION NAME', 'SIZE', 'WHEN', 'RUNTIME MEMORY (MB)', 'TIMEOUT (SEC)']))

@cli.command()
@click.option('--requirements', '-r', type=click.Path(exists=True), help="Specifies the dependencies to be installed along with the function")
@click.option('--memory', type=click.INT, help="Sets the memory size of the function environment")
@click.option('--timeout', type=click.INT, help="Sets the timeout for the function in seconds")
@click.option('--layers', help="Sets the layers to be used when the function is ran. The Layers ARN's (a maximum of 5) should be specified.")
@click.argument('function_name', nargs=1)
@click.argument('paths', nargs=-1)
def update(function_name, paths, requirements, memory, timeout, layers):
    """Update an existing function"""
    click.echo('=== Updating lambdapool function ===')

    try:
        func = LambdaPoolFunction(
            function_name=function_name,
            paths=paths,
            requirements=requirements,
            memory=memory,
            timeout=timeout,
            layers=layers.split(',') if layers else []
        )
        func.update()
    except exceptions.LambdaFunctionError as e:
        click.echo(f'ERROR: {e}')
        sys.exit(1)

    click.echo(f'=== Updated lambdapool function {function_name} ===')

@cli.command()
@click.argument('function_name', nargs=1)
def delete(function_name):
    """Delete a function"""
    click.echo('=== Deleting lambdapool function ===')

    func = LambdaPoolFunction(function_name=function_name)
    func.delete()

    click.echo(f'=== Deleted lambdapool function {function_name}===')
