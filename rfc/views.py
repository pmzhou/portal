from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response,RequestContext
from .forms import RFCForm
from .models import RFCDocument
from rest_framework.response import Response
from project.helper import *
from .serializer import RFCSerializer
from rest_framework.decorators import api_view
from crispy_forms.helper import FormHelper
from project.models import ProjectContacts, ProjectContactTitles



# Create your views here.
def rfc_view(request):

    form = RFCForm(request.POST or None)
    if form.is_valid():
        save_it = form.save(commit=False)
        save_it.save()

    return render_to_response("members/rfc/create.html", locals(), context_instance = RequestContext(request))


@login_required(login_url='/')
def rfc_log_view(request, pk):
    context = project_info_helper(request, pk)

    return render(request, "members/rfc/index.html", context)


# def rfc_log_json(request):
#
#
#     datak= serializers.serialize('json',RFCDocument.objects.all())
#     result = {}
#     result['data']=datak
#     return HttpResponse(json.dumps(result), content_type="application/json")

@api_view(['GET','POST'])
def rfc_list(request, pk):

    if request.method=='GET':
        rfcs = RFCDocument.objects.filter(rfc_project_id=pk)
        serializer = RFCSerializer(rfcs)
        datak = {}
        datak['data'] = serializer.data
        return Response(datak)
    if request.method == 'POST':
        pass


def add_rfc(request, pk):
    project = Projects.objects.get(pk=pk)

    # TODO can be a utility function itself
    title = ProjectContacts.objects.select_related().get(project_contact_id=request.user)
    print title.project_contact_title

    project_issued_person = None
    if title.project_contact_title.__str__() == 'OAR':
        project_issued_person = title.project_contact.get_full_name()

    #print project.project_name
    form = RFCForm(initial={'rfc_project': project.project_name,
                            'rfc_issued_to': project_issued_person,
                            'rfc_answer_authorized_by': project_issued_person,
    }, )
    form.fields['rfc_answer']
    print form.Meta.widgets
    # #.widgets.attrs['readonly'] = 'readonly'
    #print form
    return render(request,'members/rfc/create.html',{'form': form})


def rfc_creation_confirmation(request):

    if request.method == 'POST':
        form = RFCForm(request.POST)


        if form.is_valid():
            form.save(commit=True)
        else:
            print form.errors
    else:
            return add_rfc(request)

    return render(request,"members/rfc/confirmation.html")
