# lunch/views.py

import os
import requests
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

# 1. 변수 초기화 로직
GOOGLE_PLACES_API_KEY = os.environ.get('GOOGLE_PLACES_API_KEY')
GOOGLE_PLACES_API_URL = 'https://maps.googleapis.com/maps/api/place/textsearch/json'


# 3. 검색 및 결과 반환 함수
def search_restaurants_from_google(query):
    if not GOOGLE_PLACES_API_KEY:
        return {'error': 'Google API 키가 설정되지 않았습니다.'}, 500

    params = {
        'query': query,
        'key': GOOGLE_PLACES_API_KEY,
        'language': 'ko',
    }

    try:
        response = requests.get(GOOGLE_PLACES_API_URL, params=params)
        response.raise_for_status()
        return response.json(), 200
    except requests.exceptions.RequestException as e:
        return {'error': f'Google API 요청에 실패했습니다: {e}'}, 500


# 2. API 콜백 함수 (View)
@require_http_methods(["GET"])
def find_restaurants(request):
    fixed_query = '가산디지털단지역 맛집'
    data, status_code = search_restaurants_from_google(fixed_query)
    return JsonResponse(data, status=status_code)