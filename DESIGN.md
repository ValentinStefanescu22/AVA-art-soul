# DESIGN.md — sistemul vizual AVA Art & Soul

Scris pe 12 nov 2026, după ce am ales Acasă, Despre noi și Ce oferim pe canvas.
Paginile rămase se proiectează după fișierul ăsta, iar codul Next.js îl urmează pe el, nu canvasul.

**Sursa de adevăr vizuală:** canvasul [AVA Art & Soul](https://claude.ai/artifact/94uC9vW9Z4At3qoGQJW5cJ), paginile „Acasă: lucru”, „Despre noi: lucru”, „Ce oferim: lucru”.
Planșele vin din `.aidesigner/canvas/project/*.dc.html`. Le generează scripturile din `.aidesigner/*.py`. Paginile asamblate le scriu `acasa_combine.py` și `pages_combine.py`.
Le vezi local cu serverul „design-preview”: `.aidesigner/acasa.html`, `despre-noi.html`, `ce-facem.html`.

Conținutul (texte, prețuri, FAQ) nu stă aici, ci în `docs/continut-site.md`. Regulile de text și cele legale sunt în `CLAUDE.md`.

---

## 1. Principii

1. **Cald, nu lucios.** Te simți invitat la masă, nu ți se vinde ceva. Nimic nu trebuie să pară „corporatist”.
2. **Calm.** Un singur moment orchestrat la încărcare (hero-ul). După aceea mișcarea e discretă și apare o singură dată.
3. **Secțiunile informative sunt liniștite.** La formări, oameni sau fapte nu folosim iconițe, rame pe poze, efecte de lumină sau semnături decorative. Le folosim doar apariția la scroll. (Feedback de la Alessia, 11 nov.)
   Mișcarea mai îndrăzneață rămâne pentru hero-uri și secțiunile-vitrină.
4. **Adevărat.** Folosim poze reale, fără filtre de culoare: fără duotone, fără tentă portocalie.
   Nu inventăm dovezi (testimoniale, logo-uri, cifre).
   Ce lipsește apare ca placeholder vizibil `[ASA]`.
5. **Telefonul întâi.** Vizitatorii vin de pe Instagram. Fiecare secțiune se proiectează și la 390px.
6. **O pagină, nu module lipite.** Secțiunile curg una în alta: fundal continuu și un singur ritm de spațiu (vezi §5).
7. **Fără etichete deasupra titlurilor.** Nu punem „kicker” / „eyebrow” de tipul „DESPRE NOI” peste un titlu.

---

## 2. Culori

### Paleta de brand (din PDF-urile „Identitate AVA”)

| Token | Hex | Folosire |
|---|---|---|
| `--ink` Lut ars | `#3A2A20` | text principal, logo, butonul principal, fundalul footerului |
| `--sand` Nisip | `#E6D5BD` | fundal cald, cel mai adânc dintre cele deschise |
| `--paper` Nisip deschis | `#F4EDE4` | fundalul de bază al paginilor |
| `--terra` Teracotă | `#B4583A` | accent, **doar text mare (≥24px)** sau decor |
| `--clay` Argilă | `#C07A4E` | accent secundar (ex. sublinierea-marker din Povestea) |
| `--sage` Salvie | `#6F7B5C` | natură, calm (ca text: `#4F5A43`) |

### Culori derivate, folosite efectiv în machete

| Token | Hex | Folosire |
|---|---|---|
| `--ink2` | `#6B5444` | text secundar (meta, descrieri scurte) |
| `--body` | `#4A382C` | paragrafe lungi (Povestea, intro-uri) |
| `--terra-d` | `#9C472C` | text mic / butoane în teracotă; roluri italice, întrebări |
| `--terra-dd` | `#833A22` | hover pe teracotă; meta mic (prețuri, durate) |
| `--sand-l` | `#EDE0CD` | nisip intermediar; fundalul cu care începe footerul |
| `--cream-2` | `#EFE4D4` | capătul degradeului de la Ce oferim |
| `--card` | `#FBF7F1` / `#FBF7F0` | carduri pe fundal deschis |
| `--card-open` | `#FFFDF9` | card deschis (FAQ), câmpuri de formular |
| `--glowc` | `#F2C79C` | „Art & Soul” în hero, focus pe fundal închis |

### Fundaluri închise (hero-uri)

- **Maro de pagină** (Despre noi, Ce oferim): `#2E1C13 → #22140D`, cu `#3A2418` ca maro de pornire al degradeului lin.
- **Acasă:** fotografia de lut teracotă (`hero-lut`) cu un voal `rgba(42,20,12,…)` peste ea, ~52% sub text.
- **Textul pe fundal închis:**
  - titluri `#F4EDE4`
  - lede `#EFE3D3`
  - corp `#D8C6B2`
  - accent `#F2C79C`

### Contrast (AA)

- Teracota `#B4583A` pe fundal deschis trece doar la text ≥24px. Sub 24px folosește `#9C472C` sau Lut ars.
- Text crem pe hero-uri: minim 4.5:1. Unde textul stă pe degradeu, se măsoară culoarea din spatele lui (§6).
- Focus vizibil:
  - pe fundal deschis, `outline: 2px solid #9C472C; outline-offset: 3–4px`;
  - pe fundal închis, `#F2C79C`.

---

## 3. Tipografie

Fonturile, alese de Vali pe 5 nov:
- **Bodoni Moda** pentru titluri: greutate 400, întotdeauna cu `font-variation-settings: 'opsz' 20`, altfel liniile subțiri dispar pe ecran. Titlurile foarte mari folosesc `opsz` 72–96.
- **Hanken Grotesk** pentru text.
- **Pinyon Script** doar pentru „Art & Soul” și momente rare; niciodată text lung.

Toate trebuie să aibă subsetul latin-ext (ș, ț cu virgulă). În cod se încarcă local, prin `next/font`.

| Rol | Font | Mărime (desktop → mobil) |
|---|---|---|
| Titlul hero-ului | Bodoni 400 | `clamp(72px, 9vw, 128px)`, `line-height .95`, `letter-spacing -.025em` · mobil `clamp(56px, 16vw, 84px)` |
| Titlul de secțiune (h2) | Bodoni 400 | `clamp(40px, 4.4vw, 64px)`, `line-height 1.05` |
| Titlu de card / subtitlu | Bodoni 400 | 22–28px, `line-height 1.2` |
| Lede | Bodoni 400 | `clamp(20px, 1.7vw, 24px)`, `line-height 1.4` |
| Italic de accent (roluri, întrebări, date) | Bodoni italic | 17–36px, de obicei `--terra-d` sau `--ink2` |
| Corp | Hanken 400 | 17px / 1.6 |
| Lectură lungă | Hanken 400 | 19px / 1.75 (mobil 18px) |
| Mic / meta | Hanken 400–500 | 14–15px |
| Etichete de coloană (doar footer) | Hanken 500 | 12px, `uppercase`, `letter-spacing .14em` |
| Butoane | Hanken 500 | 15px, `letter-spacing .02em` |

**Reguli:**
- `text-wrap: balance` pe titluri, `pretty` pe paragrafe.
- `font-variant-numeric: tabular-nums` la prețuri, date și ore.
- Paragrafele au cel mult ~46–52 de caractere pe rând (`max-width: 46ch`).

---

## 4. Forme și umbre

| Element | Rază |
|---|---|
| Butoane, câmpuri, pastile, insigne | `999px` |
| Carduri (FAQ, colaboratoare, carduri închise) | `22px` + `corner-shape: squircle` |
| Fotografii în carduri și benzi | `20–24px` + squircle |
| Story-ul de eveniment | `30px` + squircle |
| Foaia meniului de mobil | `26px 26px 0 0` |
| Portretul Alessiei (Despre noi) | **dreptunghi simplu, fără ramă, fără rază** |

**Umbre:** calde și moi, niciodată gri-reci. De exemplu:
- card la hover: `0 18px 30px -22px rgba(58,30,15,.45)`;
- card deschis: `0 24px 48px -36px rgba(70,35,15,.45)`;
- pe carduri, conturul e `0 0 0 1px rgba(58,42,32,.06)`, nu `border`.

---

## 5. Așezare și ritm

- **Container:** `max-width: 1240px`, padding lateral 40px (20px sub 820px).
- **Puncte de rupere:**
  - 1020px: meniul devine burger;
  - 980px: coloanele se strâng într-una;
  - 820px: spații de mobil.
- **Ritmul între secțiuni:** 88px sus / 104px jos pe desktop, 56 / 72 pe mobil. Un singur ritm; nu adunăm padding-ul a două secțiuni.
- **Fundal continuu:** pe pagina asamblată, rădăcinile secțiunilor sunt transparente. Fiecare secțiune începe în culoarea în care s-a terminat cea dinainte, alternând `--paper` ↔ `--sand-l`, cu `--sand` ca punct cel mai adânc.
  Ex. Despre noi: maro → (degradeu lin) → paper → paper→sand-l → sand-l → footer.
- **Ancore:** `scroll-padding-top: 88px`, ca titlurile să nu ajungă sub header.
- **Ținte de atins:** minim 44px.

---

## 6. Degradeul lin maro → crem

Îl folosim când un hero închis trece într-o secțiune deschisă (Ce oferim, Despre noi → Povestea). Așa nu apare o dungă.

**Cum e făcut** (tehnica „easing gradients”):
- 18 opriri cu ease-in-out sine: culoarea se schimbă încet la capete și repede la mijloc;
- amestec în OKLab, ca să nu apară un mijloc portocaliu-tulbure;
- opriri hex simple, ca toate browserele să-l deseneze la fel.

**Funcția:** `eased_gradient(a, b, c0, c1)` din `.aidesigner/cf_pagina_options.py`. În cod va fi o funcție mică ce generează aceleași opriri.

**Lungimi:**

| Unde | Desktop | Mobil |
|---|---|---|
| Ce oferim (în hero) | 330 → 800px | 280 → 680px |
| Despre noi → Povestea | 0 → 420px (titlul de la 320px) | 0 → 340px (de la 250px) |

**Reguli:**
- Zona de trecere are minim ~400px pe desktop.
- Textul crem stă doar pe prima treime, cel închis doar pe ultima. Ambele se verifică la 4.5:1 în punctul exact.
- Headerul își schimbă tonul la mijlocul degradeului, cu variabila `--hx-dark`: distanța în px de la începutul secțiunii.

---

## 7. Componente

### Header: pastila de sticlă (Header 1)

Sursa: `header_options.py` (`acasa_parts`). E inspirat din Apple Liquid Glass.

- **În partea de sus a paginii:** bară lată, transparentă, cu logo, meniu și comutatorul RO/EN.
- **La scroll:** se strânge într-o pastilă de sticlă (max 960px, 60px înălțime, la 12px de sus) și rămâne lipită sus, ca să te urmărească.
- **Sticla e opacă destul cât textul să se citească peste orice:**
  - închisă: `rgba(40,20,12,.6)`;
  - deschisă: `rgba(250,246,240,.84)`;
  - amândouă cu `blur(22px) saturate(170%)`, o margine luminoasă sus și o umbră caldă.
- **Tonul** (închis / deschis) îl alege JS-ul după ce e sub pastilă.
- **Pagina curentă:** un punct sub link (`aria-current="page"`).
- **„Ce oferim”:**
  - pe desktop, submeniul e un panou de sticlă, cu „safe triangle”;
  - pe telefon, meniul e o foaie care urcă de jos: se închide trăgând în jos sau din ×, are linkuri mari în Bodoni și „Ce oferim” se deschide pe loc.
- **Pe Acasă,** pastila pornește sub banda de anunț (42px). Pe celelalte pagini pornește de la 0.

### Footer (Footer 3, „carte poștală pe cusătură”)

Sursa: `Footer3Heath`.
- Un card-carte poștală cu newsletterul („Rămâi aproape…”, semnătura „– Alessia Văideanu”, emailul, bifa GDPR) stă pe cusătura dintre nisip și maro.
- Dedesubt e footerul închis `#3A2A20`, cu coloanele Navigare / Ce oferim / Informații / Contact și rândul legal (PFA, ANPC, RO/EN).
- Fundalul de deasupra cusăturii e `--sand-l`, deci secțiunea dinainte trebuie să se termine în `--sand-l`.

### Pop-up newsletter (Pop-up 3, „plic cu ștampilă”)

- Apare după ~8 secunde sau la 40% din pagină, o singură dată per vizitator. După închidere nu mai apare 30 de zile.
- Pe telefon urcă de jos și îl tragi în jos ca să-l închizi.
- Deocamdată e doar pe Acasă.

### Butoane

| Tip | Cum arată | Unde |
|---|---|---|
| Principal | pastilă `--ink`, text `--paper`, 50–52px înălțime, padding 26–30px; hover `#2A1D15` | newsletter, acțiuni generale |
| Rezervare | pastilă `--terra-d` `#9C472C`, text `#F8F1E8`; hover `#833A22` | înscriere, listă de așteptare |
| Crem pe închis | pastilă `--paper` pe fundal închis | hero-uri |
| Contur pe închis | `rgba(244,237,228,.08)` + contur 1px crem 50% + blur | al doilea buton din hero |
| Link „mai mult” | text 500 + săgeată, sublinierea se strânge la hover, săgeata alunecă 4px | „Află mai multe”, „Vezi atelierul…” |

**Săgeți și telefon (Vali, 12 nov):**
- Butoanele pline nu au săgeată. Săgeata rămâne doar la linkurile de text („Află mai multe →”).
- Pe telefon, butoanele din carduri ocupă toată lățimea cardului, cu textul centrat.

**Sold out (Vali, 12 nov):** nu există listă de așteptare și nu folosim buton dezactivat, care pare stricat și nu se poate atinge de la tastatură. Biletul își păstrează ștampila „Sold out”, iar în locul butonului apare un link de text spre următorul atelier cu locuri („Vezi următorul atelier ↓”).

Textele butoanelor sunt verbe clare, cele din document sau cele aprobate în comentarii („Află mai multe”, „Vezi următoarele ateliere”, „Intră pe lista de așteptare”).

### Carduri

- **Card deschis:** `--card`, rază 22 squircle, padding 24px; la hover se ridică 3px și primește umbră caldă. Folosit la colaboratoare și FAQ.
- **Card închis:** `--ink`, text crem. Folosit pentru „Ai altă întrebare?” în FAQ.
- **Card cu poză** (servicii, acordeon): poza acoperă cardul, cu un voal de jos `rgba(22,12,7,…)` sub text.

### Altele, deja alese

- **Insignă „Sold out”:** pastilă cu contur `#9C472C`, 14px, 600. În story: etichetă italică rotită.
- **FAQ:** carduri-acordeon, unul deschis odată, primul deschis. Cercul cu „+” se umple la hover.
- **Story de eveniment (Următorul atelier A):**
  - cadre 9:16 cu bare de progres, ca la Instagram;
  - un bilet cu data și numărătoarea inversă;
  - pornește când ajunge pe ecran.
- **Testimoniale (B2):** două benzi de poze care curg în sens opus și se opresc la hover. Între ele, un citat mare, cu bare de progres de câte 9 secunde.
- **Comutatorul de servicii (Ce oferim 1):**
  - file „Pentru tine / Pentru companii / Pentru școli și copii”, scrise cu fontul titlurilor;
  - sub ele, carduri cu poză, nume, o propoziție, meta (durată · persoane · preț) și link.
- **Placeholder de conținut:** chenar punctat `#9C472C` 55%, text `--terra-d`, majuscule, de forma `[TEXTUL …: VINE DE LA …]`.

---

## 8. Mișcare

**Încărcarea.** Un singur moment orchestrat, în hero:
- **Acasă:** banda, titlul, lede-ul și butoanele urcă pe rând. Lumina-woodsprite (o luminiță caldă cu halou) urmărește cursorul; pe telefon plutește singură.
- **Despre noi:** portretul se descoperă de jos în sus și urcă 40px (1.5s).
- **Ce oferim:** literele titlului urcă pe rând (45ms între ele, cu blur care se limpezește), apoi apar lede-ul și filele.

**La scroll** (cerut de Vali, 11 nov). Fiecare bloc apare o singură dată:
- opacitate + ridicare de 16px, 800ms, `cubic-bezier(.22,1,.36,1)`, 80ms între frați (maxim 4 trepte);
- se declanșează cu `IntersectionObserver` (`rootMargin: 0 0 -8% 0`, `threshold .12`);
- folosește proprietatea `translate` și o animație cu `backwards` (nu `both`), ca să nu calce peste `transform`-urile de hover;
- nimic nu e ascuns fără JS sau cu `prefers-reduced-motion` (clasa `.js` / `.rv-on` se pune din script).

**Excepții:**
- pe Acasă, la „Cine sunt”, cele două roluri intră din lateral (48px, 1.1s);
- în Povestea, cuvintele întrebării apar pe rând, iar fraza îngroșată primește o sublinierea-marker în argilă.

**Interacțiuni:**
- sub ~300ms, ease-out, întreruptibile (pornesc din poziția curentă);
- la ceva „jucăuș”, curbă cu arc: `cubic-bezier(.3,1.32,.5,1)`;
- curba moale: `cubic-bezier(.22,1,.36,1)`.

**`prefers-reduced-motion`:** totul stă pe loc; doar culorile se pot schimba.

**Între pagini:** View Transitions, sub 300ms (în cod).

---

## 9. Imagini

- Fără filtre de culoare: pozele rămân naturale.
- Pozele de pe Unsplash sunt provizorii, până avem poze reale de la ateliere. Sunt marcate ca atare în notițele de pe canvas.
- **Portretul Alessiei:**
  - pe Despre noi, dreptunghi 4:5, `object-position: 50% 6%`, fără mască și fără ramă;
  - pe Acasă, varianta decupată.
- Text alternativ descriptiv, în română (și în engleză pe /en).
- În cod: AVIF/WebP pe mai multe lățimi, placeholder blur, `loading="lazy"` sub prima ecranare.

---

## 10. Paginile alese (12 nov 2026)

| Pagină | Secțiuni, în ordine (planșa de pe canvas) |
|---|---|
| **Acasă** (`Acasa`) | Hero: bandă de anunț + titlu centrat (`HeroAnuntCentrat`) · Cine sunt (`CopertaH`) · Ce oferim, acordeon de poze (`CeFacem5Acordeon`) · Următorul atelier, story + bilet (`UrmatorulA`) · Ce spun oamenii (`OameniB2`) · FAQ în carduri (`Faq3Carduri`) · Footer 3 · Pop-up 3 |
| **Despre noi** (`DespreNoi`) | Deschiderea maro cu portretul (`DespreNoiDeschidere`) · Povestea, interviu (`Povestea4Interviu`) · Formări, centrat (`Formari3DCentrat`) · Comunitatea AVA, intro + carduri (`Comunitate5Carduri`) · Footer 3 |
| **Ce oferim** (`CeFacem`) | Comutatorul cu degradeu (`CFPagina1Comutator`) · De ce să alegi AVA Art & Soul? (`CFDeCe`, textul vine de la Vali) · Footer 3 |
| **Ateliere de grup** (`AteliereDeGrup`) | Fotografie pe tot ecranul (`GrupHero2Aman`) · Atelierele care urmează, bilete cu ștampila „Sold out”; cele de Crăciun au o ghirlandă de beculețe care sclipește pe marginea de sus (`GrupCraciun2Beculete`, construit din `GrupAteliere3Bilete`) · Ai deja un grup? (`GrupSolicita`) · Cum funcționează + colaborări (`GrupDetalii`) · Întrebări frecvente în carduri (`GrupFaq`) · Footer 3 |

Numele fișierelor `CeFacem…` / `CF…` au rămas așa din motive tehnice; pe site scrie peste tot „Ce oferim”.

---

## 11. Ce mai e de proiectat

Procesul pe canvas:
- pentru fiecare secțiune, variante inspirate din site-uri reale numite, desktop + mobil;
- variantele respinse merg în arhivă, nu se șterg;
- textele vin doar din `docs/continut-site.md`; ce propun eu e marcat „de aprobat”.

**Pagini de completat:**
- **Șablonul paginilor de serviciu**, unul pentru toate 6, cu 4 variante pe secțiune. Structura: pentru cine e · ce se întâmplă concret · ce primești · cine facilitează · durată / preț / locație · întrebări frecvente · buton de înscriere sau contact (Stripe / Cal.com / formular). Consilierea păstrează delimitarea față de psihoterapie; atelierele pentru copii, precizarea despre terapii.
- **Retreaturi** (decizia lui Vali, 12 nov): pagina arată doar „În curând”, pentru că nu e încă nimic concret. Fără program, preț sau FAQ până nu există.
- **Evenimente**, cu 4 variante. Cel mai apropiat eveniment primul, arhiva celor trecute și starea „Pregătim următorul atelier…” + newsletter. Pornește de la cardul de eveniment de pe Acasă.
- **Galerie.**
- **Contact**, cu formularul Web3Forms și bifa GDPR. Propunere: 2 variante.
- **Paginile legale**, doar text lung, cu un singur șablon de lectură. Propunere: 2 variante.
- **Întrebări frecvente la finalul fiecărei pagini**, cum cere `CLAUDE.md`. Pe Despre noi și Ce oferim nu sunt încă puse.
