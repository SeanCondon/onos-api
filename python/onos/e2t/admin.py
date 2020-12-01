# Generated by the protocol buffer compiler.  DO NOT EDIT!
# sources: onos/e2t/admin/admin.proto
# plugin: python-betterproto
from dataclasses import dataclass
from typing import AsyncIterable, AsyncIterator, Iterable, List, Optional, Union

import betterproto
import grpclib


class E2NodeConnectionType(betterproto.Enum):
    """E2NodeConnectionType specifies the type of an E2 connection"""

    UNKNOWN = 0
    G_NB = 1
    E_NB = 2
    ENG_MB = 3
    NGE_NB = 4


@dataclass(eq=False, repr=False)
class UploadRegisterServiceModelRequest(betterproto.Message):
    """
    UploadRegisterServiceModelRequest is for streaming a model plugin file to
    the server. There is a built in limit in gRPC of 4MB - plugin is usually
    around 20MB so break in to chunks of approx 1-2MB.
    """

    # so_file is the name being streamed.
    so_file: str = betterproto.string_field(1)
    # content is the bytes content.
    content: bytes = betterproto.bytes_field(2)

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass(eq=False, repr=False)
class UploadRegisterServiceModelResponse(betterproto.Message):
    """
    UploadRegisterServiceModelResponse carries status of model plugin
    registration.
    """

    # name is name of the model plugin.
    name: str = betterproto.string_field(1)
    # version is the semantic version of the model plugin.
    version: str = betterproto.string_field(2)

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass(eq=False, repr=False)
class ListRegisteredServiceModelsResponse(betterproto.Message):
    """
    ListRegisteredServiceModelsResponse is general information about a service
    model plugin.
    """

    # name is the name given to the service model plugin - no spaces and title
    # case.
    name: str = betterproto.string_field(1)
    # version is the semantic version of the Plugin e.g. 1.0.0.
    version: str = betterproto.string_field(2)

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass(eq=False, repr=False)
class ListRegisteredServiceModelsRequest(betterproto.Message):
    """
    ListRegisteredServiceModelsRequest carries data for querying registered
    service model plugins.
    """

    # An optional filter on the name of the model plugins to list.
    model_name: str = betterproto.string_field(1)
    # An optional filter on the version of the model plugins to list
    model_version: str = betterproto.string_field(2)

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass(eq=False, repr=False)
class ListE2NodeConnectionsRequest(betterproto.Message):
    """
    ListE2NodeConnectionsRequest carries request for a list of E2 node SCTP
    connections.
    """

    pass

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass(eq=False, repr=False)
class ListE2NodeConnectionsResponse(betterproto.Message):
    """
    ListE2NodeConnectionsResponse carries information about the SCTP connection
    to the remote E2 node.
    """

    remote_ip: List[str] = betterproto.string_field(1)
    remote_port: int = betterproto.uint32_field(2)
    id: str = betterproto.string_field(3)
    plmn_id: str = betterproto.string_field(4)
    connection_type: "E2NodeConnectionType" = betterproto.enum_field(5)

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass(eq=False, repr=False)
class DropE2NodeConnectionsRequest(betterproto.Message):
    """DropE2NodeConnectionsRequest carries drop connection request"""

    connections: List["ListE2NodeConnectionsResponse"] = betterproto.message_field(1)

    def __post_init__(self) -> None:
        super().__post_init__()


@dataclass(eq=False, repr=False)
class DropE2NodeConnectionsResponse(betterproto.Message):
    """DropE2NodeConnectionsResponse carries drop connection response"""

    success: List[bool] = betterproto.bool_field(1)

    def __post_init__(self) -> None:
        super().__post_init__()


class E2TAdminServiceStub(betterproto.ServiceStub):
    """
    E2TAdminService provides means for enhanced interactions with the ONOS RIC
    E2 Termination service.
    """

    async def upload_register_service_model(
        self,
        request_iterator: Union[
            AsyncIterable["UploadRegisterServiceModelRequest"],
            Iterable["UploadRegisterServiceModelRequest"],
        ],
    ) -> "UploadRegisterServiceModelResponse":
        """
        UploadRegisterServiceModel uploads and adds the model plugin to the
        list of supported models. The file is serialized in to Chunks of less
        than 4MB so as not to break the gRPC byte array limit
        """

        return await self._stream_unary(
            "/onos.e2t.admin.E2TAdminService/UploadRegisterServiceModel",
            request_iterator,
            UploadRegisterServiceModelRequest,
            UploadRegisterServiceModelResponse,
        )

    async def list_registered_service_models(
        self, *, model_name: str = "", model_version: str = ""
    ) -> AsyncIterator["ListRegisteredServiceModelsResponse"]:
        """
        ListRegisteredServiceModels returns a stream of registered service
        models.
        """

        request = ListRegisteredServiceModelsRequest()
        request.model_name = model_name
        request.model_version = model_version

        async for response in self._unary_stream(
            "/onos.e2t.admin.E2TAdminService/ListRegisteredServiceModels",
            request,
            ListRegisteredServiceModelsResponse,
        ):
            yield response

    async def list_e2_node_connections(
        self,
    ) -> AsyncIterator["ListE2NodeConnectionsResponse"]:
        """
        ListE2NodeConnections returns a stream of existing SCTP connections.
        """

        request = ListE2NodeConnectionsRequest()

        async for response in self._unary_stream(
            "/onos.e2t.admin.E2TAdminService/ListE2NodeConnections",
            request,
            ListE2NodeConnectionsResponse,
        ):
            yield response

    async def drop_e2_node_connections(
        self, *, connections: Optional[List["ListE2NodeConnectionsResponse"]] = None
    ) -> "DropE2NodeConnectionsResponse":
        """
        DropE2NodeConnections drops the specified E2 node SCTP connections
        """

        connections = connections or []

        request = DropE2NodeConnectionsRequest()
        if connections is not None:
            request.connections = connections

        return await self._unary_unary(
            "/onos.e2t.admin.E2TAdminService/DropE2NodeConnections",
            request,
            DropE2NodeConnectionsResponse,
        )