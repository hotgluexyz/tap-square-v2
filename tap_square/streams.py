"""Stream type classes for tap-square."""

from __future__ import annotations

from pathlib import Path

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_square.client import squareStream

# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")
# TODO: - Override `UsersStream` and `GroupsStream` with your own stream definition.
#       - Copy-paste as many times as needed to create multiple stream types.

address_type = th.ObjectType(
                        th.Property('address_line_1', th.StringType),
                        th.Property('address_line_2', th.StringType),
                        th.Property('address_line_3',th.StringType),
                        th.Property('locality',th.StringType),
                        th.Property('sublocality',th.StringType),
                        th.Property('sublocality_2',th.StringType),
                        th.Property('sublocality_3',th.StringType),
                        th.Property('administrative_district_level_1',th.StringType),
                        th.Property('administrative_district_level_2',th.StringType),
                        th.Property('administrative_district_level_3',th.StringType),
                        th.Property('postal_code',th.StringType),
                        th.Property('country',th.StringType),
                        th.Property('first_name',th.StringType),
                        th.Property('last_name',th.StringType),
                    )

money_type = th.ObjectType(
        th.Property('amount',th.IntegerType),
        th.Property('currency',th.StringType),
    )

class PaymentsStream(squareStream):
    name = 'payments'
    path = '/v2/payments'
    primary_keys = ["id"]
    records_jsonpath = "$.payments[*]"
    replication_key = "created_at"

    schema = th.PropertiesList(
       th.Property('id',th.StringType),
       th.Property('created_at',th.DateTimeType),
       th.Property('updated_at',th.DateTimeType),
       th.Property('amount_money',money_type),
       th.Property('tip_money',money_type),
       th.Property('total_money',money_type),
       th.Property('app_fee_money',money_type),
       th.Property('approved_money',money_type),
       th.Property(
            'processing_fee',
            th.ObjectType(
                th.Property('effective_at',th.DateTimeType),
                th.Property('type',th.StringType),
                th.Property('amount_money',money_type)
            )
       ),
       th.Property('refunded_money',money_type),
       th.Property('status',th.StringType),
       th.Property('delay_duration',th.StringType),
       th.Property('delay_action',th.StringType),
       th.Property('delayed_until',th.StringType),
       th.Property('source_type',th.StringType),
       th.Property(
            'card_details',
            th.ObjectType(
                th.Property('status',th.StringType),
                th.Property(
                    'card',
                    th.ObjectType(
                        th.Property('card_brand',th.StringType),
                        th.Property('last_4',th.StringType),
                        th.Property('exp_month',th.StringType),
                        th.Property('exp_year',th.StringType),
                        th.Property('cardholder_name',th.StringType),
                        th.Property('billing_address',address_type),
                        th.Property('fingerprint',th.StringType),
                        th.Property('customer_id',th.StringType),
                        th.Property('merchant_id',th.StringType),
                        th.Property('reference_id',th.StringType),
                        th.Property('card_type',th.StringType),
                        th.Property('prepaid_type',th.StringType),
                        th.Property('bin',th.StringType),
                        th.Property('version',th.StringType),
                        th.Property('card_co_brand',th.StringType),
                    )
                ),
                th.Property('entry_method',th.StringType),
                th.Property('cvv_status',th.StringType),
                th.Property('avs_status',th.StringType),
                th.Property('auth_result_code',th.StringType),
                th.Property('application_identifier',th.StringType),
                th.Property('application_cryptogram',th.StringType),
                th.Property('verification_method',th.StringType),
                th.Property('verification_results',th.StringType),
                th.Property('statement_description',th.StringType),
                th.Property(
                    'card_payment_timeline',
                    th.ObjectType(
                        th.Property('authorized_at',th.DateTimeType),
                        th.Property('captured_at',th.DateTimeType),
                        th.Property('voided_at',th.DateTimeType),        
                    )
                ),
                th.Property('refund_requires_card_presence',th.BooleanType)
            ),
       ),
       th.Property(
            'cash_details',
            th.ObjectType(
                th.Property('buyer_supplied_money',money_type),
                th.Property('change_back_money',money_type),
            )
        ),
        th.Property(
            'bank_account_details',
            th.ObjectType(
                th.Property('bank_name',th.StringType),
                th.Property('transfer_type',th.StringType),
                th.Property('account_owernship_type',th.StringType),
                th.Property('fingerprint',th.StringType),
                th.Property('country',th.StringType),
                th.Property('statement_description',th.StringType),
                th.Property(
                    'ach_details',
                    th.ObjectType(
                        th.Property('routing_number',th.StringType),
                        th.Property('account_number_suffix',th.StringType),
                        th.Property('account_type',th.StringType),
                    )
                )

            )
        ),
        th.Property(
            'external_details',
            th.ObjectType(
                th.Property('type',th.StringType),
                th.Property('source',th.StringType),
                th.Property('source_id',th.StringType),
                th.Property('source_fee_money',money_type)
            )
        ),
        th.Property(
            'wallet_details',
            th.ObjectType( 
                th.Property('status',th.StringType),
                th.Property('brand',th.StringType),
                th.Property(
                    'cash_app_details',
                    th.ObjectType(
                        th.Property('buyer_full_name',th.StringType),
                        th.Property('buyer_country_code',th.StringType),
                        th.Property('buyer_cashtag',th.StringType)
                    )
                ),
            )
        ),
        th.Property(
            'buy_now_pay_later_details',
            th.ObjectType(
                th.Property('brand', th.StringType),
                th.Property(
                    'after_pay_details',
                    th.ObjectType(
                        th.Property('email_address',th.StringType)
                    )
                ),
                th.Property(
                    'clearpay_details',
                    th.ObjectType(
                        th.Property('email_address',th.StringType)
                    )
                )
            )

        ),
        th.Property('location_id',th.StringType),
        th.Property('order_id',th.StringType),
        th.Property('reference_id',th.StringType),
        th.Property('customer_id',th.StringType),
        th.Property('team_member_id',th.StringType),
        th.Property('refund_id',th.ArrayType(th.StringType)),
        th.Property('buyer_email_address', th.StringType),
        th.Property('billing_address',address_type),
        th.Property('shipping_address',address_type),
        th.Property('note',th.StringType),
        th.Property('capabilities',th.ArrayType(th.StringType)),
        th.Property('receipt_number',th.StringType),
        th.Property('receipt_url',th.StringType),
        th.Property(
            'device_details',
            th.ObjectType( 
                th.Property('device_id',th.StringType),
                th.Property('device_installation_id',th.StringType),
                th.Property('device_name',th.StringType),
            )
        ),
        th.Property(
            'application_details',
            th.ObjectType(
                th.Property('square_product',th.StringType),
                th.Property('application_id',th.StringType)
            )
        ),
        th.Property('version_token',th.StringType),
    ).to_dict()


