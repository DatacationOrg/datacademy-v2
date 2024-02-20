import datetime as dt
import sqlalchemy as sql
import sqlalchemy.orm as orm
import pandas as pd

import joblib

import app.database as database
import app.models as models
import app.schemas as schemas

def create_database():
    return database.Base.metadata.create_all(bind=database.engine)

def get_db():
    """
    Setup database session, which is always closed after use.

    Yields:
        db: database session
    """
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def check_auction_presence(db:orm.Session, companyName, auctionStart, auctionEnd):
    """
    Check if the requested auction company already has an auction overlapping the start and end date.

    Args:
        db (orm.Session): Database session.
        companyName: The name of the related company.
        auctionStart: The start date and time of the auction.
        auctionEnd: The end date and time of the auction.
    """
    return db.query(models.Auction).filter(
        sql.and_(
            models.Auction.relatedCompany == companyName,
            sql.or_(  # Test whether start or end falls within other auction of same company
                sql.and_(
                    models.Auction.auctionStart <= auctionStart,
                    models.Auction.auctionEnd >= auctionStart
                    ),
                sql.and_(
                    models.Auction.auctionStart <= auctionEnd,
                    models.Auction.auctionEnd >= auctionEnd
                    )
                )
            )
        ).first()
    
def get_auctions(db:orm.Session, skip:int, limit:int):
    """
    Retrieve the given number of auctions from the database

    Args:
        db (orm.Session): Database session.
        skip (int): The amount of records skipped before start of retrieval
        limit (int): The maximum amount of records returned
    """
    return db.query(models.Auction).offset(skip).limit(limit).all()

def create_auction(db:orm.Session, auction:schemas.AuctionCreate):
    """
    Create an auction, automatically generating the id

    Args:
        db (orm.Session): Database session.
        auction (schemas.AuctionCreate): Schema for auction creation.
    """
    db_auction = models.Auction(
        relatedCompany=auction.relatedCompany,
        auctionStart=auction.auctionStart,
        auctionEnd=auction.auctionEnd,
        branchCategory=auction.branchCategory
        )
    db.add(db_auction)
    db.commit()
    db.refresh(db_auction)
    return db_auction

def get_auction_by_ID(db:orm.Session, auctionID:int):
    """
    Retrieve auction given auction id, used to check if lot creation is valid

    Args:
        db (orm.Session): Database session.
        auctionID (int): ID of auction to be retrieved.

    Returns:
        first record found of the given auctionID
    """
    return db.query(models.Auction).filter(models.Auction.id == auctionID).first()

def create_lot(db:orm.Session, lot:schemas.LotCreate):
    """
    Create a lot, automatically generating a lot number by incrementing the number of the last created lot

    Args:
        db (orm.Session): Database session.
        lot (schemas.LotCreate): Schema for lot creation.
    """
    queryRes = db.query(models.Lots).filter(models.Lots.auctionID == lot.auctionID).order_by(models.Lots.lotNr.desc()).first()
    if queryRes:
        lotnumber=queryRes.lotNr + 1
    else:
        lotnumber=1

    auctionDuration = get_auction_duration(db=db, auctionID=lot.auctionID)

    startingBid = get_starting_bid(
        numberOfItems=lot.numberOfItems,
        estimatedValue=lot.estimatedValue,
        reserveBid=lot.reserveBid,
        auctionDuration=auctionDuration,
        category=lot.mainCategory
        )

    db_lot = models.Lots(
        auctionID=lot.auctionID,
        lotNr=lotnumber,
        numberOfItems=lot.numberOfItems, 
        estimatedValue=lot.estimatedValue,
        startingBid=startingBid,
        reserveBid=lot.reserveBid,
        mainCategory=lot.mainCategory,
        countryCode='NL',
        VAT=21,
        suffix='N/A',
        saleDate=dt.datetime(year=1000, month=1, day=1, hour=0, minute=0, second=0),
        buyerAccountID=99999,
        currentBid=99999,
        sold=False
        )

    db.add(db_lot)
    db.commit()
    db.refresh(db_lot)
    return db_lot

def get_lots_by_auctionID(db:orm.Session, auctionID:int, skip:int, limit:int):
    """
    Retrieve all lots belonging to the given auction id

    Args:
        db (orm.Session): Database session.
        auctionID (int): ID of the auction to be searched.

    Returns:
        A list of all lots belonging to the given auction
    """
    return db.query(models.Lots).filter(models.Lots.auctionID == auctionID).offset(skip).limit(limit).all()

