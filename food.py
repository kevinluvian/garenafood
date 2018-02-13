import json
import requests
import time
from tzlocal import get_localzone
from dateutil import parser
import os

token = os.getenv('GARENA_FOOD_TOKEN', '')
auth_header = {'Authorization': 'Token {}'.format(token)}


def get_today_menu():
	req = requests.get('https://dinner.seagroup.com/api/current', headers=auth_header)
	data = json.loads(req.content)
	return data['menu']


def get_food_list(menu_id):
	req = requests.get('https://dinner.seagroup.com/api/menu/{}'.format(menu_id), headers=auth_header)
	data = json.loads(req.content)
	return data['food']


def order_food(menu_id, food_id):
	req = requests.post('https://dinner.seagroup.com/api/order/{}'.format(menu_id), data={'food_id': food_id}, headers=auth_header)
	data = json.loads(req.content)
	if data['status'] == 'success':
		return True
	else:
		print('[info] Order failed, retrying in one minute.. ({})'.format(data['error']))
		return False


menu = get_today_menu()
poll_start = parser.parse(menu['poll_start']).astimezone(get_localzone())
poll_start = poll_start.strftime('%Y-%m-%d %H:%M')
menu_id = menu['id']
print('poll start: {}'.format(poll_start))

print ''
print 'Makanan:'
food_list = get_food_list(menu_id)
cnt = 0
for food in food_list:
	cnt += 1
	print('{}. {}'.format(cnt, food['name']))

print('pilih menu:')
selection = int(input()) - 1
selected_food_id = food_list[selection]['id']

while True:
	print('[info] Ordering {}, poll open at: {}'.format(food['name'], poll_start))
	success = order_food(menu_id, selected_food_id)
	if not success:
		time.sleep(60)
	else:
		print('food ordered!')
		break
