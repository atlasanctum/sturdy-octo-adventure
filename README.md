# Atlas Sanctum OS (ASOS)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

> **AI-agent orchestration system with ethics engine and blockchain audit layer**

A production-grade, open-source infrastructure for deploying autonomous agents with policy enforcement and immutable action logging.

---

## 🎯 Overview

Atlas Sanctum OS is a complete system for orchestrating AI agents in humanitarian and critical contexts. It provides:

- **Agent Orchestration**: Route natural language intents to specialized agents
- **Policy Engine**: Enforce ethics and security policies on all actions
- **Blockchain Audit**: Immutable log of all system actions
- **Event-Driven Architecture**: NATS pub/sub for real-time event streaming
- **Local-First Development**: Full system runs in Docker, no cloud dependencies

### Key Features

✅ **Fully Working Local Infrastructure** - Everything runs in Docker  
✅ **Natural Language Interface** - CLI accepts English commands  
✅ **Rule-Based Orchestration** - No LLM required for v1  
✅ **Ethics Enforcement** - Built-in policy validation  
✅ **Immutable Audit Trail** - Actions logged to smart contract  
✅ **Event Streaming** - NATS for real-time communication  
✅ **PostgreSQL Persistence** - Structured data storage  
✅ **Production Ready** - No placeholders or TODOs  

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     CLI / Client                             │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│         FastAPI Gateway (Intent Processing)                  │
│  POST /intent ────────────────────────────────────────────  │
└───────────────────────┬─────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
    ┌────────┐    ┌──────────┐   ┌────────────┐
    │ Ethics │◄───┤Orchestr. │───►│  Agents    │
    │ Engine │    │          │    └────────────┘
    └────────┘    └────┬─────┘         │
                       │               │
        ┌──────────────┼───────────────┤
        ▼              ▼               ▼
    ┌─────────┐  ┌───────────┐  ┌──────────────┐
    │ NATS    │  │PostgreSQL │  │ Blockchain   │
    │ Events  │  │Database   │  │ (Hardhat)    │
    └─────────┘  └───────────┘  └──────────────┘
```

---

## 📋 System Components

### 1. **Agents**
- **HealthAgent**: Vaccine distribution, medical logistics
- **FinanceAgent**: Fund allocation, payments, transfers
- Extensible base class for custom agents
- Async-based for high performance

### 2. **Orchestrator**
Routes intents to appropriate agents using:
- Keyword matching
- Agent capability checking
- Fallback mechanisms

### 3. **Ethics Engine**
Policy validation with:
- Regex-based rule patterns
- Database-backed policy rules
- Default allow/deny logic
- Future OPA integration ready

### 4. **Data Layer**
PostgreSQL with:
- ActionLog table for audit trail
- PolicyRule table for governance
- Indexed queries for performance
- SQL migrations in init.sql

### 5. **Messaging (NATS)**
Event streaming for:
- Action execution events
- Real-time notifications
- System observability
- Future integrations

### 6. **Blockchain (Hardhat)**
Smart contract for:
- Immutable action logging
- Timestamp verification
- Executor tracking
- External transaction linking

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose (latest)
- 4GB RAM minimum
- 10GB free disk space

### Installation & Startup

1. **Clone repository**
   ```bash
   git clone <repo-url>
   cd atlas-sanctum-os
   ```

2. **Start all services**
   ```bash
   docker-compose up --build
   ```

   Output should show:
   ```
   ✓ asos-postgres    healthy
   ✓ asos-nats        healthy
   ✓ asos-blockchain  healthy
   ✓ asos-gateway     ready
   ✓ asos-cli         ready
   ```

3. **Verify services** (in another terminal)
   ```bash
   docker-compose ps
   docker-compose logs gateway
   ```

---

## 💻 Usage Examples

### CLI: Submit Intent

```bash
docker-compose exec cli python -m cli.cli intent "Track vaccine distribution in Nakuru"
```

**Output:**
```
✓ Intent accepted
  Action ID: 1
  Status: authorized
  Agent: health

