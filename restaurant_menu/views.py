from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from .models import Item, MEAL_TYPE, Review
from django.db.models import Q
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpResponseForbidden


class MenuList(generic.ListView):
    queryset = Item.objects.order_by("date_created")
    template_name = 'index.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Item.objects.filter(
                Q(meal__icontains=query) | Q(description__icontains=query)
            ).order_by("meal")
        return Item.objects.order_by("date_created")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meals'] = MEAL_TYPE
        return context


class MenuItemDetail(generic.DetailView):
    model = Item
    template_name = 'menu_item_detail.html'

class About(generic.TemplateView):
    template_name = 'about.html'

class AddItem(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Item
    fields = ['meal', 'description', 'price', 'meal_type', 'status', 'image']
    template_name = 'add_item.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return HttpResponseForbidden("You do not have permission to access this page.")

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


class ReviewListView(generic.ListView):
    model = Review
    template_name = 'reviews.html'
    context_object_name = 'reviews'
    ordering = ['-created_at']


@login_required
def submit_review(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('home')
    else:
        form = ReviewForm()
    return render(request, 'submit_review.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # redirect after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def logout_then_home(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('home')
