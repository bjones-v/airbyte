#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
#


from abc import ABC
from typing import Any, Iterable, List, Mapping, MutableMapping, Optional, Tuple

import requests
import xmltodict
from airbyte_cdk.sources import AbstractSource
from airbyte_cdk.sources.streams import Stream
from airbyte_cdk.sources.streams.http import HttpStream
from airbyte_cdk.sources.streams.http.auth import TokenAuthenticator

class BambooHrStream(HttpStream, ABC):
    def __init__(self, config: Mapping[str, Any]) -> None:
        self.config = config
        super().__init__(authenticator=config["authenticator"])

    @property
    def url_base(self) -> str:
        return f"https://api.bamboohr.com/api/gateway.php/{self.config['subdomain']}/v1/"

    def request_headers(
        self, stream_state: Mapping[str, Any], stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
    ) -> Mapping[str, Any]:
        return {"Accept": "application/json"}

    def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
        """
        BambooHR does not support pagination.
        """
        pass


# class MetaFieldsStream(BambooHrStream):
#     primary_key = None

#     def path(self, **kwargs) -> str:
#         return "meta/fields"

#     def parse_response(self, response: requests.Response, **kwargs) -> Iterable[Mapping]:
#         yield from response.json()


# class EmployeesDirectoryStream(BambooHrStream):
#     primary_key = "id"

#     def parse_response(self, response: requests.Response, **kwargs) -> Iterable[Mapping]:
#         yield from response.json()["employees"]

#     def path(self, **kwargs) -> str:
#         return "employees/directory"
    
class EmploymentStatusStream(BambooHrCustomStream):
    primary_key = none

    def parse_response(self, response: requests.Response, **kwargs) -> Iterable[Mapping]:
        yield from json.dumps(xmltodict.parse(response.text))["employee"]

    def path(self, **kwargs) -> str:
        return "employees/changed/tables/employmentStatus?since=2020-02-01T00%3A00%3A00%2B0000"

class CompensationStream(BambooHrCustomStream):
    primary_key = none

    def parse_response(self, response: requests.Response, **kwargs) -> Iterable[Mapping]:
        yield from json.dumps(xmltodict.parse(response.text))["employee"]

    def path(self, **kwargs) -> str:
        return "employees/changed/tables/compensation?since=2020-02-01T00%3A00%3A00%2B0000"
    
class JobInfoStream(BambooHrCustomStream):
    primary_key = none

    def parse_response(self, response: requests.Response, **kwargs) -> Iterable[Mapping]:
        yield from json.dumps(xmltodict.parse(response.text))["employee"]

    def path(self, **kwargs) -> str:
        return "employees/changed/tables/jobInfo?since=2020-02-01T00%3A00%3A00%2B0000"

class CustomJobRequisition(BambooHrCustomStream):
    primary_key = none

    def parse_response(self, response: requests.Response, **kwargs) -> Iterable[Mapping]:
        yield from json.dumps(xmltodict.parse(response.text))["employee"]

    def path(self, **kwargs) -> str:
        return "employees/changed/tables/customJobRequisition?since=2020-02-01T00%3A00%3A00%2B0000"
    
class SourceBambooHrCustom(AbstractSource):
    @staticmethod
    def _get_authenticator(api_key):
        """
        Returns a TokenAuthenticator.

        The API token is concatenated with `:x` and the resulting string is base-64 encoded.
        See https://documentation.bamboohr.com/docs#authentication
        """
        return TokenAuthenticator(token=base64.b64encode(f"{api_key}:x".encode("utf-8")).decode("utf-8"), auth_method="Basic")

    @staticmethod
    def add_authenticator_to_config(config: Mapping[str, Any]) -> Mapping[str, Any]:
        """
        Adds an authenticator entry to the config and returns the config.
        """
        config["authenticator"] = SourceBambooHrCustom._get_authenticator(config["api_key"])
        return config

    def check_connection(self, logger: logging.Logger, config: Mapping[str, Any]) -> Tuple[bool, Optional[Any]]:
        """
        Verifies the config and attempts to fetch the fields from the meta/fields endpoint.
        """
        config = SourceBambooHrCustom.add_authenticator_to_config(config)

        return True

        # if not config.get("custom_reports_fields") and not config.get("custom_reports_include_default_fields"):
        #     return False, NullFieldsError()

        # available_fields = MetaFieldsStream(config).read_records(sync_mode=SyncMode.full_refresh)
        # custom_fields = convert_custom_reports_fields_to_list(config.get("custom_reports_fields", ""))
        # denied_fields = validate_custom_fields(custom_fields, available_fields)

        # if denied_fields:
        #     return False, CustomFieldsAccessDeniedError(denied_fields)

        # try:
        #     next(available_fields)
        #     return True, None
        # except StopIteration:
        #     return False, AvailableFieldsAccessDeniedError()

    # def streams(self, config: Mapping[str, Any]) -> List[Stream]:
    #     config = SourceBambooHrCustom.add_authenticator_to_config(config)
    #     return [
    #         CustomReportsStream(config),
    #     ]



