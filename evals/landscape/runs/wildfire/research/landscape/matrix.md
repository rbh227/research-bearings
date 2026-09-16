# Landscape matrix: wildfire from the air and from orbit

<!-- Eval run. Assembled mechanically in the main thread under the merger's contract: every paper line is copied from a section, every empty cell names its probe. -->

## Axes

- Formulation: active fire detection — from sections/1-formulations.md, surveys.md (Early Wildfire Detection: satellite surveillance)
- Formulation: burned area mapping — from sections/1-formulations.md, sections/4-reproduction.md
- Formulation: burn severity — from sections/1-formulations.md
- Formulation: fire spread prediction — from sections/1-formulations.md (FARSITE), sections/7-time-slice.md
- Formulation: smoke detection — from sections/6-adjacent.md, surveys.md (Early Wildfire Detection: camera networks)
- Data regime: coarse satellite (MODIS, VIIRS, GOES) — from sections/2-data-regimes.md
- Data regime: medium-resolution satellite (Landsat, Sentinel) — from sections/2-data-regimes.md, sections/4-reproduction.md
- Data regime: UAV and camera imagery — from sections/2-data-regimes.md, surveys.md (Early Wildfire Detection: UAV, camera networks)
- Data regime: deep learning benchmark dataset — from sections/2-data-regimes.md, sections/3-methods.md

## Matrix

| formulation \ regime | coarse satellite (MODIS, VIIRS, GOES) | medium-resolution satellite (Landsat, Sentinel) | UAV and camera imagery | deep learning benchmark dataset |
|---|---|---|---|---|
| active fire detection | 11 papers | 7 papers | 12 papers | 23 papers |
| burned area mapping | 11 papers | 22 papers | query returned 20 rows, 0 naming both | 12 papers |
| burn severity | query returned 20 rows, 0 naming both | 7 papers | 8 papers | 3 papers |
| fire spread prediction | 3 papers | query returned 20 rows, 0 naming both | 3 papers | 7 papers |
| smoke detection | query returned 20 rows, 0 naming both | query returned 20 rows, 0 naming both | 8 papers | 9 papers |

## Cells

### active fire detection × coarse satellite (MODIS, VIIRS, GOES)
- An Enhanced Contextual Fire Detection Algorithm for MODIS · 2003 · Remote Sensing of Environment · centrality 2 · influential _n/a_ · 77.12 cites/yr · openalex · OpenAlex `W1966272358` · verified — sections/1-formulations.md
- The collection 6 MODIS active fire detection algorithm and fire products · 2016 · openalex · OpenAlex `W2295931476` · verified — sections/1-formulations.md
- The New VIIRS 375 m active fire detection data product: Algorithm description and initial assessment · 2014 · Remote Sensing of Environment · centrality 3 · influential 103 · 90.69 cites/yr · both indexes · S2 `1ba8101ccfff95be06d1de4cb9d67eedfa5df555` · verified — sections/2-data-regimes.md
- Early characterization of the active fire detection products derived from the next generation NPOESS/VIIRS and GOES-R/ABI instruments · 2010 · IEEE International Geoscience and Remote Sensing Symposium · S2 `796f9f0a5310b0792268affed9f2b41eedc342f5` · verified — sections/cells.md
- Assessment of active fire detection in Serra da Canastra National Park using MODIS and VIIRS sensors · 2024 · The International Archives of the Photogrammetry, Remote Sensing and Spatial Information Sciences · S2 `e91f4f859fbed45b1cd81288c79598e835a5bdc4` · verified — sections/cells.md
- Sentinel-3 SLSTR active fire (AF) detection and FRP daytime product - Algorithm description and global intercomparison to MODIS, VIIRS and landsat AF data · 2023 · Science of Remote Sensing · S2 `a9bbaa2e91ea6d80b910367d808201d001140645` · verified — sections/cells.md
- First study of Sentinel-3 SLSTR active fire detection and FRP retrieval: Night-time algorithm enhancements and global intercomparison to MODIS and VIIRS AF products · 2020 · _no venue_ · S2 `4dbabd7b6727a3f2ddff6c1f7cc645f65c1f9cb6` · verified — sections/cells.md
- The Small Fire Detection Using Rgb Method Of Himawari-9 And Firms Satellite Imagery (Fire Information Resource Management System) Using Viirs And Modis Satellite Imagery In Medan Marelan (Case Study: 16 November 2023) · 2025 · Journals geographic · S2 `7731a27dd70c9b682598067583b42f19a36e53b8` · verified — sections/cells.md
- Optimization of forest burnt area assessment using MODIS and VIIRS active fire data · 2025 · Sovremennye problemy distantsionnogo zondirovaniya Zemli iz kosmosa · S2 `8762555b81bb3c9d2958650a8067ece960e7296b` · verified — sections/cells.md
- Assessing the performance of MODIS and VIIRS active fire products in the monitoring of wildfires: a case study in Turkey · 2022 · iForest : Biogeosciences and Forestry · S2 `8938a4b33c200dc090b578dc8dd0fbbf0767ebbe` · verified — sections/cells.md
- Fire Detection and Fire Radiative Power in Forests and Low-Biomass Lands in Northeast Asia: MODIS versus VIIRS Fire Products · 2020 · Remote Sensing · OpenAlex `W3083321098` · verified — sections/cells.md

### active fire detection × medium-resolution satellite (Landsat, Sentinel)
- Active fire detection using Landsat-8/OLI data · 2015 · Remote Sensing of Environment · centrality 2 · influential 26 · 28.58 cites/yr · both indexes · S2 `ec464e5a66c0b8d682fd679da29a8fef0f9129bc` · verified — sections/2-data-regimes.md
- Global operational land imager Landsat-8 reflectance-based active fire detection algorithm · 2017 · International Journal of Digital Earth · centrality 2 · influential 12 · 12.6 cites/yr · both indexes · S2 `501e51428e402698b889425516c0f65635e257c1` · verified — sections/2-data-regimes.md
- Active Fire Detection in Landsat-8 Imagery: a Large-Scale Dataset and a Deep-Learning Study · 2021 · S2 `67c44914a6ad177195583e8521ab8880e6c8f572` · verified — sections/2-data-regimes.md
- Active Fire Detection from Landsat-8 Imagery Using Deep Multiple Kernel Learning · 2022 · Remote Sensing · centrality 1 · influential 2 · 13.6 cites/yr · both indexes · S2 `f99acb7ebff50928d8f3763980161d6e85af9a7b` · verified — sections/5-abandoned.md
- A General and Robust Active Fire Detection Method Using Sentinel-2 and Landsat Shortwave Infrared Measurements · 2026 · IEEE Transactions on Geoscience and Remote Sensing · S2 `afc2fda5be267cbd8b4f3575d6d87b2770bc39e1` · verified — sections/cells.md
- Medium and High Resolution Multispectral Data from Landsat-8 and Sentinel-2 for Active Fire Monitoring and Post-Fire Assessment of Burned Areas: A Case Study on Vesuvius · 2018 · IEEE International Geoscience and Remote Sensing Symposium · S2 `6e0c678c1b492f1cb3e5fc17e06d553a6e8a6f52` · verified — sections/cells.md
- Active Fire Segmentation: A Transfer Learning Study From Landsat-8 to Sentinel-2 · 2024 · IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing · S2 `f762b5d70e5ab1fb0b83a67d13d3933b096c754d` · verified — sections/cells.md

