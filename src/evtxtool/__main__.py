import click
import evtxtool.evtx


def print_help(ctx, param, value):
    if value is True:
        click.echo(ctx.get_help())
        ctx.exit()


@click.group()
def main():
    pass


@main.command()
@click.option('--infile', default='', help='csv file path')
@click.option('--outfile', default='', help='output filename except the extension')
@click.pass_context
def json2csv(ctx, infile, outfile):
    print_help(ctx, None, value=infile=='' or outfile=='')
    tool = evtxtool.evtx.Json2csv(infile, outfile)
    tool.run()


if __name__ == '__main__':
    main()
