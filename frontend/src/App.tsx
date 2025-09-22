// frontend/src/App.tsx

import { useState, useEffect } from 'react';

// 백엔드로부터 받을 맛집 데이터의 타입을 미리 정의합니다. (TypeScript의 장점!)
interface Restaurant {
  name: string;
  address: string;
  rating: number | string;
  is_open_now: boolean | string;
}

function App() {
  // 맛집 목록을 저장할 state
  const [restaurants, setRestaurants] = useState<Restaurant[]>([]);
  // 로딩 상태를 관리할 state
  const [loading, setLoading] = useState<boolean>(true);
  // 에러를 저장할 state
  const [error, setError] = useState<string | null>(null);

  // 컴포넌트가 처음 렌더링될 때 한 번만 API를 호출합니다.
  useEffect(() => {
    async function fetchRestaurants() {
      try {
        // Django API 서버에 맛집 정보를 요청합니다.
        const response = await fetch('http://3.39.141.56:8000/api/restaurants');
        if (!response.ok) {
          throw new Error('데이터를 불러오는 데 실패했습니다.');
        }
        const data = await response.json();
        setRestaurants(data.restaurants); // state에 맛집 목록 저장
      } catch (err) {
        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError('알 수 없는 에러가 발생했습니다.');
        }
      } finally {
        setLoading(false); // 로딩 상태 종료
      }
    }

    fetchRestaurants();
  }, []); // 빈 배열을 전달하여 최초 1회만 실행되도록 설정

  // 로딩 중일 때 보여줄 화면
  if (loading) {
    return <div className="text-center text-white p-10">맛집 목록을 불러오는 중...</div>;
  }

  // 에러 발생 시 보여줄 화면
  if (error) {
    return <div className="text-center text-red-500 p-10">에러: {error}</div>;
  }

  return (
    <div className="bg-gray-900 min-h-screen text-white p-8">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-4xl font-bold text-center mb-8">오늘의 점심 추천! 🍜</h1>
        <ul className="space-y-4">
          {restaurants.map((resto) => (
            <li key={resto.name} className="bg-gray-800 p-4 rounded-lg shadow-md">
              <h2 className="text-xl font-semibold text-blue-400">{resto.name}</h2>
              <p className="text-gray-400">{resto.address}</p>
              <p className="text-yellow-500">평점: {resto.rating}</p>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;