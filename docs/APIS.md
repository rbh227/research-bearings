# Sources and keys

Every index the retrieval script talks to, what it is used for, the environment
variable that unlocks it, where to get that, and the one-line test that
`snowball.py status` runs. **No key is required.** Every source degrades to
something the script can still use, and `status` says which state you are in.

Written 2026-09-15, when the script grew from one index to four resolvers and
seven probes. Rate limits are the operators' published figures on that date and
are the kind of fact that goes stale; the script's own spacing is in
`scripts/retrieval/snowball.py` next to each resolver.

## The three states

| State | Means |
|---|---|
| `connected` | The one-line test answered, and the credential the source takes is present (or the source takes none). |
| `connected-no-key` | The one-line test answered, but the credential is missing. The source still works, at the unkeyed rate, or a subset of it works. Never an error. |
| `not connected` | The one-line test did not answer: no network, a changed endpoint, or a rejected credential. |

## Sources

### Semantic Scholar (`s2`)

- **Used for:** keyword search, paper metadata by id, references and citations
  with the citing sentence, `influentialCitationCount`. The primary index.
- **Env:** `S2_API_KEY`, sent as the `x-api-key` header. Also read: the older
  `SEMANTIC_SCHOLAR_API_KEY`, and one line in `~/.config/research-bearings/s2-api-key`.
- **Where:** <https://www.semanticscholar.org/product/api#api-key-form>. Free,
  approval takes days.
- **Rate:** 1 request per second with a key, and the script spaces to that.
  Without a key you share one pool with everyone else unkeyed, and 429s arrive
  after two or three calls; the script backs off with full jitter, five attempts,
  and reports what it got.
- **Without it:** `search` still returns rows, from OpenAlex; `verify` still
  resolves, through OpenAlex and Crossref; `neighborhood` loses the citing
  sentences and the influential flag.
- **Test:** `GET https://api.semanticscholar.org/graph/v1/paper/search?query=xbd&limit=1`

### OpenAlex (`openalex`)

- **Used for:** keyword search, `cited_by_count`, `referenced_works`, and
  works citing a given work (`filter=cites:`). The second index, and the one
  that answers when Semantic Scholar is rate-limiting.
- **Env:** `OPENALEX_MAILTO` (any email; puts you in the polite pool) and
  `OPENALEX_API_KEY` (optional, from your OpenAlex account).
- **Where:** <https://openalex.org> — an email is enough; the key is from the
  account settings page.
- **Rate:** 10 requests per second, 100,000 per day, free. The polite pool is
  faster and more reliable than the anonymous one.
- **Without it:** works fully, anonymous pool.
- **Test:** `GET https://api.openalex.org/works?search=xbd&per-page=1`

### Crossref (`crossref`)

- **Used for:** DOI lookup, `is-referenced-by-count`, issued and created dates,
  container title. The record of publication, used to confirm a title exists
  when neither index has it.
- **Env:** `CROSSREF_MAILTO` (any email; polite pool). No key exists.
- **Where:** nothing to sign up for.
- **Rate:** polite pool is 50 requests per second; the script never approaches it.
- **Without it:** works fully, anonymous pool.
- **Test:** `GET https://api.crossref.org/works/10.3390/rs12223808` (xBD itself has a DataCite DOI, which Crossref does not hold; that is why the probe uses a journal DOI)

### arXiv (`arxiv`)

- **Used for:** category and date-window search, abstracts, PDF links. The only
  index here that returns full abstracts for everything it holds.
- **Env:** none. There is no key.
- **Rate:** one request every 3 seconds, by arXiv's terms; the script enforces
  the spacing across processes with a timestamp file in the cache directory.
- **Test:** `GET https://export.arxiv.org/api/query?search_query=all:xbd&max_results=1`

### Unpaywall (`unpaywall`)

- **Used for:** the open-access location of a DOI, when a skill needs the PDF.
  Probed by `status`; no verb uses it yet.
- **Env:** `UNPAYWALL_EMAIL`. Required by the API on every call.
- **Where:** <https://unpaywall.org/products/api> — an email is the whole signup.
- **Rate:** 100,000 per day.
- **Without it:** `connected-no-key`: the endpoint answers but refuses every
  lookup until an email is set.
- **Test:** `GET https://api.unpaywall.org/v2/10.1184/R1/8135576.V1?email=$UNPAYWALL_EMAIL`

### Hugging Face papers (`huggingface`)

- **Used for:** the daily-papers index and which models and datasets cite an
  arXiv id. Probed by `status`; no verb uses it yet.
- **Env:** `HF_TOKEN`, sent as a bearer token.
- **Where:** <https://huggingface.co/settings/tokens>. A read token.
- **Without it:** the papers endpoints answer anonymously at a lower rate.
- **Test:** `GET https://huggingface.co/api/papers/search?q=xbd`

### Zotero (`zotero`)

- **Used for:** reading the user's own library, so a later skill can say which
  of the papers it found you already have. Probed by `status`; no verb uses it yet.
- **Env:** `ZOTERO_API_KEY` (header `Zotero-API-Key`) and `ZOTERO_USER_ID`.
- **Where:** <https://www.zotero.org/settings/keys> — both the key and your
  numeric user id are on that page.
- **Without it:** `connected-no-key`: the API root answers; nothing in the
  library can be read.
- **Test:** `GET https://api.zotero.org/users/$ZOTERO_USER_ID/items?limit=1`
  (with the header), or `GET https://api.zotero.org/` when there is no key.

## Which keys help most

In this order, because each one changes what the script can do:

1. `S2_API_KEY` — the primary index stops rate-limiting, and `neighborhood`
   gets the citing sentences and the influential flag.
2. `OPENALEX_MAILTO` — polite pool on the index that carries the load when
   Semantic Scholar is throttling. Costs an email.
3. `CROSSREF_MAILTO` — polite pool on the DOI record. Costs the same email.

`status` prints the top three that are missing, with these links, as
`suggest`. `/setup` copies that into `research/CONNECTIONS.md` and stops. It
never asks you to go and get one.

## Cache

Every resolver's raw responses are cached under `~/.cache/research-bearings/<resolver>/`,
keyed by the query, for 30 days. Override the root with `RESEARCH_CACHE_DIR`.
`status` never reads the cache: it is the one verb whose job is to hit the wire.

## Where web search is allowed

`WebSearch` and `WebFetch` are not sources. They are allowed in exactly two
places: the `searcher` agent, as a last resort when every index above returns
nothing, with the results labelled web-only and unverified until `verify`
resolves them; and `/scout`, to read a page one of the indexes pointed at.
Nowhere else. The write-scope guard denies `WebSearch` and `WebFetch` to every
other agent this plugin ships.
