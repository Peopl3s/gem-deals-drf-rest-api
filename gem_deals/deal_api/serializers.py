from rest_framework import serializers

from .models import Gem


class GemSerializer(serializers.ModelSerializer):
    """Сериализатор драгоценных камней."""

    class Meta:
        model = Gem
        fields = ["name"]


class CustomerSerializer(serializers.Serializer):
    """Сериализатор Клиентов с дополнительной информацией
    (количество потраченных денег и список драгоценностей).
    """

    username = serializers.CharField(max_length=255, source="customer__username")
    spent_money = serializers.IntegerField()
    gems = serializers.ListField(child=serializers.CharField(), allow_empty=True)


# Если нужно, чтобы каждая драгоценность отправлялась объектом
# gems = serializers.ListField(child=GemSerializer(), allow_empty=True)
#  "gems": [
#             {
#                 "name": "Сапфир"
#             },
#             {
#                 "name": "Рубин"
#             },
#             {
#                 "name": "Танзанит"
#             }
#         ]
