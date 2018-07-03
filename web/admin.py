from django.contrib import admin
from .models import *
# Register your models here.
import xadmin
from xadmin import views
xadmin.site.register(QuestionAnswer, QuestionAnswerAdmin)
from .models import *

# 全局修改，固定写法
class GlobalSettings(object):
    # 修改title
    site_title = 'KING后台管理界面'
    # 修改footer
    site_footer = '山东科技大学 “国服路人王"团队'
    # 收起菜单
    menu_style = 'accordion'

    # def get_site_menu(self):
    #     return [{
    #         'title': u'用户&账户', 'perm': self.get_model_perm(QuestionAnswer, 'view'),
    #         'icon': 'fa fa-users',
    #         'menus': (
    #             {'title': u'用户', 'url': self.get_model_url(QuestionAnswer, 'changelist')},
    #             # {'title': u'账户', 'url': self.get_model_url(QuestionAnswer, 'changelist'),
    #             #  'perm': self.get_model_perm(QuestionAnswer, 'view'), },
    #             # {'title': u'用户套餐', 'url': self.get_model_url(QuestionAnswer, 'changelist'),
    #             #  'perm': self.get_model_perm(QuestionAnswer, 'view'), },
    #
    #         )
    #     },
    #     ]



# 将title和footer信息进行注册
xadmin.site.register(views.CommAdminView,GlobalSettings)