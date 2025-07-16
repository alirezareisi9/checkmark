from rest_framework.viewsets import ModelViewSet

class DetailModelViewSet(ModelViewSet) :
    details_serializer_class = None

    def get_serializer_class(self):
        if self.action != 'list' and self.details_serializer_class is not None:
            return self.details_serializer_class

        return super().get_serializer_class()