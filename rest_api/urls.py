from rest_framework import routers
from rest_api.views import *

router = routers.DefaultRouter()

router.register(r'questionanswer', QuestionAnswerViews, base_name='api-questionanswer')
router.register(r'bank', BankViews, base_name='api-bank')
router.register(r'question', QuestionSearchViews, base_name='api-question-search')

api_patterns = []
api_patterns += router.urls