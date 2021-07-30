from django.contrib import admin
from django.contrib.auth.models import Permission
from django.utils.html import mark_safe
from django import forms
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class TourInline(admin.StackedInline):
    model = Tour
    pk_name = 'city'
    extra = 1

class SeatInline(admin.StackedInline):
    model = Seat
    pk_name = 'tour'
    max_num = 2

class TagInline(admin.StackedInline):
    model = Tag.tour.through

class CityAdmin(admin.ModelAdmin):
    inlines = [TourInline, ]
    list_display = ['id', 'name']
    search_fields = ['name']
    list_filter = ['name', 'tours__name']

class TourForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Tour
        fields = '__all__'

class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name', 'tour']
    list_filter = ['name', 'tour']

class TourAdmin(admin.ModelAdmin):
    inlines = [SeatInline, TagInline, ]
    form = TourForm
    list_display = ['id', 'name', 'city', 'datetime', 'available']
    search_fields = ['name', 'city__name']
    list_filter = ['name', 'city__name', 'available']
    readonly_fields = ['picture']

    def picture(self, Tour):
        return mark_safe("<img src='/static/{url}' alt={alt} width='120'/>"
                         .format(url=Tour.image.name, alt=Tour.name))

class SeatAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'tour']
    search_fields = ['price', 'tour__name']
    list_filter = ['name', 'tour__name']

class QldlAppAdminSite(admin.AdminSite):
    site_header = "QUẢN LÍ DU LỊCH"

admin_site = QldlAppAdminSite('myqldl')

admin_site.register(City, CityAdmin)
admin_site.register(Tour, TourAdmin)
admin_site.register(Seat, SeatAdmin)
admin_site.register(Tag, TagAdmin)
admin_site.register(User)
admin_site.register(Permission)
