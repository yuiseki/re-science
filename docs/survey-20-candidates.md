# 20候補の現状調査

INITIAL_PROMPT.md の第1層にある20候補について、既に誰がどこまで調べているか、公開データは何か、結果を AI 自身と独立に確かめる評価器があるかを調べた。

調査日は 2026-11-23。

## 読み方と限界

- 根拠は Web 検索の表題と抜粋である。本文まで読んだのは 7 の Lost and Found 論文 (arXiv:2511.19016) だけで、ほかは抜粋から読み取れる範囲にとどまる
- 「混み具合」は論文数を数えた値ではない。検索の上位に、同じ問いを大規模に解いた研究や専用の基盤モデルが出てくるかどうかで判断した
- 20 は検索していない
- 二次情報 (報道やブログ) だけが根拠のものは、その旨を書いた

## 一覧

混み具合は「高」が既に大きな研究グループや企業が同じ問いを大規模に解いている、「低」がそうした研究が検索で見つからないことを指す。

| # | 候補 | 混み具合 | 既にあるもの | 公開データ | 独立した評価器 |
|---|------|----------|--------------|------------|----------------|
| 1 | 菌類の未知種 | 中 | UNITE の species hypothesis (SH) が DNA だけの分類群に識別子を与え、GBIF に載せている。2026 年に ITS メタバーコーディングの新規性判定を較正するプレプリントが出た | UNITE のリリース、GBIF | 過去のリリースで名前の無かった SH が後に記載されたかを、時点で分けて確かめられる |
| 2 | 微生物の暗黒物質 | 高 | 全球メタゲノムからタンパク質ファミリーを4倍にした研究 (NAR 2026)、1.3 テラ塩基対を扱うゲノム言語モデル (bioRxiv 2026-10)、酵素機能予測の研究が続く。約950体のエージェントが逆転写酵素を探索したという報道もある (二次情報) | MGnify、IMG/M、SRA | 既知系統の再発見はできる。新機能の確定は実験が要る |
| 3 | 小型無脊椎動物 | 中 | 土壌節足動物の大半は参照ライブラリ不足で同定できないという報告、BarcodeBERT、メガバーコーディングとメタバーコーディングの統合 (2026) | BOLD | 弱い。記載には形態を見る専門家が要る |
| 4 | 海洋生物の分布 | 高 | OBIS 自身が種分布モデルを公開し 2026 年に GBIF の賞を受けた。観測空白の定量 (Nat. Commun. 2026)、12,039 種の分布図 (Sci. Data 2026) | OBIS、GBIF | 後年の出現記録で時点を分けて確かめられる |
| 5 | 植物の古い標本 | 高 | 800万枚の標本画像から全球の開花時期の変化を推定した研究 (New Phytol. 2026)、レビュー多数、ラベル読み取りの自動化 | GBIF の標本画像 (1.2 億点)、iDigBio | 専門家が確認した同定データを集める手順が 2026 年に出ている |
| 6 | 自然界の環境音 | 鳥は高、昆虫と水中は中 | Perch 2.0、BirdNET の埋め込みで未知の音クラスを探す研究、直翅目の分類器 (2026)、水中音の未知音を検出対象に昇格させる手順 (2026) | Xeno-canto、各地の録音アーカイブ | 弱い。未知の音の正体は現地確認が要る |
| 7 | 未発見の天文現象 | 高 | Fink の TDE 検出モジュールと Lost and Found (19件の核過渡現象)、Lasair を使う異常検知 AHA (2026)、ePESSTO+ の核過渡現象の全数調査 (2026-10) | Fink、ALeRCE、Lasair、ANTARES の API、ZTF の公開データ | 強い。見落とし事例の一覧があり、TNS の分類と突き合わせられる |
| 8 | 系外惑星 | 高 | RAVEN (100超を検証、2,000超の候補)、単発トランジットの ExoVeil、北天連続観測域の COUNTESS。個人が 2 分ケイデンスで観測されなかった近傍星 526 個を調べ、候補を 2 つ出した例もある | MAST の TESS 全画像 | 強い。既知の惑星と偽陽性の一覧、注入回収試験 |
| 9 | 重力波 | 中 | GWAK、MADGRAV (2026-09)、O4a のグリッチを教師なしで探す DANTE (2026)。O4b は 2026-05 に公開 | GWOSC | 検出器間の同時性。新信号の主張は基準が非常に高い |
| 10 | 微小地震 | 高、ただし地域ごとに未処理が残る | PhaseNet、南カリフォルニアのテンプレートマッチング (181万件)、Quake Neural Operator (2026) | EarthScope (旧 IRIS)、NCEDC、SCEDC | 既存カタログとの一致と、テンプレートマッチングでの相互確認 |
| 11 | 海洋の過去の観測 | 中 | WOD23 のデータ論文 (Sci. Data 2026)、9,000万プロファイルのクラウド最適化 (2026-06)、機械学習による品質管理 | World Ocean Database (AWS の公開レジストリにもある) | 重複観測や CCHDO の高品質観測との比較 |
| 12 | 地盤の微小変動 | 中 | 欧州の EGMS、北米の OPERA DISP-S1、ノルウェーの国営サービス。変動域の自動抽出はルールベースの作業報告 (2026) がある | EGMS、OPERA DISP-S1、Sentinel-1 | 地すべり台帳や水準測量、GNSS |
| 13 | 小規模湿地 | 高 | 30m の衛星データで 1.6 億個の小規模湿地を数え、湿地メタンの 24% と推定した研究 (Nat. Clim. Change 2026) が主要な問いを回収した | Landsat、Sentinel-2 | 現地のフラックス観測 |
| 14 | 未同定の化学物質 | 高 | DreaMS (2 億スペクトル)、5.2 億スペクトルから作った suspect library、薬物代謝物を対象にしたエージェント (2026) | GNPS/MassIVE、MetaboLights | MassSpecGym などのベンチマーク。構造の確定は標品が要る |
| 15 | 化学反応の失敗 | 中 | ORD、ORDerly、反応条件最適化の RxnOptBench (2026-10)、実現可能性の FREA (751 反応、2026-10)、収率予測の作法をまとめた論文 | Open Reaction Database。失敗を含むのは少数の HTE データに偏る | 取っておいた実験の予測。新しい条件の検証は実験が要る |
| 16 | 材料の合成可能性 | 中から高 | GNoME の重複や自明な変種を指摘する論文 (2026)、不純物相つきの固相合成データ (2025)、レビュー | Materials Project、GNoME、テキストマイニングの合成レシピ | 弱い。合成の成否は実験が要る |
| 17 | 古い地質調査記録 | 抽出は高、統合は地域ごとに未着手 | StratumGPT、フランドルのボーリング記述の分類、スロベニアの坑井記録、産業向けの抽出サービス | 各国の地質調査所のアーカイブ | 近くの新しいボーリングや物理探査との比較 |
| 18 | 歴史的な気象・生物記録 | 欧米は中、日本語は低 | 手書きの気象記録を読む MeteoSaver (2026)、英国気象庁の 5,400万件、EGU のデータレスキュー分科会。日本の生物季節の記録は言語とデジタル化の障壁で使われていないという指摘がある (Data 2026) | NOAA の気象日誌、各国の気象官署の記録 | 重なる期間の機器観測、近隣地点との整合 |
| 19 | 未形式化の数学 | 高 | Tau Ceti、Paper2Lean (2026-11)、AIProver (2026-10)、Formal Conjectures、Aristotle、AlphaProof | mathlib、Formal Conjectures | 最も強い。Lean のカーネルが検証する。ただし命題の形式化が正しいかは別の問題として残る |
| 20 | 真菌感染症・薬剤耐性 | 未調査 | | | |

