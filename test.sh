#!/bin/bash
# Test script for Atlas Sanctum OS
# Run this after docker-compose up to verify the system

set -e

echo "🧪 Atlas Sanctum OS - System Test Suite"
echo "========================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Services Health
echo "${YELLOW}Test 1: Checking service health...${NC}"
docker-compose ps
echo ""

# Test 2: API Health
echo "${YELLOW}Test 2: Testing API health endpoint...${NC}"
if curl -s http://localhost:8000/health | grep -q "healthy"; then
    echo -e "${GREEN}✓ API is healthy${NC}"
else
    echo -e "${RED}✗ API health check failed${NC}"
    exit 1
fi
echo ""

# Test 3: List Agents
echo "${YELLOW}Test 3: Listing available agents...${NC}"
curl -s http://localhost:8000/agents | jq .
echo ""

# Test 4: Submit Intent via API
echo "${YELLOW}Test 4: Submitting intent via API...${NC}"
RESPONSE=$(curl -s -X POST http://localhost:8000/intent \
  -H "Content-Type: application/json" \
  -d '{"intent": "Track vaccine distribution in Nakuru"}')
  
ACTION_ID=$(echo $RESPONSE | jq -r '.action_id')
echo "Response: $RESPONSE"
echo "Action ID: $ACTION_ID"
echo ""

# Test 5: Check Action Status
echo "${YELLOW}Test 5: Checking action status...${NC}"
sleep 2
curl -s http://localhost:8000/actions/$ACTION_ID | jq .
echo ""

# Test 6: List Actions
echo "${YELLOW}Test 6: Listing actions...${NC}"
curl -s http://localhost:8000/actions | jq .
echo ""

# Test 7: CLI Intent
echo "${YELLOW}Test 7: Testing CLI intent...${NC}"
docker-compose exec -T cli python -m cli.cli intent "Test intent from CLI" || true
echo ""

# Test 8: Database Check
echo "${YELLOW}Test 8: Checking database records...${NC}"
docker-compose exec -T postgres psql -U atlas -d atlas_sanctum \
  -c "SELECT id, intent, status FROM action_logs LIMIT 5;" || true
echo ""

echo -e "${GREEN}✓ All basic tests completed!${NC}"
echo ""
echo "Next steps:"
echo "1. Check API docs: http://localhost:8000/docs"
echo "2. Submit intents via CLI: docker-compose exec cli python -m cli.cli intent '<your-intent>'"
echo "3. View logs: docker-compose logs -f gateway"
