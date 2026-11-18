# NOTES — The World in One Frame, 18 November 2026

## The 8 stories and their facts

All facts below come from the bounty brief's supplied story list
(reporting of 18 November 2026, attributed in the image footer to
Reuters · AP · Al Jazeera · CBS · UN). No numbers were invented; where
the brief gave a rounded figure ("nearly 850 points", "more than
5,400 cases") the image keeps the same wording.

1. **GULF ON FIRE (lead).** US fighter jets struck a Revolutionary
   Guard missile site on Qeshm Island, Iran. Iran fired drones at a
   US radar site in Bahrain (its 3rd attack there in under a week)
   and at a US air base in Kuwait. Iran shot down a US MQ-9 drone
   near the Strait of Hormuz. Trump said the US takes an Iran
   "dirty bomb" report seriously.
2. **KERCH BRIDGE FALLS.** Ukraine hit the Crimea (Kerch) Bridge a
   second day running; part of its road span collapsed into the
   strait.
3. **SHENZHEN POWER SHIFT.** APEC summit opened in Shenzhen, China.
   Xi Jinping received Putin there. The first-ever Trump–Xi–Putin
   trilateral summit happens tomorrow, 19 Nov, in Shenzhen. Trump
   first met Quad leaders (Japan, India, Australia) in Manila and
   agreed steps to secure critical minerals.
4. **NVIDIA $115.8B.** Nvidia quarterly revenue $115.8 billion, more
   than double a year earlier. Co-founder Jensen Huang stepped down
   as CEO; the board will not reinstate him. Nvidia stopped shipping
   Hopper chips to China. The US blocked China's remote access to
   advanced AI chips.
5. **MEASLES.** The United States lost its measles-free status, held
   for 26 years. States reported more than 5,400 cases and 10 deaths.
6. **EBOLA.** The Ebola outbreak in DR Congo more than doubled in
   three months: over 11,000 cases and 5,400 deaths (UN). Nearly 3
   in 4 children under 5 infected do not survive. This is the image's
   human hook (small red heart in the footer).
7. **MARKETS SLIDE.** The Dow fell nearly 850 points; the S&P 500
   had its lowest close since July. The NSA said some internal
   systems were degraded during routine maintenance after its
   classified network went down. The FAA paused new routers after a
   ground stop.
8. **DISASTERS.** Magnitude 6.0 earthquake in Papua New Guinea;
   magnitude 5.3 earthquake in Romania; Category 5 Cyclone Xavier
   hit the Northern Cook Islands.

Deliberately NOT included (per brief): the Russian An-12 crash in
Siberia (19 dead), Democrats winning Alaska's Senate seat (56 seats),
MS Dhoni retiring from the IPL, and Voyager 1 reaching one light-day
from Earth.

## What was verified vs. what was not

- Verified in-session: `entry.png` is exactly 1024×1024 and
  172,781 bytes (under the 1 MiB limit); `main.ts` run twice produces
  byte-identical output (same sha256); the image was viewed and
  checked for overlapping or cut-off text (none found); the date
  "WEDNESDAY · 18 NOVEMBER 2026" is legible in the masthead.
- NOT independently verified: the news facts themselves. They are
  taken as supplied in the bounty brief (Reuters / AP / Al Jazeera /
  CBS / UN reporting of 18 Nov 2026). I did not re-check each figure
  against the live wires in this session, so any error in the brief
  would carry into the image. The footer line "every number above
  was reported on 18 November 2026" is a claim about the brief's
  sourcing, not a fresh verification.

## Condensations (wording shortened, facts kept)

- Story 4: "quarterly revenue $115.8 billion, more than double a
  year earlier" became "Revenue $115.8B, more than double last
  year"; "Nvidia stopped shipping Hopper chips to China" became
  "Hopper chips to China stopped"; "the US blocked China's remote
  access to advanced AI chips" became "US blocked remote AI-chip
  access". Same facts, fewer words.
- Story 7: "The NSA said some internal systems were degraded during
  routine maintenance after its classified network went down. The FAA
  paused new routers after a ground stop." became "NSA systems
  degraded in routine maintenance after its classified network went
  down; FAA paused new routers." The "ground stop" detail was
  dropped for space; the "lowest close since July" detail was kept
  as "S&P 500 lowest close since July".
- Story 3: "agreed steps to secure critical minerals" is kept in
  full; the Quad members (Japan, India, Australia) are named in the
  brief but the panel says only "Quad leaders" for space.

## Known weaknesses of the image

- The globe's numbered dots are approximate region markers, not
  precise geography; the landmass blobs are deliberately abstract
  (no fake coastline was drawn).
- Dense panels (Nvidia, Markets) render their body text at 18px
  rather than 20px because the auto-fit step shrinks text to fit the
  box; body text is therefore not a uniform size across panels.
- The DISASTERS panel is full-width but has only two lines of text,
  leaving visible empty space at its bottom.
- The design is a clean newspaper front page, not a photograph or
  illustration; its emotional hook is typographic (the Ebola panel
  + footer heart) rather than a human face.
- No live data was fetched while rendering; the image is a static
  snapshot of the brief's facts.
