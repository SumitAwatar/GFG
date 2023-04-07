pragma solidity ^0.8.0;

contract LandRegistration {
    
    struct Land {
        string name;
        string location;
        bool onSale;
        address owner;
        uint256 pincode;
    }
    
    mapping(string => Land) lands;
    
    function addLand(string memory _name, string memory _location, bool _onSale, uint256 _pincode) public {
        require(lands[_name].name != _name, "Land already exists");
        lands[_name] = Land(_name, _location, _onSale, msg.sender, _pincode);
    }
    
    function editLand(string memory _name, string memory _location, bool _onSale, uint256 _pincode) public {
        require(lands[_name].name == _name, "Land does not exist");
        require(lands[_name].owner == msg.sender, "You are not the owner of this land");
        lands[_name].location = _location;
        lands[_name].onSale = _onSale;
        lands[_name].pincode = _pincode;
    }
    
    function getLandUsingLocation(string memory _location) public view returns (string memory) {
        for (uint i = 0; i < lands.length; i++) {
            if (keccak256(bytes(lands[i].location)) == keccak256(bytes(_location))) {
                return lands[i].name;
            }
        }
        revert("No land found at the given location");
    }
    
    function getLand(string memory _name) public view returns (string memory, string memory, bool, address, uint256) {
        require(lands[_name].name == _name, "Land does not exist");
        Land memory land = lands[_name];
        return (land.name, land.location, land.onSale, land.owner, land.pincode);
    }
    
}
