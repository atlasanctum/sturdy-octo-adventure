# Development Setup Guide

Quick setup guide for local development of Atlas Sanctum OS.

## Prerequisites

- Python 3.11 or higher
- Node.js 18+ (for blockchain)
- PostgreSQL 15 (or use Docker)
- Docker & Docker Compose (recommended)

## Option 1: Docker Setup (Recommended)

Fastest way to get a complete working environment:

```bash
# Clone and navigate
git clone <repo-url>
cd atlas-sanctum-os

# Build and start all services
docker-compose up --build

# In another terminal, test
docker-compose exec cli python -m cli.cli intent "Test intent"
```

## Option 2: Local Development Setup

For development with live code reloading:

### 1. Clone Repository

```bash
git clone <repo-url>
cd atlas-sanctum-os
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Activate
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start PostgreSQL (via Docker)

```bash
docker run -d \
  --name asos-postgres \
  -e POSTGRES_USER=atlas \
  -e POSTGRES_PASSWORD=atlas_password \
  -e POSTGRES_DB=atlas_sanctum \
  -p 5432:5432 \
  postgres:15
```

### 5. Initialize Database

```bash
python -c "from data.database import init_db; init_db()"
```

Verify:
```bash
psql -U atlas -d atlas_sanctum -h localhost \
  -c "SELECT * FROM policy_rules LIMIT 1;"
```

### 6. Start NATS (Optional, for messaging)

```bash
docker run -d \
  --name asos-nats \
  -p 4222:4222 \
  nats:latest
```

### 7. Start Hardhat Blockchain (Optional)

```bash
cd blockchain
npm install
npx hardhat node
```

In another terminal:
```bash
cd blockchain
npx hardhat run scripts/deploy.js --network localhost
```

### 8. Run Gateway API

In a terminal:
```bash
python -m uvicorn gateway.main:app --reload --port 8000
```

Visit: http://localhost:8000/docs

### 9. Run CLI

In another terminal:
```bash
# From project root
python -m cli.cli intent "Your test intent"
```

## Environment Variables

Copy and customize:
```bash
cp .env.example .env
```

Edit `.env` with your settings:
```
DATABASE_URL=postgresql://atlas:atlas_password@localhost:5432/atlas_sanctum
NATS_URL=nats://localhost:4222
BLOCKCHAIN_RPC_URL=http://localhost:8545
API_HOST=0.0.0.0
API_PORT=8000
```

## Project Structure

```
atlas-sanctum-os/
├── agents/              # Agent implementations
├── blockchain/          # Smart contracts & client
├── cli/                # Command-line interface
├── data/               # Database layer
├── ethics/             # Policy engine
├── gateway/            # FastAPI app
├── infra/              # Docker configs
├── messaging/          # NATS client
├── orchestration/      # Intent routing
├── requirements.txt    # Python dependencies
└── README.md
```

## Common Tasks

### Running Tests

```bash
pytest                          # Run all tests
pytest tests/agents/            # Run specific test dir
pytest -v --cov                # Verbose with coverage
```

### Database Operations

```bash
# Connect to PostgreSQL
psql -U atlas -d atlas_sanctum -h localhost

# Run SQL file
psql -U atlas -d atlas_sanctum -h localhost -f data/init.sql

# Backup database
pg_dump -U atlas -d atlas_sanctum -h localhost > backup.sql

# Restore database
psql -U atlas -d atlas_sanctum -h localhost < backup.sql
```

### Code Style

```bash
# Format code
python -m black .

# Lint
python -m flake8 .

# Type checking
mypy .
```

### Docker Cleanup

```bash
# Stop all services
docker-compose down

# Remove volumes (reset database)
docker-compose down -v

# Remove all images
docker-compose down --rmi all

# Clean up unused Docker resources
docker system prune -a
```

## Troubleshooting

### Database Connection Issues

```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Check logs
docker logs asos-postgres

# Verify connection
psql -U atlas -d atlas_sanctum -h localhost -c "SELECT 1"
```

### API Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use different port
python -m uvicorn gateway.main:app --port 8001
```

### Virtual Environment Issues

```bash
# Deactivate and remove
deactivate
rm -rf venv

# Recreate
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Import Errors

Ensure you're:
1. In the virtual environment
2. In the project root directory
3. Have installed all requirements

```bash
# Verify
which python                    # Should show venv path
pip list | grep fastapi       # Should list installed packages
```

## IDE Setup

### VS Code

Install extensions:
- Python
- Pylance
- FastAPI
- SQLTools

Settings (.vscode/settings.json):
```json
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "ms-python.python"
}
```

### PyCharm

1. Open project
2. Configure interpreter: Project → Interpreter
3. Select venv
4. Enable code inspections

## Deployment

For production deployment, see DEPLOYMENT.md (future).

## Getting Help

- **Documentation**: Check README.md
- **API Docs**: http://localhost:8000/docs
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions

## Next Steps

1. Read [CONTRIBUTING.md](CONTRIBUTING.md)
2. Check [README.md](README.md) for architecture
3. Explore code in `agents/`, `gateway/`, etc.
4. Run tests and explore codebase
5. Open your first pull request!

Happy coding! 🚀
