# yaseru

デブ脱出プロジェクト

<img width="1340" alt="daf0f0897db28611ae6d10df21da2b8c" src="https://user-images.githubusercontent.com/760627/75547787-121d4800-5a6f-11ea-95b1-bd4c159a3246.png">

## 概要

2019年12月、体重が106キロあってさすがに豚みたいだったので、一念発起してダイエットをはじめました。

目標は、40キロ体重を落として65キロになることです。

エンジニアらしく、データエンジニアリングしながらダイエットします。
具体期にはFitbitなどのデバイスからはライフログを収集して、分析、可視化していきます。

## ChangeLog(抜粋)

* 2020/09/13 70kg以下達成
* 2020/08/18 75kg以下達成
* 2020/06/06 80kg以下達成
* 2020/04/15 85kg以下達成
* 2020/03/21 90kg以下達成
* 2020/01/29 95kg以下達成
* 2020/01/07 100kg以下達成
* 2019/12/01 ダイエット開始

more: [here](https://github.com/tsu-nera/yaseru/blob/master/CHANGELOG.md)

## 分析結果

現在はcsvで保存したデータをJupyte Notebookで分析しています。

* https://github.com/tsu-nera/yaseru/blob/master/notebooks/weights_analysis.ipynb

また、csvデータをGoogle BigQueryにアップロードして、Googleデータポータルで可視化しています。

* https://datastudio.google.com/u/0/reporting/f4bdd119-b10f-4e80-b4a3-49d50a1901ce/page/26gGB

## データ取得項目

* 体重
* BMI
* 体脂肪率
* 筋肉量
* 内臓脂肪レベル
* 基礎代謝量
* 体内年齢
* 推定骨量
* 消費カロリー
* 摂取カロリー
* 運動カロリー
* サイクリング走行距離
* サイクリング走行時間

## データ取得元

* [Fitbit](https://www.fitbit.com/)
* [HealthPlanet(タニタ)](https://www.healthplanet.jp/)
* [MyFitnessPal](https://www.myfitnesspal.com/ja/)

## References

* [Fitbit Developper](https://dev.fitbit.com)
* [Fitbit API Reference](https://dev.fitbit.com/build/reference/web-api/)
* [python-fitbit](https://github.com/orcasgit/python-fitbit)
* [Health Planet API仕様書 Ver1.0](https://www.healthplanet.jp/apis/api.html)
* [あすけん](https://www.asken.jp/)
