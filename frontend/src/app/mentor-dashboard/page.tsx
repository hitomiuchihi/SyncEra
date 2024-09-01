// 画面拡張用として作成（※今後、役職別の画面切り替え時に使用のため、開発環境残し、本番には載せない）
// src/app/manager-dashboard/page.tsx
'use client';

import LogoutButton from '@/components/signup_and_login/LogoutButton';
import app from '@/firebase/config'; // Firebase 初期化ファイルをインポート
import clientLogger from '@/lib/clientLogger';
import { getAuth, onAuthStateChanged, User } from 'firebase/auth';
import { doc, getDoc, getFirestore } from 'firebase/firestore';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import Loading from '../../components/loading';
export default function ManagerDashboard() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();
  useEffect(() => {
    const auth = getAuth(app);
    const currentUser = auth.currentUser;

    if (!currentUser) {
      router.push('/login/employee');
    }
  }, [router]);
  useEffect(() => {
    const auth = getAuth(app); // Firebase 認証オブジェクトを取得
    const db = getFirestore(app);
    const unsubscribe = onAuthStateChanged(auth, async (currentUser) => {
      if (currentUser) {
        setUser(currentUser);
        try {
          // カスタムクレームを取得
          const idTokenResult = await currentUser.getIdTokenResult(true);
          const companyId = idTokenResult.claims.companyId;

          if (!companyId) {
            router.push('/login/employee');
            return;
          }

          clientLogger.debug(`Company ID: ${companyId}`);
          // Firestoreからのデータ取得
          const userDoc = await getDoc(
            doc(db, `companies/${companyId}/employees`, currentUser.uid),
          );
          if (userDoc.exists()) {
            const userData = userDoc.data();
            clientLogger.debug(`User data:, ${JSON.stringify(userData)}`);

            // 確認: role や companyId が期待通りに存在しているか
            if (userData?.role && userData?.companyId) {
              if (userData.role !== 'mentor') {
                router.push(
                  userData.role === 'manager' ? '/manager-dashboard' : '/employee-dashboard',
                );
              }
            } else {
              clientLogger.error(
                `Role or Company ID is missing in user data:,${JSON.stringify(userData)}`,
              );
              router.push('/login/employee');
            }
          } else {
            clientLogger.error('=========ユーザーデータが見つかりません。=======');
            router.push('/login/employee');
          }
        } catch (error) {
          clientLogger.error(`Error fetching user data:,${error}`);
          router.push('/login/employee');
        }
      } else {
        router.push('/login/employee');
      }
      setLoading(false);
    });

    return () => unsubscribe();
  }, [router]);

  if (loading) {
    return <Loading />;
  }

  if (!user) {
    return '予期せぬ操作が発生しました！'; // 適切なエラーメッセージを表示
  }
  // ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝ここまで認証残し＝＝＝＝＝＝＝
  return (
    <div className='text-[25px] text-[#003366]'>
      <h1>mentorダッシュボード!</h1>
      <p>ようこそ、{user.email}さん</p>
      <p>役職別で画面を変更</p>
      {/* ログアウト機能を追加 */}

      <div>
        <Link href='/'>戻る</Link>
      </div>
      <div>
        <LogoutButton />
      </div>
    </div>
  );
}
