import click
import evtxtool.evtx
import shutil
import uuid
import os
import traceback
import sys
import platform

 
def eprint(msg):
    print(msg, file=sys.stderr)


def print_help(ctx, param, value):
    if value is True:
        click.echo(ctx.get_help())
        ctx.exit()


class Tool:
    @staticmethod
    def json2csv(infile, outfile):
        try:
            eprint(f'[*] Running JSON2CSV')
            eprint(f'[+] Convert jsonl to csv file')
            eprint(f'[+] Input filename: {infile}')
            eprint(f'[+] Output filename: {outfile}')
            tool = evtxtool.evtx.Json2csv(infile, outfile)
            tool.run()
        except:
            traceback.print_exc()

    @staticmethod
    def evtx2csv(evtx_bin, infile, outfile):
        try:
            eprint(f'[*] Running EVTX2CSV')
            cur_dir = os.path.dirname(os.path.realpath(__file__))
            tmp_dir = cur_dir + '/' + uuid.uuid4().__str__()
            os.mkdir(tmp_dir)

            eprint(f'[+] Run evtx file dump with {evtx_bin}')
            os.system(
                f'{evtx_bin} {infile} -o jsonl -f {tmp_dir}/json --ansi-codec "utf-8"'
            )

            eprint(f'[+] Run convert dump data to csv format')
            Tool.json2csv(f'{tmp_dir}/json', outfile)
            shutil.rmtree(tmp_dir)
        except:
            traceback.print_exc()
            if os.path.exists(tmp_dir):
                shutil.rmtree(tmp_dir)


@click.group()
def main():
    eprint('EVTXTool v0.2.1\n')


@main.command()
@click.option('-i', '--infile', default='', help='json file path')
@click.option('-o', '--outfile', default='', help='csv file')
@click.pass_context
def json2csv(ctx, infile, outfile):
    print_help(ctx, None, value=infile=='' or outfile=='')
    Tool.json2csv(infile, outfile)


@main.command()
@click.option('-e', '--evtx-bin', default='', help='evtx executable')
@click.option('-i', '--infile', default='', help='evtx file path')
@click.option('-o', '--outfile', default='', help='csv file')
@click.pass_context
def evtx2csv(ctx, evtx_bin, infile, outfile):
    evtx_err = False
    evtx_dump = 'evtx_dump' + ('.exe' if platform.system() == 'Windows' else '')

    if evtx_bin == '': # Check default binary
        evtx_bin = os.path.dirname(os.path.realpath(__file__))
        evtx_bin += f'/bin/{evtx_dump}'

    if os.path.exists(evtx_bin):
        evtx_err = False
    else:
        eprint(f'[*] File not found ("{evtx_bin}")')
        evtx_err = True

    param_check = infile == '' or outfile == '' or evtx_err
    print_help(ctx, None, value=param_check)
    Tool.evtx2csv(evtx_bin, infile, outfile)


if __name__ == '__main__':
    main()