### active fire detection × UAV and camera imagery
- Deep Learning and Transformer Approaches for UAV-Based Wildfire Detection and Segmentation · 2022 · Sensors · centrality 1 · influential 5 · 34.0 cites/yr · both indexes · S2 `16801631e490a9047d5c32551e1bac4649023e04` · verified — sections/2-data-regimes.md
- A review on early wildfire detection from unmanned aerial vehicles using deep learning-based computer vision algorithms · 2021 · Signal Processing · centrality 1 · influential 6 · 48.33 cites/yr · both indexes · S2 `c174e71e563fe44e754a8417b5b4b7e85702fd72` · verified — sections/2-data-regimes.md
- A Deep Learning Based Forest Fire Detection Approach Using UAV and YOLOv3 · 2019 · 2019 1st International Conference on Industrial Artificial Intelligence (IAI) · centrality 1 · influential 7 · 23.62 cites/yr · both indexes · S2 `9c68f1d2df0fc45d37f298890ca3f8d0863cacb3` · verified — sections/3-methods.md
- The Role of UAV-IoT Networks in Future Wildfire Detection · 2020 · IEEE Internet of Things Journal · centrality 1 · influential 3 · 24.71 cites/yr · both indexes · S2 `f25e6da8c1b05f1d6171792ae8c9c344921749aa` · verified — sections/3-methods.md
- SegNet: A segmented deep learning based Convolutional Neural Network approach for drones wildfire detection · 2024 · Remote Sensing Applications Society and Environment · centrality 26 · influential 1 · 16.67 cites/yr · both indexes · S2 `d2f00a4acc5ce505778ab284f9c397f054118245` · verified — sections/3-methods.md
- Real-Time Fire Detection: Integrating Lightweight Deep Learning Models on Drones with Edge Computing · 2024 · Drones · centrality 1 · influential 5 · 20.33 cites/yr · both indexes · S2 `03bd0216cc14469efeb338dec92b2a7c419a432a` · verified — sections/3-methods.md
- Depth-Homography Registration Framework and YOLOv8n-Coordinate Attention Forest Fire Detection for Visible-Infrared UAV Imagery · 2025 · Annual Conference of the IEEE Industrial Electronics Society · S2 `6e68f11209b48e6464bbbb0e320f9463612b9fcc` · verified — sections/cells.md
- Residual capsule network with threshold convolution and attention mechanism for forest fire detection using UAV imagery · 2025 · Scientific Reports · S2 `d64f689894e709bd8f85322dca2945a01aa1971d` · verified — sections/cells.md
- Thermal-Only Fire Detection: Using FLAME 3 UAV Imagery for Real-Time Thermal Fire Detection · 2025 · 2025 International Conference on Quantum Photonics, Artificial Intelligence, and Networking (QPAIN) · S2 `d81338331b0ead79dcbe5fe17e027aba201fbe94` · verified — sections/cells.md
- AF-Net: An Active Fire Detection Model Using Improved Object-Contextual Representations on Unbalanced UAV Datasets · 2024 · IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing · S2 `379bf5aa3be57ba7e94055c76c400bd85925483c` · verified — sections/cells.md
- CCLNet: An End-to-End Lightweight Network for Small-Target Forest Fire Detection in UAV Imagery · 2025 · Computers, Materials &amp; Continua · S2 `ef56e5dbc83a5f0d1e6e4790ee587dd1f6e3359e` · verified — sections/cells.md
- MFFDet: Enhancing Multi-Scale Forest Fire Detection in UAV Imagery · 2026 · Fire · S2 `473fef7cfa8b47f7a9d3bc1bec4e14a42c241f1d` · verified — sections/cells.md