Use: asos status 1 to check progress
```

### CLI: Check Status

```bash
docker-compose exec cli python -m cli.cli status 1
```

**Output:**
```
Action ID: 1
Intent: Track vaccine distribution in Nakuru
Agent: health
Status: executed
Created: 2024-01-15 10:30:45
Executed: 2024-01-15 10:30:46
Result: {"operation_type": "vaccine_distribution", "location": "Nakuru", ...}
Blockchain TX: 0x1a2b3c4d5e6f...
```

### CLI: View History

```bash
docker-compose exec cli python -m cli.cli history --limit 10
```

### CLI: List Agents

```bash
docker-compose exec cli python -m cli.cli agents
```

### API: POST Intent

```bash
curl -X POST http://localhost:8000/intent \
  -H "Content-Type: application/json" \
  -d '{
    "intent": "Track vaccine distribution in Nakuru",
    "metadata": {"user_id": "001", "region": "Kenya"}
  }'
```

**Response:**
```json
{
  "action_id": 1,
  "status": "authorized",
  "agent_type": "health",
  "data": {
    "intent": "Track vaccine distribution in Nakuru",
    "queued_for_processing": true
  },
  "message": "Intent authorized and queued for processing"
}
```

### API: GET Action Status

```bash
curl http://localhost:8000/actions/1
```

### API: LIST Actions

```bash
curl http://localhost:8000/actions?limit=20
```

### API: Health Check

```bash
curl http://localhost:8000/health
```

### API Documentation

Navigate to: **http://localhost:8000/docs**

Interactive Swagger UI with all endpoints.

---

## 📊 Complete Test Scenario

Execute this full workflow:

```bash
# 1. Submit intent
docker-compose exec cli python -m cli.cli intent "Track vaccine distribution in Nakuru"
# Action ID: 1

# 2. Check status (immediate - might be processing)
docker-compose exec cli python -m cli.cli status 1

# 3. Wait for processing
sleep 2

# 4. Check status again (should be executed)
docker-compose exec cli python -m cli.cli status 1

# 5. View database directly
docker-compose exec postgres psql -U atlas -d atlas_sanctum \
  -c "SELECT id, intent, status, result FROM action_logs ORDER BY created_at DESC LIMIT 1;"

# 6. Check blockchain logs
docker-compose logs blockchain | tail -20

# 7. View NATS events (if subscribed)
docker-compose exec nats nats sub "actions.executed"
```

**Expected Results:**
- ✅ Action logged to PostgreSQL
- ✅ Event published to NATS
- ✅ Transaction created on blockchain
- ✅ Blockchain TX hash stored in database

---

## 📁 Project Structure

```
atlas-sanctum-os/
│
├── agents/                          # Agent layer
│   ├── __init__.py
│   ├── base.py                      # BaseAgent abstract class
│   ├── health_agent.py              # Health/medical operations
│   └── finance_agent.py             # Finance/payment operations
│
├── blockchain/                      # Blockchain audit layer
│   ├── __init__.py
│   ├── ActionAuditLog.sol           # Solidity smart contract
│   ├── blockchain_client.py         # Web3.py client
│   ├── hardhat.config.js            # Hardhat configuration
│   ├── deploy.js                    # Deployment script
│   └── package.json                 # Node dependencies
│
├── cli/                             # Command-line interface
│   ├── __init__.py
│   ├── cli.py                       # Click CLI implementation
│   └── main.py                      # Entry point
│
├── data/                            # Data layer
│   ├── __init__.py
│   ├── models.py                    # SQLAlchemy ORM models
│   ├── database.py                  # Connection & session management
│   └── init.sql                     # Database initialization script
│
├── ethics/                          # Ethics engine
│   ├── __init__.py
│   └── policy_engine.py             # Policy validation logic
│
├── gateway/                         # FastAPI REST gateway
│   ├── __init__.py
│   ├── main.py                      # FastAPI application
│   └── main_entry.py                # Server entry point
│
├── infra/                           # Docker infrastructure
│   ├── Dockerfile.gateway           # Gateway service
│   ├── Dockerfile.cli               # CLI service
│   ├── Dockerfile.blockchain        # Blockchain service
│   ├── Dockerfile.postgres          # Database service
│   └── Dockerfile.nats              # NATS service
│
├── messaging/                       # Event messaging
│   ├── __init__.py
│   └── nats_client.py               # NATS client wrapper
│
├── orchestration/                   # Intent orchestration
│   ├── __init__.py
│   └── orchestrator.py              # Agent selection & routing
│
├── docker-compose.yml               # Service orchestration
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment template
├── .gitignore                       # Git ignore patterns
└── README.md                        # This file
```

---

## 🔧 Development

### Local Development (Without Docker)

Perfect for debugging and development:

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment**
   ```bash
   cp .env.example .env
   ```

4. **Start PostgreSQL** (via Docker only)
   ```bash
   docker run -d \
     -e POSTGRES_USER=atlas \
     -e POSTGRES_PASSWORD=atlas_password \
     -e POSTGRES_DB=atlas_sanctum \
     -p 5432:5432 \
     postgres:15
   ```

5. **Initialize database**
   ```bash
   python -c "from data.database import init_db; init_db()"
   ```

6. **Run gateway**
   ```bash
   python -m uvicorn gateway.main:app --reload --port 8000
   ```

7. **Run CLI** (in another terminal)
   ```bash
   python -m cli.cli intent "Your test intent"
   ```

### Creating Custom Agents

1. **Create new agent file** (`agents/custom_agent.py`)
   ```python
   from agents.base import BaseAgent, ActionResult
   from typing import Dict, Any
   
   class CustomAgent(BaseAgent):
       def __init__(self):
           super().__init__("custom")
           self.keywords = ["keyword1", "keyword2"]
       
       async def process(self, intent: str, metadata: Dict[str, Any]) -> ActionResult:
           # Your logic here
           return ActionResult(
               success=True,
               action_type=self.agent_type,
               data={"result": "..."}
           )
       
       def can_handle(self, intent: str) -> bool:
           return any(kw in intent.lower() for kw in self.keywords)
   ```

2. **Register in orchestrator** (`orchestration/orchestrator.py`)
   ```python
   from agents.custom_agent import CustomAgent
   
   # In Orchestrator.__init__:
   self.agents["custom"] = CustomAgent()
   ```

3. **Test**
   ```bash
   python -m cli.cli intent "keyword1 operation"
   ```

### Adding Policy Rules

**Option 1: Database**
```bash
docker-compose exec postgres psql -U atlas -d atlas_sanctum \
  -c "INSERT INTO policy_rules (rule_name, rule_pattern, action, description) 
      VALUES ('my_rule', 'pattern_regex', 'allow', 'Description');"
