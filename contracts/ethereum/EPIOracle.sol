// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title EPI Oracle
 * @notice On-chain oracle for Ethical Profitability Index scores
 * @dev Bridges off-chain EPI calculations to smart contracts
 *
 * From: EPI-governance repository
 * Purpose: Provide verifiable EPI scores for governance decisions
 */
contract EPIOracle is Ownable {

    // ===================
    // State Variables
    // ===================

    // Authorized data providers (e.g., EXECAI, validators)
    mapping(address => bool) public authorizedProviders;

    // Stored EPI scores by proposal/entity hash
    mapping(bytes32 => EPIScore) public epiScores;

    // Historical scores for audit trail
    mapping(bytes32 => EPIScore[]) public scoreHistory;

    // ===================
    // Structs
    // ===================

    struct EPIScore {
        uint256 score;              // EPI score (scaled by 1000, e.g., 750 = 0.75)
        uint256 ethicalComponent;   // Ethics score component
        uint256 profitComponent;    // Profitability component
        uint256 balanceRatio;       // Golden ratio balance
        uint256 trustFactor;        // Trust accumulator value
        uint256 timestamp;
        address provider;
        bool isValid;
    }

    // ===================
    // Events
    // ===================

    event ScoreSubmitted(
        bytes32 indexed entityHash,
        uint256 score,
        address indexed provider,
        uint256 timestamp
    );

    event ProviderAuthorized(address indexed provider);
    event ProviderRevoked(address indexed provider);

    // ===================
    // Constructor
    // ===================

    constructor() Ownable(msg.sender) {
        // Owner is automatically an authorized provider
        authorizedProviders[msg.sender] = true;
    }

    // ===================
    // Modifiers
    // ===================

    modifier onlyAuthorized() {
        require(authorizedProviders[msg.sender], "Not authorized provider");
        _;
    }

    // ===================
    // Core Functions
    // ===================

    /**
     * @notice Submit an EPI score for an entity
     * @param _entityHash Unique identifier hash (e.g., keccak256 of proposal ID)
     * @param _score Overall EPI score (scaled by 1000)
     * @param _ethicalComponent Ethics component score
     * @param _profitComponent Profitability component score
     * @param _balanceRatio Golden ratio balance
     * @param _trustFactor Trust accumulator value
     */
    function submitScore(
        bytes32 _entityHash,
        uint256 _score,
        uint256 _ethicalComponent,
        uint256 _profitComponent,
        uint256 _balanceRatio,
        uint256 _trustFactor
    ) external onlyAuthorized {
        require(_score <= 1000, "Score exceeds maximum");
        require(_ethicalComponent <= 1000, "Ethics exceeds maximum");
        require(_profitComponent <= 1000, "Profit exceeds maximum");

        EPIScore memory newScore = EPIScore({
            score: _score,
            ethicalComponent: _ethicalComponent,
            profitComponent: _profitComponent,
            balanceRatio: _balanceRatio,
            trustFactor: _trustFactor,
            timestamp: block.timestamp,
            provider: msg.sender,
            isValid: true
        });

        // Store current score
        epiScores[_entityHash] = newScore;

        // Add to history
        scoreHistory[_entityHash].push(newScore);

        emit ScoreSubmitted(_entityHash, _score, msg.sender, block.timestamp);
    }

    /**
     * @notice Get the current EPI score for an entity
     * @param _entityHash Entity identifier hash
     * @return EPIScore struct with all components
     */
    function getScore(bytes32 _entityHash) external view returns (EPIScore memory) {
        return epiScores[_entityHash];
    }

    /**
     * @notice Check if an entity meets the EPI threshold
     * @param _entityHash Entity identifier hash
     * @param _threshold Minimum required score (scaled by 1000)
     * @return bool True if score meets or exceeds threshold
     */
    function meetsThreshold(
        bytes32 _entityHash,
        uint256 _threshold
    ) external view returns (bool) {
        EPIScore memory score = epiScores[_entityHash];
        return score.isValid && score.score >= _threshold;
    }

    /**
     * @notice Get score history for an entity
     * @param _entityHash Entity identifier hash
     * @return Array of historical EPIScores
     */
    function getScoreHistory(
        bytes32 _entityHash
    ) external view returns (EPIScore[] memory) {
        return scoreHistory[_entityHash];
    }

    /**
     * @notice Calculate entity hash from proposal ID
     * @param _proposalId Proposal identifier
     * @return bytes32 hash
     */
    function calculateEntityHash(
        uint256 _proposalId
    ) external pure returns (bytes32) {
        return keccak256(abi.encodePacked("proposal", _proposalId));
    }

    // ===================
    // Admin Functions
    // ===================

    /**
     * @notice Authorize a new data provider
     * @param _provider Address to authorize
     */
    function authorizeProvider(address _provider) external onlyOwner {
        require(!authorizedProviders[_provider], "Already authorized");
        authorizedProviders[_provider] = true;
        emit ProviderAuthorized(_provider);
    }

    /**
     * @notice Revoke provider authorization
     * @param _provider Address to revoke
     */
    function revokeProvider(address _provider) external onlyOwner {
        require(authorizedProviders[_provider], "Not authorized");
        require(_provider != owner(), "Cannot revoke owner");
        authorizedProviders[_provider] = false;
        emit ProviderRevoked(_provider);
    }

    /**
     * @notice Invalidate a score (e.g., for corrections)
     * @param _entityHash Entity identifier hash
     */
    function invalidateScore(bytes32 _entityHash) external onlyOwner {
        epiScores[_entityHash].isValid = false;
    }
}
