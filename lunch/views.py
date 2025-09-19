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


# # 2. API 콜백 함수 (View)
# @require_http_methods(["GET"])
# def find_restaurants(request):
#     fixed_query = '가산디지털단지역 맛집'
#     data, status_code = search_restaurants_from_google(fixed_query)
#     return JsonResponse(data, status=status_code)

@require_http_methods(["GET"])
def find_restaurants(request):
    """
    맛집 정보를 요청하고, 받은 데이터를 필요한 필드만 추출하여 가공 후 반환합니다.
    """
    fixed_query = '가산디지털단지역 맛집'
    google_data, status_code = search_restaurants_from_google(fixed_query)

    # 1. view(Google API 응답 데이터)를 불러온 뒤,
    # -----------------------------------------------
    # 요청 실패 시, 에러 메시지를 그대로 반환합니다.
    if status_code != 200:
        return JsonResponse(google_data, status=status_code)

    # 2. 거기서 필드만 빼와서
    # -----------------------------------------------
    # 프론트엔드에 전달할 깔끔한 데이터를 담을 빈 리스트를 생성합니다.
    processed_results = []
    # Google 데이터의 'results' 리스트를 순회합니다.
    for place in google_data.get('results', []):
        # 각 식당(place)에서 필요한 정보만 추출하여 새로운 딕셔너리를 만듭니다.
        restaurant_info = {
            'name': place.get('name'),
            'address': place.get('formatted_address'),
            # 'rating'이나 'photos'는 없을 수도 있으므로, .get()을 사용해 안전하게 접근합니다.
            'rating': place.get('rating', 'N/A'), # 평점 정보가 없으면 'N/A'로 표시
            'is_open_now': place.get('opening_hours', {}).get('open_now', '정보 없음')
        }
        processed_results.append(restaurant_info)

    # 3. 출력하면 끝!
    # -----------------------------------------------
    # 최종적으로 가공된 데이터와 'status'를 함께 담아 반환합니다.
    final_response = {
        'status': 'success',
        'restaurants': processed_results
    }
    return JsonResponse(final_response, status=200)
