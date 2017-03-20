from django.contrib import admin

from core.models import User, ACompany, ASite


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'last_login')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-last_login',)
    readonly_fields = ('last_login',)


@admin.register(ACompany)
class ACompanyAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'link', 'max_score')
    list_filter = ('is_active',)
    search_fields = ('owner__email', 'title', 'text')
    readonly_fields = ('created', 'updated')


@admin.register(ASite)
class ASiteAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'link', 'owner')
    list_filter = ('is_active', 'topic')
    search_fields = ('owner__email', 'title')
    readonly_fields = ('created', 'updated')
