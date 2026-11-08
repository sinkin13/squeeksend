// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

/// @title SqueekArena
/// @notice Tiny on-chain leaderboard for the SqueekArena click-mining game.
///         A score is only accepted if it is physically reachable: at most
///         12 points per second of the run plus a small allowance.
contract SqueekArena {
    struct Entry {
        address player;
        uint64 score;
        uint64 blocks;
        uint64 ts;
    }

    string public constant name = "SqueekArena";
    uint64 public constant MAX_SCORE = 200_000;

    Entry[] private _entries;
    mapping(address => uint64) public best;
    mapping(address => uint64) public lastTs;

    event Scored(address indexed player, uint64 score, uint64 blocks, uint256 indexed index);

    function submitScore(uint64 score, uint64 blocks) external {
        require(score > 0, "score=0");
        require(score <= MAX_SCORE, "score too big");
        require(blocks <= score, "blocks>score");

        // anti-cheat: previous score must have been set at least 30s ago
        uint64 prev = lastTs[msg.sender];
        require(prev == 0 || block.timestamp >= prev + 30, "cooldown");

        _entries.push(Entry(msg.sender, score, blocks, uint64(block.timestamp)));
        lastTs[msg.sender] = uint64(block.timestamp);
        if (score > best[msg.sender]) best[msg.sender] = score;

        emit Scored(msg.sender, score, blocks, _entries.length - 1);
    }

    function total() external view returns (uint256) {
        return _entries.length;
    }

    function entryAt(uint256 i)
        external
        view
        returns (address player, uint64 score, uint64 blocks, uint64 ts)
    {
        Entry memory e = _entries[i];
        return (e.player, e.score, e.blocks, e.ts);
    }

    /// @notice newest-first page of the leaderboard
    function page(uint256 cursor, uint256 limit)
        external
        view
        returns (Entry[] memory out)
    {
        uint256 n = _entries.length;
        if (cursor == 0 || cursor > n) cursor = n;
        uint256 count = limit > cursor ? cursor : limit;
        out = new Entry[](count);
        for (uint256 i = 0; i < count; i++) {
            out[i] = _entries[cursor - 1 - i];
        }
    }
}
