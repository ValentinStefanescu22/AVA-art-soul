# AVA Art & Soul — site de prezentare

## Despre proiect

Site-ul brandului personal al Alessiei Văideanu: artist ceramist și consilier acreditat în dezvoltare personală. AVA Art & Soul oferă ateliere creative cu lut, ateliere pentru companii, consiliere 1:1, ateliere private 1:1, retreaturi și ateliere pentru școli și copii.

Tagline: **autocunoaștere prin creație**
Valori: conectare, comunitate, apartenență.
Misiune: să ne relaxăm, să ne conectăm și să creăm conștient, împreună.

Tot conținutul site-ului (texte, structură, FAQ-uri, prețuri) e în `docs/continut-site.md`. Folosește textele de acolo exact cum sunt scrise. Ce e între paranteze drepte, [așa], e încă necompletat: păstrează-l ca placeholder vizibil și nu inventa valori. Fișierul vine dintr-un export Google Docs, cu bold pus literă cu literă (`**c**u**riozi**t**a**t**e**`): curăță formatarea, nu cuvintele.

Designul ales și sistemul vizual: `DESIGN.md` (se scrie după ce alegem direcția din canvas-ul de direcții).

## Stack

- Next.js (App Router) + TypeScript + Tailwind CSS
- Export static (`output: 'export'`), găzduire pe **Cloudflare Pages** (gratuit și pentru uz comercial). Domeniu nou, cumpărat mai târziu (Cloudflare Registrar).
- Fără bază de date, fără CMS, fără server propriu. Conținutul care se schimbă des stă în fișiere de date: `content/evenimente.ts`, `content/testimoniale.ts`, `content/galerie.ts`. Le actualizează Vali.
- Imaginile se optimizează la build (scriptul nostru cu `sharp`, AVIF/WebP pe mai multe lățimi), pentru că exportul static dezactivează optimizarea din `next/image`.
- Fonturile se încarcă local prin `next/font` (nu de la Google la runtime).

### Servicii externe (toate gratuite)

| Nevoie | Serviciu | Cum |
|---|---|---|
| Plată ateliere de grup | Stripe Payment Links | Un link per eveniment, în `content/evenimente.ts`. Limită de plăți = nr. de locuri. Checkout-ul cere telefon, acord foto (câmp custom) și acord termeni. Cod de reducere 5% acceptat. Banii ajung în contul ING Business al PFA. |
| Programări + plată consiliere și ateliere 1:1 | Cal.com (plan gratuit) + Stripe | Sincronizat cu calendarul de iPhone al Alessiei (iCloud). Încorporat pe paginile de servicii. |
| Formulare (contact, ofertă companii) | Web3Forms | Trimite pe email, fără backend. Honeypot anti-spam. |
| Newsletter + pop-up | MailerLite (gratuit) | Pop-up-ul e al nostru (în stilul site-ului) și trimite în MailerLite. Emailul de bun venit conține codul Stripe de 5%. |
| Analytics | Cloudflare Web Analytics | Fără cookies, deci fără banner de cookies. |

Facturarea (e-Factura) rămâne la contabilă / SmartBill / Oblio, nu în site. Alessia își creează singură contul Stripe (verificare de identitate).

## Bilingv (RO/EN)

- Rute: `/ro/...` și `/en/...` (`app/[lang]/...` cu `generateStaticParams`); rădăcina `/` redirecționează spre `/ro` (regulă `_redirects` în Cloudflare).
- Slug-urile rămân în română în ambele limbi (ex. `/en/ce-facem/ateliere-de-grup`).
- Fără librărie de i18n: câte un dicționar / fișier de conținut per limbă. Engleza o traduce Claude, o verifică Alessia. Paginile legale au și versiune EN, cu mențiunea că varianta în română e cea obligatorie.

## Pagini

Meniu: Acasă · Despre noi · Ce facem · Evenimente · Galerie · Contact

Subpagini „Ce facem”: Ateliere de grup · Pentru companii · Consiliere 1:1 · Atelier privat 1:1 · Retreaturi · Pentru școli și copii

Footer: FAQ · Înscrieri, plată și anulare · Termeni și condiții · Politica de confidențialitate · Cookies · link ANPC · datele PFA · Instagram

Paginile de servicii folosesc același șablon: pentru cine e, ce se întâmplă concret, ce primești, cine facilitează, durată / preț / locație, întrebări frecvente, buton de înscriere sau contact.

Fiecare pagină are la final o secțiune „Întrebări frecvente” (acordeon), cu întrebările din documentul de conținut.

Evenimente: cel mai apropiat eveniment primul (primul e cel din 15 noiembrie 2026). Dacă nu e niciunul viitor, afișează un mesaj „Pregătim următorul atelier…” + abonare la newsletter (textul îl propune Claude, îl aprobă Alessia). Evenimentele trecute merg într-o arhivă.

## Locație

Nicăieri adresa exactă. Pe site apare „București”, plus zona sau locația parteneră la fiecare eveniment (ex. „Cotroceni, sector 5”). Adresa exactă se trimite în mesajul de confirmare după plată. Nu folosi „Strada Elefterie 31” din document.

