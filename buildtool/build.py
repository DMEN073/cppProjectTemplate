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

def configLogic(buildType):
    is_msvc = "VisualStudioVersion" in os.environ or "VSINSTALLDIR" in os.environ
    os.makedirs(__BUILD_DIR, exist_ok=True)
    if(is_msvc):
        run_command(["cmake", "-S", ".", "-B", __BUILD_DIR, f"-DBUILD_TYPE_CACHE={buildType}"])
    else:
        run_command(["cmake", "-S", ".", "-B", __BUILD_DIR+"/"+buildType, f"-DBUILD_TYPE_CACHE={buildType}"])

def buildLogic(target, build_type = None):
    if build_type is not None:
        cmd = ["cmake", "--build", __BUILD_DIR+"/"+build_type]
    else:
        cmd = ["cmake", "--build", __BUILD_DIR]
    is_msvc = "VisualStudioVersion" in os.environ or "VSINSTALLDIR" in os.environ
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
    configLogic(buildType)

@cli.command()
@click.option("--target", default=None)
def build(target, build_type = None):
    buildLogic(target,build_type)

@cli.command()
@click.option("--target", default=None)
def fullbuild(target):
    is_msvc = "VisualStudioVersion" in os.environ or "VSINSTALLDIR" in os.environ
    if is_msvc:
        for config in ["Debug", "Release"]:
            configLogic(config)
            cmd = ["cmake", "--build", __BUILD_DIR, "--config", config]
            if target:
                cmd += ["--target", target]
            run_command(cmd)
    else:
        for build_type in ["Debug", "Release"]:
            configLogic(build_type)
            buildLogic(target, build_type)


if __name__ == "__main__":
    cli()