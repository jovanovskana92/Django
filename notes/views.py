from django.shortcuts import render
from django.http import Http404
# Create your views here.
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import DeleteView
from .forms import NotesForm
from .models import Notes
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect


class NotesDeleteView(DeleteView):
    model = Notes
    success_url = '/smart/notes'
    template_name = 'notes/notes_delete.html'


class NotesUpdateView(UpdateView):
    model = Notes
    success_url = '/smart/notes'
    form_class = NotesForm
    login_url = "/admin"


class NotesCreateView(CreateView):
    model = Notes
    success_url = '/smart/notes'
    form_class = NotesForm
    login_url = "/admin"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class NotesListView(LoginRequiredMixin, ListView):
    model = Notes
    context_object_name = "notes"
    template_name = "notes/notes_list.html"
    login_url = "/admin"

    def get_queryset(self):
        return self.request.user.notes.all()


class NotesDetailView(DetailView):
    model = Notes
    context_object_name = "note"


@csrf_protect
def user(request):
    return render(request, "notes_form.html", user)