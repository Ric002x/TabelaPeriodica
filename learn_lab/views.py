from django.http import Http404
from .models import Activity
from .forms import ActivityForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
# Create your views here.


def lear_lab_list_view(request):
    search_term = request.GET.get('q', '').strip()
    activities = Activity.objects.filter(is_published=True,).order_by('-id')
    context = {}

    if search_term:
        activities.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term)
            ),
        ).order_by('-id')
        context['search_term'] = search_term
        context['learn_lab_search_page'] = True

    paginator = Paginator(activities, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    dict_home = {'activities': page_obj.object_list, 'page_obj': page_obj,
                 'learn_lab_page': True, 'activity_list_page': True,
                 'placeholder_input': 'Buscar por uma atividade...'}
    context.update(dict_home)

    return render(request, 'pages/learn_lab_home.html', context)


def learn_lab_detail_view(request, slug):
    activity = get_object_or_404(Activity, slug=slug, is_published=True)

    return render(request, 'pages/learn_lab_activity_detail.html', context={
        'activity': activity,
        "activiy_detail_page": True,
    })


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

    return render(request, 'pages/learn_lab_home.html', context)


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

    return render(request, 'pages/learn_lab_home.html', context)


@login_required(login_url='authors:login', redirect_field_name='next')
def activity_create(request, id=None):
    if request.method == 'POST':
        form = ActivityForm(
            data=request.POST,
            files=request.FILES)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = request.user
            activity.save()
            form.save()
            messages.success(request, 'Atividade criada!')
            return redirect('users:profile')
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
        return render(request, 'pages/learn_lab_activity_create.html', {
            'form': form,
            'form_action': reverse('learn_lab:activity_create')
        })


@login_required(login_url='authors:login', redirect_field_name='next')
def activity_delete(request, slug):
    if request.method == 'POST':
        activity = get_object_or_404(
            Activity, slug=slug, user=request.user)
        activity.delete()
        messages.success(request, '✅ Atividade deletada com sucesso')
        return redirect('users:profile')
    else:
        raise Http404


@login_required(login_url='authors:login', redirect_field_name='next')
def activity_update(request, slug=None):
    activity = Activity.objects.filter(
        user=request.user,
        slug=slug,
        is_published=False,
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

    return render(request, 'pages/learn_lab_activity_update.html', context={
        'activity': activity,
        'form': form
    })
