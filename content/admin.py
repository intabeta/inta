from django.contrib import admin
from content.models import InterestGroup, IgProposal, Entry, Logo

class InterestGroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    
class IgProposalAdmin(admin.ModelAdmin):
    pass

class LogoAdmin(admin.ModelAdmin):
    pass

class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'ig', 'domain', 'date_added')
   
admin.site.register(InterestGroup, InterestGroupAdmin)
admin.site.register(IgProposal, IgProposalAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Logo, LogoAdmin)