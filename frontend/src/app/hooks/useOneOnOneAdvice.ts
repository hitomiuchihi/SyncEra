// hooks/useOneOnOneAdvice.ts
'use client';

// import { useState } from 'react';

// export default function useOneOnOneAdvice() {
//   const [adviceData, setAdviceData] = useState<string | null>(null);
//   const [loading, setLoading] = useState(false);
//   const [error, setError] = useState<string | null>(null);

//   const fetchAdvice = async (slackUserId: string, startDate: string, endDate: string) => {
//     setLoading(true);
//     setError(null);

//     try {
//       // モックデータを設定
//       setAdviceData(
//         `ここにアドバイスが表示されます。ユーザーID: ${slackUserId}, 開始日: ${startDate}, 終了日: ${endDate}`,
//       );
//     } catch (err) {
//       setError('アドバイスの取得に失敗しました');
//     } finally {
//       setLoading(false);
//     }
//   };

//   return { adviceData, loading, error, fetchAdvice };
// }

'use client';

import { useEffect, useState } from 'react';

interface UseAdviceDataResult {
  adviceData: string | null;
  loading: boolean;
  error: string | null;
}

export default function useOneOnOneAdvice(
  slack_user_id: string | null,
  start_date: string | null,
  end_date: string | null,
): UseAdviceDataResult {
  const [adviceData, setAdviceData] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchAdviceData() {
      setLoading(true);
      setError(null); // Reset error state before fetch
      try {
        if (!start_date || !end_date) {
          throw new Error('Start date and end date must be provided');
        }
        const response = await fetch(
          `http://localhost:8000/client/print_advices/${slack_user_id}/?start_date=${encodeURIComponent(start_date)}&end_date=${encodeURIComponent(end_date)}`,
        );
        if (!response.ok) {
          throw new Error(`Failed to fetch advice data: ${response.status}`);
        }
        const data: String = await response.json();
        setAdviceData(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    }

    if (slack_user_id && start_date && end_date) {
      fetchAdviceData();
    }
  }, [slack_user_id, start_date, end_date]);

  return { adviceData, loading, error };
}
