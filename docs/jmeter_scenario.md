# 負荷テスト
```txt
主要なエンドポイントに対して、どのくらいの負荷をかけるとエラーが発生しやすくなるかを検証した。
今回はDBに保存されたデータをGETする処理のみを検証しており、POSTする処理については未検証。
```

## テスト結果概要
**📍エンドポイント: /client/all_employee/**

テスト条件:
- スレッド数: 1000
- リクエスト数: 1000
- テスト時間: 30秒

結果：
- 平均応答時間: 91ミリ秒
- 最小応答時間: 2ミリ秒
- 最大応答時間: 1095ミリ秒
- エラー率: 0.00%
***
**📍エンドポイント: /client/print_all_summary_reports/sample_4/**

テスト条件:
- スレッド数: 1
- リクエスト数: 100
- テスト時間: 約1分36秒

テスト結果
- 平均応答時間: 18089 ms
- 最小応答時間: 6 ms
- 最大応答時間: 36161 ms
- エラー率: 55.00%

備考:
- サーバー負荷が高くなり始めるのは、リクエスト数が50を超えた時点から
- リクエスト数が100に達するにつれて、応答時間が急激に増加し、エラー率も高まる
- 最大応答時間は36161 msに達し、エラー率は55%
- リクエスト数が増えるにつれてサーバーの負荷が急激に上がり、エラーが多発する傾向
```bash
jmeter  | summary +      6 in 00:00:03 =    1.9/s Avg:   124 Min:     6 Max:   393 Err:     0 (0.00%) Active: 1 Started: 6 Finished: 5
jmeter  | summary +     50 in 00:01:00 =    0.8/s Avg:  7930 Min:     8 Max: 30095 Err:    11 (22.00%) Active: 45 Started: 100 Finished: 55
jmeter  | summary =     56 in 00:01:03 =    0.9/s Avg:  7093 Min:     6 Max: 30095 Err:    11 (19.64%)
jmeter  | summary +     40 in 00:00:30 =    1.3/s Avg: 31684 Min: 30010 Max: 36161 Err:    40 (100.00%) Active: 5 Started: 100 Finished: 95
jmeter  | summary =     96 in 00:01:33 =    1.0/s Avg: 17340 Min:     6 Max: 36161 Err:    51 (53.12%)
jmeter  | summary +      4 in 00:00:02 =    1.7/s Avg: 36083 Min: 36075 Max: 36095 Err:     4 (100.00%) Active: 0 Started: 100 Finished: 100
jmeter  | summary =    100 in 00:01:36 =    1.0/s Avg: 18089 Min:     6 Max: 36161 Err:    55 (55.00%)
jmeter  | Tidying up ...    @ August 26, 2024 5:36:02 AM CEST (1724643362997)
```
***
**📍エンドポイント: /client/print_all_career_survey_results/sample_4/**

テスト条件:
- スレッド数: 1
- リクエスト数: 100
- テスト時間: 約1分36秒

テスト結果:
- 平均応答時間: 16139 ms
- 最小応答時間: 5 ms
- 最大応答時間: 36084 ms
- エラー率: 48.00%

備考:
- サーバー負荷が高くなり、エラー率が増加し始めるのは、リクエスト数が約60を超えた時点。
- 特に、リクエスト数が100を超えた際には、応答時間が大幅に増加し、エラー率が急上昇。
- 最大応答時間が30000 msを超え、エラー率が50%近くに達している。
```bash
jmeter  | summary +     18 in 00:00:13 =    1.4/s Avg:   480 Min:     5 Max:  2471 Err:     0 (0.00%) Active: 5 Started: 22 Finished: 17
jmeter  | summary +     28 in 00:00:29 =    1.0/s Avg:  1358 Min:     9 Max: 15066 Err:     0 (0.00%) Active: 21 Started: 71 Finished: 50
jmeter  | summary =     46 in 00:00:42 =    1.1/s Avg:  1014 Min:     5 Max: 15066 Err:     0 (0.00%)
jmeter  | summary +     22 in 00:00:28 =    0.8/s Avg: 25374 Min: 11497 Max: 30035 Err:    16 (72.73%) Active: 33 Started: 100 Finished: 67
jmeter  | summary =     68 in 00:01:10 =    1.0/s Avg:  8895 Min:     5 Max: 30035 Err:    16 (23.53%)
jmeter  | summary +     32 in 00:00:25 =    1.3/s Avg: 31532 Min: 30011 Max: 36084 Err:    32 (100.00%) Active: 0 Started: 100 Finished: 100
jmeter  | summary =    100 in 00:01:36 =    1.0/s Avg: 16139 Min:     5 Max: 36084 Err:    48 (48.00%)
```
***
**📍エンドポイント:client/print_all_advices/sample_4/**

テスト条件:
- スレッド数: 1
- リクエスト数: 100
- テスト時間: 約2分9秒

結果：
- 平均応答時間: 8035 ms
- 最小応答時間: 5 ms
- 最大応答時間: 30072 ms
- エラー率: 25.00%

備考:
- サーバー負荷が高くなるのは、リクエスト数が50を超えた時点から。
- リクエスト数が100に達する頃には、応答時間が急激に増加し、エラー率も高まる。
- 最大応答時間は30072 msに達し、エラー率は25%。
```bash
jmeter  | summary +     14 in 00:00:13 =    1.1/s Avg:    38 Min:    10 Max:   119 Err:     0 (0.00%) Active: 1 Started: 14 Finished: 13
jmeter  | summary +     30 in 00:00:30 =    1.0/s Avg:   150 Min:     6 Max:  1992 Err:     0 (0.00%) Active: 1 Started: 44 Finished: 43
jmeter  | summary =     44 in 00:00:43 =    1.0/s Avg:   114 Min:     6 Max:  1992 Err:     0 (0.00%)
jmeter  | summary +     28 in 00:00:32 =    0.9/s Avg:  1493 Min:     5 Max:  6046 Err:     0 (0.00%) Active: 2 Started: 76 Finished: 74
jmeter  | summary =     72 in 00:01:15 =    1.0/s Avg:   651 Min:     5 Max:  6046 Err:     0 (0.00%)
jmeter  | summary +      4 in 00:00:30 =    0.1/s Avg:  9025 Min:   980 Max: 30072 Err:     1 (25.00%) Active: 25 Started: 100 Finished: 75
jmeter  | summary =     76 in 00:01:45 =    0.7/s Avg:  1091 Min:     5 Max: 30072 Err:     1 (1.32%)
jmeter  | summary +     24 in 00:00:24 =    1.0/s Avg: 30023 Min: 30010 Max: 30064 Err:    24 (100.00%) Active: 0 Started: 100 Finished: 100
jmeter  | summary =    100 in 00:02:09 =    0.8/s Avg:  8035 Min:     5 Max: 30072 Err:    25 (25.00%)
jmeter  | Tidying up ...    @ August 26, 2024 6:01:56 AM CEST (1724644916515)
jmeter  | ... end of run
jmeter exited with code 0
```