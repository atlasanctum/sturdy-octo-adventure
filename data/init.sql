-- Initialize database for Atlas Sanctum OS

CREATE TABLE IF NOT EXISTS action_logs (
    id SERIAL PRIMARY KEY,
    intent VARCHAR(500) NOT NULL,
    agent_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    metadata JSONB,
    blockchain_tx_hash VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    executed_at TIMESTAMP,
    result TEXT,
    INDEX idx_status (status),
    INDEX idx_created_at (created_at),
    INDEX idx_blockchain_tx_hash (blockchain_tx_hash)
);

CREATE TABLE IF NOT EXISTS policy_rules (
    id SERIAL PRIMARY KEY,
    rule_name VARCHAR(100) UNIQUE NOT NULL,
    rule_pattern VARCHAR(500) NOT NULL,
    action VARCHAR(20) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default policies
INSERT INTO policy_rules (rule_name, rule_pattern, action, description) VALUES
    ('humanitarian_health', 'vaccine|medicine|treatment|health|medical', 'allow', 'Authorize health and medical operations'),
    ('humanitarian_finance', 'fund|allocate|transfer|support', 'allow', 'Authorize financial support operations'),
    ('dangerous_operation', 'destroy|delete|poison|bomb|harm', 'deny', 'Block dangerous operations'),
    ('unauthorized_access', 'steal|hack|breach|penetrate', 'deny', 'Block unauthorized access attempts')
ON CONFLICT DO NOTHING;

-- Grant permissions
ALTER TABLE action_logs OWNER TO atlas;
ALTER TABLE policy_rules OWNER TO atlas;
