from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Event, Invitation, Decision
import uuid


@login_required(login_url='/admin')
def decision(request):
    context = {}
    context['events'] = Event.objects.filter(creator=request.user)
    return render(request, 'events/invite.html', context=context)


@login_required(login_url='/admin')
def invite(request):
    context = {}
    context['events'] = Event.objects.filter(creator=request.user)
    return render(request, 'events/invite.html', context=context)


@login_required(login_url='/admin')
def add_invite(request):
    for i in range(int(request.POST['count'])):
        new_invitation = Invitation(
            event_id=int(request.POST.get('event')),
            key=str(uuid.uuid4()),
            recipient=request.POST.get('contact' + str(i)),
            count=int(request.POST.get('quantity' + str(i))),
        )
        new_invitation.save()
        new_decision = Decision(
            invitation_id=int(new_invitation.id)
        )
        new_decision.save()
    return HttpResponseRedirect('/profile')


@login_required(login_url='/admin')
def change(request):
    context = {}
    context['events'] = Event.objects.filter(creator=request.user)
    invitations = []
    for e in context['events']:
        invitations += [
            *list(Invitation.objects.filter(event=e.id))
        ]
    context['invitations'] = invitations
    return render(request, 'events/profile.html', context=context)


@login_required(login_url='/admin')
def change_invite(request):
    Invitation.objects.filter(id=request.POST.get('id')).update(count=request.POST.get('count'))
    return HttpResponseRedirect('/profile')


@login_required(login_url='/admin')
def delete_invite(request):
    Invitation.objects.filter(id=request.POST.get('id')).delete()
    return HttpResponseRedirect('/profile')