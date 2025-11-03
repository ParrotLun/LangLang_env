import importlib.metadata
import sys

# ANSI color codes for better output
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"
YELLOW = "\033[93m"

# --- List of packages to check ---
packages_to_check = [
    "langgraph",
    "langgraph-checkpoint",
    "langgraph-cli[inmem]",
    "langgraph-supervisor",
    "langmem",
    "langchain",
    "langchain-core",
    "langchain-openai",
    "langchain-community",
    "langchain-postgres",
    "openai",
    "fastapi[standard]",
    "uvicorn[standard]",
    "pydantic",
    "pydantic-settings",
    "requests",
    "httpx",
    "python-dotenv",
    "psycopg-binary",
    "psycopg2-binary",
    "pytest",
    "pytest-asyncio",
    "tenacity",
    "loguru",
    "python-docx",
    "nbformat",
]

print(f"🐍 Checking {len(packages_to_check)} Python packages...\n")

missing_packages = []
installed_count = 0

for pkg_name in packages_to_check:
    # Normalize the package name to check for installation
    # This removes extras like [standard] or [inmem]
    # e.g., "fastapi[standard]" -> "fastapi"
    base_pkg_name = pkg_name.split('[')[0]

    try:
        # Check for the package metadata using its distribution name
        version = importlib.metadata.version(base_pkg_name)
        print(f"  {GREEN}✓ {pkg_name:<25} (Found: {base_pkg_name}=={version}){RESET}")
        installed_count += 1
    
    except importlib.metadata.PackageNotFoundError:
        # This is the standard exception if the package isn't found
        print(f"  {RED}✗ {pkg_name:<25} (Package '{base_pkg_name}' not found){RESET}")
        missing_packages.append(pkg_name)
    
    except Exception as e:
        # Catch other potential errors
        print(f"  {YELLOW}E {pkg_name:<25} (Error checking '{base_pkg_name}': {e}){RESET}")
        missing_packages.append(pkg_name) # Treat as missing if error

# --- Summary ---
print("\n" + "="*40)
print("✨ Check Complete ✨")
print(f"  Installed: {installed_count}")
print(f"  Missing:   {len(missing_packages)}")
print("="*40)

if missing_packages:
    print(f"\n{RED}Action Required:{RESET}")
    print("To install all missing packages, copy and run this command:")
    
    # Create a pip install command for the *original* names (with extras)
    pip_command = "pip install " + " ".join(f'"{pkg}"' for pkg in missing_packages)
    print(f"\n{YELLOW}{pip_command}{RESET}\n")
    sys.exit(1) # Exit with an error code if packages are missing
else:
    print(f"\n{GREEN}All packages are installed!{RESET}\n")
    sys.exit(0) # Exit with success code