# re-science

既に観測・保存されているのに人間が調べきれていない科学データへ、AI の注意を向ける実験の置き場。

出発点は [INITIAL_PROMPT.md](INITIAL_PROMPT.md) の幅優先探索である。そこに挙がった候補を、次の4条件で絞っていく。

- 人間が調べていない候補が大量にある
- 仮説を安く作れて、何度も試せる
- 結果を AI 自身とは独立した方法で確かめられる
- 正しかったとき、既存の知識を実際に更新できる

## 中身

- [docs/survey-20-candidates.md](docs/survey-20-candidates.md): 20候補それぞれについて、既にある研究、公開データ、評価器を調べた結果
- [docs/procedure.md](docs/procedure.md): 分野を問わず使う5段の手順
- [docs/geoai-skills-for-astronomy.md](docs/geoai-skills-for-astronomy.md): GeoAI-master-skills の手法を天文学にどこまで使えるかの検討
- [poc/ztf-rediscovery/](poc/ztf-rediscovery/): ZTF のアーカイブで見落とされていた現象を、どれだけの目視の予算で拾い直せるかを測る PoC
- [poc/jp-historical-records/](poc/jp-historical-records/): 同じ手順を日本の歴史的な気象記録で走らせた2回目。気象庁が均質でないと印を付けた官署の年を、年平均気温だけで拾い直せるかを測った

## 進め方

新しい現象を探す前に、既に見つかっている見落とし事例を再現できるかを測る。再現できない手順が出した「発見」は、偽陽性と区別がつかないためである。

評価に使う正解表を見てから手順を調整しない。スコアやしきい値は、正解表のデータを取得する前にコミットする。
