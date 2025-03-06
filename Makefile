.PHONY: help install test docs run build clean profile profile-viz

version := 0.1.0
project := nebula-orion

help:
	@echo --------------------------------------------------
	@echo Usage: make [target]
	@echo
	@echo Available Targets:
	@echo   help       : Display this help message and usage instructions.
	@echo   install    : Install project and development dependencies from requirements files.
	@echo   test       : Run all tests using pytest with coverage and verbose output.
	@echo   docs       : Build documentation using MkDocs.
	@echo   run        : Launch the application using uvicorn.
	@echo   build      : Build the application using hatch.
	@echo   clean      : Remove caches, build artifacts, virtual environments, logs, and IDE directories.
	@echo   profile    : Run the application with cProfile and generate profile data.
	@echo   profile-viz: Visualize profile data using snakeviz.
	@echo --------------------------------------------------

install:
	@echo "Starting installation of dependencies..."
	uv venv
	uv sync
	@echo "Dependencies installed successfully."

test:
	@echo "Running test suite with pytest..."
	uv run python -m pytest tests --cov=src --verbose
	@echo "Test suite execution completed."

docs:
	@echo "Building documentation with Sphinx..."
	# Uncomment below to enable documentation build:
	# sphinx-build -b html docs/source docs/build
	@echo "Documentation build process completed (if enabled)."

run:
	@echo "Launching the application..."
	uv run python -m nebula_orion.main
	@echo "Application execution finished."

build:
	@echo "Building the application using hatch..."
	uv build
	@echo "Application build completed."

clean:
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
	@echo "Running application with profiling (library code only)..."
	uv run python -c "import cProfile, pstats, nebula_orion.main; \
					  cProfile.run('nebula_orion.main.main()', 'profile.stats'); \
					  p = pstats.Stats('profile.stats'); \
					  p.strip_dirs().sort_stats('cumulative').print_stats('nebula_orion')"
	@echo "Profile data saved to profile.stats (filtered output printed above)"

profile-viz:
	@echo "Launching snakeviz profile visualization for library code..."
	uv run snakeviz profile.stats
