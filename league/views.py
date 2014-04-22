from django.db.models import Q
from django import forms
from django.shortcuts import render
from django.views import generic
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, HTML, Layout
from rest_framework import viewsets

from league.models import Match, Player, PlayerHistory


class IndexView(generic.ListView):
    def get_queryset(self):
        return Match.objects.order_by('-timestamp')[:10].select_related()


class MatchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MatchForm, self).__init__(*args, **kwargs)
        self.fields['score_team1'].label = 'Score'
        self.fields['score_team2'].label = 'Score'
        self.fields['team1_player1'].label = 'Attacker'
        self.fields['team1_player2'].label = 'Defender'
        self.fields['team2_player1'].label = 'Attacker'
        self.fields['team2_player2'].label = 'Defender'

    class Meta:
        model = Match

    def clean(self, *args, **kwargs):
        player_list = [v for k, v in self.cleaned_data.iteritems() if k in
                       ('team1_player1', 'team1_player2',
                        'team2_player1', 'team2_player2')]
        if len(player_list) > len(set(player_list)):
            raise forms.ValidationError('You have entered duplicate players.',
                                        code='duplicate')
        return self.cleaned_data


class MatchCreate(generic.CreateView):
    model = Match
    form_class = MatchForm

    fields = ('score_team1', 'team1_player1', 'team1_player2',
              'score_team2', 'team2_player1', 'team2_player2')

    def form_valid(self, form):
        from trueskill import Rating, rate
        match = form.save(commit=False)
        histories = []
        player_list = (match.team1_player1, match.team1_player2,
                       match.team2_player1, match.team2_player2)
        ratings = [Rating(mu=p.mu, sigma=p.sigma) for p in player_list]
        ranks = [match.score_team2 > match.score_team1,
                 match.score_team2 < match.score_team1]
        new_ratings = rate([ratings[0:2], ratings[2:4]], ranks=ranks)
        new_ratings = new_ratings[0] + new_ratings[1]
        match.save()
        for i in range(len(player_list)):
            p = player_list[i]
            p.mu = new_ratings[i].mu
            p.sigma = new_ratings[i].sigma
            p.rank = p.mu - 3 * p.sigma
            p.save()
            p.old_mu = ratings[i].mu
            p.old_sigma = ratings[i].sigma
            p.old_rank = p.old_mu - 3 * p.old_sigma
            histories.append(PlayerHistory(
                match=match, player=p, mu=p.mu, sigma=p.sigma, rank=p.rank))
        PlayerHistory.objects.bulk_create(histories)

        context = {
            'match': match,
            'player_list': player_list,
            'ratings': ratings,
        }
        return render(self.request, 'league/match_enter_success.html', context)

    def get_form(self, *args, **kwargs):
        form = super(MatchCreate, self).get_form(*args, **kwargs)
        form.helper = FormHelper(form)
        form.helper.form_class = 'row'
        form.helper.label_class = 'col-lg-3'
        form.helper.field_class = 'col-lg-9'
        form.helper.layout = Layout(
            HTML("""
    <div class="col-sm-6">
        <div class="form-horizontal">
            <h3 class="text-center">Party 1</h3>
                 """),
            Field('score_team1'),
            Field('team1_player1'),
            Field('team1_player2'),
            HTML("""
        </div>
    </div>
    <div class="col-sm-6">
        <div class="form-horizontal">
            <h3 class="text-center">Party 2</h3>
                 """),
            Field('score_team2'),
            Field('team2_player1'),
            Field('team2_player2'),
            HTML("""
        </div>
        <button type="submit" class="btn btn-primary pull-right">
            Submit match results</button>
    </div>
                 """)
        )
        return form


class MatchView(generic.ListView):

    template_name = 'league/match_history.html'
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super(MatchView, self).get_context_data(**kwargs)
        context['player_list'] = self.player_list
        context['selected_player'] = self.selected_player
        # we want to reuse the player objects
        p_dict = self.player_dict
        for m in context['match_list']:
            m._team1_player1_cache = p_dict.get(m.team1_player1_id)
            m._team1_player2_cache = p_dict.get(m.team1_player2_id)
            m._team2_player1_cache = p_dict.get(m.team2_player1_id)
            m._team2_player2_cache = p_dict.get(m.team2_player2_id)
        return context

    def get_queryset(self):
        self.player_list = Player.objects.all()
        self.player_dict = {p.pk: p for p in self.player_list}
        id = self.request.GET.get('player')
        try:
            id = int(id)
        except Exception:
            pass
        self.selected_player = self.player_dict.get(id)
        if self.selected_player:
            matches = Match.objects.order_by('-timestamp').filter(
                Q(team1_player1=self.selected_player) |
                Q(team1_player2=self.selected_player) |
                Q(team2_player1=self.selected_player) |
                Q(team2_player2=self.selected_player))
        else:
            self.selected_player = None
            matches = Match.objects.order_by('-timestamp')

        return matches


class PlayerView(generic.ListView):
    def get_queryset(self):
        return Player.objects.order_by('-rank')


class PlayerTop(generic.ListView):
    template_name = 'league/player_top.html'

    def get_queryset(self):
        players = Player.objects.order_by('-rank')[:10]
        for player in players:
            player.history = player.playerhistory_set.select_related(
                'match').order_by('match__timestamp')
        return players


class PlayerDetailView(generic.DetailView):
    queryset = Player.objects.all()

    def get_context_data(self, **kwargs):
        context = super(PlayerDetailView, self).get_context_data(**kwargs)
        context['history'] = PlayerHistory.objects.filter(
            player=context['player']).select_related('match').order_by(
            'match__timestamp')
        return context


class MatchViewSet(viewsets.ReadOnlyModelViewSet):
    model = Match
    queryset = Match.objects.order_by('-timestamp').select_related()


class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
    model = Player


def about(request):
    return render(request, 'league/about.html')