class LocationsStream(squareStream):
    name = "locations"
    path = "/v2/locations"
    records_jsonpath="$.locations[*]"
    primary_keys=["id"]
    replication_key = None 
    

    schema = th.PropertiesList(
        th.Property('id',th.StringType),
        th.Property('name',th.StringType),
        th.Property('address',address_type),
        th.Property('timezone',th.StringType),
        th.Property('capabilities',th.ArrayType(th.StringType)),
        th.Property('status',th.StringType),
        th.Property('created_at',th.StringType),
        th.Property('merchant_id',th.StringType),
        th.Property('country',th.StringType),
        th.Property('language_code',th.StringType),
        th.Property('currency',th.StringType),
        th.Property('phone_number',th.StringType),
        th.Property('business_name',th.StringType),
        th.Property('type',th.StringType),
        th.Property('website_url',th.StringType),
        th.Property(
            'business_hours',
            th.ObjectType(
                th.Property('day_of_week',th.StringType),
                th.Property('start_local_time',th.StringType),
                th.Property('end_local_time',th.StringType),
            )
        ),
        th.Property('business_email',th.StringType),
        th.Property('description',th.StringType),
        th.Property('twitter_username',th.StringType),
        th.Property('instagram_username',th.StringType),
        th.Property('facebook_url',th.StringType),
        th.Property(
            'coordinates',
            th.ObjectType(
                th.Property('latitude',th.NumberType),
                th.Property('longitude',th.NumberType),
            )
        ),
        th.Property('logo_url',th.StringType),
        th.Property('pos_background_url',th.StringType),
        th.Property('mcc',th.StringType),
        th.Property('full_format_logo_url',th.StringType),
        th.Property(
            'tax_ids',
            th.ObjectType(
                th.Property('eu_vat',th.StringType),
                th.Property('fr_siret',th.StringType),
                th.Property('fr_naf',th.StringType),
                th.Property('es_nif',th.StringType),
            )
        ),
    ).to_dict()

    def get_child_context(self, record, context): 
        return { 
            "location": record["id"]
        }