### active fire detection × deep learning benchmark dataset
- Advancements in remote sensing for active fire detection: A review of datasets and methods · 2024 · The Science of The Total Environment · centrality 0 · influential _n/a_ · 26.67 cites/yr · openalex · OpenAlex `W4399246435` · verified — sections/1-formulations.md
- Deep Learning and Transformer Approaches for UAV-Based Wildfire Detection and Segmentation · 2022 · Sensors · centrality 1 · influential 5 · 34.0 cites/yr · both indexes · S2 `16801631e490a9047d5c32551e1bac4649023e04` · verified — sections/2-data-regimes.md
- Wildfire detection through deep learning based on Himawari-8 satellites platform · 2022 · International Journal of Remote Sensing · centrality 1 · influential 3 · 6.2 cites/yr · both indexes · S2 `959a0376a230e1425836640bd7914281d2d7a654` · verified — sections/2-data-regimes.md
- Optimizing Deep Learning Models for Fire Detection, Classification, and Segmentation Using Satellite Images · 2025 · Fire · centrality 1 · influential 0 · 12.5 cites/yr · both indexes · S2 `e5cf2ffd31726e0388633e461f2a9cb3bdba24b4` · verified — sections/2-data-regimes.md
- Active Fire Detection in Landsat-8 Imagery: a Large-Scale Dataset and a Deep-Learning Study · 2021 · S2 `67c44914a6ad177195583e8521ab8880e6c8f572` · verified — sections/2-data-regimes.md
- Review of Modern Forest Fire Detection Techniques: Innovations in Image Processing and Deep Learning · 2024 · Information · centrality 25 · influential 0 · 16.67 cites/yr · both indexes · S2 `368048845826e64373366fd6030977a0b00c04a5` · verified — sections/2-data-regimes.md
- A review on early wildfire detection from unmanned aerial vehicles using deep learning-based computer vision algorithms · 2021 · Signal Processing · centrality 1 · influential 6 · 48.33 cites/yr · both indexes · S2 `c174e71e563fe44e754a8417b5b4b7e85702fd72` · verified — sections/2-data-regimes.md
- A Deep Learning Based Forest Fire Detection Approach Using UAV and YOLOv3 · 2019 · 2019 1st International Conference on Industrial Artificial Intelligence (IAI) · centrality 1 · influential 7 · 23.62 cites/yr · both indexes · S2 `9c68f1d2df0fc45d37f298890ca3f8d0863cacb3` · verified — sections/3-methods.md
- SegNet: A segmented deep learning based Convolutional Neural Network approach for drones wildfire detection · 2024 · Remote Sensing Applications Society and Environment · centrality 26 · influential 1 · 16.67 cites/yr · both indexes · S2 `d2f00a4acc5ce505778ab284f9c397f054118245` · verified — sections/3-methods.md
- HybriDet: A Hybrid Neural Network Combining CNN and Transformer for Wildfire Detection in Remote Sensing Imagery · 2025 · Remote Sensing · centrality 9 · influential 0 · 4.5 cites/yr · both indexes · S2 `04f35698c8452540acbd559dfdaf83e0f34db6d8` · verified — sections/3-methods.md
- Real-Time Fire Detection: Integrating Lightweight Deep Learning Models on Drones with Edge Computing · 2024 · Drones · centrality 1 · influential 5 · 20.33 cites/yr · both indexes · S2 `03bd0216cc14469efeb338dec92b2a7c419a432a` · verified — sections/3-methods.md
- An open flame and smoke detection dataset for deep learning in remote sensing based fire detection · 2024 · Geo-Spatial Information Science · centrality 1 · influential 3 · 17.33 cites/yr · both indexes · S2 `f03b37be0b0b24f15d8f3f56da49ea1b5fe1606d` · verified — sections/3-methods.md
- A deep learning model using geostationary satellite data for forest fire detection with reduced detection latency · 2022 · GIScience &amp; Remote Sensing · centrality 25 · influential 2 · 18.0 cites/yr · both indexes · S2 `de8ac5752362608da615bc695792a9839422d5c9` · verified — sections/5-abandoned.md
- Active Fire Detection Using a Novel Convolutional Neural Network Based on Himawari-8 Satellite Images · 2022 · Frontiers in Environmental Science · centrality 1 · influential 2 · 11.4 cites/yr · both indexes · S2 `24351af01bdfbd1912bd53d0374e597eb12dbcf6` · verified — sections/5-abandoned.md
- An Improved Forest Fire Detection Method Based on the Detectron2 Model and a Deep Learning Approach · 2023 · Sensors · centrality 0 · influential _n/a_ · 37.0 cites/yr · openalex · OpenAlex `W4318464214` · verified — sections/6-adjacent.md
- Visual fire detection using deep learning: A survey · 2024 · Neurocomputing · centrality 0 · influential _n/a_ · 22.33 cites/yr · openalex · OpenAlex `W4399268516` · verified — sections/6-adjacent.md
- Fire Detection with Deep Learning: A Comprehensive Review · 2024 · Land · centrality 0 · influential _n/a_ · 19.33 cites/yr · openalex · OpenAlex `W4403494901` · verified — sections/6-adjacent.md
- Towards a Deep-Learning-Based Framework of Sentinel-2 Imagery for Automated Active Fire Detection · 2021 · Remote Sensing · S2 `384df2a36e5416a8174dc577793fcf042e1ede52` · verified — sections/cells.md
- DAFDM: A Discerning Deep Learning Model for Active Fire Detection Based on Landsat-8 Imagery · 2025 · IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing · S2 `642bff72b4acd0027ab0eb50072dc19cdbbb2cae` · verified — sections/cells.md
- Early Forest Fire Detection With UAV Image Fusion: A Novel Deep Learning Method Using Visible and Infrared Sensors · 2025 · IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing · S2 `be4d51932fe5aa2f08d7d23f5770c54418b557a3` · verified — sections/cells.md
- Deep Learning-Based Multistage Fire Detection System and Emerging Direction · 2024 · Fire · S2 `2cec82779212e051cdcd25a1dad352406f532380` · verified — sections/cells.md
- FASDD: An Open-access 100,000-level Flame and Smoke Detection Dataset for Deep Learning in Fire Detection · 2022 · _no venue_ · S2 `62142455c4a506d5dfacfffc3740be11e1f3b6eb` · verified — sections/cells.md
- Early Fire Detection and Segmentation Using Frame Differencing and Deep Learning Algorithms with an Indoor Dataset · 2024 · International Conference on Machine Learning and Soft Computing · S2 `e857d94ea6c310a63d1747fe2210f56ac8c6f864` · verified — sections/cells.md

### burned area mapping × coarse satellite (MODIS, VIIRS, GOES)
- A VIIRS direct broadcast algorithm for rapid response mapping of wildfire burned area in the western United States · 2018 · Remote Sensing of Environment · centrality 13 · influential 0 · 1.44 cites/yr · both indexes · S2 `1c2978705437a2a24cffa9f367901dfcdbf014fa` · verified — sections/4-reproduction.md
- The Collection 6 MODIS burned area mapping algorithm and product · 2018 · S2 `1ebb3236a20633e3393c5be83aa37bf8b383d5d4` · verified — sections/4-reproduction.md
- Global validation of the collection 6 MODIS burned area product · 2019 · S2 `489473ae0515b36c0f15d1e3c265d3a6b331b4e1` · verified — sections/4-reproduction.md
- The NASA VIIRS burned area product, global validation, and intercomparison with the NASA MODIS burned area product · 2025 · Remote Sensing of Environment · S2 `e3b7b423f79c92a3edeef8bd4724046c754aa6a2` · verified — sections/cells.md
- Global Near-Real-Time Burned Area Mapping Using Sentinel-2 and VIIRS Active Fires · 2026 · Fire · S2 `67bf218dc84c34539e252f26ca47069a0422a8de` · verified — sections/cells.md
- An automatic procedure for mapping burned areas globally using Sentinel-2 and VIIRS/MODIS active fires in Google Earth Engine · 2024 · Isprs Journal of Photogrammetry and Remote Sensing · S2 `e4ef04ac8a1e69d847bb40eb1fd19bc08df3f027` · verified — sections/cells.md
- Assessing VIIRS capabilities to improve burned area mapping over the Brazilian Cerrado · 2020 · _no venue_ · S2 `bc6f51fcc6a0302a35b61a54da21498a8e7c2859` · verified — sections/cells.md
- Interannual Dynamics of Boreal Forest Wildfires (2020–2024) Derived from MODIS-Constrained Sentinel-2 Burned-Area Mapping · 2026 · International Journal of Applied Earth Observation and Geoinformation · S2 `3d52e67f4cd2ebe58b6f08f1d43ff41830cf97e3` · verified — sections/cells.md
- Global burned area mapping from Sentinel-3 Synergy and VIIRS active fires · 2022 · Remote Sensing of Environment · S2 `6b0f130c9e940858e8dfce4f1dc1d14f0881e27c` · verified — sections/cells.md
- An Algorithm for Burned Area Detection in the Brazilian Cerrado Using 4 µm MODIS Imagery · 2015 · Remote Sensing · OpenAlex `W2179943257` · verified — sections/cells.md
- Size-dependent validation of MODIS MCD64A1 burned area over six vegetation types in boreal Eurasia: Large underestimation in croplands · 2017 · Scientific Reports · OpenAlex `W2658499583` · verified — sections/cells.md

