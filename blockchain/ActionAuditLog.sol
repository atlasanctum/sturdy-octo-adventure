// SPDX-License-Identifier: Apache-2.0
pragma solidity ^0.8.0;

/**
 * @title ActionAuditLog
 * @dev Logs all critical actions to blockchain for immutable audit trail.
 */
contract ActionAuditLog {
    
    struct LogEntry {
        uint256 timestamp;
        address indexed executor;
        string action;
        string metadata;
        bytes32 txHash;
    }
    
    LogEntry[] public entries;
    address public owner;
    
    event ActionLogged(uint256 indexed logId, address indexed executor, string action);
    
    constructor() {
        owner = msg.sender;
    }
    
    /**
     * @dev Log an action to the blockchain.
     * @param action Description of the action
     * @param metadata JSON metadata (stringified)
     * @param txHash External transaction hash for linking
     */
    function logAction(
        string memory action,
        string memory metadata,
        bytes32 txHash
    ) public returns (uint256) {
        LogEntry memory entry = LogEntry({
            timestamp: block.timestamp,
            executor: msg.sender,
            action: action,
            metadata: metadata,
            txHash: txHash
        });
        
        entries.push(entry);
        uint256 logId = entries.length - 1;
        
        emit ActionLogged(logId, msg.sender, action);
        return logId;
    }
    
    /**
     * @dev Get total number of logged actions.
     */
    function getLogCount() public view returns (uint256) {
        return entries.length;
    }
    
    /**
     * @dev Get a specific log entry.
     */
    function getLog(uint256 index) public view returns (LogEntry memory) {
        require(index < entries.length, "Log index out of bounds");
        return entries[index];
    }
    
    /**
     * @dev Get the latest log entry.
     */
    function getLatestLog() public view returns (LogEntry memory) {
        require(entries.length > 0, "No logs available");
        return entries[entries.length - 1];
    }
}
