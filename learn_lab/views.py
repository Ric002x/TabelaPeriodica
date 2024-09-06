from django.http import Http404
from .models import Activity, ActivityRating
from .forms import ActivityForm, RatingForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.db import IntegrityError
# Create your views here.


def lear_lab_list_view(request):
    search_term = request.GET.get('q', '').strip()

    if search_term:
        activities = Activity.objects.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term)
            ),
            is_published=True
        ).order_by('-id')
        paginator = Paginator(activities, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(
            request, 'learn_lab/pages/learn_lab_home.html',
            {'activities': page_obj.object_list, 'page_obj': page_obj,
             'learn_lab_page': True, 'activity_list_page': True,
             'placeholder_input': 'Buscar por uma atividade...',
             'search_term': search_term, 'learn_lab_search_page': True})

    activities = Activity.objects.filter(is_published=True,).order_by('-id')

    paginator = Paginator(activities, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'activities': page_obj.object_list, 'page_obj': page_obj,
               'learn_lab_page': True, 'activity_list_page': True,
               'placeholder_input': 'Buscar por uma atividade...'}

    return render(request, 'learn_lab/pages/learn_lab_home.html', context)


def learn_lab_detail_view(request, slug):
    # Get the object of selected Activity
    activity = get_object_or_404(Activity, slug=slug, is_published=True)

    # Get all the rating of select activity.
    try:  # If a user is logged
        user_rating = ActivityRating.objects.filter(
            activity=activity,
            user=request.user
        ).first()
        others_ratings = ActivityRating.objects.filter(
            activity=activity
        ).order_by('-id').exclude(user=request.user)
    except TypeError:  # If a user is not logged
        user_rating = None
        others_ratings = ActivityRating.objects.filter(
            activity=activity
        ).order_by('-id')

    # Start the form for user rating
    rating_form_create = RatingForm()

    # Form to edit a rate made by de user
    rating_form_edit = RatingForm(
        instance=user_rating,
    )

    context = {
        'activity': activity,
        'activiy_detail_page': True,
        'rating_form': rating_form_create,
        'rating_form_create_action': reverse('learn_lab:activity_rate_create',
                                             kwargs={'slug': activity.slug}),
        'rating_form_edit_action': reverse('learn_lab:activity_rate_edit',
                                           kwargs={'slug': activity.slug}),
        'others_ratings': others_ratings,
        'user_rating': user_rating,
        'stars_range': (1, 2, 3, 4, 5,),
        'rating_form_edit': rating_form_edit,
    }

    return render(
        request, 'learn_lab/pages/learn_lab_activity_detail.html', context)


def learn_lab_subject_list_view(request, id=None):
    if id:
        activities = Activity.objects.filter(
            is_published=True,
            subject_id=id
        ).order_by('-id')
    if not activities:
        raise Http404

    paginator = Paginator(activities, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'activities': page_obj.object_list,
        'page_obj': page_obj,
        'learn_lab_page': True,
        'activity_list_page': True,
        'placeholder_input': 'Buscar por uma atividade...',
    }

    return render(request, 'learn_lab/pages/learn_lab_home.html', context)


def learn_lab_level_list_view(request, id=None):
    if id:
        activities = Activity.objects.filter(
            is_published=True,
            level_id=id
        ).order_by('-id')
    if not activities:
        raise Http404

    paginator = Paginator(activities, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'activities': page_obj.object_list,
        'page_obj': page_obj,
        'learn_lab_page': True,
        'activity_list_page': True,
        'placeholder_input': 'Buscar por uma atividade...',
    }

    return render(request, 'learn_lab/pages/learn_lab_home.html', context)


@login_required(login_url='users:login', redirect_field_name='next')
def activity_create(request, id=None):
    if request.method == 'POST':
        form = ActivityForm(
            data=request.POST,
            files=request.FILES)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = request.user
            activity.save()
            messages.success(request, 'Atividade criada!')
            return redirect('users:profile_posts')
        else:
            messages.error(request, 'Erro no formulário de atividade')
            return redirect(reverse('learn_lab:activity_create'))

    else:
        activity = Activity.objects.filter(
            pk=id,
            user=request.user
        ).first()

        form = ActivityForm(
            instance=activity
        )
        return render(
            request, 'learn_lab/pages/learn_lab_activity_create.html', {
                'form': form,
                'form_action': reverse('learn_lab:activity_create')
            })


@login_required(login_url='users:login', redirect_field_name='next')
def activity_delete(request, slug):
    if request.method == 'POST':
        activity = get_object_or_404(
            Activity, slug=slug, user=request.user)
        activity.delete()
        messages.success(request, '✅ Atividade deletada com sucesso')
        return redirect('users:profile_posts')
    else:
        raise Http404


@login_required(login_url='users:login', redirect_field_name='next')
def activity_update(request, slug=None):
    activity = Activity.objects.filter(
        user=request.user,
        slug=slug,
    ).first()

    if request.method == "POST":
        form = ActivityForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=activity,
        )
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = request.user
            activity.is_published = False
            activity.save()

            messages.success(request, "Atividade atualizada!")
            return redirect(reverse('learn_lab:activity_update',
                                    kwargs={'slug': activity.slug}))
        else:
            messages.error(request, 'Erro na validação da atividade')
            redirect(reverse('learn_lab:activity_update',
                             kwargs={'slug': activity.slug}))

    if not activity:
        raise Http404

    form = ActivityForm(
        instance=activity
    )

    return render(request, 'learn_lab/pages/learn_lab_activity_update.html',
                  context={
                      'activity': activity,
                      'form': form
                  })


@login_required(login_url='users:login', redirect_field_name='next')
def rating_create(request, slug):
    if request.method == 'POST':
        try:
            form = RatingForm(data=request.POST)
            if form.is_valid():
                rate = form.save(commit=False)
                rate.user = request.user
                rate.activity = Activity.objects.get(slug=slug)
                rate.save()
                messages.success(request, 'Avalição enviada')
                return redirect(reverse('learn_lab:learn_lab_activity',
                                        kwargs={'slug': slug}))
            else:
                form = RatingForm()
                messages.error(request, 'Erro na avaliação')
                return redirect(reverse('learn_lab:learn_lab_activity',
                                        kwargs={'slug': slug}))
        except IntegrityError:
            messages.warning(request, 'Você já avaliou esta atividade')
            return redirect(reverse('learn_lab:learn_lab_activity',
                                    kwargs={'slug': slug}))
    else:
        raise Http404


def rating_edit(request, slug):
    if request.method == 'POST':
        activity = Activity.objects.get(slug=slug)
        user_rating = ActivityRating.objects.filter(
            activity=activity,
            user=request.user
        ).first()
        form = RatingForm(
            instance=user_rating,
            data=request.POST or None,
        )
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user = request.user
            rate.activity = activity
            rate.save()

            messages.success(request, 'Sua avalição foi alterada!')
            return redirect(reverse(
                'learn_lab:learn_lab_activity', kwargs={'slug': slug}
            ))
        else:
            messages.error(request, 'Erro no formulário')
            return redirect(reverse(
                'learn_lab:learn_lab_activity', kwargs={'slug': slug}
            ))

    else:
        raise Http404


def rating_delete(request, slug):
    if request.method == "POST":
        activity = get_object_or_404(Activity, slug=slug)
        user_rating = ActivityRating.objects.filter(
            activity=activity,
            user=request.user
        ).first()
        user_rating.delete()
        messages.success(request, "Avalição deletada")
        return redirect(reverse(
            'learn_lab:learn_lab_activity', kwargs={'slug': slug}
        ))
    else:
        raise Http404