### burned area mapping × medium-resolution satellite (Landsat, Sentinel)
- Deep learning high resolution burned area mapping by transfer learning from Landsat-8 to PlanetScope · 2022 · Remote Sensing of Environment · centrality 1 · influential 1 · 13.0 cites/yr · both indexes · S2 `dde1180fe3010953eef816eee6c5f27369fe1bfd` · verified — sections/1-formulations.md
- BiAU-Net: Wildfire burnt area mapping using bi-temporal Sentinel-2 imagery and U-Net with attention mechanism · 2024 · International Journal of Applied Earth Observation and Geoinformation · centrality 1 · influential 1 · 9.33 cites/yr · s2 · S2 `995a21d7dcf14885cc2f2b908f89a2b15cfb88c0` · verified — sections/1-formulations.md
- Total-variation regularized U-Net for wildfire burned area mapping based on Sentinel-1 C-Band SAR backscattering data · 2023 · Isprs Journal of Photogrammetry and Remote Sensing · centrality 1 · influential 1 · 5.25 cites/yr · s2 · S2 `e2a5716eb118b4ae1a1c55381e0d4508c23524fb` · verified — sections/1-formulations.md
- An alternative approach for mapping burn scars using Landsat imagery, Google Earth Engine, and Deep Learning in the Brazilian Savanna · 2021 · Remote Sensing Applications Society and Environment · centrality 1 · influential 2 · 10.5 cites/yr · both indexes · S2 `8e14e7f07891e687a836eecc0749b2c200409518` · verified — sections/3-methods.md
- Exploitation of Sentinel-2 Time Series to Map Burned Areas at the National Level: A Case Study on the 2017 Italy Wildfires · 2019 · Remote Sensing · centrality 25 · influential 4 · 17.88 cites/yr · both indexes · S2 `84a022c46616ada11a1800fcef97bd17a8c70523` · verified — sections/4-reproduction.md
- Burnt-Net: Wildfire burned area mapping with single post-fire Sentinel-2 data and deep learning morphological neural network · 2022 · Ecological Indicators · centrality 1 · influential 4 · 16.6 cites/yr · both indexes · S2 `c4da91b0bf547727479ce179677a11753a28a4a9` · verified — sections/5-abandoned.md
- Burned area detection and mapping using time series Sentinel-2 multispectral images · 2023 · Remote Sensing of Environment · centrality 1 · influential 2 · 12.25 cites/yr · both indexes · S2 `1771b3e2ea2d7df139d876b5081ffd2a9c0d471b` · verified — sections/5-abandoned.md
- Automatic Mapping of Burned Areas Using Landsat 8 Time-Series Images in Google Earth Engine: A Case Study from Iran · 2022 · Remote Sensing · centrality 1 · influential 2 · 4.4 cites/yr · both indexes · S2 `4b0f8e7eb77ab5e1822d43e67404377541c90d14` · verified — sections/5-abandoned.md
- Regional-scale burned area mapping in Mediterranean regions based on the multitemporal composite integration of Sentinel-1 and Sentinel-2 data · 2022 · GIScience &amp; Remote Sensing · centrality 1 · influential 1 · 5.6 cites/yr · both indexes · S2 `40f30597c19343d067011ef2700c774f1ca492fb` · verified — sections/5-abandoned.md
- Improved Burned Area Mapping Using Monotemporal Landsat-9 Imagery and Convolutional Shift-Transformer · 2023 · Measurement · centrality 1 · influential 0 · 5.0 cites/yr · both indexes · S2 `30a3dfdd86440313c2b545d5a4e19a999862edb1` · verified — sections/5-abandoned.md
- FLOGA: A Machine-Learning-Ready Dataset, a Benchmark, and a Novel Deep Learning Model for Burnt Area Mapping With Sentinel-2 · 2023 · IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing · centrality 1 · influential 0 · 3.5 cites/yr · both indexes · S2 `ca8ec0ac15bcf2542d7f6b0a5d5b9518eb1286ae` · verified — sections/5-abandoned.md
- Sentinel-2 sampling design and reference fire perimeters to assess accuracy of Burned Area products over Sub-Saharan Africa for the year 2019 · 2022 · Isprs Journal of Photogrammetry and Remote Sensing · centrality 1 · influential 0 · 2.8 cites/yr · both indexes · S2 `ab4b6f94d754e019172e32ae195d1db917891349` · verified — sections/5-abandoned.md
- Burned area mapping across the Arctic-boreal zone with Landsat and Sentinel-2 imagery · 2026 · International Journal of Remote Sensing · S2 `3bb09cfd03361614254f0b48f995d48aca64db4c` · verified — sections/cells.md
- Landsat-8 and Sentinel-2 burned area mapping - A combined sensor multi-temporal change detection approach · 2019 · Remote Sensing of Environment · S2 `348665625eeb316f40990de36cf109625427ae28` · verified — sections/cells.md
- Landsat and Sentinel-2 Based Burned Area Mapping Tools in Google Earth Engine · 2021 · Remote Sensing · S2 `efd47740335a86ef6a0559d78795ea1d87e2fea8` · verified — sections/cells.md
- Hyperspectral Knowledge-Guided Cross-Sensor Burned-Area Mapping: Distilling AVIRIS Semantics to Sentinel-2 and Landsat-8 · 2026 · IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing · S2 `a0b84b76361d6cc35238b00591ab8456bca5311f` · verified — sections/cells.md
- Exploring the utility of Sentinel-2 MSI and Landsat 8 OLI in burned area mapping for a heterogenous savannah landscape · 2020 · PLoS ONE · S2 `f4897363c3e5efe7c279b9bbafd68cff359951fb` · verified — sections/cells.md
- Deep learning-based burned area mapping of California wildfires using Sentinel-2 and Landsat-8 imagery enhanced with super-resolution techniques · 2026 · International Journal of Applied Earth Observation and Geoinformation · S2 `2eb712cf3a0eb2502fd7a80cce3b67ca84dcbe03` · verified — sections/cells.md
- Mapping Wetland Burned Area from Sentinel-2 across the Southeastern United States and Its Contributions Relative to Landsat-8 (2016–2019) · 2021 · Fire · S2 `1b3bed9ebf9dab120d12677a86e2dc07f5a158d2` · verified — sections/cells.md
- Comparative Analysis of Burned Area Detection Using Sentinel-2 and Landsat 8/9 in the 2025 Türkiye Wildfires · 2025 · 2025 4th International Conference on Geographic Information and Remote Sensing Technology (GIRST) · S2 `88f5c4eb95e6d61473aaef40f7c7ffbf293c35c6` · verified — sections/cells.md
- Refined burned-area mapping protocol using Sentinel-2 data increases estimate of 2019 Indonesian burning · 2021 · Earth System Science Data · S2 `535c7feb8a372f5c7a2201891ae543e1b06a0dab` · verified — sections/cells.md
- Burned area detection and mapping using Sentinel-1 backscatter coefficient and thermal anomalies · 2019 · Remote Sensing of Environment · OpenAlex `W2968773978` · verified — sections/cells.md

