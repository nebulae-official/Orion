.PHONY: help install test docs run build clean profile profile-viz

# Run each recipe in a single shell and use bash.
.ONESHELL:
SHELL := /bin/bash

# version and project variables remain unchanged.
version := 0.1.0
project := nebula-orion

help:
	@echo "====================== Nebula Orion (v${version}) ======================"
	@echo "Usage: make [target]"
	@echo
	@echo "Development Targets:"
	@echo "  install-dev   : Install all development dependencies"
	@echo "  install-docs  : Install documentation dependencies"
	@echo "  install-prod  : Install production dependencies only"
	@echo "  test          : Run tests with pytest and coverage"
	@echo
	@echo "Documentation Targets:"
	@echo "  docs          : Build documentation using MkDocs"
	@echo
	@echo "Application Targets:"
	@echo "  run           : Launch the application"
	@echo "  build         : Build the application package"
	@echo
	@echo "Maintenance Targets:"
	@echo "  clean         : Remove all build artifacts and caches"
	@echo
	@echo "Profiling Targets:"
	@echo "  profile       : Run application with cProfile"
	@echo "  profile-viz   : Visualize profile data with snakeviz"
	@echo
	@echo "For detailed information, visit: https://github.com/nebulae-official/Orion"
	@echo "=================================================================="

install-dev:
	@set -e
	@set -o pipefail
	@trap 'echo "Error: Development installation process failed"; exit 1' ERR
	@echo "Starting installation of development dependencies..."
	@uv venv
	@uv sync
	@echo "Development dependencies installed successfully."

install-prod:
	@set -e
	@set -o pipefail
	@trap 'echo "Error: Production installation process failed"; exit 1' ERR
	@echo "Starting installation of production dependencies..."
	@uv venv
	@uv sync --no-dev
	@echo "Production dependencies installed successfully."

install-docs:
	@set -e
	@set -o pipefail
	@trap 'echo "Error: Documentation dependencies installation process failed"; exit 1' ERR
	@echo "Starting installation of documentation dependencies..."
	@uv venv
	@uv sync --group docs
	@echo "Documentation dependencies installed successfully."

test:
	@set -e
	@set -o pipefail
	@trap 'echo "Error: Test suite execution failed"; exit 1' ERR
	@echo "Running test suite with pytest..."
	@uv run python -m pytest tests --cov=src --verbose
	@echo "Test suite execution completed."

docs:
	@set -e
	@set -o pipefail
	@trap 'echo "Error: Documentation build process failed"; exit 1' ERR
	@echo "Starting local MkDocs server..."
	@uv run python -m mkdocs serve
	@echo "Documentation server is running. Visit http://127.0.0.1:8000 to view."

run:
	@set -e
	@set -o pipefail
	@trap 'echo "Error: Application execution failed"; exit 1' ERR
	@echo "Launching the application..."
	@uv run python -m nebula_orion.main
	@echo "Application execution finished."

build:
	@set -e
	@set -o pipefail
	@trap 'echo "Error: Application build failed"; exit 1' ERR
	@echo "Building the application using hatch..."
	@uv build
	@echo "Application build completed."

clean:
	@set -e
	@set -o pipefail
	@trap 'echo "Error: Cleanup process failed"; exit 1' ERR
	@echo "Starting cleanup process..."
	@echo "Removing Python caches..."
	@find . -type d \( -name "__pycache__" -o -name ".pytest_cache" -o -name ".mypy_cache" -o -name ".ruff_cache" \) 2>/dev/null -exec rm -rf {} +
	@uv clean -q
	@echo "Removing build artifacts and coverage reports..."
	@find . -type d \( -name "docs/build" -o -name ".tox" -o -name "dist" -o -name "build" -o -name "*.egg-info" \) 2>/dev/null -exec rm -rf {} +
	@find . -type d \( -name "coverage_html_report" \) 2>/dev/null -exec rm -rf {} +
	@find . -type f \( -name "coverage.xml" -o -name ".coverage*" \) 2>/dev/null -delete
	@echo "Removing virtual environments..."
	@find . -type d \( -name ".venv" -o -name ".env" -o -name "venv" -o -name "env" \) 2>/dev/null -exec rm -rf {} +
	@echo "Removing logs and temporary files..."
	@find . -type f \( -name "*.log" -o -name "*.pdb" -o -name "*.tmp" -o -name "*.tmp.*" -o -name "*.swp" -o -name "*.swo" -o -name ".DS_Store" \) 2>/dev/null -delete
	@echo "Removing IDE-specific directories..."
	@find . -type d \( -name ".idea" -o -name ".vscode" \) 2>/dev/null -exec rm -rf {} +
	@echo "Cleanup completed."

profile:
	@set -e
	@set -o pipefail
	@trap 'echo "Error: Profiling process failed"; exit 1' ERR
	@echo "Running application with profiling (library code only)..."
	@uv run python -c "import cProfile, pstats, nebula_orion.main; \
					  cProfile.run('nebula_orion.main.main()', 'profile.stats'); \
					  p = pstats.Stats('profile.stats'); \
					  p.strip_dirs().sort_stats('cumulative').print_stats('nebula_orion')"
	@echo "Profile data saved to profile.stats (filtered output printed above)"

profile-viz:
	@set -e
	@set -o pipefail
	@trap 'echo "Error: Profile visualization failed"; exit 1' ERR
	@echo "Launching snakeviz profile visualization for library code..."
	@uv run snakeviz profile.stats
