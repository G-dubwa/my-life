from django.contrib import admin

# Register your models here.
from .models import Priority, Element, Aspect, User,Entity_Amount,Entity_Aspect,Financial_Entity,Event

#from django.contrib.auth.admin import UserAdmin

admin.site.register(User)
admin.site.register(Entity_Amount)
admin.site.register(Entity_Aspect)
admin.site.register(Financial_Entity)
admin.site.register(Event)
'''admin.site.register(Priority)
admin.site.register(Element)
admin.site.register(Aspect)'''

class AspectInline(admin.TabularInline):
    model = Aspect
    extra = 1

class ElementInline(admin.TabularInline):
    model = Element
    extra = 1
    

class PriorityAdmin(admin.ModelAdmin):
    
    inlines = [ElementInline]
    list_display  = ('priority_name','description')

class ElementAdmin(admin.ModelAdmin):
    
    inlines = [AspectInline]
    list_display  = ('element_name','description')

admin.site.register(Element, ElementAdmin)
admin.site.register(Priority, PriorityAdmin)
