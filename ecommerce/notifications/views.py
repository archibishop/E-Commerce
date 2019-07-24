from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views import View
from authentication.models import Person
from product.models import Category
from .models import Notification
# Create your views here.


class NotificationDetailView(DetailView):
    model = Notification
    template_name = 'notification.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = kwargs['object']
        product.read = True
        product.save()
        if self.request.user.is_authenticated:
            person = Person.objects.get(user=self.request.user)
            context['person'] = person
        notifications_unread = Notification.objects.filter(
            user=self.request.user, read=False)
        context['vendors'] = get_vendors()
        context['categories'] = get_categories()
        context['num_notifications'] = len(notifications_unread)
        return context

class NotificationsView(View):
    template_name = 'notifications.html'

    def get(self, request, *args, **kwargs):
        person = Person.objects.get(user=self.request.user)
        notification_items = Notification.objects.filter(user=self.request.user)
        notifications_unread = Notification.objects.filter(
            user=self.request.user, read=False)
        return render(request, self.template_name, {
            'vendors': get_vendors(), 
            'categories': get_categories(), 
            'person': person, 
            'num_notifications': len(notifications_unread),
            'notification_items': notification_items})

def get_vendors():
    vendors = Person.objects.filter(customer=False)
    return vendors


def get_categories():
    categories = Category.objects.all()
    return categories
