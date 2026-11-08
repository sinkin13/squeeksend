// SPDX-License-Identifier: MIT
pragma solidity ^0.8.26;

/// @title SqueekBattle
/// @notice On-chain proof for a fully deterministic battle royale.
///         The whole match is a pure function of `seed`. Anyone can replay
///         the same seed with the same rules and check `winnerId` is honest.
contract SqueekBattle {
    struct Match {
        address reporter;
        uint64 seed;
        uint8 winnerId;
        uint8 survivors;
        uint16 durationSec;
        uint64 ts;
    }

    string public constant name = "SqueekBattle";

    Match[] private _matches;
    mapping(uint64 => bool) public seedUsed;

    event MatchRecorded(
        uint64 indexed seed,
        address indexed reporter,
        uint8 winnerId,
        uint8 survivors,
        uint16 durationSec,
        uint256 indexed index
    );

    function recordMatch(uint64 seed, uint8 winnerId, uint8 survivors, uint16 durationSec) external {
        // one record per seed: the match is a pure function of it, so a second
        // record for the same seed would have to be identical anyway.
        require(!seedUsed[seed], "seed already recorded");
        require(winnerId < 32, "bad winner id");
        require(survivors >= 1 && survivors <= 32, "bad survivors");
        require(durationSec > 0 && durationSec <= 600, "bad duration");

        seedUsed[seed] = true;
        _matches.push(Match(msg.sender, seed, winnerId, survivors, durationSec, uint64(block.timestamp)));
        emit MatchRecorded(seed, msg.sender, winnerId, survivors, durationSec, _matches.length - 1);
    }

    function total() external view returns (uint256) {
        return _matches.length;
    }

    function matchAt(uint256 i)
        external
        view
        returns (address reporter, uint64 seed, uint8 winnerId, uint8 survivors, uint16 durationSec, uint64 ts)
    {
        Match memory m = _matches[i];
        return (m.reporter, m.seed, m.winnerId, m.survivors, m.durationSec, m.ts);
    }

    function page(uint256 cursor, uint256 limit)
        external
        view
        returns (Match[] memory out)
    {
        uint256 n = _matches.length;
        if (cursor == 0 || cursor > n) cursor = n;
        uint256 count = limit > cursor ? cursor : limit;
        out = new Match[](count);
        for (uint256 i = 0; i < count; i++) {
            out[i] = _matches[cursor - 1 - i];
        }
    }
}
