from django.shortcuts import render, redirect
from .models import League, Team, Player
from django.db.models import Count, Sum

from . import team_maker

def index(request):
	#3) All curr players in ICBC
	teams = Team.objects.filter(league=League.objects.get(id=2))
	icbc = []
	for team in teams:
		for player in team.curr_players.all():
			icbc.append(player)
	#4) All curr players in American Conference of Amateur Football with last name Lopez
	teams = Team.objects.filter(league=League.objects.get(id=7))
	acaf = []
	for team in teams:
		for player in team.curr_players.filter(last_name='Lopez'):
			acaf.append(player)
	#5) All football players
	teams = Team.objects.filter(league=League.objects.filter(sport='Football'))
	football = []
	for team in teams:
		for player in team.curr_players.all():
			football.append(player)
	#6) All teams with current player named Sophia
	teams = Team.objects.all()
	team_sophia = []
	for team in teams:
		if team.curr_players.filter(first_name='Sophia'):
			team_sophia.append(team)
	#7) All leagues with a current player named Sophia
	leagues = League.objects.all()
	league_sophia = []
	for league in leagues:
		for team in league.teams.all():
			if team.curr_players.filter(first_name='Sophia'):
				league_sophia.append(league)
	#9) All teams Samuel Evans played on
	teams = Team.objects.all()
	samuel_evans = []
	for team in teams:
		if team.curr_players.filter(id=115) or team.all_players.filter(id=115):
			samuel_evans.append(team)
	#12) All teams Jacob Gray played for before Oregon Colts
	gray = []
	for team in Team.objects.exclude(id=24):
		if team.all_players.filter(id=151):
			gray.append(team)
	#13) Everyone named Joshua who has played in Atlantic Federation of Amateur Baseball
	# print League.objects.all()
	joshua = []
	for team in League.objects.get(id=3).teams.all():
		for player in team.all_players.all().filter(first_name='Joshua'):
			joshua.append(player)
	#14) All teams that have had 12 or more players
	num_players = []
	for team in Team.objects.all():
		if team.all_players.all().count() >= 12:
			num_players.append(team)
	#15) All players sorted by number of teams they played for
	for player in Player.objects.all():
		print player.first_name, player.last_name, player.all_teams.all().count()
	context = {
		'atlantic': Team.objects.filter(league=League.objects.get(id=5)),
		'curr_penguins': Team.objects.get(id=28).curr_players.all(),
		'icbc': icbc,
		'acaf': acaf,
		'football': football,
		'team_sophia': team_sophia,
		'league_sophia': league_sophia,
		'flores': Player.objects.filter(last_name='Flores').exclude(curr_team=10),
		'samuel_evans': samuel_evans,
		'manitoba': Team.objects.get(id=37).all_players.all(),
		'vikings': Team.objects.get(id=40).all_players.all(),
		'gray': gray,
		'joshua': joshua,
		'num_players': num_players,
		'all_players': Player.objects.annotate(count=Count('all_teams')).order_by('-count'),
		"leagues": League.objects.all(),
		"teams": Team.objects.all(),
		"players": Player.objects.all(),
	}
	return render(request, "leagues/index.html", context)

def make_data(request):
	team_maker.gen_leagues(10)
	team_maker.gen_teams(50)
	team_maker.gen_players(200)

	return redirect("index")
