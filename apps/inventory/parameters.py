from drf_spectacular.utils import OpenApiParameter

PRODUCT_ID_PARAM = OpenApiParameter(
    name="product_id",
    type=int,
    location=OpenApiParameter.QUERY,
    required=True,
    description="Filter outlets by product availability",
)