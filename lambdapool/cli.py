import click
import os

from .function import LambdaPoolFunction
from . import utils
from tabulate import tabulate

@click.group()
def cli():
    pass

@cli.command()
@click.option('--requirements', '-r', type=click.Path(exists=True))
@click.argument('function_name', nargs=1)
@click.argument('paths', nargs=-1, type=click.Path(exists=True))
def create(function_name, paths, requirements):
    click.echo('=== Creating lambdapool function ===')
    func = LambdaPoolFunction(function_name, paths, requirements)
    func.create()
    click.echo(f'=== Succesfully created lambdapool function {function_name} ===')

@cli.command()
def list():
    funcs = LambdaPoolFunction.list()
    funcs = sorted(funcs, key=lambda x: x['last_updated'], reverse=True)
    rows = []
    for func in funcs:
        rows.append([func['function_name'], utils.convert_size(func['size']), utils.datestr(func['last_updated'])])
    click.echo(tabulate(rows, headers=['FUNCTION NAME', 'SIZE', 'WHEN']))

@cli.command()
@click.option('--requirements', '-r', type=click.Path(exists=True))
@click.argument('function_name', nargs=1)
@click.argument('paths', nargs=-1)
def update(function_name, paths, requirements):
    click.echo('=== Updating lambdapool function ===')

    func = LambdaPoolFunction(function_name, paths, requirements)
    func.update()

    click.echo('=== Updated lambdapool function ===')


@cli.command()
@click.argument('function_name', nargs=1)
def delete(function_name):
    click.echo('=== Deleting lambdapool function ===')

    func = LambdaPoolFunction(function_name)
    func.delete()

    click.echo('=== Deleted lambdapool function ===')
