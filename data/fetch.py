import click


@click.command()
@click.option("--target", type=click.Path(exists=True), default="titles.txt")
@click.option("--output", type=click.Path(exists=False), default="output.txt")
def main(target, output):
    pass


if __name__ == '__main__':
    main()
