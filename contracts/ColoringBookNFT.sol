// contracts/ColoringBookNFT.sol

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Royalty.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract ColoringBookNFT is ERC721URIStorage, ERC721Royalty, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;
    
    // Mapping from token ID to its collection ID
    mapping(uint256 => uint256) public tokenCollection;
    
    // Collection details
    struct Collection {
        string name;
        uint256 royaltyFraction;
        address creator;
        bool active;
    }
    
    mapping(uint256 => Collection) public collections;
    Counters.Counter private _collectionIds;
    
    event CollectionCreated(uint256 indexed collectionId, string name, address creator);
    event DesignMinted(uint256 indexed tokenId, uint256 indexed collectionId, address creator);

    constructor() ERC721("ColoringBook", "CLRB") {}
    
    function createCollection(
        string memory name,
        uint96 royaltyFraction
    ) public returns (uint256) {
        _collectionIds.increment();
        uint256 newCollectionId = _collectionIds.current();
        
        collections[newCollectionId] = Collection({
            name: name,
            royaltyFraction: royaltyFraction,
            creator: msg.sender,
            active: true
        });
        
        emit CollectionCreated(newCollectionId, name, msg.sender);
        return newCollectionId;
    }
    
    function mintDesign(
        uint256 collectionId,
        string memory tokenURI
    ) public returns (uint256) {
        require(collections[collectionId].active, "Collection does not exist");
        require(
            collections[collectionId].creator == msg.sender,
            "Only collection creator can mint"
        );
        
        _tokenIds.increment();
        uint256 newTokenId = _tokenIds.current();
        
        _safeMint(msg.sender, newTokenId);
        _setTokenURI(newTokenId, tokenURI);
        tokenCollection[newTokenId] = collectionId;
        
        // Set royalties for the token
        _setTokenRoyalty(
            newTokenId,
            collections[collectionId].creator,
            uint96(collections[collectionId].royaltyFraction)
        );
        
        emit DesignMinted(newTokenId, collectionId, msg.sender);
        return newTokenId;
    }
    
    // Override required by Solidity
    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721Royalty)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
    
    function _burn(uint256 tokenId)
        internal
        override(ERC721URIStorage, ERC721Royalty)
    {
        super._burn(tokenId);
    }
}