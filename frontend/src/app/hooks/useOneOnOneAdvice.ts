// hooks/useOneOnOneAdvice.ts
'use client';

import { useEffect, useState } from 'react';

// Adviceの型定義
interface Advice {
  advice: string;
  date: string;
}

export default function useOneOnOneAdvice(slackUserId: string, startDate: string, endDate: string) {
  const [adviceData, setAdviceData] = useState<Advice | null>(null); // Advice型またはnull
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchAdviceData = async () => {
    setLoading(true);
    setError(null);

    try {
      // クエリパラメータを含むURLを構築
      const response = await fetch(
        `http://localhost:8000/client/print_advices/${slackUserId}/?start_date=${encodeURIComponent(startDate)}&end_date=${encodeURIComponent(endDate)}`,
      );
      if (!response.ok) {
        throw new Error(`Failed to fetch advice: ${response.status} ${response.statusText}`);
      }
      const data: Advice = await response.json(); // APIのレスポンスがAdvice型
      setAdviceData(data); // 状態に設定
    } catch (err) {
      console.error('Error fetching advice:', err);
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (slackUserId && startDate && endDate) {
      fetchAdviceData();
    }
  }, [slackUserId, startDate, endDate]);

  return { adviceData, loading, error, fetchAdvice: fetchAdviceData };
}
