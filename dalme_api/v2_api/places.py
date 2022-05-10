from rest_framework.decorators import action
from rest_framework.response import Response

from dalme_api import api
from dalme_app.models import Place


class Places(api.Places):
    """Endpoint for the Place resource."""

    # TODO: Make this generic on DALMEBaseViewSet.
    @action(detail=False, methods=['patch'])
    def inline_update(self, request, *args, **kwargs):
        pks = [str(pk) for pk in request.data.keys()]
        for pk in pks:
            obj = self.queryset.filter(pk=pk)
            obj_data = request.data[pk]

            # Update fields.
            # TODO: Temporary until sorting out api parser/renderer.
            from stringcase import snakecase
            fields = {
                snakecase(field): value for field, value in obj_data.items()
                if not isinstance(value, dict)
            }
            obj.update(**fields)

            # Update foreign keys.
            related = {
                snakecase(fk_field): value
                for fk_field, value in obj_data.items()
                if snakecase(fk_field) not in fields
            }
            for fk_field, value in related.items():
                RelatedModel = Place._meta.get_field(fk_field).rel.to
                instance = RelatedModel.objects.get(pk=value.id)
                obj.update(fk_field=instance)

        return Response({'message': f'Updated {len(pks)} rows.'}, 201)
