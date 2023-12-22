import sqlalchemy as sql
import sqlalchemy.orm as orm

import app.database as database


class Auction(database.Base):
    __tablename__ = "auctions"
    id = sql.Column(sql.Integer, primary_key=True, index=True)
    relatedCompany = sql.Column(sql.String, index=True)
    auctionStart = sql.Column(sql.DateTime, index=True)
    auctionEnd = sql.Column(sql.DateTime, index=True)
    branchCategory = sql.Column(sql.String, index=True)

    # orm.relationship("Lots", back_populates="...")


class Lots(database.Base):
    __tablename__ = "lots"
    countryCode = sql.Column(sql.String, index=True)
    saleDate = sql.Column(sql.DateTime, index=True)
    auctionID = sql.Column(sql.Integer, sql.ForeignKey("auctions.id"), primary_key=True)
    lotNr = sql.Column(sql.Integer, primary_key=True, index=True)
    suffix = sql.Column(sql.String, index=True)
    numberOfItems = sql.Column(sql.Integer, index=True)
    buyerAccountID = sql.Column(sql.Integer, index=True)
    estimatedValue = sql.Column(sql.Float, index=True)
    startingBid = sql.Column(sql.Float, index=True)
    reserveBid = sql.Column(sql.Float, index=True)
    currentBid = sql.Column(sql.Float, index=True)
    VAT = sql.Column(sql.Float, index=True)
    mainCategory = sql.Column(sql.String, index=True)
    sold = sql.Column(sql.Boolean, index=True)

    # orm.relationship("Bids", back_populates="...")


class Bids(database.Base):
    __tablename__ = "bids"
    auctionID = sql.Column(sql.Integer, sql.ForeignKey("lots.auctionID"), primary_key=True)
    lotNr = sql.Column(sql.Integer, sql.ForeignKey("lots.lotNr"), primary_key=True)
    bidNr = sql.Column(sql.Integer, primary_key=True, index=True)
    lotID = sql.Column(sql.Integer, index=True)
    isCombination = sql.Column(sql.Boolean, index=True)
    accountID = sql.Column(sql.Integer, index=True)
    isCompany = sql.Column(sql.Boolean, index=True)
    bidPrice = sql.Column(sql.Float, index=True)
    biddingDateTime = sql.Column(sql.DateTime, index=True)
    closingDateTime = sql.Column(sql.DateTime, index=True)

    # orm.relationship("Lots", back_populates="...")