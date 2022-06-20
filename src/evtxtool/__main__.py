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
@click.option('--conf', default='', help='path of configuration file')
@click.option('--path', default='', help='csv file path')
@click.option('--out', default='', help='output filename except the extension')
@click.pass_context
def json2csv(ctx, conf, path, out):
    print_help(ctx, None, value=path is None)
    evtxtool.evtx.json2csv(conf, path, out)


if __name__ == '__main__':
    main()
