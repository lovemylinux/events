from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from datetime import datetime, timezone
from django.conf import settings
import uuid

from .models import Event, Invitation, Decision, Hit


def invitation(request, key):
    """
    Страница, показывающая информацию о приглашении
    :param key: Хэш приглашения
    """
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
    if Decision.objects.filter(invitation=int(context['invitation'].id)).last().decision is True:
        context['true'] = ['btn-primary', 'disabled']
        context['false'] = ['', '']
    else:
        context['false'] = ['btn-primary', 'disabled']
        context['true'] = ['', '']
    if datetime.now(timezone.utc) > context['event'].deadline:
        context['deadline'] = 'disabled'
    return render(request, 'events/invitation.html', context=context)


def get_decision(request):
    Decision.objects.filter(invitation=int(request.POST.get('id'))).update(is_valid=False)
    new_decision = Decision(
        invitation_id=int(request.POST.get('id'))
    )
    if request.POST.get('decision') == 'yes':
        new_decision.decision = True
        new_decision.save()
    elif request.POST.get('decision') == 'no':
        new_decision.decision = False
        new_decision.save()
    link = '/invitation/' + request.POST.get('key')
    return HttpResponseRedirect(link)


@login_required(login_url='/admin')
def create_invite(request):
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
def profile(request):
    context = {}
    invitations = []

    context['invitations'] = invitations
    context['domain_port'] = settings.PROJECT_DOMAIN + ':' + settings.PROJECT_PORT
    context['events'] = Event.objects.filter(creator=request.user)
    context['filter_by_event'] = -1

    events_to_show = context['events']

    try:
        filter_by_event = int(request.GET['filter_by_event'])
        events_to_show = context['events'].filter(id=filter_by_event)
        context['filter_by_event'] = filter_by_event
    except:
        pass

    for e in events_to_show:
        invitations += [
            *list(Invitation.objects.filter(event=e.id))
        ]

    context['empty_invitations'] = True if len(invitations) == 0 else False

    return render(request, 'events/profile.html', context=context)


@login_required(login_url='/admin')
def change_invite(request):
    if get_creator(request) == request.user:
        Invitation.objects.filter(id=request.POST.get('id')).update(count=request.POST.get('count'))
    else:
        raise Http404
    return HttpResponseRedirect('/profile')


@login_required(login_url='/admin')
def delete_invite(request):
    if get_creator(request) == request.user:
        Invitation.objects.filter(id=request.POST.get('id')).delete()
    else:
        raise Http404
    return HttpResponseRedirect('/profile')


def get_creator(request):
    return Event.objects.filter(
        id=Invitation.objects.filter(
            id=int(request.POST.get('id'))
        ).first().event.id
    ).first().creator


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
