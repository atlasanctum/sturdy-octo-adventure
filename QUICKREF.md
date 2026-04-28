# Quick Reference Guide

## Common Commands

### Start System
```bash
docker-compose up --build
```

### Stop System
```bash
docker-compose down
```

### Reset Everything (Database + Containers)
```bash
docker-compose down -v
docker-compose up --build
```

## CLI Usage

### Submit Intent
```bash
docker-compose exec cli python -m cli.cli intent "Your intent here"
```

### Check Status
```bash
docker-compose exec cli python -m cli.cli status 1
```

### View History
```bash
docker-compose exec cli python -m cli.cli history --limit 20
```

### List Agents
```bash
docker-compose exec cli python -m cli.cli agents
```

## API Usage

### Test Intent
```bash
curl -X POST http://localhost:8000/intent \
  -H "Content-Type: application/json" \
  -d '{"intent": "Track vaccine distribution in Nakuru"}'
```

### Check Status
```bash
curl http://localhost:8000/actions/1
```

### List Actions
```bash
curl http://localhost:8000/actions
```

### API Documentation
```
http://localhost:8000/docs
```

## Database

### Connect to PostgreSQL
```bash
docker-compose exec postgres psql -U atlas -d atlas_sanctum
```

### View Action Logs
```bash
SELECT id, intent, agent_type, status FROM action_logs ORDER BY created_at DESC LIMIT 10;
```

### View Policy Rules
```bash
SELECT rule_name, rule_pattern, action FROM policy_rules;
```

## Debugging

### View Gateway Logs
```bash
docker-compose logs gateway -f
```

### View All Logs
```bash
docker-compose logs -f
```

### View Specific Service
```bash
docker-compose logs postgres -f
docker-compose logs nats -f
docker-compose logs blockchain -f
```

### Execute Shell in Container
```bash
docker-compose exec gateway bash
docker-compose exec postgres bash
```

## Development

### Run Tests
```bash
pytest
```

### Code Formatting
```bash
black .
```

### Type Checking
```bash
mypy .
```

### Lint
```bash
flake8 .
```

## Port Reference

| Service | Port | URL |
|---------|------|-----|
| API Gateway | 8000 | http://localhost:8000 |
| PostgreSQL | 5432 | localhost:5432 |
| NATS | 4222 | nats://localhost:4222 |
| Hardhat | 8545 | http://localhost:8545 |

## Environment

Edit .env for configuration:
```
DATABASE_URL=postgresql://atlas:atlas_password@postgres:5432/atlas_sanctum
NATS_URL=nats://nats:4222
BLOCKCHAIN_RPC_URL=http://blockchain:8545
API_PORT=8000
```

## Health Checks

```bash
# API Health
curl http://localhost:8000/health

# PostgreSQL
docker-compose exec postgres pg_isready -U atlas

# NATS
curl http://localhost:8222/varz

# Blockchain
curl http://localhost:8545 -X POST \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"eth_blockNumber","params":[],"id":1}'
```

## Common Issues

### Port in Use
```bash
# Find process
lsof -i :8000

# Kill it
kill -9 <PID>
```

### Database Connection Failed
```bash
# Check PostgreSQL
docker-compose ps | grep postgres

# View logs
docker-compose logs postgres
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Documentation Links

- README.md - Full documentation
- DEVELOPMENT.md - Setup guide
- CONTRIBUTING.md - How to contribute
- API Docs - http://localhost:8000/docs

## Testing Scenarios

### Health Intent
```bash
asos "Track vaccine distribution in Nakuru"
asos status 1
```

### Finance Intent
```bash
asos "Transfer $50000 to Red Cross"
asos status 2
```

### Policy Violation
```bash
asos "Hack into hospital records"
```

Should be denied with policy error.
