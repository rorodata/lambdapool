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
@click.option('--requirements', '-r', type=click.Path(exists=True))
@click.option('--memory', type=click.INT)
@click.option('--timeout', type=click.INT)
@click.option('--layers')
@click.argument('function_name', nargs=1)
@click.argument('paths', nargs=-1, type=click.Path(exists=True))
def create(function_name, paths, requirements, memory, timeout, layers):
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
@click.option('--requirements', '-r', type=click.Path(exists=True))
@click.option('--memory', type=click.INT)
@click.option('--timeout', type=click.INT)
@click.option('--layers')
@click.argument('function_name', nargs=1)
@click.argument('paths', nargs=-1)
def update(function_name, paths, requirements, memory, timeout, layers):
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
    click.echo('=== Deleting lambdapool function ===')

    func = LambdaPoolFunction(function_name=function_name)
    func.delete()

    click.echo(f'=== Deleted lambdapool function {function_name}===')
