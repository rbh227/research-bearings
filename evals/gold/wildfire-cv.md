# Gold set — wildfire, end to end

The recall half of chunk 2's done-check (`docs/design/chunk-02-scout.md` §6.4).
Originally scoped to the acceptance-run topic the map records — post-disaster
building damage assessment from aerial and satellite imagery — and widened on
2026-09-14 to the wildfire field as a whole: detection, mapping, spread, drivers,
smoke, and the damage assessment that follows a fire.

**Score per heading, not per file.** A scout run answers one question, so recall
is computed against the heading or headings that question covers. The original
acceptance run is graded on *damage assessment*, *structure loss and the WUI*,
and the damage rows of *datasets*; the rest of the file is there for later runs.

## Provenance

**Written from memory, without searching — by Claude Opus 5, on 2026-09-14, not
by the user.** No search tool was called, no file was consulted, nothing was
verified before writing. That constraint is the whole point: a list produced by
searching is not a test of whether search finds things.

Read the recall number with the substitution in mind. The scout is also a Claude
model, so a paper this file misses because the model never held it is a paper the
scout can be blind to at no scoring cost — a shared blind spot passes. This list
therefore tests *whether search surfaces what the canon already contains in
memory*. It does not test coverage of work outside that memory: recent
(post-cutoff) work, non-English literature, grey literature, and small venues are
systematically under-represented here, and a scout that finds them scores nothing
for it. A human-written gold set would still be worth more, and this one does not
replace writing it.

Years without a `?` are ones I'm confident of; `?` means the entry is right but
the year is a guess. `[unsure]` means I believe the work exists roughly as
described but would not bet on the title or the author. Resolve those first —
an entry that turns out not to exist must be **deleted, not corrected**, or it
scores the scout for failing to find something that isn't there.

Resolved to Semantic Scholar ids by §6.2, through the retrieval script's `batch`
verb.

**Never edited after a scout run has been scored against it.** The moment this
file moves to match what the scout found, it stops measuring anything. Add to it
only before a run, never after one. Deleting an entry that resolution proves
imaginary is the one exception, and only before the first scored run.

## Papers — damage assessment from aerial and satellite imagery