### burned area mapping × UAV and camera imagery
- query `burned area mapping UAV camera imagery` returned 20 rows, 0 naming both — sections/cells.md

### burned area mapping × deep learning benchmark dataset
- Deep learning high resolution burned area mapping by transfer learning from Landsat-8 to PlanetScope · 2022 · Remote Sensing of Environment · centrality 1 · influential 1 · 13.0 cites/yr · both indexes · S2 `dde1180fe3010953eef816eee6c5f27369fe1bfd` · verified — sections/1-formulations.md
- An alternative approach for mapping burn scars using Landsat imagery, Google Earth Engine, and Deep Learning in the Brazilian Savanna · 2021 · Remote Sensing Applications Society and Environment · centrality 1 · influential 2 · 10.5 cites/yr · both indexes · S2 `8e14e7f07891e687a836eecc0749b2c200409518` · verified — sections/3-methods.md
- Burnt-Net: Wildfire burned area mapping with single post-fire Sentinel-2 data and deep learning morphological neural network · 2022 · Ecological Indicators · centrality 1 · influential 4 · 16.6 cites/yr · both indexes · S2 `c4da91b0bf547727479ce179677a11753a28a4a9` · verified — sections/5-abandoned.md
- Improved Burned Area Mapping Using Monotemporal Landsat-9 Imagery and Convolutional Shift-Transformer · 2023 · Measurement · centrality 1 · influential 0 · 5.0 cites/yr · both indexes · S2 `30a3dfdd86440313c2b545d5a4e19a999862edb1` · verified — sections/5-abandoned.md
- FLOGA: A Machine-Learning-Ready Dataset, a Benchmark, and a Novel Deep Learning Model for Burnt Area Mapping With Sentinel-2 · 2023 · IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing · centrality 1 · influential 0 · 3.5 cites/yr · both indexes · S2 `ca8ec0ac15bcf2542d7f6b0a5d5b9518eb1286ae` · verified — sections/5-abandoned.md
- Deep Learning-Based Burned Area Mapping Using Bi-Temporal Siamese Networks and AlphaEarth Foundation Datasets · 2025 · arXiv.org · S2 `24e515ccb74b2d6316b153860aa2b9c93bc24438` · verified — sections/cells.md
- Assessment of L-Band and C-Band SAR on Burned Area Mapping of Multiseverity Forest Fires Using Deep Learning · 2025 · IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing · S2 `6ec61e8887e567a99d8d4dbd75e265a500b510ad` · verified — sections/cells.md
- DLSR-FireCNet: A Deep Learning Framework for Burned Area Mapping Based on Decision Level Super-Resolution · 2025 · Remote Sensing Applications Society and Environment · S2 `8bebb4d6db79d7e946b7ccabd0f51c852731fcc1` · verified — sections/cells.md
- RADARSAT Constellation Mission Compact Polarisation SAR Data for Burned Area Mapping with Deep Learning · 2024 · arXiv.org · S2 `921bc8230761bbdf01392619613fad85077447a7` · verified — sections/cells.md
- Burned Area Mapping With Radarsat Constellation Mission Data and Deep Learning · 2024 · IEEE International Geoscience and Remote Sensing Symposium · S2 `b1091361320149f15b9aa1bbf35f85a52c9120e9` · verified — sections/cells.md
- Mapping Burned Area in the Caatinga Biome: Employing Deep Learning Techniques · 2024 · Fire · S2 `3c0356826cb889ef8592767e2a5b8427a9af828b` · verified — sections/cells.md
- Assessment of Vegetation Indices for Mapping Burned Areas Using a Deep Learning Method and a Comprehensive Forest Fire Dataset from Landsat Collection · 2024 · Advances in Space Research · S2 `a89fe669c77360371da9d1c0f574525ee04ead94` · verified — sections/cells.md

### burn severity × coarse satellite (MODIS, VIIRS, GOES)
- query `burn severity MODIS VIIRS GOES` returned 20 rows, 0 naming both — sections/cells.md

### burn severity × medium-resolution satellite (Landsat, Sentinel)
- An Assessment of the Suitability of Sentinel-2 Data for Identifying Burn Severity in Areas of Low Vegetation · 2022 · Journal of the Indian Society of Remote Sensing · centrality 1 · influential 0 · 2.0 cites/yr · s2 · S2 `cf1dd5bbd653bb046f8045a3e02c7b15f134217b` · verified — sections/1-formulations.md
- Comparing Sentinel-2 and Landsat 8 for Burn Severity Mapping in Western North America · 2022 · Remote Sensing · S2 `ae4c5f4ad97590b7b8ac634e472d5ee2ee48f03c` · verified — sections/cells.md
- Inter comparison of post-fire burn severity indices of Landsat-8 and Sentinel-2 imagery using Google Earth Engine · 2021 · Earth Science Informatics · S2 `694b95bfdffa2b1b1644a9adbcbeabeea44067e2` · verified — sections/cells.md
- Evaluation and comparison of Landsat 8, Sentinel-2 and Deimos-1 remote sensing indices for assessing burn severity in Mediterranean fire-prone ecosystems · 2019 · International Journal of Applied Earth Observation and Geoinformation · S2 `ebd2ef85752a901d1fcd3e04fb40dfb51160c3d6` · verified — sections/cells.md
- Combination of Landsat and Sentinel-2 MSI data for initial assessing of burn severity · 2018 · International Journal of Applied Earth Observation and Geoinformation · S2 `0f662d6bff227edb6d8f9db0160b45447892d167` · verified — sections/cells.md
- Assessment of the Analytic Burned Area Index for Forest Fire Severity Detection Using Sentinel and Landsat Data · 2024 · Fire · S2 `4ad7af84338065c5f9b3099fe922735d49391bc1` · verified — sections/cells.md
- Evaluating and comparing Sentinel 2A and Landsat-8 Operational Land Imager (OLI) spectral indices for estimating fire severity in a Mediterranean pine ecosystem of Greece · 2017 · GIScience & Remote Sensing · OpenAlex `W2737778496` · verified — sections/cells.md

