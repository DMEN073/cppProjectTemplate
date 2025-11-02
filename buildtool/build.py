import click
import subprocess
import shutil
import os


__BUILD_DIR = "build"
__BIN_DIR = "bin"
__LIB_DIR = "lib"

VERBOSE = False

def echo(msg):
    if VERBOSE:
        echo(msg)

def run_command(cmd):
    echo(f"Running: {' '.join(cmd)}")
    subprocess.check_call(cmd)



@click.group()
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose output")
@click.pass_context
def cli(ctx, verbose):
    ctx.ensure_object(dict)
    ctx.obj["VERBOSE"] = verbose


@cli.command()
def clean():
    for path in [__BUILD_DIR,__BIN_DIR,__LIB_DIR]:
        if os.path.exists(path):
            echo(f"Removing {path}...")
            shutil.rmtree(path)

@cli.command()
@click.option("--build-type", "buildType",default="Debug", type=click.Choice(["Debug", "Release"]))        
def configure(buildType):
    os.makedirs(__BUILD_DIR, exist_ok=True)
    run_command(["cmake", "-S", ".", "-B", __BUILD_DIR, f"-DBUILD_TYPE_CACHE={buildType}"])

@cli.command()
@click.option("--target", default=None)
def build(target):
    cmd = ["cmake", "--build", __BUILD_DIR]
    is_msvc = "VisualStudioVersion" in os.environ or "VSINSTALLDIR" in os.environ
    build_type = None
    if is_msvc:
        # Read from CMake cache
        cache_file = os.path.join(__BUILD_DIR, "CMakeCache.txt")
        if os.path.exists(cache_file):
            with open(cache_file, "r") as f:
                for line in f:
                    if line.startswith("BUILD_TYPE_CACHE:"):
                        build_type = line.split('=')[1].strip()
                        break
        if build_type:
            cmd += ["--config", build_type]

    if target:
        cmd += ["--target", target]
    run_command(cmd)



if __name__ == "__main__":
    cli()