- Gupta — xBD / xView2, a dataset for assessing building damage from satellite imagery — 2019
- Weber & Kané — building disaster damage assessment, multi-temporal fusion (xView2 baseline) — 2020
- Zheng — ChangeOS, object-based semantic change detection for building damage — 2021
- Galanis — DamageMap, a post-wildfire damaged-buildings classifier — 2021?
- Gupta & Shah — RescueNet, joint building segmentation and damage assessment — 2020? (name collides with Rahnemoonfar's UAV RescueNet; different work)
- Xu — building damage detection in satellite imagery using CNNs (generalization across disasters) — 2019
- Fujita — damage detection from aerial images via convolutional neural networks (washed-away buildings) — 2017
- Cooner — detection of urban damage using remote sensing and machine learning, 2010 Haiti earthquake — 2016
- Rudner — Multi3Net, rapid segmentation of flooded buildings by fusing multiresolution/multisensor/multitemporal imagery — 2019
- Voigt — global trends in satellite-based emergency mapping — 2016
- Rahnemoonfar — FloodNet, UAV imagery for post-flood scene understanding — 2021
- Rahnemoonfar — RescueNet, UAV post-Hurricane-Michael pixel-level damage — 2023?
- Kalluri? — post-wildfire building damage from very-high-resolution imagery — 2021? [unsure]
- Bai — Sentinel-1/2 building damage detection with deep learning — 2020? [unsure]

## Papers — structure loss and the wildland-urban interface

- Cohen — preventing disaster: home ignitability in the wildland-urban interface — 2000
- Calkin — how risk management can prevent future wildfire disasters in the WUI — 2014
- Radeloff — rapid growth of the US wildland-urban interface raised wildfire risk — 2018
- Syphard — housing arrangement and location determine the likelihood of housing loss due to wildfire — 2012
- Syphard & Keeley — factors associated with structure loss in the 2013–2018 California wildfires — 2019
- Alexandre — factors related to building loss due to wildfires in the conterminous United States — 2016
- Kramer — high wildfire damage in interface communities in California — 2019
- Kramer — where wildfires destroy buildings in the US relative to the WUI — 2018?
- Knapp — housing arrangement and vegetation factors in single-family home survival, 2018 Camp Fire — 2021
- Moritz — learning to coexist with wildfire — 2014
- Higuera — shifting social-ecological fire regimes explain increasing structure loss in the western US — 2023?
- Wang / Guan — economic footprint of California wildfires — 2021
- Mell — the wildland-urban interface fire problem, current approaches and research needs — 2010

## Papers — wildfire detection, mapping and burned area

- Dewangan — FIgLib & SmokeyNet, a dataset and model for real-time wildland fire smoke detection — 2022
- Govil — preliminary results from a wildfire detection system using deep learning on remote camera images — 2020
- Giglio — the MODIS Collection 6 active fire product — 2016
- Schroeder — the new VIIRS 375 m active fire detection data product — 2014
- Giglio — the Collection 6 MODIS burned area mapping algorithm and product (MCD64A1) — 2018
- Wooster — retrieval of biomass combustion rates and totals from fire radiative power observations — 2005
- Key & Benson — landscape assessment: NBR and the Composite Burn Index (FIREMON) — 2006
- Miller & Thode — quantifying burn severity with a relative version of dNBR (RdNBR) — 2007
- Eidenshink — a project for monitoring trends in burn severity (MTBS) — 2007
- Chuvieco — historical background and current developments for mapping burned area from satellite EO — 2019
- Lizundia-Loiola — a spatio-temporal active-fire clustering approach for global burned area (FireCCI51) — 2020
- Roy — prototyping a global algorithm for systematic fire-affected area mapping (bidirectional reflectance) — 2005?
- Koltunov — the development and first validation of the GOES Early Fire Detection algorithm — 2016
- Kumar & Roy — global operational Landsat-8 reflectance-based active fire detection — 2018
- Barmpoutis — a review on early forest fire detection systems using optical remote sensing — 2020
- Muhammad — CNN-based fire detection in surveillance videos — 2018
- Frizzi — convolutional neural network for video fire and smoke detection — 2016
- Ba — SmokeNet, satellite smoke scene detection with spatial and channel-wise attention — 2019
- Toulouse — computer vision for wildfire research, an evolving image dataset (Corsican fire database) — 2017
- Yuan — a survey on technologies for automatic forest fire monitoring and detection using UAVs — 2015
- Merino — an unmanned aircraft system for automatic forest fire monitoring and measurement — 2012
- Shamsoshoara — aerial imagery pile-burn detection using deep learning (FLAME) — 2021
- Jakubik — Prithvi, foundation models for generalist geospatial AI (burn-scar downstream task) — 2023
- Yebra — a global review of remote sensing of live fuel moisture content — 2013
- Andela — a human-driven decline in global burned area — 2017
- Hawbaker — Landsat burned area essential climate variable products for the US — 2017? [unsure]

## Papers — fire-spread prediction and modelling

- Rothermel — a mathematical model for predicting fire spread in wildland fuels — 1972
- Van Wagner — development and structure of the Canadian Forest Fire Weather Index System — 1987
- Finney — FARSITE, fire area simulator, model development and evaluation — 1998
- Finney — a method for ensemble wildland fire simulation (FSim) — 2011
- Andrews — BehavePlus fire modeling system — 2007?
- Scott & Burgan — standard fire behavior fuel models — 2005
- Sullivan — wildland surface fire spread modelling 1990–2007 (physical / empirical / simulation reviews) — 2009
- Cruz & Alexander — uncertainty associated with model predictions of surface and crown fire rate of spread — 2013
- Mandel — coupled atmosphere-wildland fire modeling with WRF 3.3 and SFIRE 2011 — 2011
- Coen — WRF-Fire, coupled weather-wildland fire modeling with WRF — 2013
- Bakhshaii & Johnson — a review of a new generation of wildfire-atmosphere modeling — 2019
- Hantson — the status and challenge of global fire modelling (FireMIP) — 2016
- Jain — a review of machine learning applications in wildfire science and management — 2020
- Huot — Next Day Wildfire Spread, an ML dataset to predict wildfire spreading from remote-sensing data — 2022
- Radke — FireCast, leveraging deep learning to predict wildfire spread — 2019
- Hodges & Lattimer — wildland fire spread modeling using convolutional neural networks — 2019
- Burge — convolutional LSTM neural networks for modeling wildland fire dynamics — 2020?
- Allaire — emulation of wildland fire spread simulation using deep learning — 2021
- Gerard — WildfireSpreadTS, a dataset of multi-modal time series for wildfire spread prediction — 2023
- Prapas — deep learning methods for daily wildfire danger forecasting — 2021
- Kondylatos — wildfire danger prediction and understanding with deep learning — 2022
- Prapas — TeleViT, teleconnection-driven transformers for long-term wildfire forecasting — 2023
- Ganapathi Subramanian & Crowley — using spatial reinforcement learning to build forest wildfire dynamics models from satellite images — 2018
- Julian & Kochenderfer — distributed wildfire surveillance with autonomous aircraft using deep reinforcement learning — 2019
- Sayad — predictive modeling of wildfires, a new dataset and machine learning approach — 2019
- Vitolo — ERA5-based global meteorological wildfire danger maps — 2020

## Papers — fire regimes, drivers and climate

- Westerling — warming and earlier spring increase western US forest wildfire activity — 2006
- Abatzoglou & Williams — impact of anthropogenic climate change on wildfire across western US forests — 2016
- Parks & Abatzoglou — warmer and drier fire seasons contribute to increases in area burned at high severity — 2020
- Balch — human-started wildfires expand the fire niche across the United States — 2017
- Bowman — fire in the Earth system — 2009
- Bowman — vegetation fires in the Anthropocene — 2020
- Keeley & Syphard — twenty-first century California, USA, wildfires: fuel-dominated vs wind-dominated fires — 2019
- Burke — the changing risk and burden of wildfire in the United States — 2021
- Jolly — climate-induced variations in global wildfire danger 1979–2013 — 2015
- Williams — observed impacts of anthropogenic climate change on wildfire in California — 2019
- Hessburg — managing forests and fire in changing climates / wildfire paradox — 2015? [unsure]

## Papers — smoke, emissions and health

- van der Werf — global fire emissions estimates during 1997–2016 (GFED4s) — 2017
- Wiedinmyer — the Fire INventory from NCAR (FINN), a high-resolution global fire emissions model — 2011
- Reid — critical review of health impacts of wildfire smoke exposure — 2016
- Childs — daily local-level estimates of ambient wildfire smoke PM2.5 for the contiguous US — 2022
- Burke — the contribution of wildfire to PM2.5 trends in the USA — 2023
- Aguilera — wildfire smoke impacts respiratory health more than fine particles from other sources — 2021
- Jaffe — wildfire and prescribed burning impacts on air quality in the United States — 2020
- O'Dell — contribution of wildland-fire smoke to US PM2.5 and its influence on recent trends — 2019

## Datasets and benchmarks

- xBD / xView2 — pre/post satellite pairs, 19 disasters, 4-level damage scale; wildfire events include Santa Rosa (Tubbs), Woolsey, Carr, Pinery bushfire
- Maxar Open Data Program — post-event high-resolution imagery releases, most major US wildfires
- CAL FIRE DINS — Damage Inspection database, structure-by-structure destroyed/damaged records, California
- FEMA / NOAA post-event aerial imagery — oblique and nadir, US disasters
- FloodNet — UAV post-Hurricane-Harvey semantic segmentation
- RescueNet — UAV post-Hurricane-Michael pixel-level building damage
- FLAME — UAV RGB + thermal pile-burn video, Arizona prescribed fire
- FLAME 2 — paired RGB/IR UAV video, prescribed burn, with side information
- FLAME 3 — radiometric thermal + multispectral UAV fire imagery — 2024? [unsure]
- WIT-UAS — wildland-fire infrared thermal UAS dataset, crew/asset detection in thermal — 2023?
- FIgLib — Fire Ignition Library, HPWREN tower images around ~300 ignitions, ±40 min
- HPWREN / ALERTWildfire / ALERTCalifornia — the tower camera networks themselves
- Corsican Fire Database — visible and NIR fire-front imagery with segmentation ground truth
- FASDD — Flame and Smoke Detection Dataset, multi-source — 2023?
- D-Fire — fire and smoke bounding-box image dataset, Brazil
- Pyro-SDIS / Pyronear — French tower smoke-detection dataset — 2025? [unsure]
- Next Day Wildfire Spread — Huot, 1 km US rasters, 12 drivers + previous/next fire mask, 2012–2020
- WildfireSpreadTS — daily multi-modal time series, ~600 US fire events, 23 channels
- Mesogeos — Mediterranean wildfire datacube, daily 1 km, ML-ready — 2023
- SeasFire cube — global 8-day 0.25° seasonal fire drivers datacube
- WildfireDB — Singla, US spatio-temporal fire occurrence + fuel + weather — 2021? [unsure]
- MODIS MCD14ML / MCD14DL — active fire detections, 1 km, 2000–
- VIIRS VNP14IMG / VJ114 — 375 m active fire detections, 2012–
- NASA FIRMS — near-real-time active fire delivery for both of the above
- MODIS MCD64A1 — global monthly burned area, 500 m
- FireCCI51 — ESA CCI global burned area from MODIS 250 m
- GFED4 / GFED4s — global fire emissions and burned area, 0.25°
- Global Fire Atlas — Andela, individual fire perimeters, ignition, spread rate and direction from MCD64
- FIRED — fire event delineations from MODIS burned area, Balch/Earth Lab
- MTBS — Monitoring Trends in Burn Severity, US 1984–, dNBR/RdNBR, ≥1000 ac West
- FPA FOD — Short, spatial database of US wildfires 1992–, ~2 million records with cause
- GeoMAC / NIFC interagency fire perimeters — operational US perimeter history
- LANDFIRE — US fuels, vegetation and canopy layers at 30 m
- EFFIS — European Forest Fire Information System, burned area and danger
- NBAC / CNFDB — Canadian national burned area composite and fire database
- GOES-16/17/18 ABI fire product (FDCA) — geostationary 5-minute fire detection, Americas
- Sentinel-2 / Landsat burn-severity composites — dNBR from analysis-ready pairs
- ERA5 / ERA5-Land + FWI (Vitolo) — the standard meteorological driver stack for fire-danger models
- FireSat / Earth Fire Alliance — 5 m-class constellation for early detection — 2025? [unsure]

## People and groups

- Ritwik Gupta — DIU / Berkeley, xView2, computer vision for disaster response
- Maryam Rahnemoonfar — UAV disaster datasets (FloodNet, RescueNet)
- Robin Murphy — CRASAR, disaster robotics and UAS in the field
- Volker Radeloff — SILVIS Lab, Wisconsin, the WUI maps everyone uses
- Alexandra Syphard / Jon Keeley — structure loss and California fire regimes
- Jack Cohen — home ignition zone, retired USFS Missoula
- Mark Finney / Matt Jolly / Karen Short — USFS Missoula Fire Sciences Lab (FARSITE, FSim, FOD)
- Jennifer Balch — Earth Lab, CU Boulder (FIRED, human ignitions)
- John Abatzoglou / Crystal Kolden — UC Merced, climate and fire
- Emilio Chuvieco — Universidad de Alcalá, FireCCI, global burned area
- Louis Giglio / Luigi Boschetti / Wilfrid Schroeder — the MODIS and VIIRS fire products
- James Randerson / Yang Chen / Niels Andela — GFED, Global Fire Atlas
- Marta Yebra — ANU, live fuel moisture from remote sensing
- Sander Veraverbeke — VU Amsterdam, boreal fire and lightning ignition
- Fatemeh Afghah — Clemson, FLAME datasets and UAV fire imaging
- Ioannis Papoutsis / Ioannis Prapas / Spyros Kondylatos — NOA / ESA Φ-lab, Mediterranean wildfire deep learning
- Gustau Camps-Valls — Universitat de València, ML for Earth observation
- Marshall Burke / Sam Heft-Neal — Stanford ECHO lab, smoke, PM2.5 and economics
- Mike Gollner — UC Berkeley fire research lab, firebrands and WUI fire spread
- Janice Coen — NCAR, coupled fire-atmosphere modelling
- Google Research wildfire team — Next Day Wildfire Spread, boundary tracking, FireSat partnership
- Pyregence / Spatial Informatics Group — ELMFIRE and operational spread forecasting
- Descartes Labs / Muon Space / Earth Fire Alliance — commercial early-detection constellations

## Status

- Written: **2026-09-14**, by Claude Opus 5 from memory, no search (see Provenance)
- Resolved to S2 ids: _not yet_
- Scored against a run: _not yet_