### burn severity × UAV and camera imagery
- Forest Burn Severity Mapping Using Multispectral Unmanned Aerial Vehicle Images and Light Detection and Ranging (LiDAR) Data: Comparison of Maximum Likelihood, Spectral Angle Mapper, and U-Net Classifiers · 2022 · Sensors and materials · centrality 1 · influential 0 · 0.6 cites/yr · s2 · S2 `0b31d8155894a1dca4e6763fbd493b7d8a6a8e21` · verified — sections/1-formulations.md
- Evaluating Burn Severity and Post-Fire Woody Vegetation Regrowth in the Kalahari Using UAV Imagery and Random Forest Algorithms · 2024 · Remote Sensing · S2 `9c43e8e4b36b8582537d5b6c17a1906b8f9a8070` · verified — sections/cells.md
- Early Visible Greenness Change in Forest Burned Areas Across Burn Severity and Mountainous Topography Using UAV RGB Imagery · 2026 · Fire · S2 `9c4fd52a827a7204c8d052d92888f6e6696ab2c1` · verified — sections/cells.md
- Integrating Physical-Based Models and Structure-from-Motion Photogrammetry to Retrieve Fire Severity by Ecosystem Strata from Very High Resolution UAV Imagery · 2024 · Fire · S2 `1609fc451b6ac7dc7ac60e676c0b16ee3c5c4750` · verified — sections/cells.md
- Automated Extraction of Forest Burn Severity Based on Light and Small UAV Visible Remote Sensing Images · 2022 · Forests · S2 `8154cad1a110f6edce91f46edf5260597de759da` · verified — sections/cells.md
- Calibrating Satellite-Based Indices of Burn Severity from UAV-Derived Metrics of a Burned Boreal Forest in NWT, Canada · 2017 · Remote Sensing · S2 `d40f3b89d7d4a96b83aed7dec4af61cf7b8efb89` · verified — sections/cells.md
- Evaluation of Fire Severity Indices Based on Pre- and Post-Fire Multispectral Imagery Sensed from UAV · 2019 · Remote Sensing · OpenAlex `W2940696663` · verified — sections/cells.md
- Using UAV Multispectral Images for Classification of Forest Burn Severity—A Case Study of the 2019 Gangneung Forest Fire · 2019 · Forests · OpenAlex `W2983291940` · verified — sections/cells.md

### burn severity × deep learning benchmark dataset
- Deep Learning Approaches for Wildfire Severity Prediction: A Comparative Study of Image Segmentation Networks and Visual Transformers on the EO4WildFires Dataset · 2024 · Fire · S2 `3d2b04705d3dc82a1344e53ee9a3b10a440b1228` · verified — sections/cells.md
- Predicting Wildfire Burn Severity from Pre-Fire SAR Signatures: A Deep Learning Approach · 2026 · 2026 International Conference on Advances in Artificial Intelligence and Machine Learning (AAIML) · S2 `1e5bfb7da3a8f1a2f24c627c306dedbdf9db6b45` · verified — sections/cells.md
- Deep Learning based fully automatic efficient Burn Severity Estimators for better Burn Diagnosis · 2020 · IEEE International Joint Conference on Neural Network · S2 `a2360084944c07b0042d00ce8005a60c684554e5` · verified — sections/cells.md

### fire spread prediction × coarse satellite (MODIS, VIIRS, GOES)
- Utilizing MODIS remote sensing and integrated data for forest fire spread modeling in the southwest region of Canada · 2024 · Environmental Research Communications · S2 `c34666a09dc9dc6eca2ba8db44f0c285579e559d` · verified — sections/cells.md
- Evaluating characterization of fire extent and fire spread in boreal and tundra fires of Alaska from coarse and moderate resolution MODIS and VIIRS data · 2017 · _no venue_ · S2 `0565388bddd09458c196c3508bec9215d42a270f` · verified — sections/cells.md
- California wildfire spread derived using VIIRS satellite observations and an object-based tracking system · 2022 · Scientific Data · OpenAlex `W4281685235` · verified — sections/cells.md

### fire spread prediction × medium-resolution satellite (Landsat, Sentinel)
- query `fire spread prediction Landsat Sentinel-2` returned 20 rows, 0 naming both — sections/cells.md

### fire spread prediction × UAV and camera imagery
- Wildfire Spread Prediction Through Remote Sensing and UAV Imagery-Driven Machine Learning Models · 2024 · International Conference on Control, Automation, Robotics and Vision · S2 `3d82281b5f997841584c13b00d39831bf6ea668e` · verified — sections/cells.md
- FireCast-fusion: Physics-Guided fusion of UAV RGB–thermal imagery and environmental data for near-term wildfire spread prediction · 2026 · Science of Remote Sensing · S2 `86fe6b2c167bdf07d353a744b9d48aaee9c6c236` · verified — sections/cells.md
- Prediction of Forest Fire Spread Rate Using UAV Images and an LSTM Model Considering the Interaction between Fire and Wind · 2021 · Remote Sensing · S2 `daf9f183127221da6e2cd4f9e5ad7cb2f39d9d6a` · verified — sections/cells.md

### fire spread prediction × deep learning benchmark dataset
- A global wildfire dataset for the analysis of fire regimes and fire behaviour · 2019 · Scientific Data · centrality 26 · influential 10 · 47.38 cites/yr · both indexes · S2 `53b9b53a62572d60878c54ad511ca6fe161ccb0d` · verified — sections/1-formulations.md
- Next Day Wildfire Spread: A Machine Learning Dataset to Predict Wildfire Spreading From Remote-Sensing Data · 2021 · s2 · S2 `b205af39f42e87a99738f30621c1ef48ed609893` · verified — sections/1-formulations.md
- CNN-BiLSTM: A Novel Deep Learning Model for Near-Real-Time Daily Wildfire Spread Prediction · 2024 · Remote Sensing · centrality 1 · influential 4 · 27.33 cites/yr · both indexes · S2 `df2c61815dae0722fe5b7c77548cb022831e5e54` · verified — sections/3-methods.md
- Machine Learning and Deep Learning for Wildfire Spread Prediction: A Review · 2024 · Fire · centrality 25 · influential _n/a_ · 21.0 cites/yr · openalex · OpenAlex `W4405528901` · verified — sections/3-methods.md
- Generative AI as a Pillar for Predicting 2D and 3D Wildfire Spread: Beyond Physics-Based Models and Traditional Deep Learning · 2025 · Fire · centrality 14 · influential 0 · 7.0 cites/yr · both indexes · S2 `f96dde8e78f4b9cf657f3c0b753fd39a0fbb33aa` · verified — sections/7-time-slice.md
- ABNextFire: A Multisource Deep Learning Based Dataset for Wildfire Spread Prediction · 2026 · IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing · S2 `fabc78a44cbc74c0a6c97a035c571dc0d6085e31` · verified — sections/cells.md
- Assessment of deep learning models integrated with weather and environmental variables for wildfire spread prediction and a case study of the 2023 Maui fires · 2025 · Natural Hazards · S2 `d106c1951f82ace9776607177d8eb51b919d807c` · verified — sections/cells.md

### smoke detection × coarse satellite (MODIS, VIIRS, GOES)
- query `smoke detection MODIS VIIRS GOES` returned 20 rows, 0 naming both — sections/cells.md

### smoke detection × medium-resolution satellite (Landsat, Sentinel)
- query `smoke detection Landsat Sentinel-2` returned 20 rows, 0 naming both — sections/cells.md

