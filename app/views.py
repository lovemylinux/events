from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from datetime import datetime, timezone
from types import SimpleNamespace as Placeholder
import uuid

from .models import Event, Invitation, Hit


def show_index_page(request):
    """
    Show main page
    :param request:
    """
    return render(request, 'events/index.html')


@login_required
def show_dashboard_page(request):
    """

    :param request:
    """
    events_to_show = events = Event.objects.filter(creator=request.user)

    # Check if filter param is valid and exists
    filtering_event_str = request.GET.get('filter_by_event')
    if filtering_event_str and filtering_event_str.isdigit():
        events_to_show = events.filter(id=int(filtering_event_str))
        filtering_event_str = int(filtering_event_str)
    else:
        filtering_event_str = ''

    invitations = []
    for e in events_to_show:
        invitations += list(Invitation.objects.filter(event=e.id))

    context = {
        'invitations': invitations,
        'events': events,
        'filter_by_event': filtering_event_str
    }

    return render(request, 'events/profile.html', context=context)


@login_required
def show_create_invite_page(request):
    """
    Page for creating new events
    :param request:
    """
    return render(request, 'events/invite.html', context={
        'events': Event.objects.filter(creator=request.user),
    })


def show_invitation(request, key):
    """
    Page that show invitation
    :param key: invitation's hash
    """
    target_invitation = get_object_or_404(Invitation, key=key)
    target_event = target_invitation.event

    context = {
        'invitation': target_invitation,
        'event': target_event,
        'key': key,
        'deadline': datetime.now(timezone.utc) > target_event.deadline,
    }

    # Logging
    if __get_creator_by_invitation_request(key=key) != request.user and ('api' not in request.session):
        Hit.objects.filter(invitation=target_invitation).update(is_valid=False)
        Hit.objects.create(
            invitation_id=target_invitation.id,
            user_agent=request.META['HTTP_USER_AGENT'],
            ip=request.META.get('REMOTE_ADDR'),
            referal=request.META.get('HTTP_REFERER'),
            decision=(Hit.objects.order_by('-dtm').first() or Placeholder(decision=False)).decision,
        )

    # For button style
    try:
        if Hit.objects.filter(invitation=target_invitation.id).order_by('-dtm').first().decision:
            context['decision'] = True
        else:
            context['decision'] = False
    except AttributeError:
        context['decision'] = False

    return render(request, 'events/invitation.html', context=context)


# API


@login_required
def add_invite(request):
    """
    Create new invites
    :param request:
    :return:
    """
    for i in range(int(request.POST['count'])):
        new_invitation = Invitation(
            event_id=int(request.POST.get('event')),
            key=str(uuid.uuid4()),
            recipient=request.POST.get('contact' + str(i)),
            count=int(request.POST.get('quantity' + str(i))),
        )
        if new_invitation.event.creator == request.user:
            new_invitation.save()
        else:
            raise PermissionDenied
    return HttpResponseRedirect(reverse('dashboard'))


@login_required
def change_invite(request):
    """

    :param request:
    :return:
    """
    if __get_creator_by_invitation_request(id=request.POST.get('id')) == request.user:
        Invitation.objects.filter(id=request.POST.get('id')).update(count=request.POST.get('count'))
    else:
        raise PermissionDenied
    return HttpResponseRedirect(reverse('dashboard'))


@login_required
def delete_invite(request):
    """

    :param request:
    :return:
    """
    if __get_creator_by_invitation_request(id=request.POST.get('id')) == request.user:
        Invitation.objects.filter(id=request.POST.get('id')).delete()
    else:
        raise PermissionDenied
    return HttpResponseRedirect(reverse('dashboard'))


def change_decision(request):
    """

    :param request:
    :return:
    """
    hits = Hit.objects.filter(invitation=int(request.POST.get('id')))
    if hits.first():
        h = hits.order_by('-dtm').first()
        h.decision = request.POST.get('decision') == 'yes'
        h.save()
    else:
        Hit.objects.create(
            invitation_id=Invitation.objects.filter(key=request.POST.get('key')).first().id,
            user_agent=request.META['HTTP_USER_AGENT'],
            ip=request.META.get('REMOTE_ADDR'),
            referal=request.META.get('HTTP_REFERER'),
            decision=request.POST.get('decision') == 'yes',
        )
    request.session['api'] = True
    return HttpResponseRedirect(reverse('show_invitation', args=[request.POST.get('key')]))


# Utils


def __get_creator_by_invitation_request(**kwargs):
    return Event.objects.filter(id=Invitation.objects.filter(**kwargs).first().event.id).first().creator
