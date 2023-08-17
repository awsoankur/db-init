from __future__ import annotations
from db.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped,mapped_column#,relationship
from datetime import datetime,date
#from typing import Optional


class State(Base):
    __tablename__="state"

    id : Mapped[str] = mapped_column(primary_key=True)
    value : Mapped[str]

class CreditReportData(Base):
    __tablename__="credit_report_data"

    id : Mapped[str] = mapped_column(primary_key=True)
    merchant : Mapped[str] = mapped_column(ForeignKey("merchant.id"),unique=True)
    json_data : Mapped[str]

class Service(Base):
    __tablename__="service"

    id : Mapped[str] = mapped_column(primary_key=True)
    name : Mapped[str]
    is_primary_payin_account : Mapped[bool] = mapped_column(nullable=True)
    is_primary_payout_account : Mapped[bool] = mapped_column(nullable=True)

class Partner(Base):
    __tablename__="partner"

    id : Mapped[str] = mapped_column(primary_key=True)
    name : Mapped[str]

class Otp(Base):
    __tablename__="otp"

    id : Mapped[str] = mapped_column(primary_key=True)
    otp : Mapped[str]
    merchant : Mapped[str] = mapped_column(ForeignKey("merchant.id"))
    destination : Mapped[str] = mapped_column(nullable=True)

class PayinCollection(Base):
    __tablename__="payin_collection"

    id : Mapped[str] = mapped_column(primary_key=True)
    payin_va : Mapped[str] = mapped_column(ForeignKey("payin_va.id"))
    collection_id : Mapped[str]
    amount : Mapped[float]
    mode : Mapped[str] = mapped_column(nullable=True)
    remitter_upi_id : Mapped[str]
    remitter_account_number : Mapped[str] = mapped_column(nullable=True)
    remitter_ifsc_code : Mapped[str]
    remitter_name : Mapped[str]
    remitter_phone_number : Mapped[str]
    utr : Mapped[str] = mapped_column(nullable=True)
    remarks : Mapped[str] = mapped_column(nullable=True)
    merchant_initiated_transaction : Mapped[str] = mapped_column(ForeignKey("merchant_initiated_transaction.id"),unique=True)
    request_hostname : Mapped[str]
    payin_collection_settlement : Mapped[str] = mapped_column(ForeignKey("payin_collection_settlement.id"),unique=True)

class MerchantInitiatedTransaction(Base):
    __tablename__="merchant_initiated_transaction"

    id : Mapped[str] = mapped_column(primary_key=True)
    merchant : Mapped[str] = mapped_column(ForeignKey("merchant.id"))
    remitter_phone_number : Mapped[str]
    transaction_id : Mapped[str]
    mode : Mapped[str] = mapped_column(nullable=True)
    status : Mapped[str] = mapped_column(nullable=True)
    link : Mapped[str]
    shortened_link : Mapped[str] = mapped_column(nullable=True)
    link_expiry : Mapped[datetime]

class PayinCollectionSettlement(Base):
    __tablename__="payin_collection_settlement"
    id : Mapped[str] = mapped_column(primary_key=True)
    batch_id : Mapped[str]
    amount : Mapped[float]
    status : Mapped[str] = mapped_column(nullable=True)
    initiated_by : Mapped[str] = mapped_column(nullable=True)
    collection_ids : Mapped[str]  = mapped_column(nullable=True)      # , seperated values as an array
    payin_settlement_bank_account : Mapped[str] = mapped_column(ForeignKey("payin_settlement_bank_account.id"),unique=True)

class PayinCollectionSettlementCallbackDump(Base):
    __tablename__="payin_collection_settlement_callback_dump"

    id : Mapped[str] = mapped_column(primary_key=True)
    payin_collection_settlement : Mapped[str] = mapped_column(ForeignKey("payin_collection_settlement.id"),unique=True)
    settlement_json_dump : Mapped[str] = mapped_column(nullable=True)

class PayinCollectionCallbackDump(Base):
    __tablename__="payin_collection_callback_dump"

    id : Mapped[str] = mapped_column(primary_key=True)
    payin_collection : Mapped[str] = mapped_column(ForeignKey("payin_collection.id"),unique=True)
    dump : Mapped[str] = mapped_column(nullable=True)

class PayinSettlementBankAccount(Base):
    __tablename__="payin_settlement_bank_account"

    id : Mapped[str] = mapped_column(primary_key=True)
    payin_va : Mapped[str] = mapped_column(ForeignKey("payin_va.id"),unique=True)
    merchant_bank_account : Mapped[str] = mapped_column(ForeignKey("merchant_bank_account.id"))
    kyc_status : Mapped[str] = mapped_column(nullable=True)

