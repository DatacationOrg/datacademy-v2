import datetime as dt
import pydantic as pydantic

class _AuctionBase(pydantic.BaseModel):
    relatedCompany: str
    auctionStart: dt.datetime
    auctionEnd: dt.datetime
    branchCategory: str

class AuctionCreate(_AuctionBase):
    pass

class Auction(_AuctionBase):
    id: int

    class Config:
        orm_mode = True


class _LotBase(pydantic.BaseModel):
    auctionID: int
    numberOfItems: int
    estimatedValue: float
    reserveBid: float
    mainCategory: str

class LotCreate(_LotBase):
    pass

class Lot(_LotBase):
    lotNr: int
    countryCode: str
    saleDate: dt.datetime
    startingBid: float
    suffix: str
    buyerAccountID: int
    currentBid: float
    VAT: float
    sold: bool

    class Config:
        orm_mode = True


class _BidBase(pydantic.BaseModel):
    auctionID: int
    lotNr: int
    isCombination: bool
    accountID: int
    isCompany: bool
    bidPrice: float
    biddingDateTime: dt.datetime

class BidCreate(_BidBase):
    pass

class Bid(_BidBase):
    bidNr: int
    closingDateTime: dt.datetime

    class Config:
        orm_mode = True


class _StartingPriceBase(pydantic.BaseModel):
    numberOfItems:int
    estimatedValue:float
    reserveBid:float
    branchCategory:str
    auctionDuration:float

class Price(_StartingPriceBase):
    best_starting_bid_price: float

    class Config:
        orm_mode = True