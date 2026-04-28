# Contributing to Atlas Sanctum OS

Thank you for your interest in contributing to Atlas Sanctum OS! We welcome contributions from developers, researchers, and organizations.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Report issues responsibly
- Help others learn and grow

## Getting Started

1. **Fork** the repository
2. **Clone** your fork
   ```bash
   git clone https://github.com/YOUR-USERNAME/atlas-sanctum-os.git
   cd atlas-sanctum-os
   ```

3. **Create a branch** for your feature
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

5. **Make your changes** following code style guidelines (see below)

6. **Test your changes**
   ```bash
   pytest
   ```

7. **Commit with clear messages**
   ```bash
   git commit -m "Add feature: brief description"
   ```

8. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

9. **Open a Pull Request** with:
   - Clear title and description
   - Reference to any related issues
   - Screenshots/examples if applicable

## Code Style Guidelines

### Python

- Follow **PEP 8** conventions
- Use **type hints** for function signatures
- Add **docstrings** to modules, classes, and functions
- Keep lines **≤100 characters**
- Use **f-strings** for string formatting

Example:
```python
from typing import Dict, Any, Optional

async def process_intent(
    intent: str,
    metadata: Optional[Dict[str, Any]] = None
) -> ActionResult:
    """
    Process a user intent through the system.
    
    Args:
        intent: The user's natural language intent
        metadata: Optional context metadata
        
    Returns:
        ActionResult containing success status and data
    """
    # Implementation
    pass
```

### JavaScript/Solidity

- Use **2-space indentation**
- Add **JSDoc comments** for functions
- Follow **camelCase** for variables

## Contribution Areas

### 1. New Agents

Create domain-specific agents for handling new types of operations:

```python
# agents/logistics_agent.py
class LogisticsAgent(BaseAgent):
    def __init__(self):
        super().__init__("logistics")
    
    async def process(self, intent, metadata):
        # Your implementation
        pass
```

### 2. Ethics Engine

Improve policy validation and rule processing:
- Add new policy types
- Implement OPA integration
- Enhance pattern matching

### 3. Infrastructure

- Kubernetes deployment
- CI/CD pipeline
- Monitoring and logging

### 4. Testing

- Unit tests for agents
- Integration tests
- Load testing
- Security testing

### 5. Documentation

- Setup guides
- API documentation
- Architectural diagrams
- Use case examples

### 6. Performance

- Optimize database queries
- Improve async handling
- Caching strategies
- Load balancing

### 7. Security

- Input validation
- Authentication/authorization
- Encryption
- Audit logging

## Testing

### Running Tests

```bash
# Unit tests
pytest

# With coverage
pytest --cov=.

# Specific test file
pytest tests/agents/test_health_agent.py
```

### Manual Testing

```bash
# Start all services
docker-compose up --build

# Run test script
./test.sh

# Test via CLI
docker-compose exec cli python -m cli.cli intent "Your test intent"

# Check status
docker-compose exec cli python -m cli.cli status 1
```

## Documentation

When contributing, please include:

- **Docstrings** for all public functions
- **Comments** for complex logic
- **README section** if adding major features
- **CHANGELOG entry** for notable changes

## Git Workflow

1. Keep commits **atomic and focused**
2. Use **descriptive commit messages**
3. Reference **issues in commits** (e.g., "Fixes #123")
4. **Rebase** before opening PR to keep history clean
5. Resolve **merge conflicts** before requesting review

Example commit messages:
```
Add vaccine tracking agent
Fix database connection pool issue
Refactor ethics engine policy matching
Document blockchain integration
```

## Pull Request Process

1. **Update README** if adding features
2. **Add tests** for new functionality
3. **Update dependencies** in requirements.txt if needed
4. **Pass all CI checks**
5. **Request reviews** from maintainers
6. **Address feedback** promptly

### PR Title Format

```
[type] Brief description

Types: feature, bugfix, docs, refactor, perf, test
```

Examples:
- `[feature] Add logistics agent`
- `[bugfix] Fix database connection leak`
- `[docs] Update API documentation`

## Issues

### Reporting Bugs

Include:
- **Description** of the bug
- **Steps to reproduce**
- **Expected behavior**
- **Actual behavior**
- **Environment** (OS, Python version, etc.)
- **Screenshots** if applicable

### Suggesting Features

Include:
- **Problem statement** - what issue does this solve?
- **Proposed solution** - how should it work?
- **Alternatives** - other approaches considered
- **Examples** - use cases and examples

## Licensing

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.

## Community

- **Discussions**: GitHub Discussions for ideas
- **Issues**: Bug reports and feature requests
- **Email**: eugeneochako@gmail.com for questions

## Recognition

Contributors are recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation

Thank you for making Atlas Sanctum OS better! 🙏
