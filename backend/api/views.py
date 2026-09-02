from rest_framework.generics import ListAPIView
from rest_framework import viewsets
from .models import Listing
from .serializers import ListingSerializer


class ListingListView(ListAPIView):
    serializer_class = ListingSerializer

    def get_queryset(self):
        status = self.request.query_params.get("status", "Active")

        queryset = Listing.objects.all()

        if status.lower() == "active":
            queryset = queryset.filter(status="Active")

        elif status.lower() == "inactive":
            queryset = queryset.filter(status="Inactive")

        elif status.lower() == "all":
            pass

        return queryset.order_by("-date_posted")


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all().order_by("-date_posted")
    serializer_class = ListingSerializer

