# encoding: utf-8
import json

from django.http import HttpResponse, Http404
from django.views.generic import CreateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from .models import Picture
from .response import JSONResponse, response_mimetype
from .serialize import serialize


def file_authenticate(req_user, file_owner):
    # super user can operate all files
    if req_user.is_authenticated and (req_user == file_owner or req_user.is_superuser):
        return True
    else:
        return False


# loginRequiredMixin redirect the url to login page if not already logged in
class PictureCreateView(LoginRequiredMixin, CreateView):
    model = Picture
    fields = ['file', 'slug']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        self.object = form.save()
        self.object.domain = self.request.META['HTTP_HOST']
        files = [serialize(self.object)]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def form_invalid(self, form):
        data = json.dumps(form.errors)
        return HttpResponse(content=data, status=400, content_type='application/json')


class PictureDeleteView(DeleteView):
    model = Picture

    def get(self, *args, **kwargs):
        raise Http404("Page not found!")

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if file_authenticate(request.user, self.object.owner):
            self.object.delete()
            response = JSONResponse("File deleted!", mimetype=response_mimetype(request))
        else:
            raise PermissionDenied
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class PictureListView(ListView):
    model = Picture

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            files = list()
            for f in self.get_queryset():
                if file_authenticate(self.request.user, f.owner):
                    # get server address.
                    f.domain = self.request.META['HTTP_HOST']
                    files.append(serialize(f))
            data = {'files': files}
            response = JSONResponse(data, mimetype=response_mimetype(self.request))
            response['Content-Disposition'] = 'inline; filename=files.json'
            return response
        else:
            raise Http404("Page not found!")