"""
# TODO: Most comments in this class are instructive and should be deleted after the source is implemented.

This file provides a stubbed example of how to use the Airbyte CDK to develop both a source connector which supports full refresh or and an
incremental syncs from an HTTP API.

The various TODOs are both implementation hints and steps - fulfilling all the TODOs should be sufficient to implement one basic and one incremental
stream from a source. This pattern is the same one used by Airbyte internally to implement connectors.

The approach here is not authoritative, and devs are free to use their own judgement.

There are additional required TODOs in the files within the integration_tests folder and the spec.yaml file.
"""


# # Basic full refresh stream
# class BambooHrCustomStream(HttpStream, ABC):
#     def __init__(self, config: Mapping[str, Any]) -> None:
#         self.config = config
#         super().__init__(authenticator=config["authenticator"])

#     @property
#     def url_base(self) -> str:
#         return f"https://api.bamboohr.com/api/gateway.php/{self.config['subdomain']}/v1/"

#     # def request_headers(
#     #     self, stream_state: Mapping[str, Any], stream_slice: Mapping[str, Any] = None, next_page_token: Mapping[str, Any] = None
#     # ) -> Mapping[str, Any]:
#     #     return {"Accept": "application/json"}

#     def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
#         """
#         BambooHR does not support pagination.
#         """
#         pass



"""
    TODO remove this comment

    This class represents a stream output by the connector.
    This is an abstract base class meant to contain all the common functionality at the API level e.g: the API base URL, pagination strategy,
    parsing responses etc..

    Each stream should extend this class (or another abstract subclass of it) to specify behavior unique to that stream.

    Typically for REST APIs each stream corresponds to a resource in the API. For example if the API
    contains the endpoints
        - GET v1/customers
        - GET v1/employees

    then you should have three classes:
    `class BambooHrCustomStream(HttpStream, ABC)` which is the current class
    `class Customers(BambooHrCustomStream)` contains behavior to pull data for customers using v1/customers
    `class Employees(BambooHrCustomStream)` contains behavior to pull data for employees using v1/employees

    If some streams implement incremental sync, it is typical to create another class
    `class IncrementalBambooHrCustomStream((BambooHrCustomStream), ABC)` then have concrete stream implementations extend it. An example
    is provided below.

    See the reference docs for the full list of configurable options.
    """

    # # TODO: Fill in the url base. Required.
    # url_base = f"https://api.bamboohr.com/api/gateway.php/{self.config['subdomain']}/v1/"

    # def next_page_token(self, response: requests.Response) -> Optional[Mapping[str, Any]]:
    #     """
    #     TODO: Override this method to define a pagination strategy. If you will not be using pagination, no action is required - just return None.

    #     This method should return a Mapping (e.g: dict) containing whatever information required to make paginated requests. This dict is passed
    #     to most other methods in this class to help you form headers, request bodies, query params, etc..

    #     For example, if the API accepts a 'page' parameter to determine which page of the result to return, and a response from the API contains a
    #     'page' number, then this method should probably return a dict {'page': response.json()['page'] + 1} to increment the page count by 1.
    #     The request_params method should then read the input next_page_token and set the 'page' param to next_page_token['page'].

    #     :param response: the most recent response from the API
    #     :return If there is another page in the result, a mapping (e.g: dict) containing information needed to query the next page in the response.
    #             If there are no more pages in the result, return None.
    #     """
    #     return None

    # def request_params(
    #     self, stream_state: Mapping[str, Any], stream_slice: Mapping[str, any] = None, next_page_token: Mapping[str, Any] = None
    # ) -> MutableMapping[str, Any]:
    #     """
    #     TODO: Override this method to define any query parameters to be set. Remove this method if you don't need to define request params.
    #     Usually contains common params e.g. pagination size etc.
    #     """
    #     return {}

    # def parse_response(self, response: requests.Response, **kwargs) -> Iterable[Mapping]:
    #     """
    #     TODO: Override this method to define how a response is parsed.
    #     :return an iterable containing each record in the response
    #     """
    #     yield {}



# # Basic incremental stream
# class IncrementalBambooHrCustomStream(BambooHrCustomStream, ABC):
#     """
#     TODO fill in details of this class to implement functionality related to incremental syncs for your connector.
#          if you do not need to implement incremental sync for any streams, remove this class.
#     """

#     # TODO: Fill in to checkpoint stream reads after N records. This prevents re-reading of data if the stream fails for any reason.
#     state_checkpoint_interval = None

#     @property
#     def cursor_field(self) -> str:
#         """
#         TODO
#         Override to return the cursor field used by this stream e.g: an API entity might always use created_at as the cursor field. This is
#         usually id or date based. This field's presence tells the framework this in an incremental stream. Required for incremental.

#         :return str: The name of the cursor field.
#         """
#         return []

#     def get_updated_state(self, current_stream_state: MutableMapping[str, Any], latest_record: Mapping[str, Any]) -> Mapping[str, Any]:
#         """
#         Override to determine the latest state after reading the latest record. This typically compared the cursor_field from the latest record and
#         the current state and picks the 'most' recent cursor. This is how a stream's state is determined. Required for incremental.
#         """
#         return {}


