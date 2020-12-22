from rest_framework import routers

from projects.views import (
    ProjectViewset,
    PositionViewset,
    ProjectDocumentViewset,
    PositionDocumentViewset
)


router = routers.DefaultRouter()

router.register('projects', ProjectViewset)
router.register('positions', PositionViewset)
router.register('project_documents', ProjectDocumentViewset, basename='project_documents')
router.register('position_documents', PositionDocumentViewset, basename='position_documents')


urlpatterns = router.urls