### smoke detection × UAV and camera imagery
- A Wildfire Smoke Detection System Using Unmanned Aerial Vehicle Images Based on the Optimized YOLOv5 · 2022 · Sensors · centrality 1 · influential 6 · 20.0 cites/yr · both indexes · S2 `dd6dc3d2e24704be75416d5f0fd09dadc0870743` · verified — sections/2-data-regimes.md
- LMDFS: A Lightweight Model for Detecting Forest Fire Smoke in UAV Images Based on YOLOv7 · 2023 · Remote Sensing · centrality 1 · influential 2 · 14.25 cites/yr · both indexes · S2 `4e0c74e2b2743e38c74333af44d713222438a1d1` · verified — sections/3-methods.md
- Semi-Supervised YOLO Framework for Real-Time Wildfire Smoke Detection from UAV Imagery · 2025 · 2025 28th International Conference on Computer and Information Technology (ICCIT) · S2 `d1c129fdd5afdca9150b59879ad697773263004b` · verified — sections/cells.md
- Wildfire Fire-Smoke Detection in UAV Imagery via Scale-Guided Feature Routing and Uncertainty-Aware Localization · 2026 · IEEE Access · S2 `41702998c1936a6a7e89fccc3ac4a471cc674665` · verified — sections/cells.md
- DSC-Det: A Detail–Scale–Context Detection Network for Forest-Fire-Oriented Early Fire and Smoke Detection in UAV-View and Complex-Background Imagery · 2026 · Fire · S2 `6835ec8416ccb6da27813a4e673b284d279c753f` · verified — sections/cells.md
- Efficient Detection of Forest Fire Smoke in UAV Aerial Imagery Based on an Improved Yolov5 Model and Transfer Learning · 2023 · Remote Sensing · S2 `9e5703e15440a5449cb34565fa30db1afd9f6d6a` · verified — sections/cells.md
- Real-Time Detection of Smoke and Fire in the Wild Using Unmanned Aerial Vehicle Remote Sensing Imagery · 2025 · Forests · S2 `641022444ea4b3b0e6e4d6d966eab043338f792d` · verified — sections/cells.md
- An Improved Wildfire Smoke Detection Based on YOLOv8 and UAV Images · 2023 · Sensors · OpenAlex `W4387503115` · verified — sections/cells.md

### smoke detection × deep learning benchmark dataset
- Real-Time Detection of Full-Scale Forest Fire Smoke Based on Deep Convolution Neural Network · 2022 · Remote Sensing · centrality 25 · influential _n/a_ · 18.6 cites/yr · openalex · OpenAlex `W4207031702` · verified — sections/3-methods.md
- A forest fire smoke detection model combining convolutional neural network and vision transformer · 2023 · Frontiers in Forests and Global Change · centrality 25 · influential _n/a_ · 10.0 cites/yr · openalex · OpenAlex `W4366212872` · verified — sections/3-methods.md
- An open flame and smoke detection dataset for deep learning in remote sensing based fire detection · 2024 · Geo-Spatial Information Science · centrality 1 · influential 3 · 17.33 cites/yr · both indexes · S2 `f03b37be0b0b24f15d8f3f56da49ea1b5fe1606d` · verified — sections/3-methods.md
- SmokeNet: Satellite Smoke Scene Detection Using Convolutional Neural Network with Spatial and Channel-Wise Attention · 2019 · Remote Sensing · centrality 25 · influential 12 · 19.5 cites/yr · both indexes · S2 `f874e9bc3d50fc44a81c3baf124eda5b4f63184f` · verified — sections/6-adjacent.md
- Integrating Color and Contour Analysis with Deep Learning for Robust Fire and Smoke Detection · 2025 · Italian National Conference on Sensors · S2 `92834ad773369bd09241e5072cacf7cec574e17b` · verified — sections/cells.md
- FASDD: An Open-access 100,000-level Flame and Smoke Detection Dataset for Deep Learning in Fire Detection · 2022 · _no venue_ · S2 `62142455c4a506d5dfacfffc3740be11e1f3b6eb` · verified — sections/cells.md
- High Quality Fire Smoke Dataset: A Benchmark for Fire and Smoke Detection · 2024 · MCGE@MM · S2 `84d597b7469fbc9d182ab70b55c354223422dca9` · verified — sections/cells.md
- Deep Learning-Based Fire Detector Robust to Smoke–Fog Ambiguity in Outdoor Scenes · 2026 · Applied Sciences · S2 `086b76c0f1d572874c7cccebd61ce49c09c1dc49` · verified — sections/cells.md
- A dataset for fire and smoke object detection · 2022 · Multimedia Tools and Applications · OpenAlex `W4292074855` · verified — sections/cells.md

## Contradictions