## Design

- Identitate vizuală (din PDF-urile „Identitate AVA”):
  - Culori: Lut ars `#3A2A20` (text, logo) · Nisip `#E6D5BD` (fundal principal) · Nisip deschis `#F4EDE4` (fundal secundar) · Teracotă `#B4583A` (accent) · Argilă `#C07A4E` (accent secundar) · Salvie `#6F7B5C` (natură, calm)
  - Fonturi alese de Vali (5 nov 2026): **Bodoni Moda** (titluri, greutate 400, `font-variation-settings: 'opsz' 20`, altfel liniile subțiri dispar pe ecran) + **Hanken Grotesk** (texte). Respinse: Gloock + Commissioner („arată a AI slop”), Newsreader + Host Grotesk (alternativa rămasă în Tweaks). În PDF-ul de identitate erau Fraunces + Jost. **Pinyon Script** rămâne accentul decorativ, doar pentru „Art & Soul” și momente rare, niciodată text lung. Orice font folosit trebuie să aibă ș/ț cu virgulă (subsetul latin-ext).
  - Element grafic: „inelele de lut” (trei linii ondulate: două închise, una teracotă)
  - Logo: vasul de lut + „AVA” + „ART & SOUL” + tagline. Momentan redesenat în SVG; înlocuiește cu fișierul original dacă îl primim.
- Contrast: Teracotă `#B4583A` pe fundal deschis trece doar pentru text mare (≥24px). Pentru text mic / butoane folosește `#9C472C` sau Lut ars. Text secundar: `#6B5444`. Salvie ca text: `#4F5A43`.
- Atmosferă: elegant, calm, bogat; lumină difuză care trece din bej în maro deschis.
- „Woodsprites”: luminițe mici, calde, care plutesc și urmăresc cursorul (pe mobil plutesc singure). Se opresc complet la `prefers-reduced-motion`.
- Mobile-first: majoritatea vizitatorilor vin de pe Instagram, de pe telefon.
- Imagini în `public/images/`: `atelier-hero.(webp|jpg)` (atelierul din octombrie), `alessia.(webp|png)` (portret decupat cu segmentarea de persoane din macOS Vision, margini curățate, nuanțe încălzite), `alessia-stamp.webp` (încadrat pătrat pentru cercul-ștampilă). Logo în `public/brand/`.
- Direcția aleasă (Runda 2 din canvas): hero „Ștampila în lut” (ștampila brandului imprimată în lut generat procedural cu filtre SVG; lumina-woodsprite urmărește cursorul cu arcuri critic amortizate și mută umbrele imprimării; text în dreapta, „AVA” deasupra „Art & Soul”), secțiunea-ștampilă din C pentru „Despre”, cardul de eveniment din A. Sursa de adevăr de portat: `.aidesigner/canvas/project/Acasa.dc.html` (sursele canvas-ului; `python3 .aidesigner/dc2html.py <artboard> <out.html>` le face pagini vizibile local, ex. `.aidesigner/acasa.html` (imaginile canvas-ului, `/_blob/<id>`, sunt copiate în `.aidesigner/_blob/`) pe serverul „design-preview” din `.claude/launch.json`). `.aidesigner/stampila.html` și `HeroStampila` sunt versiuni mai vechi. Fundalul hero-ului e o fotografie de lut sculptat în valuri, teracotă (`public/images/hero-lut.webp|jpg`, 2880px; mărită de Vali cu un upscaler AI la 2960px, apoi redusă la 2880 și cu o granulație fină de lut adăugată ca suprafețele să nu pară ceruite). Peste ea, un voal închis `rgba(42,20,12,…)` mai slab peste ștampilă și ~52% sub text (orizontal pe desktop, vertical pe mobil), ca textul crem să treacă de 4.5:1. Text crem (`#F4EDE4`, lede `#EFE3D3`, „Art & Soul” `#F2C79C`), meniu și butoane deschise pe fundal închis. Lumina-woodsprite are în jur un halou cald difuz (`.glow`, radial-gradient cu `mix-blend-mode: screen`, poziție în `--lx/--ly`). Ștampila NU folosește feDiffuseLighting (Chrome îl desenează la rezoluția viewBox-ului, deci neclar la zoom / Retina): e din straturi vectoriale cu `<mask>` (fundul canalului mai închis; umbră clară = forma minus forma mutată departe de lumină; perete umbrit moale = aceeași diferență pe 3–6 unități, cu blur, tăiată în forma clară; perete luminat și buză luminoasă de partea opusă), deplasate din JS după poziția luminii; apăsarea la încărcare e un `scale` din JS, nu o animație CSS. Să nu pară „corporatist”; hero-ul închis e cald (lut ars), nu greu, iar restul paginii rămâne deschis.
- Context de produs pentru skill-urile de design: `PRODUCT.md`.

## Animații