class InvoicesStream(squareStream):
    name = 'invoices'
    parent_stream_type = LocationsStream
    path = "/v2/invoices?location_id={location}"
    ignore_parent_replication_keys = True
    replication_key = None
    primary_keys = ["id"] 
    records_jsonpath = "$.invoices[*]"

    schema = th.PropertiesList( 
        th.Property('id',th.StringType),
        th.Property('version', th.IntegerType),
        th.Property('location_id',th.StringType),
        th.Property('order_id',th.StringType),
        th.Property(
            'primary_recipient', 
            th.ObjectType(
                th.Property('customer_id',th.StringType),
                th.Property('given_name',th.StringType),
                th.Property('family_name',th.StringType),
                th.Property('email_address',th.StringType),
                th.Property('address', address_type), 
                th.Property('phone_number',th.StringType),
                th.Property('company_name',th.StringType),
                th.Property(
                    'tax_ids',
                    th.ArrayType(th.StringType)
                ),
            )
        ),
        th.Property(
            'payment_requests', th.ArrayType(
                th.ObjectType(
                    th.Property('request_type',th.StringType),
                    th.Property('due_date',th.DateTimeType),
                    th.Property('fixed_amount_requested_money',money_type),
                    th.Property('percentage_required',th.StringType),
                    th.Property('tipping_enabled',th.BooleanType),
                    th.Property('automatic_payment_source',th.StringType),
                    th.Property('card_id',th.StringType),
                    th.Property(
                        'reminders',
                        th.ArrayType(
                            th.ObjectType(
                                th.Property('uid',th.StringType),
                                th.Property('relative_scheduled_days',th.IntegerType),
                                th.Property('message',th.StringType),
                                th.Property('status',th.StringType),
                                th.Property('sent_at',th.DateTimeType),
                            )
                        )
                    ),
                    th.Property('computed_amount_money',money_type),
                    th.Property('total_completed_amount_money',money_type),
                    th.Property('rounding_adjustment_included_money',money_type),
                )
            )
        ),
        th.Property('delivery_method',th.StringType),
        th.Property('invoice_number',th.StringType),
        th.Property('title',th.StringType),
        th.Property('description',th.StringType),
        th.Property('scheduled_at',th.StringType),
        th.Property('public_url',th.StringType),
        th.Property('next_payment_amount_money',money_type),
        th.Property('status',th.StringType),
        th.Property('timezone',th.StringType),
        th.Property('created_at',th.DateTimeType),
        th.Property('updated_at',th.DateTimeType),
        th.Property(
            'accepted_payment_methods',
            th.ObjectType(
                th.Property('card',th.BooleanType),
                th.Property('square_gift_card',th.BooleanType),
                th.Property('bank_account',th.BooleanType),
                th.Property('buy_now_pay_later',th.BooleanType),
            
            )
        ),
        th.Property(
            'custom_fields',
            th.ArrayType(
                th.ObjectType( 
                    th.Property('label',th.StringType),
                    th.Property('value',th.StringType),
                    th.Property('placement',th.StringType),
                )
            )
        ),
        th.Property('subscription_id',th.StringType),
        th.Property('sale_or_service_date',th.DateTimeType),
        th.Property('payment_conditions',th.StringType),
        th.Property('store_payment_method_enabled',th.BooleanType),
    ).to_dict()
    

class SubscriptionsStream(squareStream):
    # TODO: add buyer_self_management / notes?
    name = 'subscriptions'
    path = f'/v2/subscriptions/search'
    replication_key = None
    primary_keys = ["id"] 
    records_jsonpath = "$.subscriptions[*]"
    
    rest_method = 'POST'

    schema = th.PropertiesList(
        th.Property('id',th.StringType),
        th.Property('location_id',th.StringType),
        th.Property('plan_id',th.StringType),
        th.Property('customer_id',th.StringType),
        th.Property('start_date',th.DateTimeType),
        th.Property('canceled_date',th.DateTimeType),
        th.Property('charged_through_date',th.DateTimeType),
        th.Property('status',th.StringType),
        th.Property('tax_percentage',th.StringType),
        th.Property('invoice_ids',th.ArrayType(th.StringType)),
        th.Property('price_override_money',money_type),
        th.Property('version',th.IntegerType),
        th.Property('created_at',th.DateTimeType),
        th.Property('card_id',th.StringType),
        th.Property('paid_until_date',th.StringType),
        th.Property('timezone',th.DateTimeType),
        th.Property(
            'source',
            th.ObjectType(
                th.Property('name',th.StringType)
            )
        ),
    ).to_dict()