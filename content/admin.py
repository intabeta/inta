from django.contrib import admin
from content.models import InterestGroup, IgProposal, Entry, Logo, InterestEmail
from django.contrib.admin import DateFieldListFilter

class InterestGroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    
class IgProposalAdmin(admin.ModelAdmin):
    pass

class LogoAdmin(admin.ModelAdmin):
    pass

class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'domain', 'date_added', 'submitted_by')
    search_fields = ['title']
    list_filter = (
        ('date_added', DateFieldListFilter),
    )
    fields = ('title', 'url', 'slug', 'domain', 'summary', 'photo', 'score', 'tags')
    readonly_fields = ('submitted_by',)

class InterestEmailAdmin(admin.ModelAdmin):
	list_display = ('id','email')

class GraphAdmin(admin.ModelAdmin):
    list_display = ('name')
    fieldsets = (
        (None, {
            'fields': ('name')
        }),
        ('Data', {
            'fields': ('edges', 'points')
        })
    )
   
admin.site.register(InterestGroup, InterestGroupAdmin)
admin.site.register(IgProposal, IgProposalAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Logo, LogoAdmin)
admin.site.register(InterestEmail, InterestEmailAdmin)
admin.site.register(Graph, GraphAdmin)
