param(
    [Parameter(Position=0)]
    [string]$Command
)

function Setup {
    Write-Host "Setting up the project..."
    python -m venv .venv
    uv pip install -r requirements.txt
    uv pip install -r requirements-dev.txt
}

function RunTests {
    Write-Host "Running tests..."
    .\.venv\Scripts\Activate.ps1
    pytest src\tests
}

function RunMain {
    Write-Host "Running the main script..."
    .\.venv\Scripts\Activate.ps1
    python src\main.py
}

function ShowHelp {
    Write-Host "Usage: .\run.ps1 [command]"
    Write-Host "Commands:"
    Write-Host "  setup  - Set up the project and install dependencies"
    Write-Host "  test   - Run tests"
    Write-Host "  run    - Run the main script"
}

switch ($Command) {
    "setup" { Setup }
    "test" { RunTests }
    "run" { RunMain }
    default { ShowHelp }
}
