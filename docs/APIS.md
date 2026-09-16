# Sources and keys

Every index the retrieval script talks to, what it is used for, the environment
variable that unlocks it, where to get that, and the one-line test that
`snowball.py status` runs. **No key is required.** Every source degrades to
something the script can still use, and `status` says which state you are in.

Written 2026-09-15, when the script grew from one index to four resolvers and
seven probes. Extended 2026-09-16 with GitHub and OpenReview, for the reading
milestone's dataset ledger and review notes: nine sources now. Rate limits are
the operators' published figures on those dates and are the kind of fact that
goes stale; the script's own spacing is in `scripts/retrieval/snowball.py` next
to each resolver, and the reading-side verbs are in `papers.py` beside it.

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
  Read by `papers.py fetch`, after the index PDF and arXiv and before giving
  up. Without the email, a paper whose only open copy is neither on arXiv nor
  named by an index comes back `no text`, and `/read` skims it from the
  abstract.
- **Env:** `UNPAYWALL_EMAIL`. Required by the API on every call.
- **Where:** <https://unpaywall.org/products/api> — an email is the whole signup.
- **Rate:** 100,000 per day.
- **Without it:** `connected-no-key`: the endpoint answers but refuses every
  lookup until an email is set.
- **Test:** `GET https://api.unpaywall.org/v2/10.1184/R1/8135576.V1?email=$UNPAYWALL_EMAIL`

### Hugging Face papers (`huggingface`)

- **Used for:** the hub's dataset search, by `papers.py datasets`: licence,
  size category, modality, splits, downloads. The daily-papers index is probed
  and not used. Without the token the same endpoints answer at a lower rate.
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

### GitHub (`github`)

- **Used for:** the repository behind a dataset, by `papers.py datasets`:
  licence, stars, last push, description. Reached over the REST API, **never
  the `gh` command** — the guard admits only this plugin's retrieval scripts in
  Bash, and widening that fence for one agent is a worse trade than one more
  HTTP call.
- **Env:** `GITHUB_TOKEN`, sent as a bearer token. Any classic token with no
  scopes is enough; nothing here reads private data.
- **Where:** <https://github.com/settings/tokens>
- **Rate:** 10 searches a minute unauthenticated, 30 with a token.
- **Without it:** works, at the lower rate.
- **Note:** search has no idea what field you are in. Measured 2026-09-16, a
  bare "xBD" returns an Xbox diagnostic tool above the xView2 solution, which
  is why the verb takes `--context` and appends it to the GitHub query only.
- **Test:** `GET https://api.github.com/rate_limit`

### OpenReview (`openreview`)

- **Used for:** a paper's reviews, ratings, author responses and decision, by
  `papers.py reviews`.
- **Env:** `OPENREVIEW_USERNAME` and `OPENREVIEW_PASSWORD`, exchanged for a
  bearer token at `/login`.
- **Where:** <https://openreview.net/signup> — a free account.
- **Without it:** partly. **Measured 2026-09-16: `/notes/search` answers
  anonymously and `/notes?forum=<id>` returns `ChallengeRequiredError`, a bot
  challenge, on both `api.openreview.net` and `api2.openreview.net`.** So
  without credentials the verb finds the submission and returns its venue,
  decision field and url, and reports `login required` for the reviews
  themselves. That is a state, and `/reviews` records it on the card rather
  than leaving the section unrun.
- **Note:** search takes titles, not arXiv ids, and only an exact title match
  is accepted — a near title is a different submission, and its reviews on
  this card would be worse than none.
- **Test:** `GET https://api2.openreview.net/notes/search?term=xbd&limit=1`

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

`GITHUB_TOKEN` and the OpenReview login are probed and **never suggested**.
Both sources work unkeyed for what this plugin asks of them, and a suggestion
list that grows every chunk stops being read.

## Cache

Every resolver's raw responses are cached under `~/.cache/research-bearings/<resolver>/`,
keyed by the query, for 30 days. Override the root with `RESEARCH_CACHE_DIR`.
`status` never reads the cache: it is the one verb whose job is to hit the wire.

## Where web search is allowed

`WebSearch` and `WebFetch` are not sources. Nine sources are. They are
allowed in exactly two places: the `searcher` agent, as a last resort when every index above returns
nothing, with the results labelled web-only and unverified until `verify`
resolves them; and `/scout`, to read a page one of the indexes pointed at.
Nowhere else. The write-scope guard denies `WebSearch` and `WebFetch` to every
other agent this plugin ships.
