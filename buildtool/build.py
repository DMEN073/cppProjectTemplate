import click
import subprocess
import shutil
import os
from pathlib import Path

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

def is_msvc(build_dir: Path) -> bool:
    """Detect if the configured compiler is MSVC."""
    cache_file = build_dir / "CMakeCache.txt"
    if not cache_file.exists():
        return False
    with open(cache_file, "r") as f:
        for line in f:
            if line.startswith("CMAKE_GENERATOR:INTERNAL="):
                return "Visual Studio" in line
    return False

def read_build_type(build_dir: Path) -> str:
    cache_file = build_dir / "CMakeCache.txt"
    if not cache_file.exists():
        raise RuntimeError(f"CMakeCache.txt not found in {build_dir}. Please run configure first.")

    with open(cache_file) as f:
        for line in f:
            if line.startswith("BUILD_TYPE_CACHE:"):
                return line.split('=')[1].strip()

    raise RuntimeError(f"BUILD_TYPE_CACHE not found in {cache_file}. Did you pass it during configure?")

def configLogic(buildType):
    build_dir = Path(__BUILD_DIR)
    build_dir.mkdir(parents=True, exist_ok=True)
    # Base CMake command
    cmake_cmd = ["cmake", "-S", ".", "-B", str(build_dir)]

    # On Windows, recommend specifying architecture
    if os.name == "nt":
        cmake_cmd += ["-A", "x64"]  # works for MSVC

    # ALWAYS write a custom cache variable to remember build type
    cmake_cmd += [f"-DBUILD_TYPE_CACHE={buildType}"]
    run_command(cmake_cmd)

def buildLogic(target, build_type = None):
    """Build project using the existing configuration."""
    build_dir = Path(__BUILD_DIR)
    if not (build_dir / "CMakeCache.txt").exists():
        raise RuntimeError("CMake has not been configured yet. Run config first.")
    build_type = read_build_type(build_dir)
    msvc = is_msvc(build_dir)
    if msvc:
        # Multi-config generator: pass --config
        click.echo("build dir is "+ str(build_dir))
        cmd = ["cmake", "--build", str(build_dir), "--config", build_type]
    else:
        # Single-config generator: build_type folder
        click.echo("not msvc build dir is "+ str(build_dir))
        single_config_build_dir = build_dir / build_type
        single_config_build_dir.mkdir(parents=True, exist_ok=True)
        cmd = ["cmake", "--build", str(single_config_build_dir)]

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