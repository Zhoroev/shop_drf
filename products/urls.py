from rest_framework.routers import SimpleRouter

from products.views import ProductViewSet

router = SimpleRouter()

router.register('products', ProductViewSet)

urlpatterns = []

urlpatterns += router.urls