```

**Option 2: SQL File**
Edit `data/init.sql` and redeploy:
```bash
docker-compose down -v
docker-compose up --build
```

---

## 🔐 Security

### Current Security Measures

✅ Environment variables for secrets  
✅ No hardcoded credentials  
✅ Database authentication required  
✅ PostgreSQL user/pass in `.env`  
✅ Private key management for blockchain  
✅ Policy engine for authorization  

### Production Recommendations

For production deployment:

1. **Secrets Management**
   - Use HashiCorp Vault
   - AWS Secrets Manager
   - Azure Key Vault
   - Environment-specific `.env` files

2. **Authentication**
   - Add JWT/OAuth2 to API
   - CLI API key management
   - User session tracking

3. **Database Security**
   - Enable PostgreSQL SSL
   - Separate read/write users
   - Row-level security policies
   - Regular backups

4. **Blockchain**
   - Use hardware wallet for production
   - Multi-sig key management
   - Audit smart contract code
   - Use testnet before mainnet

5. **Network**
   - Rate limiting on API
   - Request validation
   - CORS configuration
   - Firewall rules

6. **Monitoring**
   - Application logging
   - Performance monitoring
   - Security audit logs
   - Alert thresholds

---

## 📦 Dependency Management

### Python Dependencies

Core dependencies in `requirements.txt`:
- **fastapi** - REST framework
- **uvicorn** - ASGI server
- **sqlalchemy** - ORM
- **psycopg2-binary** - PostgreSQL adapter
- **web3** - Blockchain client
- **click** - CLI framework
- **httpx** - HTTP client
- **pydantic** - Data validation
- **python-dotenv** - Environment management
- **nats-py** - NATS client

### Node Dependencies

Blockchain (`blockchain/package.json`):
- **hardhat** - Ethereum framework
- **@nomicfoundation/hardhat-toolbox** - Testing & compilation

### Infrastructure

- **PostgreSQL 15** - Data persistence
- **NATS Server** - Message broker
- **Hardhat Node** - Local blockchain
- **Python 3.11** - Runtime
- **Node.js 18** - Blockchain tooling

---

## 🧪 Testing

### Manual Test Cases

**Test 1: Health Intent**
```bash
docker-compose exec cli python -m cli.cli intent "Track vaccine distribution in Nakuru"
docker-compose exec cli python -m cli.cli status 1
# Expected: Agent=health, Status=executed
```

**Test 2: Finance Intent**
```bash
docker-compose exec cli python -m cli.cli intent "Transfer $50000 to Red Cross"
docker-compose exec cli python -m cli.cli status 2
# Expected: Agent=finance, Status=executed
```

**Test 3: Denied Intent**
```bash
docker-compose exec cli python -m cli.cli intent "Hack into hospital records"
# Expected: Status=rejected, Reason=policy_violation
```

**Test 4: API Integration**
```bash
# Submit via API
ACTION_ID=$(curl -s -X POST http://localhost:8000/intent \
  -H "Content-Type: application/json" \
  -d '{"intent":"Track vaccine distribution"}' | jq -r '.action_id')