## 読み取れること

- 評価器が強い候補ほど混んでいる。7、8、19 は検証が機械的にできるため、専用の基盤や企業の参入が進んでいる
- 混んでいても、個人が成果を出した例はある。8 では「2 分ケイデンスで観測されなかった近傍星」という、既存の探索が対象から外していた標本を選んでいた。空きは分野の単位ではなく、既存の手順が対象から外した部分集合の単位で残る
- 13 は、INITIAL_PROMPT.md が候補に挙げた問いそのものが 2026 年の論文で回収されている。候補から外す
- 空きの信号がはっきりしているのは 18 の日本語資料である。障壁が言語とデジタル化にあると、当の分野の論文が書いている
- 12 と 17 は、製品や抽出手法は公開されているのに、全域をなめて台帳と突き合わせる作業が地域ごとに残っている

## PoC の対象

INITIAL_PROMPT.md の第3層 A (Fink/ZTF) から始める。

- Lost and Found が、Fink の TDE 分類器と目視で見つけた23天体 (核過渡現象19、超新星候補4) を表にしている。これを正解表にできる
- Fink の API は認証なしで光度曲線を返す。1天体は数十 KB で、計算資源をほとんど使わない
- 問いは「新しい現象を見つける」ではなく「この23天体は、どれだけの目視の予算があれば拾えたか」に置く。背景の天体と混ぜて単純な特徴量で順位をつけ、正解表が上位何 % に入るかを測る

