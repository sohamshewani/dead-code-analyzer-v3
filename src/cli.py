import click
from rich.console import Console
from rich.table import Table
import asyncio
from .core import analyze_code, cache_analysis_result, get_analysis_result

console = Console()

@click.group()
@click.version_option()
@click.pass_context
@click.option('--cache/--no-cache', default=True, help='Cache analysis results in SQLite database')
@click.option('--concurrency', default=5, help='Number of concurrent tasks')
def cli(ctx, cache, concurrency):
    ctx.ensure_object(dict)
    ctx.obj['cache'] = cache
    ctx.obj['concurrency'] = concurrency

@cli.command()
@click.argument('filepaths', nargs=-1, type=click.Path(exists=True))
def analyze(filepaths):
    cache = ctx.obj['cache']
    concurrency = ctx.obj['concurrency']
    tasks = []
    for filepath in filepaths:
        if cache and get_analysis_result(filepath) == 'Not cached':
            task = asyncio.create_task(analyze_code(filepath))
            tasks.append(task)
        else:
            console.print(f'[yellow]Skipping cached file: {filepath}[/yellow]')
    if tasks:
        results = asyncio.gather(*tasks, return_exceptions=True)
        for result in asyncio.run(results):
            filename = result[0]
            result = result[1]
            cache_analysis_result(filename, result)
            console.print(f'[green]Dead code found in: {filename}[/green]' if 'dead code' in result else f'[green]No dead code in: {filename}[/green]')

@cli.command()
def stress_test():
    concurrency = ctx.obj['concurrency']
    console.print(f'[blue]Starting stress test with {concurrency} concurrent requests[/blue]')
    urls = ['http://example.com/api'] * concurrency
    tasks = [asyncio.create_task(stress_test_api(url)) for url in urls]
    results = asyncio.gather(*tasks, return_exceptions=True)
    for result in asyncio.run(results):
        console.print(result)

async def stress_test_api(url: str):
    try:
        async with asyncio.timeout(5):
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return f'Response from {url}: {response.status}'
    except Exception as e:
        return f'Error: {e}'