# class Employees(IncrementalBambooHrCustomStream):
#     """
#     TODO: Change class name to match the table/data source this stream corresponds to.
#     """

#     # TODO: Fill in the cursor_field. Required.
#     cursor_field = "start_date"

#     # TODO: Fill in the primary key. Required. This is usually a unique field in the stream, like an ID or a timestamp.
#     primary_key = "employee_id"

#     def path(self, **kwargs) -> str:
#         """
#         TODO: Override this method to define the path this stream corresponds to. E.g. if the url is https://example-api.com/v1/employees then this should
#         return "single". Required.
#         """
#         return "employees"

#     def stream_slices(self, stream_state: Mapping[str, Any] = None, **kwargs) -> Iterable[Optional[Mapping[str, any]]]:
#         """
#         TODO: Optionally override this method to define this stream's slices. If slicing is not needed, delete this method.

#         Slices control when state is saved. Specifically, state is saved after a slice has been fully read.
#         This is useful if the API offers reads by groups or filters, and can be paired with the state object to make reads efficient. See the "concepts"
#         section of the docs for more information.

#         The function is called before reading any records in a stream. It returns an Iterable of dicts, each containing the
#         necessary data to craft a request for a slice. The stream state is usually referenced to determine what slices need to be created.
#         This means that data in a slice is usually closely related to a stream's cursor_field and stream_state.

#         An HTTP request is made for each returned slice. The same slice can be accessed in the path, request_params and request_header functions to help
#         craft that specific request.

#         For example, if https://example-api.com/v1/employees offers a date query params that returns data for that particular day, one way to implement
#         this would be to consult the stream state object for the last synced date, then return a slice containing each date from the last synced date
#         till now. The request_params function would then grab the date from the stream_slice and make it part of the request by injecting it into
#         the date query param.
#         """
#         raise NotImplementedError("Implement stream slices or delete this method!")

# class SourceBambooHrCustom(AbstractSource):
    # @staticmethod
    # def _get_authenticator(api_key):
    #     """
    #     Returns a TokenAuthenticator.

    #     The API token is concatenated with `:x` and the resulting string is base-64 encoded.
    #     See https://documentation.bamboohr.com/docs#authentication
    #     """
    #     return TokenAuthenticator(token=base64.b64encode(f"{api_key}:x".encode("utf-8")).decode("utf-8"), auth_method="Basic")

    # @staticmethod
    # def add_authenticator_to_config(config: Mapping[str, Any]) -> Mapping[str, Any]:
    #     """
    #     Adds an authenticator entry to the config and returns the config.
    #     """
    #     config["authenticator"] = SourceBambooHrCustom._get_authenticator(config["api_key"])
    #     return config

    # def check_connection(self, logger: logging.Logger, config: Mapping[str, Any]) -> Tuple[bool, Optional[Any]]:
    #     """
    #     Verifies the config and attempts to fetch the fields from the meta/fields endpoint.
    #     """
    #     config = SourceBambooHrCustom.add_authenticator_to_config(config)

    #     if not config.get("custom_reports_fields") and not config.get("custom_reports_include_default_fields"):
    #         return False, NullFieldsError()

    #     available_fields = MetaFieldsStream(config).read_records(sync_mode=SyncMode.full_refresh)
    #     custom_fields = convert_custom_reports_fields_to_list(config.get("custom_reports_fields", ""))
    #     denied_fields = validate_custom_fields(custom_fields, available_fields)

    #     if denied_fields:
    #         return False, CustomFieldsAccessDeniedError(denied_fields)

    #     try:
    #         next(available_fields)
    #         return True, None
    #     except StopIteration:
    #         return False, AvailableFieldsAccessDeniedError()

    # def streams(self, config: Mapping[str, Any]) -> List[Stream]:
    #     config = SourceBambooHrCustom.add_authenticator_to_config(config)
    #     return [
    #         EmploymentStatusStream(config),
    #         CompensationStream(config),
    #         JobInfoStream(config),
    #         CustomJobRequisition(config),
    #     ]

# Source
# class SourceBambooHrCustom(AbstractSource):
#     def check_connection(self, logger, config) -> Tuple[bool, any]:
#         return True, None
#         """
#         TODO: Implement a connection check to validate that the user-provided config can be used to connect to the underlying API

#         See https://github.com/airbytehq/airbyte/blob/master/airbyte-integrations/connectors/source-stripe/source_stripe/source.py#L232
#         for an example.

#         :param config:  the user-input config object conforming to the connector's spec.yaml
#         :param logger:  logger object
#         :return Tuple[bool, any]: (True, None) if the input config can be used to connect to the API successfully, (False, error) otherwise.
#         """
#         return True, None

#     def streams(self, config: Mapping[str, Any]) -> List[Stream]:
#         """
#         TODO: Replace the streams below with your own streams.

#         :param config: A Mapping of the user input configuration as defined in the connector spec.
#         """
#         # TODO remove the authenticator if not required.
#         auth = TokenAuthenticator(token="api_key")  # Oauth2Authenticator is also available if you need oauth support
#         return [Customers(authenticator=auth), Employees(authenticator=auth)]
