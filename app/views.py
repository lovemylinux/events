from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Event, Invitation, Decision, Hit
from datetime import datetime, timezone

import uuid


def handler404(request):
    return render(request, 'events/404.html')


def decision(request, key):
    context = {
        'invitation': Invitation.objects.filter(key=key).first(),
    }
    if context['invitation'] is None:
        return HttpResponseRedirect('/404')
    new_hit = Hit(
        invitation_id=context['invitation'].id,
        user_agent=request.META['HTTP_USER_AGENT'],
        ip=get_client_ip(request),
        referal=request.META.get('HTTP_REFERER'),
    )
    new_hit.save()
    context['event'] = context['invitation'].event
    if Decision.objects.filter(invitation=int(context['invitation'].id)).first().decision is True:
        context['true'] = 'btn-primary'
        context['false'] = ''
    else:
        context['false'] = 'btn-primary'
        context['true'] = ''
    context['deadline'] = ''
    if datetime.now(timezone.utc) > context['event'].deadline:
        context['deadline'] = 'disabled'
    return render(request, 'events/invitation.html', context=context)


def get_decision(request):
    if request.POST.get('decision') == 'yes':
        Decision.objects.filter(invitation=int(request.POST.get('id'))).update(decision=True)
    else:
        Decision.objects.filter(invitation=int(request.POST.get('id'))).update(decision=False)
    link = '/invitation/' + request.POST.get('key')
    return HttpResponseRedirect(link)


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
        if new_invitation.event.creator == request.user:
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
    if get_creator(request) == request.user:
        Invitation.objects.filter(id=request.POST.get('id')).update(count=request.POST.get('count'))
    else:
        return HttpResponseRedirect('/404')
    return HttpResponseRedirect('/profile')


@login_required(login_url='/admin')
def delete_invite(request):
    if get_creator(request) == request.user:
        Invitation.objects.filter(id=request.POST.get('id')).delete()
    else:
        return HttpResponseRedirect('/404')
    return HttpResponseRedirect('/profile')


def get_creator(request):
    return Event.objects.filter(
        id=Invitation.objects.filter(id=int(request.POST.get('id'))).first().event.id).first().creator


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def not_found(request):
    return render(request, 'events/404.html')