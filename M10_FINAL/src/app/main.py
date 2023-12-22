import fastapi as fastapi
import sqlalchemy.orm as orm

import app.services as services
import app.schemas as schemas

app = fastapi.FastAPI()
services.create_database()

@app.post("/auctions/", response_model=schemas.Auction)
def create_auction(
    auction:schemas.AuctionCreate, db:orm.Session=fastapi.Depends(services.get_db)
):
    """
    # Create auction if the related company does not already have an auction that overlays another of their auctions.

    ## Args:
        - auction (schemas.AuctionCreate): The schema used to send data to/receive data from the auction table.
        - db (orm.Session, optional): Database session.

    ## Raises:
        - fastapi.HTTPException: Overlay found in auction of the given related company.

    ## Returns:
        - Auction created trigger.
    """
    
    db_auction = services.check_auction_presence(
        db=db, 
        companyName=auction.relatedCompany, 
        auctionStart=auction.auctionStart,
        auctionEnd=auction.auctionEnd
        )

    # Only create auction if does not already exists.
    if db_auction:
        raise fastapi.HTTPException(
            status_code=400, detail="Auction already exists"
        )
    else:
        return services.create_auction(db=db, auction=auction)

@app.get("/auctions/", response_model=list[schemas.Auction])
def read_auctions(
    skip:int=0,
    limit:int=10,
    db:orm.Session = fastapi.Depends(services.get_db)
):
    """
    # Retrieve auctions from the auction table using the given skip and limit boundaries.

    ## Args:
        - skip (int, optional): Number of records to skip before starting retrieval process. Defaults to 0.
        - limit (int, optional): Maximal number of records to retrieve. Defaults to 10.
        - db (orm.Session, optional): Database session.

    ## Returns:
        - List of auctions retrieved.
    """
    auctions = services.get_auctions(db=db, skip=skip, limit=limit)
    return auctions

@app.post("/lots/", response_model=schemas.Lot)
def create_lot(
    lot:schemas.LotCreate, db:orm.Session=fastapi.Depends(services.get_db)
):
    """
    # Create a lot for the given auction.

    ## Args:
        - lot (schemas.LotCreate): The schema used to send data to/receive data from the lots table.
        - db (orm.Session, optional): Database Session.

    ## Raises:
        - fastapi.HTTPException: Given auction ID has no reference in the auction table (Foreign key relation).

    ## Returns:
        - Lot created trigger.
    """
    db_auction = services.get_auction_by_ID(db=db, auctionID=lot.auctionID)
    if not db_auction:
        raise fastapi.HTTPException(
            status_code=500, detail= "Requested auction does not exist"
        )
    
    else:
        return services.create_lot(db=db, lot=lot)

@app.get("/lots/", response_model=list[schemas.Lot])
def read_lots(
    auctionID:int,
    skip:int=0,
    limit:int=10,
    db:orm.Session = fastapi.Depends(services.get_db)
):
    """
    # Retrieve lots from the lots table of the given auction, using the given skip and limit boundaries.

    ## Args:
        - auctionID (int): ID reference of the auction of which the lots are desired to be retrieved.
        - skip (int, optional): Number of records to skip before starting retrieval process. Defaults to 0.
        - limit (int, optional): Maximal number of records to retrieve. Defaults to 10.
        - db (orm.Session, optional): Database session.

    ## Raises:
        - fastapi.HTTPException: Given auction ID has no reference in the auction table (Foreign key relation).

    ## Returns:
        - List of lots retrieved.
    """
    db_auction = services.get_auction_by_ID(db=db, auctionID=auctionID)
    if not db_auction:
        raise fastapi.HTTPException(
            status_code=500, detail= "Requested auction does not exist"
        )
    else:
        return services.get_lots_by_auctionID(db=db, auctionID=auctionID, skip=skip, limit=limit)

@app.get("/bids/", response_model=list[schemas.Bid])
def read_bids(
    auctionID:int,
    lotNr:int,
    skip:int=0,
    limit:int=10,
    db:orm.Session = fastapi.Depends(services.get_db)
):
    """
    # Retrieve bids from the bids table of the concerning auction and lot, using the given skip and limit boundaries

    ## Args:
        - auctionID (int): ID reference of the auction of which (in combination with the lotID) bids need to be retrieved.
        - lotID (int): ID reference of the lot of which (in combination with the auctionID) bids need to be retrieved.
        - skip (int, optional): Number of records to skip before starting retrieval process. Defaults to 0.
        - limit (int, optional): Maximal number of records to retrieve. Defaults to 10.
        - db (orm.Session, optional): Database session.
    
    ## Raises:
        - fastapi.HTTPException: Given Lot does not exist within the given auction.

    ## Returns:
        - List of bids retrieved.
    """
    db_bids = services.get_bids_by_IDs(db=db, auctionID=auctionID, lotNr=lotNr, skip=skip, limit=limit)
    if not db_bids:
        raise fastapi.HTTPException(
            status_code=500, detail= "Given LotID and/or AuctionID do not exist"
        )
    else:
        return db_bids

@app.post("/bids/", response_model=schemas.Bid)
def create_bid(
    bid:schemas.BidCreate, db:orm.Session=fastapi.Depends(services.get_db)
):
    """
    # Create a bid for the given auction and lot combination.

    ## Args:
        - bid (schemas.BidCreate): The schema used to send data to/receive data from the lots table.
        - db (orm.Session, optional): Database Session.

    ## Raises:
        - fastapi.HTTPException: Given Lot does not exist within the given auction.

    ## Returns:
        - Bid created trigger.
    """
    db_lot = services.get_auction_lot_combination(db=db, auctionID=bid.auctionID, lotNr=bid.lotNr)
    if not db_lot:
        raise fastapi.HTTPException(
            status_code=500, detail= "Given LotID and/or AuctionID do not exist"
        )
    else:
        return services.create_bid(db=db, bid=bid)

@app.get("/", response_model=schemas.Price)
def optimal_bid_price(
    numberOfItems:int,
    estimatedValue:float,
    reserveBid:float,
    branchCategory:str,
    auctionDuration:float,
    min_starting_bid:int,
    max_starting_bid:int,
    step_size:int
    ):
    """
    # Retrieve bids from the bids table of the concerning auction and lot, using the given skip and limit boundaries

    ## Args:
        - numberOfItems (int): The number of items in the concerning lot.
        - estimatedValue (int): The estimated values of the items comprising the lot.
        - reserveBid (int): The minimal amount accepted as a sale by the seller.
        - branchCategory (str): The branch category in which the auction will take place.
        - auctionDuration (float): The total duration of the auction.
        - min_starting_bid (int): The minimal price for the auction starting bid.
        - max_starting_bid (int): The maximal price for the auction starting bid.
        - step_size (int): The stepsize between the min_starting_bid and max_starting_bid.
    
    ## Raises:
        - fastapi.HTTPException: When an optimal starting bid price can not be found.

    ## Returns:
        - Auction with the optimal starting price.
    """
    auction_with_starting_bid = services.get_starting_bid(numberOfItems=numberOfItems, estimatedValue=estimatedValue,
                                                          reserveBid=reserveBid, branchCategory=branchCategory, 
                                                          auctionDuration=auctionDuration, min_bid=min_starting_bid, 
                                                          max_bid=max_starting_bid, step_size=step_size)

    if not auction_with_starting_bid.best_starting_bid_price:
        raise fastapi.HTTPException(
            status_code=500, detail= "This will never be sold given the current specifications"
        )
    else:
        return auction_with_starting_bid