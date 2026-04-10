---
layout: default
title: スキルシート
---

<!--
いらすとや イラスト利用（ライセンス・出典メモ）
- 作品名: やんのかステップのイラスト（サバトラ）
- 掲載ページ: https://www.irasutoya.com/2024/03/blog-post_20.html
- サイト側の説明: 掲載イラストは無料で利用できるが著作権は放棄されていない。
  ご利用について https://www.irasutoya.com/p/terms.html および FAQ を確認のうえ、規約の範囲内で利用すること。
-->

# S・N

<figure class="irasutoya-figure" style="max-width: 320px; margin: 1rem auto;">
  <img
    src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiDwZgnq1aQiO4rfOQb6WMJO-8uIstS7_oQpxmR2q6nEcGNmN8TlKbmBvDCiBrc8WXsqmwaHKNDNdCYvg85k0DuZvOSRy3fD3K2fQd8XvUwMAU_qVo4Izyp3TD0ctoBVprX6FbroZmzevkD1Ozq2DTDZIdKhJP4i50uzD0Lt6ZkSiiBu0-eLGeMjg00-Urt/s701/cat_yannnoka_step_cha.png"
    alt="やんのかステップのイラスト"
    width="320"
    loading="lazy"
    decoding="async"
  />
  <figcaption style="font-size: 0.85rem; margin-top: 0.5rem; text-align: center;">
    イラスト出典:
    <a href="https://www.irasutoya.com/2024/03/blog-post_20.html" rel="noopener noreferrer">いらすとや</a>
    「やんのかステップのイラスト」
  </figcaption>
</figure>

職務用スキルシートの本文は、次のリンクからご覧ください。

{% assign ss = site.data.skill_sheet %}
{% assign gh_branch = site.github.default_branch %}
{% if gh_branch == nil or gh_branch == "" %}
{% assign gh_branch = "main" %}
{% endif %}
{% comment %} site.github.* が空だと相対リンク化され tree/ファイル名 扱いで 404 になるため、blob は絶対 URL で組む {% endcomment %}
**[スキルシート全文（Markdown）](https://github.com/snklab77/my-skill-sheet/blob/{{ gh_branch }}/{{ ss.file }})**