- Historical background and current developments for mapping burned area from satellite Earth observation — id OpenAlex W2920767026 in sections/1-formulations.md, S2 4e604cb0bb8b4718fcfdfdcbf9e397e76557414c in sections/6-adjacent.md
- Global burned area and biomass burning emissions from small fires — id OpenAlex W2131491776 in sections/1-formulations.md, S2 3201126ca0d32ad192f2e1e1e04ecb104eb8d8a8 in sections/4-reproduction.md
- The human dimension of fire regimes on Earth — id OpenAlex W1535679254 in sections/1-formulations.md, S2 f4f4fca059406e752c5630b2fd4f8e432279d55e in sections/4-reproduction.md
- FARSITE: Fire Area Simulator-model development and evaluation — id OpenAlex W1531419578 in sections/1-formulations.md, OpenAlex W1531419578 in sections/3-methods.md, S2 6abe7536ae31f2fa37ee3f6e05c6601183f4ca0a in sections/4-reproduction.md, S2 6abe7536ae31f2fa37ee3f6e05c6601183f4ca0a in sections/7-time-slice.md
- Climate controls on the variability of fires in the tropics and subtropics — id OpenAlex W1581244734 in sections/1-formulations.md, S2 0a62c3b2b79ea0ef080e5a6ec8aebd771328d622 in sections/4-reproduction.md
- Modeling fire and the terrestrial carbon balance — id OpenAlex W1657442206 in sections/1-formulations.md, S2 25d8c0aae1989e981670e2d3fe77ad2e223a402c in sections/4-reproduction.md
- An Enhanced Contextual Fire Detection Algorithm for MODIS — id OpenAlex W1966272358 in sections/1-formulations.md, S2 f2376acb71a89f5fe4f2c4dbb46b50f6524a6442 in sections/5-abandoned.md, S2 f2376acb71a89f5fe4f2c4dbb46b50f6524a6442 in sections/6-adjacent.md
- Large-scale impoverishment of Amazonian forests by logging and fire — id OpenAlex W1626806761 in sections/1-formulations.md, S2 4a31feb8468936a9bb3246196bcff5a3bc2d0c99 in sections/4-reproduction.md, S2 4a31feb8468936a9bb3246196bcff5a3bc2d0c99 in sections/5-abandoned.md
- The collection 6 MODIS active fire detection algorithm and fire products — id OpenAlex W2295931476 in sections/1-formulations.md, S2 9f9c0f5fa7076a9388db22e5a18f6c0d170d33d3 in sections/2-data-regimes.md, S2 9f9c0f5fa7076a9388db22e5a18f6c0d170d33d3 in sections/5-abandoned.md
- Global and Regional Trends and Drivers of Fire Under Climate Change — id OpenAlex W4223653531 in sections/1-formulations.md, S2 79d6feefc8a0a4e9fa75a8d9d110de9a2873319d in sections/4-reproduction.md, S2 79d6feefc8a0a4e9fa75a8d9d110de9a2873319d in sections/6-adjacent.md
- A survey on technologies for automatic forest fire monitoring, detection, and fighting using unmanned aerial vehicles and remote sensing techniques — id OpenAlex W1852719163 in sections/1-formulations.md, S2 9ced279cf4b48349b9d960e2f65c2ae0cc0b3eb2 in sections/4-reproduction.md, S2 9ced279cf4b48349b9d960e2f65c2ae0cc0b3eb2 in sections/5-abandoned.md
- A review of machine learning applications in wildfire science and management — id OpenAlex W3008626511 in sections/1-formulations.md, S2 b8f75b848b6cef0f2b5a1a11b794332ca9bccb45 in sections/2-data-regimes.md, OpenAlex W3008626511 in sections/3-methods.md, OpenAlex W3008626511 in sections/6-adjacent.md
- Forest fire surveillance systems: A review of deep learning methods — id OpenAlex W4389279575 in sections/1-formulations.md, S2 2c0539d40c4f2b0aca9cd37ae292c25a49667a51 in sections/2-data-regimes.md, OpenAlex W4389279575 in sections/4-reproduction.md, S2 2c0539d40c4f2b0aca9cd37ae292c25a49667a51 in sections/7-time-slice.md
- U-Net: Convolutional Networks for Biomedical Image Segmentation — id S2 6364fdaa0a0eccd823a779fcdd489173f938e91a in sections/2-data-regimes.md, OpenAlex W1901129140 in sections/3-methods.md, S2 6364fdaa0a0eccd823a779fcdd489173f938e91a in sections/4-reproduction.md, S2 6364fdaa0a0eccd823a779fcdd489173f938e91a in sections/7-time-slice.md
- Fully convolutional networks for semantic segmentation — id S2 6fc6803df5f9ae505cae5b2f178ade4062c768d0 in sections/2-data-regimes.md, OpenAlex W1903029394 in sections/3-methods.md, S2 6fc6803df5f9ae505cae5b2f178ade4062c768d0 in sections/4-reproduction.md
- Active fire detection using Landsat-8/OLI data — id S2 ec464e5a66c0b8d682fd679da29a8fef0f9129bc in sections/2-data-regimes.md, OpenAlex W2200518663 in sections/3-methods.md
- Deep Residual Learning for Image Recognition — id S2 2c03df8b48bf3fa39054345bafabfeff15bfd11d in sections/2-data-regimes.md, OpenAlex W2194775991 in sections/3-methods.md, S2 2c03df8b48bf3fa39054345bafabfeff15bfd11d in sections/4-reproduction.md, S2 2c03df8b48bf3fa39054345bafabfeff15bfd11d in sections/7-time-slice.md
- ImageNet: A large-scale hierarchical image database — id S2 d2c733e34d48784a37d717fe43d9e93277a8c53e in sections/2-data-regimes.md, OpenAlex W2108598243 in sections/3-methods.md, S2 d2c733e34d48784a37d717fe43d9e93277a8c53e in sections/4-reproduction.md
- Deep Learning Approaches for Wildland Fires Using Satellite Remote Sensing Data: Detection, Mapping, and Prediction — id S2 a78ab85056f1d12d09d406fc153d7a05afaa506a in sections/2-data-regimes.md, OpenAlex W4382624116 in sections/3-methods.md, S2 a78ab85056f1d12d09d406fc153d7a05afaa506a in sections/4-reproduction.md
- Going deeper with convolutions — id OpenAlex W2097117768 in sections/3-methods.md, S2 e15cf50aa89fee8535703b9f9512fca5bfc43327 in sections/4-reproduction.md, S2 e15cf50aa89fee8535703b9f9512fca5bfc43327 in sections/6-adjacent.md, S2 e15cf50aa89fee8535703b9f9512fca5bfc43327 in sections/7-time-slice.md
- Machine Learning and Deep Learning for Wildfire Spread Prediction: A Review — id OpenAlex W4405528901 in sections/3-methods.md, S2 b9447d630486b8e888f0baca0b7fe1c6b67ac704 in sections/7-time-slice.md
- A Review on Early Forest Fire Detection Systems Using Optical Remote Sensing — id S2 18e8eb6860fdedc651f22f80cc7e0dea10997c23 in sections/3-methods.md, S2 18e8eb6860fdedc651f22f80cc7e0dea10997c23 in sections/5-abandoned.md, OpenAlex W3100733145 in sections/6-adjacent.md
- Review Article Digital change detection techniques using remotely-sensed data — id OpenAlex W2036798369 in sections/3-methods.md, S2 870b887ad2f17ea722f0c27fd4e195cce691792b in sections/5-abandoned.md
- Advancing horizons in remote sensing: a comprehensive survey of deep learning models and applications in image classification and beyond — id OpenAlex W4401253027 in sections/6-adjacent.md, S2 c3bc69e723e7420294cf143b5af7e6bcd47f7eb2 in sections/7-time-slice.md
- CLLMate: A Multimodal Benchmark for Weather and Climate Events Forecasting — year 2025 in sections/7-time-slice.md, 2024 in sections/7-time-slice.md
- CLLMate: A Multimodal Benchmark for Weather and Climate Events Forecasting — id S2 907ac8c37715e71d29cd655361f54060038b4594 in sections/7-time-slice.md, S2 d7d205e61a42f41897cfbf7700af42e58e0db0ca in sections/7-time-slice.md

## Sources

- sections/1-formulations.md — 63 papers
- sections/2-data-regimes.md — 63 papers
- sections/3-methods.md — 62 papers
- sections/4-reproduction.md — 63 papers
- sections/5-abandoned.md — 60 papers
- sections/6-adjacent.md — 60 papers
- sections/7-time-slice.md — 60 papers
- sections/surveys.md — 20 papers
- sections/cells.md — 388 rows over 20 probes

## Status

2026-09-16. Cells 15 filled / 5 empty / 20 total. Contradictions 26. Sections reporting a degraded index: sections/1-formulations.md, sections/3-methods.md, sections/surveys.md.
