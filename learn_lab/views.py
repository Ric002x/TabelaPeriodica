import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import Q
from django.forms import model_to_dict
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from .forms import ActivityForm, RatingForm
from .models import Activity, ActivityLevel, ActivityRating, ActivitySubject

# Create your views here.


class LearnLabListView(ListView):
    template_name = "learn_lab/pages/learn_lab_home.html"
    paginate_by = 20
    model = Activity
    context_object_name = "activities"
    ordering = '-id'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '').strip()
        qs = Activity.objects.filter(
            is_published=True,
        ).order_by('-id').select_related('user', 'level', 'subject')
        if search_term:
            qs_search = qs.filter(
                Q(
                    Q(title__icontains=search_term) |
                    Q(description__icontains=search_term) |
                    Q(content__icontains=search_term)
                ),
                is_published=True,
            ).order_by('-id').select_related('user', 'level', 'subject')
            return qs_search
        return qs

    def get_context_data(self, **kwargs):
        search_term = self.request.GET.get('q', '').strip()
        context = super().get_context_data(**kwargs)
        context.update({
            'learn_lab_page': True, 'activity_list_page': True,
            'placeholder_input': 'Buscar por uma atividade...',
            'form_search': reverse('learn_lab:learn_lab_activity_search'),
        })
        if search_term:
            context['search_term'] = search_term
            context['learn_lab_search_page'] = True
        return context


class LearnLabListViewApi(LearnLabListView):
    def render_to_response(self, context, **response_kwargs):
        activities = self.get_context_data()['activities']
        activities_list = [
            {
                "id": activity.id,
                "title": activity.title,
                "description": activity.description,
                "content": activity.content,
                'level': ActivityLevel.objects.get(name=activity.level).name,
                'subjects': ActivitySubject.objects.get(
                    name=activity.subject).name,
            }
            for activity in activities
        ]

        return JsonResponse(
            activities_list,
            safe=False
        )


class LearnLabDetailView(DetailView):
    model = Activity
    template_name = "learn_lab/pages/learn_lab_activity_detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "activity"

    def get_object(self, queryset=None):
        try:
            activity = Activity.objects.get(
                slug=self.kwargs.get('slug'),
                is_published=True)
        except Activity.DoesNotExist:
            raise Http404
        return activity

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        activity = self.get_object()

        try:
            user_rating = ActivityRating.objects.filter(
                activity=activity,
                user=self.request.user
            ).first()
            others_ratings = ActivityRating.objects.filter(
                activity=activity
            ).order_by('-id').exclude(user=self.request.user)
        except TypeError:  # Se o usuário não estiver logado
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

        context.update({
            'activity': activity,
            'activiy_detail_page': True,
            'rating_form': rating_form_create,
            'rating_form_create_action': (
                reverse('learn_lab:activity_rate_create',
                        kwargs={'slug': activity.slug})),
            'rating_form_edit_action': (
                reverse('learn_lab:activity_rate_edit',
                        kwargs={'slug': activity.slug})),
            'others_ratings': others_ratings,
            'user_rating': user_rating,
            'stars_range': (1, 2, 3, 4, 5,),
            'rating_form_edit': rating_form_edit,
        })
        return context


class LearnLabDetailViewApi(LearnLabDetailView):
    def render_to_response(self, context, **response_kwargs):
        activity = self.get_context_data()['activity']
        activity_dict = model_to_dict(activity)

        engine = os.getenv("DATABASE_ENGINE")

        if activity_dict.get('file'):
            if engine == "django.db.backends.sqlite3":
                activity_dict['file'] = "http://127.0.1:8000" + \
                    activity_dict['file'].url

            elif engine == "django.db.backends.postgresql":
                activity_dict['file'] = (
                    "https://atomicdiscoveries.ricardovenicius.com.br") + \
                    activity_dict['file'].url
        else:
            activity_dict['file'] = ""

        activity_dict['level'] = ActivityLevel.objects.get(
            name=activity.level).name

        activity_dict['subject'] = ActivitySubject.objects.get(
            name=activity.subject).name

        del activity_dict['is_published']

        return JsonResponse(
            activity_dict,
            safe=False
        )


class LearnLabSubjectListView(LearnLabListView):
    def get_queryset(self, *args, **kwargs):
        subject_request = self.kwargs.get('subject')
        try:
            subject_query = ActivitySubject.objects.get(name=subject_request)
        except ActivitySubject.DoesNotExist:
            raise Http404
        subject_list = Activity.objects.filter(
            subject=subject_query,
            is_published=True,
        ).order_by('-id').select_related('user', 'level', 'subject')
        return subject_list


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


@ login_required(login_url='users:login', redirect_field_name='next')
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


@ login_required(login_url='users:login', redirect_field_name='next')
def activity_delete(request, slug):
    if request.method == 'POST':
        activity = get_object_or_404(
            Activity, slug=slug, user=request.user)
        activity.delete()
        messages.success(request, '✅ Atividade deletada com sucesso')
        return redirect('users:profile_posts')
    else:
        raise Http404


@ login_required(login_url='users:login', redirect_field_name='next')
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


@ login_required(login_url='users:login', redirect_field_name='next')
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
