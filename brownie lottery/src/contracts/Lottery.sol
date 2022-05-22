// SPDX-License-Identifier: MIT

/*
    Conversions
    1 Ether = 10**18 wei
    1 gwei = 10**9 wei
    1 wei  = 1 wei
*/

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

import "@openzeppelin/contracts/access/Ownable.sol";

import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract Lottery is VRFConsumerBase, Ownable {
    address payable[] public players;
    uint256 public usdEntryFee;

    AggregatorV3Interface internal ethUsdPriceFeed;

    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }
    LOTTERY_STATE public lottery_state;

    uint256 public fee;
    bytes32 public keyhash;

    address payable public recentWinner;
    uint256 recentRandomness;

    constructor(
        address _priceFeedAddress,
        address _vrfCoordinator,
        address _linkToken,
        uint256 _fee,
        bytes32 _keyhash
    ) public VRFConsumerBase(_vrfCoordinator, _linkToken) {
        // Fee in Wei
        usdEntryFee = 50 * (10**18);
        // Setting the price feed based on parameterized address given during deployment
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSED;

        // VRFConsumerBase constructor work
        fee = fee;
        keyhash = _keyhash;
    }

    function enter() public payable {
        // $50 per player minimum
        require(
            lottery_state == LOTTERY_STATE.OPEN,
            "Lottery is closed/calculating winner"
        );
        require(
            msg.value >= getEntranceFee(),
            "Please provide more ETH to enter the lottery."
        );
        players.push(msg.sender);
    }

    function getEntranceFee() public view returns (uint256) {
        /*
            This returns entrance fee in Wei
        */

        // Example price returned by getPrice: 204282647552
        // The returned price contains 12 digits and 8 Decimals
        // As per https://docs.chain.link/docs/ethereum-addresses/

        uint256 price = getEthUsdPriceInUsd();

        // Converting to wei... 8 decimals * 10^10 makes 10^18
        uint256 adjustedPrice = uint256(price) * (10**10);

        // $50/$2000 * 10**18 to get entry price in wei
        // And since solidity cannot deal with decimals we multiply by 10**18 first then divide the result by price
        uint256 costToEnter = (usdEntryFee * (10**18)) / adjustedPrice;

        // CostToEnter price in wei
        return costToEnter;
    }

    function getEthUsdPriceInUsd() public view returns (uint256) {
        (, int256 price, , , ) = ethUsdPriceFeed.latestRoundData();
        return uint256(price);
    }

    function startLottery() public onlyOwner {
        require(
            lottery_state == LOTTERY_STATE.CLOSED,
            "Lottery is closed right now. Please come back later."
        );
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function endLottery() public onlyOwner {
        /*
        This is not a true random number as most/all the parameters of hash are predictable,
        not to be used in production applications
        uint256(
            keccak256(
                abi.encodePacked(
                    nonce, // nonce is predictable aka transaction number
                    msg.sender, // msg.sender is predictable
                    block.difficulty, // can actually be manipulated by miners!
                    block.timestamp // timestamp is predictable
                )
            )
        ) % players.length;
        */

        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;

        // Request -> Callback Architecture
        // We are requesting randomness here
        // Contract will use callback fulfillRandomness() to fulfil the request
        bytes32 requestId = requestRandomness(keyhash, fee);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomness)
        internal
        override
    {
        require(
            lottery_state == LOTTERY_STATE.CALCULATING_WINNER,
            "Lottery is closed right now. Please come back later."
        );
        require(randomness > 0, "Random number not found!");
        uint256 winnerIndex = randomness % players.length;
        recentWinner = players[winnerIndex];
        lottery_state = LOTTERY_STATE.CLOSED;
        recentWinner.transfer(address(this).balance);
        recentRandomness = randomness;

        // Reset
        players = new address payable[](0);
        lottery_state = LOTTERY_STATE.CLOSED;
    }
}