class PayinVa(Base):
    __tablename__="payin_va"

    id : Mapped[str] = mapped_column(primary_key=True)
    va : Mapped[str] = mapped_column(nullable=True)
    ifsc : Mapped[str]
    vpa : Mapped[str] = mapped_column(nullable=True)
    merchant_partner_service : Mapped[str] = mapped_column(ForeignKey("merchant_partner_service.id"))
    status : Mapped[str] = mapped_column(nullable=True)
    reject_reason : Mapped[str] = mapped_column(nullable=True)

class Qr(Base):
    __tablename__="qr"

    id : Mapped[str] = mapped_column(primary_key=True)
    value : Mapped[str] 

class QrOrder(Base):
    __tablename__="qr_order"

    id : Mapped[str] = mapped_column(primary_key=True)
    qr_code : Mapped[str] = mapped_column(ForeignKey("qr.id"),unique=True)
    merchant : Mapped[str] = mapped_column(ForeignKey("merchant.id"))
    order_date : Mapped[date] = mapped_column(default=date.today())
    payment_mode : Mapped[str] = mapped_column(nullable=True)
    order_status : Mapped[str] = mapped_column(nullable=True)
    # merchant_address : Mapped[str] = mapped_column(ForeignKey("merchant_address.id"),unique=True)
    delivery_date : Mapped[date] = mapped_column(nullable=True)
    request_id : Mapped[str]
    article_id : Mapped[str]
    amount : Mapped[str] = mapped_column(nullable=True)
    payment_url : Mapped[str] 
    refernce_id : Mapped[str] 
    pickup_date : Mapped[date]
    remark : Mapped[str] = mapped_column(nullable= True)
    pincode_available_for_delivery : Mapped[str] = mapped_column(nullable=True)
    base_tariff : Mapped[float]
    pickup_charges : Mapped[float]
    total_tariff : Mapped[float]
    label_url : Mapped[str]
    reorder_for_qr : Mapped[str] = mapped_column(ForeignKey("qr_order.id"),nullable=True)

class Merchant(Base):
    __tablename__="merchant"

    id : Mapped[str] = mapped_column(primary_key=True)
    name : Mapped[str] 
    phone : Mapped[str]
    bussiness_type : Mapped[str] = mapped_column(nullable=True)
    bussiness_catagory : Mapped[str] = mapped_column(nullable=True)
    email : Mapped[str] = mapped_column(nullable=True)
    checkout_page_link : Mapped[str]
    status : Mapped[str] = mapped_column(nullable=True)
    onboarding_type : Mapped[str] = mapped_column(nullable=True)
    imei_number : Mapped[str]
    digital_qr_code : Mapped[str] = mapped_column(nullable=True)
    annual_turnover : Mapped[float]
    external_upi : Mapped[str]
    dob : Mapped[date]
    gender : Mapped[str]
    rrn : Mapped[str]
    uri : Mapped[str]

class MerchantPartnerService(Base):
    __tablename__="merchant_partner_service"

    id : Mapped[str] = mapped_column(primary_key=True)
    merchant : Mapped[str] = mapped_column(ForeignKey("merchant.id"),unique=True)
    partner : Mapped[str] = mapped_column(ForeignKey("partner.id"))
    service : Mapped[str] = mapped_column(ForeignKey("service.id"))
    status : Mapped[str] = mapped_column(nullable=True)

class BankAccount(Base):
    __tablename__="bank_account"

    id : Mapped[str] = mapped_column(primary_key=True)
    account_number : Mapped[str]
    account_type : Mapped[str] = mapped_column(nullable=True)
    ifsc_code : Mapped[str]
    name_on_bank : Mapped[str]
    bank_name : Mapped[str]
    branch_name : Mapped[str]
    verified_by_partner : Mapped[str] = mapped_column(nullable=True)

class UPI(Base):
    __tablename__= "upi"

    id : Mapped[str] = mapped_column(primary_key=True)
    upi_id : Mapped[str]
    name_on_bank : Mapped[str]
    verified_by_partner : Mapped[str] = mapped_column(nullable=True)
    verification_initiated_by_partner : Mapped[str] = mapped_column(nullable=True)

class MerchantBankAccount(Base):
    __tablename__ = "merchant_bank_account"

    id : Mapped[str] = mapped_column(primary_key=True)
    bank_account : Mapped[str] = mapped_column(ForeignKey("bank_account.id"),unique=True)
    merchant : Mapped[str] = mapped_column(ForeignKey("merchant.id"),unique=True)
    is_primary : Mapped[bool] = mapped_column(nullable=True)

class TransactionLog(Base):
    __tablename__ = "transaction_log"

    id : Mapped[str] = mapped_column(primary_key=True)
    entity_type : Mapped[str] = mapped_column(nullable=True)
    entity_id : Mapped[str]
    action : Mapped[str] = mapped_column(nullable=True)
    timestamp : Mapped[datetime] = mapped_column(default=datetime.now())

class NewCol(Base):
    __tablename__ = "temp"

    id : Mapped[str] = mapped_column(primary_key=True)
    entity_id : Mapped[str]
