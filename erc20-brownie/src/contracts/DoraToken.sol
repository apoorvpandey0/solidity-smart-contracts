// contracts/GLDToken.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "OpenZeppelin/openzeppelin-contracts@4.0.0/contracts/token/ERC20/ERC20.sol";

contract DoraToken is ERC20 {
    constructor(uint256 initialSupply) ERC20("Dora", "DORA") {
        _mint(msg.sender, initialSupply);
    }
}
