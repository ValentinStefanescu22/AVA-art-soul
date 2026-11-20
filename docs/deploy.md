# Publicarea pe Cloudflare (o singură dată, de făcut de Vali)

Site-ul e un Worker Cloudflare numit `ava-art-soul`, care servește fișierele din `out/`. Pipeline-ul din GitHub (`.github/workflows/ci.yml`) îl publică singur, după ce trec toate testele. Până faci pașii de mai jos, deploy-ul e oprit, iar testele rulează oricum.

Celălalt site din contul tău (Ramona) nu e atins: sunt Workers separați, cu nume diferite.

## 1. Tokenul Cloudflare

Un token e o „cheie” cu drepturi limitate, pe care GitHub o folosește în locul parolei tale.

1. Cloudflare → **My Profile → API Tokens → Create Token → Create Custom Token**.
2. Nume: `github-ava-art-soul-deploy`.
3. Permissions:
   - `Account` · `Workers Scripts` · `Edit`
   - `Account` · `Account Settings` · `Read`
4. Account Resources: `Include` · contul tău. Zone Resources: nu e nevoie.
5. Opțional: TTL / IP filtering, nu.
6. **Create Token**. Copiază tokenul. Se vede o singură dată. Nu-l pune nicăieri altundeva, nici în chat, nici în cod.

> Atenție: drepturile pe Workers sunt la nivel de cont. Tokenul ar putea modifica și Worker-ul Ramonei, dacă ar ajunge în mâini greșite. De aceea stă doar în GitHub Secrets. GitHub îl dă doar deploy-ului de pe `main`, niciodată unui pull request dintr-un fork.

**Account ID**: în dashboard, pe pagina principală a contului (bara din dreapta, „Account ID”), sau în URL: `dash.cloudflare.com/<account-id>/…`.

**Subdomeniul workers.dev**: Workers & Pages → în dreapta apare `<ceva>.workers.dev`. Site-ul va fi la `https://ava-art-soul.<ceva>.workers.dev`.

## 2. GitHub: secretele și variabilele

În repo: **Settings → Environments → New environment → `production`**. Apoi, în environment:

**Environment secrets** (secrete, nu se mai pot citi după ce le salvezi):

| Nume | Valoare |
|---|---|
| `CLOUDFLARE_API_TOKEN` | tokenul de la pasul 1 |
| `CLOUDFLARE_ACCOUNT_ID` | Account ID |

Apoi **Settings → Secrets and variables → Actions → Variables** (publice, nu sunt secrete):

| Nume | Valoare | Ce face |
|---|---|---|
| `DEPLOY_ENABLED` | `true` | pornește deploy-ul |
| `SITE_URL` | `https://ava-art-soul.<ceva>.workers.dev` | URL-urile canonice, sitemap-ul și Open Graph |
| `SITE_INDEXABLE` | `false` | **rămâne `false` până la lansare.** La lansare, pe domeniul real, devine `true` și Google poate indexa. |
| `CF_ANALYTICS_TOKEN` | (gol deocamdată) | Cloudflare Web Analytics, la lansare |

## 3. Siguranța repo-ului (Settings → Code security)

Repo-ul e public, așa că pornește:
- **Dependabot alerts** și **Dependabot security updates**;
- **Secret scanning** și **Push protection**: GitHub refuză un push care conține din greșeală un token sau o parolă;
- **Code scanning**: CodeQL rulează deja din `.github/workflows/codeql.yml`.

## 4. Primul deploy

După pașii 1 și 2, orice push pe `main` publică site-ul, dacă testele trec. Ca să-l pornești fără un commit nou: **Actions → CI → Run workflow**.

Verificări după deploy:
- `https://ava-art-soul.<ceva>.workers.dev/` te duce la `/ro`;
- în DevTools → Network, răspunsul paginii are `content-security-policy` și `x-robots-tag: noindex`.
