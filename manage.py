import os
import sys
import subprocess


def set_env(env_name: str):
    """Set environment variable cross-platform and print mode"""
    os.environ["ENV"] = env_name
    print(f"⚙️  Running '{env_name} mode'")


def run_uvicorn(reload=True):
    cmd = [sys.executable, "-m", "uvicorn", "main:app"]
    if reload:
        cmd.append("--reload")
    subprocess.run(cmd, check=True)


def run_tests():
    cmd = [sys.executable, "-m", "pytest", "-v", "-s"]
    subprocess.run(cmd, check=True)


def print_help():
    print(
        """
Usage: python manage.py [command]

Commands:
  dev     Run the app in development mode (with reload)
  test    Run tests in test mode
  prod    Run the app in production mode (no reload)
"""
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "dev":
        set_env("dev")
        run_uvicorn(reload=True)
    elif command == "test":
        set_env("test")
        run_tests()
    elif command == "prod":
        set_env("prod")
        run_uvicorn(reload=False)
    else:
        print_help()
        sys.exit(1)