- Un singur moment orchestrat la încărcare (hero), apoi mișcare discretă. La scroll (cerut de Vali, 11 nov 2026): blocurile de conținut apar o singură dată, opacitate + ridicare de 16px, 800ms ease-out, decalaj de 80ms între frați; nimic ascuns fără JS sau cu `prefers-reduced-motion` (vezi `REVEAL` în `.aidesigner/acasa_combine.py`).
- Animații întreruptibile (lerp / spring din poziția curentă), fără să blocheze input-ul. Easing ease-out, sub ~300ms pentru interacțiuni.
- Tot ce se mișcă respectă `prefers-reduced-motion`.

## Detalii UX de aplicat (din lista celor 20)

Se aplică: prerendering cu Speculation Rules (`moderate`, link-uri interne), placeholder blur pentru imagini (generat la build), View Transitions între pagini (sub 300ms), animații întreruptibile, ținte de atins ≥44px, safe-area insets (`viewport-fit=cover`), `tabular-nums` la prețuri / date / ore, `text-wrap: balance` pe titluri și `pretty` pe paragrafe, `corner-shape: squircle` lângă `border-radius`, safe triangle pe submeniul „Ce facem”, butoane dezactivate cât timp se trimite un formular, bottom sheet cu swipe pentru meniul de mobil (cu buton de închidere).

Nu se aplică (site static de prezentare): skeleton loaders, optimistic updates, command menu, scurtături de tastatură, undo toasts, stale-while-revalidate, predictive back (Android nativ), one-time-code, idempotency keys (le gestionează Stripe).

La final, raportează toate cele 20: Built / Already done / Skipped, cu fișierele și cum se verifică.

## Reguli de conținut (importante)

- Limba principală: română, cu diacritice corecte (ș, ț cu virgulă dedesubt).
- Vocea e la persoana I, a Alessiei („Sunt Alessia…”, „Te ghidez…”), caldă și simplă, nu corporatistă.
- Colaboratoarele apar în secțiunea „Comunitatea AVA” ca colaboratoare, NU ca echipă, co-fondatoare sau co-organizatoare.
- Alessia NU este psiholog sau psihoterapeut înregistrat. Nicăieri pe site nu apar cuvintele „psiholog”, „psihoterapeut” sau „terapie” / „art-terapie” ca serviciu oferit. Serviciile se numesc „consiliere în dezvoltare personală” și „autocunoaștere prin artă”. Poate scrie că studiază terapii experiențiale și artterapie.
- Pagina de consiliere păstrează delimitarea dintre consiliere și psihoterapie, exact cum e în document.
- La atelierele pentru copii rămâne precizarea că nu înlocuiesc logopedia, terapia ocupațională sau kinetoterapia.

## Înscrieri și plăți

- Plata online e la lansare: Stripe Payment Links pentru ateliere de grup, Cal.com + Stripe pentru consiliere și ateliere 1:1.
- Locul se confirmă după plata integrală.
- Politica de anulare: banii nu se returnează, dar anunțul cu cel puțin 24 de ore înainte îți păstrează locul la următorul atelier (la consiliere: reprogramare).
- De verificat cu contabila: excepția de la dreptul de retragere (OUG 34/2014) pentru ședințele de consiliere.

## Legal (România)

- Footer cu datele PFA: VAIDEANU ALESSIA-ALEXANDRA PFA, CUI 55380756, Reg. Com. F2026038934007, email ava.events.26@gmail.com. Sediul: adresa completă din Constanța vine de la Vali (până atunci placeholder `[ADRESA SEDIULUI]`).
- Politica de confidențialitate (GDPR) și bifă de acord în fiecare formular; la înscriere și acord foto separat.
- Date colectate: nume întreg, vârstă, email, detalii firmă dacă e cazul, adresă de facturare; email de promo doar opțional.
- Fără banner de cookies cât timp analytics-ul e fără cookies. Pagina de cookies spune asta.
- Link ANPC (SAL) în footer.
- Contact: ava.events.26@gmail.com · 0730301996 · Instagram @ava.art.soul

## SEO și calitate

- Titluri și descrieri meta pentru fiecare pagină, în ambele limbi; `hreflang` + canonical; Open Graph (imagine per pagină); `sitemap.xml` cu alternativele de limbă; `robots.txt`.
- Date structurate JSON-LD: LocalBusiness / ProfessionalService (zonă deservită: București, fără adresă), Person (Alessia), **Event** pentru fiecare eveniment, BreadcrumbList.
- Core Web Vitals: fonturi locale, imagini optimizate, efectele decorative se încarcă după conținutul principal.
- În afara site-ului (de făcut de Alessia / Vali): Google Search Console + trimis sitemap, Google Business Profile (zonă deservită, fără adresă).
- Imagini cu text alternativ descriptiv în română (și engleză pe /en).
- Accesibilitate: contrast bun, navigare de la tastatură, focus vizibil, butoane clare.

## Unelte

- MCP-ul AIDesigner e configurat în `.mcp.json` (trebuie conectat cu `/mcp` într-o sesiune nouă).

## Cum lucrăm

- Dezvoltatorul învață web development prin proiectul ăsta: explică pe scurt și simplu ce faci și de ce, definind termenii noi.
- Fă pașii mici și verificabili; după fiecare pagină, rulează build-ul și spune cum se poate vedea local.
- Nu adăuga librării sau servicii plătite fără să întrebi.