この PoC が示せるのは再発見の効率までである。新しい候補を出す段階に進むには、TNS との照合と、Fink が既に走らせている分類器との差を調べる必要がある。

## 出典

- 1: https://reader.openrxivlabs.org/content/10.64898/2026.07.29.741524v2 、https://pubmed.ncbi.nlm.nih.gov/37953409
- 2: https://academic.oup.com/nar/article/54/18/gkag938/8840863 、https://biorxiv.org/content/10.64898/2026.10.21.760802v1.full.pdf
- 3: https://academic.oup.com/cz/article/70/5/637/7453492 、https://arxiv.org/html/2311.02401v2 、https://onlinelibrary.wiley.com/doi/10.1111/1755-0998.70166
- 4: https://obis.org/2026/09/30/sdm-enc26/ 、https://link.springer.com/article/10.1038/s41467-026-73613-z
- 5: https://nph.onlinelibrary.wiley.com/doi/full/10.1111/nph.70139 、https://nph.onlinelibrary.wiley.com/doi/full/10.1002/ppp3.70149
- 6: https://frontiersin.org/journals/ecology-and-evolution/articles/10.3389/fevo.2024.1409407/full 、https://arxiv.org/html/2606.13236
- 7: https://arxiv.org/abs/2511.19016 、https://arxiv.org/html/2602.12955 、https://arxiv.org/html/2610.18633v1
- 8: https://arxiv.org/abs/2603.22597 、https://arxiv.org/html/2606.02778v1 、https://github.com/paraschopra/tess-planet-candidates
- 9: https://arxiv.org/html/2609.39583 、https://arxiv.org/html/2607.18136v3 、https://gwosc.org/news/o4b-open-data-release/
- 10: https://github.com/AI4EPS/PhaseNet 、https://pmc.ncbi.nlm.nih.gov/articles/PMC13338072
- 11: https://nature.com/articles/s41597-026-06957-2.pdf 、https://earthmover.io/blog/aquaview-wod-ocean-profiles/
- 12: https://land.copernicus.eu/en/products/european-ground-motion-service 、https://www.earthdata.nasa.gov/data/projects/opera
- 13: https://ideas.repec.org/a/nat/natcli/v16y2026i5d10.1038_s41558-026-02609-w.html
- 14: https://link.springer.com/content/pdf/10.1038/s41587-025-02663-3.pdf 、https://pmc.ncbi.nlm.nih.gov/articles/PMC10733301 、https://pmc.ncbi.nlm.nih.gov/articles/PMC13320852
- 15: https://arxiv.org/pdf/2610.02242v1 、https://arxiv.org/html/2610.06614v1 、https://pmc.ncbi.nlm.nih.gov/articles/PMC13449950
- 16: https://arxiv.org/html/2610.13885 、https://doi.org/10.48550/arxiv.2606.30967 、https://pmc.ncbi.nlm.nih.gov/articles/PMC12717135
- 17: https://ui.adsabs.harvard.edu/abs/2026TUSTI.17808013Y/abstract 、https://arxiv.org/html/2407.10991v1
- 18: https://gmd.copernicus.org/articles/19/3213/2026 、https://www.mdpi.com/2306-5729/11/9/212
- 19: https://arxiv.org/abs/2611.26272 、https://doi.org/10.48550/arxiv.2610.05367 、https://arxiv.org/html/2605.13171v1
