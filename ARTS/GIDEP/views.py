# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404, render_to_response

from django.http import HttpResponse, FileResponse, Http404

from django.utils import timezone

from .models import Document

# Create your views here.

#@login_required()
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def home(request):
    docs = Document.objects.filter(arts_date__lte=timezone.now()).order_by('arts_date')
    return render(request, 'gidep/home.html', {'documents' : docs})

def doc_view(request, _id):
    doc = get_object_or_404(Document, arts_ID=_id)
#    form = CommentForm(request.POST or None)
#    if form.is_valid():
#        comment = form.save(commit=False)
#        comment.post = post
#        comment.save()
#    return redirect('document_detail', _id=doc.arts_ID)
    return render_to_response('gidep/view.html',
                              {
                                  'document': doc,
#                                  'form': form,
                              })