def get_auction_lot_combination(db:orm.Session, auctionID:int, lotNr:int):
    """
    Retrieve auction and lot to test whether this combination exists

    Args:
        db (orm.Session): Database session.
        auctionID (int): ID reference of the auction.
        lotNr (int): Lot number refering to the product to be sold in the given auction.
    """
    return db.query(models.Lots).filter(
                sql.and_(
                    models.Lots.auctionID==auctionID,
                    models.Lots.lotNr==lotNr
                    )
                ).first()

def get_bids_by_IDs(db:orm.Session, auctionID:int, lotNr:int, skip:int, limit:int):
    """
    Retrieve all lots belonging to the given auction id

    Args:
        db (orm.Session): Database session.
        auctionID (int): ID of the auction to be searched.

    Returns:
        A list of all lots belonging to the given auction
    """
    return db.query(models.Bids).filter(
                    sql.and_(
                        models.Bids.auctionID == auctionID,
                        models.Bids.lotNr == lotNr
                        )        
                    ).offset(skip).limit(limit).all()

def create_bid(db:orm.Session, bid:schemas.BidCreate):
    """
    Create a bid, automatically generating a lot number by incrementing the number of the last created bid

    Args:
        db (orm.Session): Database Session.
        bid (schemas.BidCreate): Schema for bid creation.
    """
    # Retrieve bid number for reference incrementation
    queryRes = db.query(models.Bids).filter(
        sql.and_(
            models.Bids.auctionID == bid.auctionID,
            models.Bids.lotNr == bid.lotNr
            )
        ).order_by(models.Bids.bidNr.desc()).first()
    
    if queryRes:
        bidnumber=queryRes.bidNr + 1
    else:
        bidnumber=1

    # Retrieve auction for closingDateTime
    relatedAuction = db.query(models.Auction).filter(models.Auction.id==bid.auctionID).first()

    db_bid = models.Bids(
        auctionID=bid.auctionID,
        lotNr=bid.lotNr,
        bidNr=bidnumber,
        isCombination=bid.isCombination,
        accountID=bid.accountID,
        isCompany=bid.isCompany,
        bidPrice=bid.bidPrice,
        biddingDateTime=dt.datetime.now(),
        closingDateTime=relatedAuction.auctionEnd
        )
    
    db.add(db_bid)
    db.commit()
    db.refresh(db_bid)
    return db_bid

def get_auction_duration(db:orm.session, auctionID:int) -> int:
    """
    Retrieve the duration of a given auction.

    Args:
        db (orm.session): Database Session.
        auctionID (int): ID reference of an auction.

    Returns:
        int: The duration of the auction in hours.
    """
    auction = get_auction_by_ID(db=db, auctionID=auctionID)
    return int((auction.auctionEnd - auction.auctionStart) / dt.timedelta(hours=1))

def get_starting_bid(numberOfItems:int, estimatedValue:float, reserveBid:float, branchCategory:str, auctionDuration:float, min_bid:int, max_bid:int, step_size:int):
    """
    Return the optimal starting bid (highest with prediction sale) for the given auction lot.

    Args:
        numberOfItems (int): The number of items in the concerning lot.
        estimatedValue (float): The estimated values of the items comprising the lot.
        reserveBid (float): The minimal amount accepted as a sale by the seller.
        branchCategory (str): The branch category in which the auction will take place.
        auctionDuration (float): The total duration of the auction.

    Returns:
        class: Proposed starting bid value in the schemas.Price form.
    """
    # Load the pickled pipeline
    model_pipe = joblib.load("./src/trained_pipeline.pkl")
    
    # Loop over the starting bids ranging from
    startingBids = list(range(min_bid, max_bid, step_size))

    # Create an input for the pipeline
    trialdf = pd.DataFrame(data={
        'numberOfItems': [numberOfItems] * len(startingBids),
        'estimatedValue': [estimatedValue] * len(startingBids),
        'startingBid': startingBids,
        'reserveBid': [reserveBid] * len(startingBids),
        'branchCategory': [branchCategory] * len(startingBids),
        'auctionDuration': [auctionDuration] * len(startingBids),
    })

    # Predict and save the results
    trialdf['saleNoSale'] = model_pipe.predict(trialdf)
    idx = trialdf[trialdf['saleNoSale'] == 1.0].index.tolist()
    startingBid = startingBids[max(idx)]
    
    # Return in the corresponding schema
    output_with_best_start_price = schemas.Price(
            numberOfItems=numberOfItems,
            estimatedValue=estimatedValue,
            reserveBid=reserveBid,
            branchCategory=branchCategory,
            auctionDuration=auctionDuration,
            best_starting_bid_price=startingBid
        )

    return output_with_best_start_price