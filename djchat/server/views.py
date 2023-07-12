from django.db.models import Count
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError, AuthenticationFailed

from .serializer import ServerSerializer
from rest_framework.response import Response
from .models import Server


class ServerListViewSet(viewsets.ViewSet):
    """
    A view set for listing servers based on various filters.
    """

    queryset = Server.objects.all()

    def list(self, request):
        """
        Retrieve a list of servers based on the provided filters.

        Args:
            request: The HTTP request object.

        Returns:
            Response: The HTTP response object containing the serialized server data.
        """

        # Retrieve query parameters
        category = request.query_params.get("category")
        qty = request.query_params.get("qty")
        by_user = request.query_params.get("by_user") == "true"
        by_serverid = request.query_params.get("by_serverid")
        with_num_members = request.query_params.get("with_num_members") == "true"

        # Check if user authentication is required
        if by_user and not request.user.is_authenticated:
            raise AuthenticationFailed()

        # Filter servers by category
        if category:
            self.queryset = self.queryset.filter(category__name=category)

        # Filter servers by user
        if by_user:
            user_id = request.user.id
            self.queryset = self.queryset.filter(member=user_id)

        # Annotate servers with the number of members
        if with_num_members:
            self.queryset = self.queryset.annotate(num_members=Count("member"))

        # Filter server by server ID
        if by_serverid:
            try:
                self.queryset = self.queryset.filter(id=by_serverid)
                if not self.queryset.exists():
                    raise ValidationError(detail=f"Server with id {by_serverid} not found")
            except ValueError:
                raise ValidationError(detail=f"Server value error")

        # Limit the number of results by quantity
        if qty:
            self.queryset = self.queryset[:int(qty)]

        # Serialize the server data
        serializer = ServerSerializer(self.queryset, many=True, context={"num_members": with_num_members})

        # Return the serialized server data as a response
        return Response(serializer.data)
