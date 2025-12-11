// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/security/Pausable.sol";

/**
 * @title MicroAI Governance
 * @notice EPI-enforced governance contract for multi-chain DAO operations
 * @dev Integrates with EPIOracle for ethical-profitability validation
 *
 * From: EPI-governance repository
 * Purpose: Ethereum layer for treasury and cross-chain governance
 */
contract MicroAiGovernance is Ownable, ReentrancyGuard, Pausable {

    // ===================
    // State Variables
    // ===================

    uint256 public epiThreshold;           // Minimum EPI score (scaled by 1000)
    uint256 public votingPeriod;           // Voting duration in seconds
    uint256 public quorumPercentage;       // Required quorum (scaled by 100)
    uint256 public proposalCount;

    address public epiOracle;              // EPIOracle contract address

    // ===================
    // Structs
    // ===================

    struct Proposal {
        uint256 id;
        address proposer;
        string title;
        string description;
        string ipfsHash;                   // Detailed proposal data
        uint256 epiScore;                  // EPI score from oracle
        uint256 votesFor;
        uint256 votesAgainst;
        uint256 votesAbstain;
        uint256 startTime;
        uint256 endTime;
        bool executed;
        bool vetoed;
        ProposalStatus status;
    }

    struct VoterInfo {
        uint256 votingPower;
        bool isRegistered;
    }

    struct GuardianInfo {
        bool isGuardian;
        uint256 vetoCount;
    }

    enum ProposalStatus {
        Pending,
        Active,
        Succeeded,
        Defeated,
        Executed,
        Vetoed
    }

    enum VoteType {
        Against,
        For,
        Abstain
    }

    // ===================
    // Mappings
    // ===================

    mapping(uint256 => Proposal) public proposals;
    mapping(address => VoterInfo) public voters;
    mapping(address => GuardianInfo) public guardians;
    mapping(uint256 => mapping(address => bool)) public hasVoted;

    uint256 public totalVotingPower;

    // ===================
    // Events
    // ===================

    event ProposalCreated(
        uint256 indexed proposalId,
        address indexed proposer,
        string title,
        uint256 epiScore
    );

    event VoteCast(
        uint256 indexed proposalId,
        address indexed voter,
        VoteType voteType,
        uint256 weight
    );

    event ProposalExecuted(uint256 indexed proposalId);
    event ProposalVetoed(uint256 indexed proposalId, address indexed guardian);
    event VoterRegistered(address indexed voter, uint256 votingPower);
    event GuardianAdded(address indexed guardian);
    event EPIThresholdUpdated(uint256 newThreshold);

    // ===================
    // Constructor
    // ===================

    constructor(
        uint256 _epiThreshold,
        uint256 _votingPeriod,
        uint256 _quorumPercentage
    ) Ownable(msg.sender) {
        epiThreshold = _epiThreshold;       // e.g., 700 for 0.70
        votingPeriod = _votingPeriod;       // e.g., 86400 for 1 day
        quorumPercentage = _quorumPercentage; // e.g., 50 for 50%
    }

    // ===================
    // Modifiers
    // ===================

    modifier onlyRegisteredVoter() {
        require(voters[msg.sender].isRegistered, "Not a registered voter");
        _;
    }

    modifier onlyGuardian() {
        require(guardians[msg.sender].isGuardian, "Not a guardian");
        _;
    }

    modifier proposalExists(uint256 _proposalId) {
        require(_proposalId > 0 && _proposalId <= proposalCount, "Proposal does not exist");
        _;
    }

    // ===================
    // Core Functions
    // ===================

    /**
     * @notice Submit a new proposal
     * @param _title Proposal title
     * @param _description Proposal description
     * @param _ipfsHash IPFS hash for detailed data
     * @param _epiScore EPI score (from off-chain calculation or oracle)
     */
    function submitProposal(
        string calldata _title,
        string calldata _description,
        string calldata _ipfsHash,
        uint256 _epiScore
    ) external onlyRegisteredVoter whenNotPaused returns (uint256) {
        require(bytes(_title).length > 0 && bytes(_title).length <= 100, "Invalid title");
        require(bytes(_description).length > 0, "Description required");
        require(_epiScore >= epiThreshold, "EPI score below threshold");

        proposalCount++;

        Proposal storage proposal = proposals[proposalCount];
        proposal.id = proposalCount;
        proposal.proposer = msg.sender;
        proposal.title = _title;
        proposal.description = _description;
        proposal.ipfsHash = _ipfsHash;
        proposal.epiScore = _epiScore;
        proposal.startTime = block.timestamp;
        proposal.endTime = block.timestamp + votingPeriod;
        proposal.status = ProposalStatus.Active;

        emit ProposalCreated(proposalCount, msg.sender, _title, _epiScore);

        return proposalCount;
    }

    /**
     * @notice Cast a vote on a proposal
     * @param _proposalId Proposal ID
     * @param _voteType Vote type (0=Against, 1=For, 2=Abstain)
     */
    function castVote(
        uint256 _proposalId,
        VoteType _voteType
    ) external onlyRegisteredVoter proposalExists(_proposalId) whenNotPaused {
        Proposal storage proposal = proposals[_proposalId];

        require(proposal.status == ProposalStatus.Active, "Proposal not active");
        require(block.timestamp <= proposal.endTime, "Voting period ended");
        require(!hasVoted[_proposalId][msg.sender], "Already voted");

        uint256 weight = voters[msg.sender].votingPower;
        hasVoted[_proposalId][msg.sender] = true;

        if (_voteType == VoteType.For) {
            proposal.votesFor += weight;
        } else if (_voteType == VoteType.Against) {
            proposal.votesAgainst += weight;
        } else {
            proposal.votesAbstain += weight;
        }

        emit VoteCast(_proposalId, msg.sender, _voteType, weight);
    }

    /**
     * @notice Execute a successful proposal
     * @param _proposalId Proposal ID
     */
    function executeProposal(
        uint256 _proposalId
    ) external proposalExists(_proposalId) nonReentrant whenNotPaused {
        Proposal storage proposal = proposals[_proposalId];

        require(block.timestamp > proposal.endTime, "Voting not ended");
        require(!proposal.executed, "Already executed");
        require(!proposal.vetoed, "Proposal vetoed");

        // Check quorum
        uint256 totalVotes = proposal.votesFor + proposal.votesAgainst + proposal.votesAbstain;
        uint256 quorumVotes = (totalVotingPower * quorumPercentage) / 100;
        require(totalVotes >= quorumVotes, "Quorum not reached");

        // Check majority
        require(proposal.votesFor > proposal.votesAgainst, "Proposal defeated");

        proposal.executed = true;
        proposal.status = ProposalStatus.Executed;

        emit ProposalExecuted(_proposalId);
    }

    /**
     * @notice Guardian veto power
     * @param _proposalId Proposal ID to veto
     */
    function vetoProposal(
        uint256 _proposalId
    ) external onlyGuardian proposalExists(_proposalId) {
        Proposal storage proposal = proposals[_proposalId];

        require(
            proposal.status == ProposalStatus.Active ||
            proposal.status == ProposalStatus.Succeeded,
            "Cannot veto"
        );
        require(!proposal.vetoed, "Already vetoed");

        proposal.vetoed = true;
        proposal.status = ProposalStatus.Vetoed;
        guardians[msg.sender].vetoCount++;

        emit ProposalVetoed(_proposalId, msg.sender);
    }

    // ===================
    // Admin Functions
    // ===================

    function registerVoter(
        address _voter,
        uint256 _votingPower
    ) external onlyOwner {
        require(!voters[_voter].isRegistered, "Already registered");

        voters[_voter] = VoterInfo({
            votingPower: _votingPower,
            isRegistered: true
        });

        totalVotingPower += _votingPower;

        emit VoterRegistered(_voter, _votingPower);
    }

    function addGuardian(address _guardian) external onlyOwner {
        require(!guardians[_guardian].isGuardian, "Already guardian");

        guardians[_guardian] = GuardianInfo({
            isGuardian: true,
            vetoCount: 0
        });

        emit GuardianAdded(_guardian);
    }

    function setEPIThreshold(uint256 _newThreshold) external onlyOwner {
        epiThreshold = _newThreshold;
        emit EPIThresholdUpdated(_newThreshold);
    }

    function setEPIOracle(address _oracle) external onlyOwner {
        epiOracle = _oracle;
    }

    function pause() external onlyOwner {
        _pause();
    }

    function unpause() external onlyOwner {
        _unpause();
    }

    // ===================
    // View Functions
    // ===================

    function getProposal(uint256 _proposalId) external view returns (Proposal memory) {
        return proposals[_proposalId];
    }

    function getVoterInfo(address _voter) external view returns (VoterInfo memory) {
        return voters[_voter];
    }

    function isProposalActive(uint256 _proposalId) external view returns (bool) {
        Proposal storage proposal = proposals[_proposalId];
        return proposal.status == ProposalStatus.Active &&
               block.timestamp <= proposal.endTime;
    }
}
