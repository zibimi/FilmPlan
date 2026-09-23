# Metadata Research

## Search Order

For every unresolved single film:

1. Use Google/web search for discovery with the existing title plus `豆瓣`; replace dots with spaces. Add director, year, country, or language when ambiguous.
2. Open the matching Douban subject page when available. Prefer its Chinese title, foreign/original title, year, director, and alternate titles.
3. Check IMDb for original title, year, director, runtime, and same-title disambiguation.
4. Cross-check TMDb or an authoritative national archive, film institute, festival, distributor, BFI, Criterion, MUBI, Letterboxd, Wikipedia, or another credible source.
5. Use specialist databases when appropriate: HKMDB, Taiwan film archives, Bangumi, or TheTVDB.

Search snippets are discovery evidence, not enough by themselves when ambiguous.

## Query Tactics

- Chinese filename: `导演名 中文名 豆瓣`.
- Foreign filename: convert `Title.Words` to `Title Words`, then search `Title Words year 豆瓣`.
- No Douban hit: confirm original title/director in IMDb or an archive, then retry Douban using that title.
- Japanese film without English: keep the established Japanese title, kana, romanization, or Chinese title; English is not mandatory.
- Slavic/accented titles: try normalized ASCII and native spelling, but preserve the established original title when practical.

## Confidence

Execute automatically only at 80 percent confidence or above and when the request authorizes filesystem changes.

High confidence normally requires exact source-title match, compatible year, matching director/country/language/plot/cast/runtime, no plausible competing version, and a reliable Chinese title or explicitly authorized translation.

Keep `review` when the filename is generic, the version is unclear, sources conflict, or a number may be a broadcast date. Record source URLs, confidence, reason, and translation decisions. Research never marks a proposal executed.

## Media Type

Distinguish feature/short film, documentary, concert, stage/musical recording, TV episode/series, and extra/interview/commentary/video essay before applying naming semantics. Concert and stage recordings may use a user-supplied or cautious translated Chinese rendering plus performer/work/venue and a deliberately chosen year.