# Check status
curl http://localhost:8000/actions/$ACTION_ID
```

### Future Testing

- [ ] Unit tests with pytest
- [ ] Integration tests
- [ ] Load testing
- [ ] Security testing
- [ ] Blockchain transaction validation

---

## 📖 API Documentation

### Interactive Docs

Swagger UI: **http://localhost:8000/docs**  
ReDoc: **http://localhost:8000/redoc**

### Endpoints Reference

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/` | Service info |
| `GET` | `/health` | Health check |
| `POST` | `/intent` | Submit intent |
| `GET` | `/actions/{id}` | Get action status |
| `GET` | `/actions` | List actions |
| `GET` | `/agents` | List agents |

---

## 🤝 Contributing

We welcome contributions from developers, researchers, and organizations!

### How to Contribute

1. **Fork** the repository
2. **Branch** for your feature
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit** with clear messages
   ```bash
   git commit -m "Add amazing feature"
   ```
4. **Push** to your fork
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Pull Request** with description

### Contribution Areas

- **Agents**: New domain-specific agents
- **Ethics**: Policy engine improvements
- **Infrastructure**: Kubernetes deployment
- **Testing**: Test suite expansion
- **Documentation**: Guides and tutorials
- **Performance**: Optimization
- **Security**: Hardening & audits

### Code Style

- Follow **PEP 8**
- Use **type hints**
- Write **docstrings**
- Keep functions **small & focused**
- Add **error handling**

### Community

- GitHub Issues: Questions & bugs
- GitHub Discussions: Ideas & feedback
- Pull Requests: Code contributions

---

## 📜 License

**Apache License 2.0**

This project is licensed under the Apache License 2.0. See [LICENSE](LICENSE) for full details.

### Summary

You are **free to**:
- ✅ Use commercially
- ✅ Modify code
- ✅ Distribute copies
- ✅ Sublicense

You **must**:
- ✅ Include license
- ✅ State changes
- ✅ Provide license text

### SPDX Identifier

```
SPDX-License-Identifier: Apache-2.0
```

---

## 🗺️ Roadmap

### v1.1 (Q2 2024)
- [ ] Comprehensive test suite
- [ ] Request validation middleware
- [ ] Advanced logging
- [ ] Performance benchmarks

### v1.2 (Q3 2024)
- [ ] OPA policy engine integration
- [ ] User authentication
- [ ] Action approval workflows
- [ ] Advanced analytics dashboard

### v2.0 (Q4 2024)
- [ ] LLM-based agent selection
- [ ] Multi-agent coordination
- [ ] Distributed deployment
- [ ] Advanced audit interface

---

## 🙏 Acknowledgments

Built for humanitarian and critical infrastructure use cases where:
- **Transparency** is paramount
- **Accountability** is non-negotiable
- **Ethics** guides every action

Special thanks to:
- OpenAI for ethical AI practices
- Ethereum community for blockchain inspiration
- Open source community for tools & guidance

---

## 📞 Support & Contact

### Getting Help

- **GitHub Issues**: Bug reports & feature requests
- **GitHub Discussions**: Questions & ideas
- **Documentation**: Check README & API docs
- **Email**: eugeneochako@gmail.com

### Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Web3.py Docs](https://web3py.readthedocs.io/)
- [Hardhat Docs](https://hardhat.org/docs)
- [NATS Docs](https://docs.nats.io/)

---

## ⚡ Vision

> Build systems where technology serves humanity, decisions are transparent, and accountability is immutable.

---

**Built with ❤️ for a more transparent, accountable, and ethical future.**

<img width="1536" height="1024" alt="ChatGPT Image Apr 28, 2026, 11_51_48 AM" src="https://github.com/user-attachments/assets/6236c19d-fd4a-40b0-aaee-d186d8cf1449" />



Last Updated: April 2026  
Version: 1.0.0
