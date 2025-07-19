import click
import subprocess
import shutil
import os


__BUILD_DIR = "build"
__BIN_DIR = "bin"
__LIB_DIR = "lib"

def run_command(cmd):
    click.echo(f"Running: {' '.join(cmd)}")
    subprocess.check_call(cmd)


@click.group
def cli():
    pass

@cli.command()
def clean():
    for path in [__BUILD_DIR,__BIN_DIR,__LIB_DIR]:
        if os.path.exists(path):
            click.echo(f"Removing {path}...")
            shutil.rmtree(path)

@cli.command()
@click.option("--build-type", "buildType",default="Debug", type=click.Choice(["Debug", "Release"]))        
def configure(buildType):
    os.makedirs(__BUILD_DIR, exist_ok=True)
    run_command(["cmake", "-S", ".", "-B", __BUILD_DIR, f"-DCMAKE_BUILD_TYPE={buildType}"])

@cli.command()
@click.option("--target", default=None)
def build(target):
    cmd = ["cmake", "--build", __BUILD_DIR]
    if target:
        cmd += ["--target", target]
    run_command(cmd)



if __name__ == "__main__":
    cli()