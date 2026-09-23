# Landscape matrix: post-disaster building damage assessment from aerial and satellite imagery

<!-- Eval run. Assembled mechanically in the main thread under the merger's contract: every paper line is copied from a section, every empty cell names its probe. -->

## Axes

- Formulation: per-building damage classification — from sections/1-formulations.md, surveys.md (Decadal Review: damage detection and analysis)
- Formulation: semantic change detection — from sections/3-methods.md
- Formulation: building segmentation and localization — from sections/1-formulations.md, sections/4-reproduction.md (RescueNet)
- Formulation: object-based change analysis — from sections/5-abandoned.md
- Data regime: paired pre/post satellite (xBD, xView2) — from sections/2-data-regimes.md, sections/4-reproduction.md
- Data regime: UAV and oblique aerial post-event — from sections/1-formulations.md, sections/6-adjacent.md
- Data regime: SAR and multisensor — from sections/6-adjacent.md, surveys.md (Decadal Review: data fusion)
- Data regime: weak or cross-event supervision — from sections/2-data-regimes.md, sections/4-reproduction.md (out-of-domain generalization)

## Matrix

| formulation \ regime | paired pre/post satellite (xBD, xView2) | UAV and oblique aerial post-event | SAR and multisensor | weak or cross-event supervision |
|---|---|---|---|---|
| per-building damage classification | 20 papers | 10 papers | 17 papers | 5 papers |
| semantic change detection | 14 papers | 6 papers | 15 papers | 1 paper |
| building segmentation and localization | 3 papers | 3 papers | 8 papers | query returned 13 rows, 0 naming both |
| object-based change analysis | 1 paper | 7 papers | 4 papers | 1 paper |

## Cells

### per-building damage classification × paired pre/post satellite (xBD, xView2)
- Building Damage Detection Using U-Net with Attention Mechanism from Pre- and Post-Disaster Remote Sensing Datasets · 2021 · Remote Sensing · centrality 26 · influential 4 · 21.0 cites/yr · both indexes · S2 `da79cea06877710ef6ddc40195b8766bb1b72177` · verified — sections/1-formulations.md
- SATELLITE IMAGE CLASSIFICATION OF BUILDING DAMAGES USING AIRBORNE AND SATELLITE IMAGE SAMPLES IN A DEEP LEARNING APPROACH · 2018 · ISPRS annals of the photogrammetry, remote sensing and spatial information sciences · centrality 26 · influential 2 · 12.22 cites/yr · both indexes · S2 `9778a858fb9660a7c613344aa8a4cbcc2b8c8ce6` · verified — sections/1-formulations.md
- BDANet: Multiscale Convolutional Neural Network With Cross-Directional Attention for Building Damage Assessment From Satellite Images · 2021 · IEEE Transactions on Geoscience and Remote Sensing · centrality 3 · influential 13 · 22.0 cites/yr · both indexes · S2 `013ec50cdd6524f78bb0f575f5b51a498c669fcb` · verified — sections/1-formulations.md
- Building-damage detection using post-seismic high-resolution SAR satellite data · 2010 · International Journal of Remote Sensing · centrality 2 · influential 5 · 7.65 cites/yr · both indexes · S2 `8a39e9e2c373bc2c2b8c9fbd80cf25b4624aed6a` · verified — sections/1-formulations.md
- BD-SKUNet: Selective-Kernel UNets for Building Damage Assessment in High-Resolution Satellite Images · 2023 · Remote Sensing · centrality 25 · influential 2 · 6.5 cites/yr · both indexes · S2 `5e1f1e4b4d024e14e3a3dd430674ea1f68ccddf1` · verified — sections/1-formulations.md
- Large‐scale building damage assessment using a novel hierarchical transformer architecture on satellite images · 2022 · Comput. Aided Civ. Infrastructure Eng. · centrality 20 · influential 8 · 21.6 cites/yr · both indexes · S2 `14f3b91fd524d853aea082b322008411d555da5e` · verified — sections/1-formulations.md
- On Transfer Learning for Building Damage Assessment from Satellite Imagery in Emergency Contexts · 2022 · Remote Sensing · centrality 1 · influential 3 · 10.0 cites/yr · both indexes · S2 `6652acdf80a6fbb7a76c73a15c6525026124e603` · verified — sections/1-formulations.md
- Automated building damage assessment and large‐scale mapping by integrating satellite imagery, GIS, and deep learning · 2024 · Computer-Aided Civil and Infrastructure Engineering · centrality 1 · influential 1 · 24.67 cites/yr · both indexes · S2 `008e6d9e0d45f54cbc61405eeddc5c8da96e9472` · verified — sections/1-formulations.md
- Bitemporal Attention Transformer for Building Change Detection and Building Damage Assessment · 2024 · IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing · centrality 25 · influential 1 · 12.33 cites/yr · both indexes · S2 `04c8c9e047b33a20b945140e09faa202b1df7319` · verified — sections/3-methods.md
- xBD: A Dataset for Assessing Building Damage from Satellite Imagery · 2019 · _no venue_ · centrality 27 · influential _n/a_ · 8.62 cites/yr · openalex · OpenAlex `W2991131216` · verified — sections/4-reproduction.md
- RescueNet: Joint Building Segmentation and Damage Assessment from Satellite Imagery · 2021 · International Conference on Pattern Recognition · centrality 23 · influential 10 · 3.83 cites/yr · both indexes · S2 `0c433390c7d5c10441ccc45af60f597446f18f64` · verified — sections/4-reproduction.md
- Creating xBD: A Dataset for Assessing Building Damage from Satellite Imagery · 2019 · CVPR Workshops · centrality 2 · influential 37 · 19.5 cites/yr · both indexes · S2 `ec58b5946c57f7d4d4a3cff0566941bb93291c95` · verified — sections/4-reproduction.md
- An Attention-Based System for Damage Assessment Using Satellite Imagery · 2020 · 2021 IEEE International Geoscience and Remote Sensing Symposium IGARSS · centrality 2 · influential 6 · 8.29 cites/yr · both indexes · S2 `5f75fdfb01a721d9694fe09f3c829342b73063d5` · verified — sections/4-reproduction.md
- Building Damage Detection in Satellite Imagery Using Convolutional Neural Networks · 2019 · _no venue_ · centrality 2 · influential _n/a_ · 14.5 cites/yr · openalex · OpenAlex `W2980937832` · verified — sections/4-reproduction.md
- Disaster assessment using computer vision and satellite imagery: Applications in detecting water-related building damages · 2022 · Frontiers in Environmental Science · centrality 14 · influential 0 · 3.8 cites/yr · both indexes · S2 `30eb0b260032aaec8d8a00c8abd20da6369e4987` · verified — sections/4-reproduction.md
- Building Damage Detection using Satellite Images and Patch-Based Transformer Methods · 2026 · arXiv.org · centrality 2 · influential 0 · 2.0 cites/yr · both indexes · S2 `32c1bf47110ecb6bee2a8f0da93ac0a94762192c` · verified — sections/4-reproduction.md
- CADSNet: Cross-Aligned Dual-Stream Network for Building Damage Assessment Using Disaster Satellite Imagery · 2025 · International Conferences on Computing Advancements · S2 `30174c0412fc1a0c0fa9909ce9dfe519850b31a1` · verified — sections/cells.md
- DeepDamageNet: A two-step deep-learning model for multi-disaster building damage segmentation and classification using satellite imagery · 2024 · arXiv.org · S2 `d7e737d6626e554361e6865e1a52f08ace5819a8` · verified — sections/cells.md
- Vision transformer based damage assessment from post-disaster satellite imagery: an applied study on hurricane harvey · 2026 · Earth Science Informatics · S2 `5302b3cfb61ef0121adf16528600788e1d348a2f` · verified — sections/cells.md
- Deep object segmentation and classification networks for building damage detection using the xBD dataset · 2024 · International Journal of Digital Earth · OpenAlex `W4390670365` · verified — sections/cells.md

### per-building damage classification × UAV and oblique aerial post-event
- Disaster damage detection through synergistic use of deep learning and 3D point cloud features derived from very high resolution oblique aerial images, and multiple-kernel-learning · 2017 · ISPRS Journal of Photogrammetry and Remote Sensing · centrality 2 · influential 12 · 33.6 cites/yr · both indexes · S2 `15b7774071b369240eecdfc962a507c2d3cfdf73` · verified — sections/1-formulations.md
- UAV-based urban structural damage assessment using object-based image analysis and semantic reasoning · 2015 · Natural hazards and earth system sciences · centrality 2 · influential 5 · 19.75 cites/yr · both indexes · S2 `3cf417fc3bdd5ec057ef0d05be40aebd8b648605` · verified — sections/1-formulations.md
- Damage detection from aerial images via convolutional neural networks · 2017 · IAPR International Workshop on Machine Vision Applications · centrality 3 · influential 14 · 16.3 cites/yr · both indexes · S2 `c93b0d1b6676395467094b2a7c4ce2a76a86f91f` · verified — sections/4-reproduction.md
- Post-Disaster Building Damage Assessment Using 3D Surface Models Derived from Unmanned Aerial Vehicle (UAV) Imagery · 2026 · ISPRS Annals of the Photogrammetry, Remote Sensing and Spatial Information Sciences · S2 `cac1d29fba4c5f718db4e73eb6dc469f2f054629` · verified — sections/cells.md
- Building Damage Detection from Post-Event Aerial Imagery Using Single Shot Multibox Detector · 2019 · Applied Sciences · S2 `4ff2ccbc3b68c472592f9a9b82a64b5fa4bbb0be` · verified — sections/cells.md
- Assessing the Benefits of Combining Advanced Deep Learning Techniques for Post-Disaster Building Damage Assessment from UAV Imagery · 2026 · _no venue_ · S2 `3381f492cc8b7dc08bdaa3cc44ca0a08a7d4f731` · verified — sections/cells.md
- Comparative analysis of deep feature fusion and machine learning classifiers for UAV imagery in post-earthquake building damage assessment · 2026 · Gümüşhane Üniversitesi Fen Bilimleri Enstitüsü Dergisi · S2 `86123a4a9743f85831ac03b8342b44a3a7211be9` · verified — sections/cells.md
- Graph-Attention Network for Spatially-Aware Post-Hurricane Building Damage Assessment from UAV Imagery · 2026 · ISPRS Annals of the Photogrammetry, Remote Sensing and Spatial Information Sciences · S2 `a25312602d9eb300579e42a632bb5286ab9af369` · verified — sections/cells.md
- MCANet: A Multi-Scale Class-Specific Attention Network for Multi-Label Post-Hurricane Damage Assessment using UAV Imagery · 2025 · arXiv.org · S2 `b4196dc3582d7838fb4a482c28f18ae6dcc0a65c` · verified — sections/cells.md
- BDHE-Net: A Novel Building Damage Heterogeneity Enhancement Network for Accurate and Efficient Post-Earthquake Assessment Using Aerial and Remote Sensing Data · 2024 · Applied Sciences · S2 `98bee6ea9a3db8b8d3b74bda0bb25f27f8b26a01` · verified — sections/cells.md

### per-building damage classification × SAR and multisensor
- Multi-Resolution Feature Fusion for Image Classification of Building Damages with Convolutional Neural Networks · 2018 · Remote Sensing · centrality 25 · influential 6 · 11.67 cites/yr · both indexes · S2 `21f0bbf41bd01b058183dd85a219a875a3fd9e57` · verified — sections/1-formulations.md
- Building-damage detection using post-seismic high-resolution SAR satellite data · 2010 · International Journal of Remote Sensing · centrality 2 · influential 5 · 7.65 cites/yr · both indexes · S2 `8a39e9e2c373bc2c2b8c9fbd80cf25b4624aed6a` · verified — sections/1-formulations.md
- Post-disaster damage classification based on deep multi-view image fusion · 2022 · Computer-Aided Civil and Infrastructure Engineering · centrality 1 · influential 3 · 14.4 cites/yr · both indexes · S2 `cecf8e95877546774bc297bda1e3db27e8440152` · verified — sections/1-formulations.md
- Earthquake building damage detection based on synthetic-aperture-radar imagery and machine learning · 2023 · Natural hazards and earth system sciences · centrality 1 · influential 3 · 16.5 cites/yr · both indexes · S2 `f2d267c446212b48d024b48d487cc9953928aa2f` · verified — sections/2-data-regimes.md
- Stepwise Building Damage Estimation Through Time-Scaled Multi-Sensor Integration: A Case Study of the 2024 Noto Peninsula Earthquake · 2025 · Remote Sensing · centrality 0 · influential 1 · 1.0 cites/yr · both indexes · S2 `c693831cf572d085b5f4338ea32dafcf86fd5fac` · verified — sections/2-data-regimes.md
- A review on synthetic aperture radar-based building damage assessment in disasters · 2020 · Remote Sensing of Environment · centrality 1 · influential 8 · 18.71 cites/yr · both indexes · S2 `47afbffb421193db8a8b509b61935a87ac385c71` · verified — sections/2-data-regimes.md
- Integrating post-event very high resolution SAR imagery and machine learning for building-level earthquake damage assessment · 2024 · Bulletin of Earthquake Engineering · centrality 2 · influential 2 · 16.0 cites/yr · both indexes · S2 `1474a6815e23e7e74fd99b1d23e487538545ac6e` · verified — sections/7-time-slice.md
- Evaluation of Simulated SAR Images for Building Damage Classification · 2025 · IEEE Geoscience and Remote Sensing Letters · S2 `db5831867a459a473e4e6a9e6e8caa84f05f09e7` · verified — sections/cells.md
- CFP-SwinT: building damage classification during floods using cross fusion pyramid Swin-T · 2025 · International Journal of Digital Earth · S2 `d7f6902bc4f4754fca70b06ecb43896e67c1a6bf` · verified — sections/cells.md
- High-precision building damage detection method based on optical-SAR heterogeneous data fusion and a UNet++-based framework · 2026 · International Conference on Computer Vision and Augmented Reality (CVAR 2026) · S2 `a118bf97f86ffb8147af9d3ce26eb2bc11decd98` · verified — sections/cells.md
- Report on the 2025 IEEE GRSS Data Fusion Contest: All-Weather Land Cover and Building Damage Mapping [Technical Committees] · 2025 · IEEE Geoscience and Remote Sensing Magazine · S2 `32d778ebab5557796b0c4f0859dee5e66a2e9ed0` · verified — sections/cells.md
- Integration of Local and Global Structural Information for Building Damage Assessment in Tsunami-Affected Areas Using SAR Intensity Imagery · 2025 · IEEE Asia-Pacific Conference on Synthetic Aperture Radar · S2 `ed8b51dfed27a33bcd83c674e7390ba622244fe5` · verified — sections/cells.md
- Building damage detection from multi-feature fusion of Sentinel-1/2 imagery using variational autoencoder and MLP-Mixer network: insights from the Jishishan earthquake · 2025 · Big Earth Data · S2 `6127ede80f33ec4835b0f97cb65071fe92cd5100` · verified — sections/cells.md
- A Deep Learning Framework for Rapid Building Damage Detection through Multimodal Data Fusion: Application to the 2025 Myanmar Earthquake · 2026 · ISPRS Annals of the Photogrammetry, Remote Sensing and Spatial Information Sciences · S2 `495eff0a91768b0d7285a8a2993dec613e7534ec` · verified — sections/cells.md
- Dual-Branch ConvNeXt with Attention-Based Fusion for Building Damage Detection · 2025 · 2025 International Conference on Intelligent and Cloud Computing (ICoICC) · S2 `5a10a9c99c8113f9c9761717d3ef6728cefcd142` · verified — sections/cells.md
- Multi-Source Data Fusion Based on Ensemble Learning for Rapid Building Damage Mapping during the 2018 Sulawesi Earthquake and Tsunami in Palu, Indonesia · 2019 · Remote Sensing · OpenAlex `W2937588654` · verified — sections/cells.md
- Detection of Earthquake-Induced Building Damages Using Polarimetric SAR Data · 2020 · Remote Sensing · OpenAlex `W2998403761` · verified — sections/cells.md

### per-building damage classification × weak or cross-event supervision
- On Transfer Learning for Building Damage Assessment from Satellite Imagery in Emergency Contexts · 2022 · Remote Sensing · centrality 1 · influential 3 · 10.0 cites/yr · both indexes · S2 `6652acdf80a6fbb7a76c73a15c6525026124e603` · verified — sections/1-formulations.md
- Geographic Bias Analysis and Cross-Domain Generalization in Deep Learning-Based Building Damage Assessment · 2026 · Remote Sensing · centrality 1 · influential 0 · 1.0 cites/yr · both indexes · S2 `76f4a5a19863f6f1d277a12868da70a9d44681eb` · verified — sections/2-data-regimes.md
- Assessing out-of-domain generalization for robust building damage detection · 2020 · _no venue_ · centrality 15 · influential _n/a_ · 2.14 cites/yr · openalex · OpenAlex `W3107461612` · verified — sections/4-reproduction.md
- Zero-Shot and Few-Shot Learning with Vision-Language Models for Post-disaster Structural Damage Assessment · 2025 · Hybrid Artificial Intelligence Systems · centrality 2 · influential 1 · 1.0 cites/yr · both indexes · S2 `1b417aef72a9937765709acdc6fbc661ca3f36a0` · verified — sections/7-time-slice.md
- Revolutionizing building damage detection: A novel weakly supervised approach using high-resolution remote sensing images · 2023 · International Journal of Digital Earth · OpenAlex `W4390409973` · verified — sections/cells.md

### semantic change detection × paired pre/post satellite (xBD, xView2)
- FCD-R2U-net: Forest change detection in bi-temporal satellite images using the recurrent residual-based U-net · 2022 · Earth Science Informatics · centrality 1 · influential 1 · 11.0 cites/yr · both indexes · S2 `a799d031ebd553bbd5bfb9a3d34e032964e7b3dd` · verified — sections/1-formulations.md
- Deep learning based building change detection by integrating building footprint data to pre and post-earthquake VHR satellite images from February 6, 2023, Kahramanmaraş earthquake: a case study for Hatay-Antakya · 2025 · International Journal of Remote Sensing · centrality 0 · influential 0 · 1.0 cites/yr · both indexes · S2 `35f9ec7eb41fb3f1b83fd9f4ce5cbb8d5f255c2f` · verified — sections/2-data-regimes.md
- S2Looking: A Satellite Side-Looking Dataset for Building Change Detection · 2021 · Remote Sensing · centrality 26 · influential 26 · 39.0 cites/yr · both indexes · S2 `76a936ae537d79a1078135f692c1728ab40ef663` · verified — sections/3-methods.md
- A deeply supervised image fusion network for change detection in high resolution bi-temporal remote sensing images · 2020 · ISPRS Journal of Photogrammetry and Remote Sensing · centrality 3 · influential 155 · 173.71 cites/yr · both indexes · S2 `f4e61d31666087d850a9f45f187254366d0a6419` · verified — sections/3-methods.md
- DASNet: Dual Attentive Fully Convolutional Siamese Networks for Change Detection in High-Resolution Satellite Images · 2020 · IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing · centrality 3 · influential 48 · 90.0 cites/yr · both indexes · S2 `13b5e856f3e22072bc916ff45248a3d68100ce88` · verified — sections/3-methods.md
- End-to-End Change Detection for High Resolution Satellite Images Using Improved UNet++ · 2019 · Remote Sensing · centrality 2 · influential 34 · 96.0 cites/yr · both indexes · S2 `5c1680927fdbe638976207bfbbfb006e5bcecfbc` · verified — sections/3-methods.md
- Bitemporal Attention Transformer for Building Change Detection and Building Damage Assessment · 2024 · IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing · centrality 25 · influential 1 · 12.33 cites/yr · both indexes · S2 `04c8c9e047b33a20b945140e09faa202b1df7319` · verified — sections/3-methods.md
- Inferring 3D change detection from bitemporal optical images · 2022 · Isprs Journal of Photogrammetry and Remote Sensing · centrality 1 · influential 6 · 8.6 cites/yr · both indexes · S2 `6536e0c2e3bbf00ad92f547d4bd38c9b5ef784a4` · verified — sections/3-methods.md
- SiamixFormer: a fully-transformer Siamese network with temporal Fusion for accurate building detection and change detection in bi-temporal remote sensing images · 2022 · International Journal of Remote Sensing · centrality 1 · influential 3 · 7.6 cites/yr · both indexes · S2 `bf6ad2eb0def2146375a25a6192e771cb1d59425` · verified — sections/3-methods.md
- A review of multi-class change detection for satellite remote sensing imagery · 2022 · Geo-spatial Information Science · centrality 0 · influential _n/a_ · 32.6 cites/yr · openalex · OpenAlex `W4306942281` · verified — sections/4-reproduction.md
- A Weakly Supervised Bitemporal Scene Change Detection Approach for Pixel-Level Building Damage Assessment Using Pre- and Post-Disaster High-Resolution Remote Sensing Images · 2024 · IEEE Transactions on Geoscience and Remote Sensing · S2 `916c479c7683755826194cd136c28801262ff33e` · verified — sections/cells.md
- Post Disaster Mapping With Semantic Change Detection in Satellite Imagery · 2019 · 2019 IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW) · S2 `3a9ae06cf6a3fb161a4e10304f323669118c61cb` · verified — sections/cells.md
- D2ANet: Difference-aware attention network for multi-level change detection from satellite imagery · 2023 · Computational Visual Media · S2 `b1b9dd8681d616ec561e979e5c987604e9acc500` · verified — sections/cells.md
- CNN-Based Semantic Change Detection in Satellite Imagery · 2019 · International Conference on Artificial Neural Networks · S2 `fb1cc62b95586aa1a5878923130aca227930f140` · verified — sections/cells.md

### semantic change detection × UAV and oblique aerial post-event
- Change Detection Based on Deep Siamese Convolutional Network for Optical Aerial Images · 2017 · IEEE Geoscience and Remote Sensing Letters · centrality 3 · influential 32 · 54.5 cites/yr · both indexes · S2 `b702cf22afb725b1bf9d633ffdd96cfb00a87253` · verified — sections/3-methods.md
- AGSPNet: A framework for parcel-scale crop fine-grained semantic change detection from UAV high-resolution imagery with agricultural geographic scene constraints · 2024 · Computers and Electronics in Agriculture · S2 `d2bc09f3b621d9a3fd3167bcf1fa10b132a24bbe` · verified — sections/cells.md
- UAV-SCD: A High-Resolution UAV Dataset for Semantic Change Detection with Fine-Grained Annotations · 2025 · 2025 6th International Conference on Geology, Mapping and Remote Sensing (ICGMRS) · S2 `47d3526016c47f4bbd2c5662ac4b85951980d4dd` · verified — sections/cells.md
- Exploring GPT-4o for Semantic Change Detection in Aerial Imagery: An Exploratory Comparison With Traditional and Deep Learning Approaches · 2026 · IEEE Access · S2 `b54012400feb10f601c166d66708cb3134cdd251` · verified — sections/cells.md
- Deep learning-based temporal change detection of broadleaved weed infestation in rice fields using UAV multispectral imagery · 2025 · Frontiers in Plant Science · S2 `2c48a7ab6889e986d6286470ee14ce9f4cf53985` · verified — sections/cells.md
- Change Detection and Land Cover Classification of Flooded Regions in UAVSAR Imagery Using Deep Learning · 2025 · 2025 IEEE International Conference on Data Mining Workshops (ICDMW) · S2 `45874c2a2ed67898ce20641ccfa3ebf459c09ab5` · verified — sections/cells.md

### semantic change detection × SAR and multisensor
- A deeply supervised image fusion network for change detection in high resolution bi-temporal remote sensing images · 2020 · ISPRS Journal of Photogrammetry and Remote Sensing · centrality 3 · influential 155 · 173.71 cites/yr · both indexes · S2 `f4e61d31666087d850a9f45f187254366d0a6419` · verified — sections/3-methods.md
- A CBAM Based Multiscale Transformer Fusion Approach for Remote Sensing Image Change Detection · 2022 · IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing · centrality 25 · influential 2 · 42.0 cites/yr · both indexes · S2 `eda551303411a40052363a7fb8b3d4477c4b879c` · verified — sections/3-methods.md
- SiamixFormer: a fully-transformer Siamese network with temporal Fusion for accurate building detection and change detection in bi-temporal remote sensing images · 2022 · International Journal of Remote Sensing · centrality 1 · influential 3 · 7.6 cites/yr · both indexes · S2 `bf6ad2eb0def2146375a25a6192e771cb1d59425` · verified — sections/3-methods.md
- Multi-Scale Fusion Siamese Network Based on Three-Branch Attention Mechanism for High-Resolution Remote Sensing Image Change Detection · 2024 · Remote Sensing · centrality 9 · influential 0 · 5.33 cites/yr · both indexes · S2 `cd999e82b7f39488f0a4c07d58013e82184c155f` · verified — sections/5-abandoned.md
- Adaptive Multisensor Fusion for Remote Sensing Change Detection Using USASE · 2025 · IEEE Sensors Journal · S2 `66f47121010c6ab2f188220139e8407219fe0f2a` · verified — sections/cells.md
- Assessing Buildings Damage from Multi-Temporal Sar Images Fusion using Semantic Change Detection · 2022 · IEEE International Geoscience and Remote Sensing Symposium · S2 `beb2e7c2336b098a16f152cce85433acc7171699` · verified — sections/cells.md
- Spatial–Temporal Semantic and Geographic Correlation Network for SAR Image Change Detection With Limited Training Data · 2025 · IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing · S2 `79a1c4b79454e7ead59d62e8dbc81779757e9efb` · verified — sections/cells.md
- Mamba-FCS: Joint Spatio-Frequency Feature Fusion, Change-Guided Attention, and SeK Inspired Loss for Enhanced Semantic Change Detection in Remote Sensing · 2025 · IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing · S2 `22173c2b104e95061eff2628fc59ec3857bb8a06` · verified — sections/cells.md
- Fusion of Bi-Temporal Zhuhai-1 Orbita Hyperspectral and Multiseason Sentinel-2 Remote Sensing Imagery for Semantic Change Detection Based on Dual-Path 3DCNN-LSTM · 2025 · IEEE Geoscience and Remote Sensing Letters · S2 `357ad937ac9cb6a626e390b3d0c28e4e875a7791` · verified — sections/cells.md
- Semantic Change Detection of Carbon Sources and Sinks via Spatiotemporal Attention and Multiscale Fusion · 2025 · IEEE Geoscience and Remote Sensing Letters · S2 `222267159ac3633c40480903c3572786815c91d8` · verified — sections/cells.md
- Feature Fusion and Difference Enhancement Optimization Network for Remote Sensing Image Semantic Change Detection · 2025 · 2025 IEEE 6th International Seminar on Artificial Intelligence, Networking and Information Technology (AINIT) · S2 `d3cfc5924582871f0bf18355836ac58479afb62a` · verified — sections/cells.md
- CoAFNet: a correlation modelling and Attention Fusion Network for semantic change detection · 2025 · International Journal of Remote Sensing · S2 `9a0cf9021a506f446ade08e6c8323c676e576d7e` · verified — sections/cells.md
- Statistic Ratio Attention-Guided Siamese U-Net for SAR Image Semantic Change Detection · 2024 · IEEE Geoscience and Remote Sensing Letters · S2 `aba063db04572f8fbca5836d21b3e19614627f25` · verified — sections/cells.md
- Change Detection in Heterogeneous Optical and SAR Remote Sensing Images Via Deep Homogeneous Feature Fusion · 2020 · IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing · OpenAlex `W3015287366` · verified — sections/cells.md
- Building Change Detection in VHR SAR Images via Unsupervised Deep Transcoding · 2020 · IEEE Transactions on Geoscience and Remote Sensing · OpenAlex `W3036616251` · verified — sections/cells.md

### semantic change detection × weak or cross-event supervision
- Domain-Adapted Remote Sensing for Urban Change Detection Using Weak Supervision from Maps · 2025 · Multidisciplinary Research in Computing Information Systems · S2 `bac56fd997b4d394c8787e974d5ed5c5c23ed47e` · verified — sections/cells.md

### building segmentation and localization × paired pre/post satellite (xBD, xView2)
- Fully Convolutional Networks for Multisource Building Extraction From an Open Aerial and Satellite Imagery Data Set · 2018 · IEEE Transactions on Geoscience and Remote Sensing · centrality 1 · influential 268 · 217.33 cites/yr · both indexes · S2 `53edb3776cea0e6ee4de742d7bb906355fd8279b` · verified — sections/2-data-regimes.md
- Deep learning based building change detection by integrating building footprint data to pre and post-earthquake VHR satellite images from February 6, 2023, Kahramanmaraş earthquake: a case study for Hatay-Antakya · 2025 · International Journal of Remote Sensing · centrality 0 · influential 0 · 1.0 cites/yr · both indexes · S2 `35f9ec7eb41fb3f1b83fd9f4ce5cbb8d5f255c2f` · verified — sections/2-data-regimes.md
- RescueNet: Joint Building Segmentation and Damage Assessment from Satellite Imagery · 2021 · International Conference on Pattern Recognition · centrality 23 · influential 10 · 3.83 cites/yr · both indexes · S2 `0c433390c7d5c10441ccc45af60f597446f18f64` · verified — sections/4-reproduction.md

### building segmentation and localization × UAV and oblique aerial post-event
- Fully Convolutional Networks for Multisource Building Extraction From an Open Aerial and Satellite Imagery Data Set · 2018 · IEEE Transactions on Geoscience and Remote Sensing · centrality 1 · influential 268 · 217.33 cites/yr · both indexes · S2 `53edb3776cea0e6ee4de742d7bb906355fd8279b` · verified — sections/2-data-regimes.md
- Aerial visual localization through novel applications of Weisfeiler-Lehman graph embeddings · 2025 · Defense + Security · S2 `c6d8c327c244723c9a98cdb7ce8b52f2bc6a7f3e` · verified — sections/cells.md
- Unsupervised Knowledge Extraction of Distinctive Landmarks from Earth Imagery Using Deep Feature Outliers for Robust UAV Geo-Localization · 2025 · Machine Learning and Knowledge Extraction · S2 `9ffaf0e0efa80208bd718e1d6c6be5e0c5d53b5f` · verified — sections/cells.md

### building segmentation and localization × SAR and multisensor
- SIMSL: A Semantic Instance-Based Multisensor Fusion Localization System for Challenging Dynamic and Degraded Environments · 2025 · IEEE transactions on industrial electronics (1982. Print) · S2 `9846ed40ebb62a63ad8827464828612faecd0747` · verified — sections/cells.md
- Building Extraction From High-Resolution Multispectral and SAR Images Using a Boundary-Link Multimodal Fusion Network · 2025 · IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing · S2 `b02ba7c50d407dbd32eb9e8489c9ca5985bf35d4` · verified — sections/cells.md
- Progressive fusion learning: A multimodal joint segmentation framework for building extraction from optical and SAR images · 2023 · Isprs Journal of Photogrammetry and Remote Sensing · S2 `d23b341da2ca10aa36dcd153c6625ad464fdcd09` · verified — sections/cells.md
- Multi-directional Local-Global feature Fusion Network for Building Segmentation in Remote Sensing Images · 2024 · 2024 International Conference on Image Processing, Computer Vision and Machine Learning (ICICML) · S2 `7382910656ecae77ed3623cc7e658a0d875f0e0f` · verified — sections/cells.md
- MMVP: Multiscene Indoor Localization for Smartphones by Using Collaborative Visual Localization and Multisensor Fusion · 2026 · IEEE Internet of Things Journal · S2 `24830fe931791603383afb5abfd2ac5ca8de98a6` · verified — sections/cells.md
- Exploiting Deep Matching and SAR Data for the Geo-Localization Accuracy Improvement of Optical Satellite Images · 2017 · Remote Sensing · OpenAlex `W2608922915` · verified — sections/cells.md
- CG-Net: Conditional GIS-aware Network for Individual Building Segmentation in VHR SAR Images · 2020 · _no venue_ · OpenAlex `W3127104941` · verified — sections/cells.md
- Fusion of Multiscale Convolutional Neural Networks for Building Extraction in Very High-Resolution Images · 2019 · Remote Sensing · OpenAlex `W2912114399` · verified — sections/cells.md

### building segmentation and localization × weak or cross-event supervision
- query `building segmentation localization weak supervision domain adaptation cross-event generalization` returned 13 rows, 0 naming both — sections/cells.md

### object-based change analysis × paired pre/post satellite (xBD, xView2)
- OBJECT-ORIENTED ANALYSIS OF SATELLITE IMAGES USING ARTIFICIAL NEURAL NETWORKS FOR POST-EARTHQUAKE BUILDINGS CHANGE DETECTION · 2017 · _no venue_ · S2 `055e328d273f51d482765e032ef9ef7c714dbf11` · verified — sections/cells.md

### object-based change analysis × UAV and oblique aerial post-event
- UAV-based urban structural damage assessment using object-based image analysis and semantic reasoning · 2015 · Natural hazards and earth system sciences · centrality 2 · influential 5 · 19.75 cites/yr · both indexes · S2 `3cf417fc3bdd5ec057ef0d05be40aebd8b648605` · verified — sections/1-formulations.md
- Using object‐based image analysis with multi‐temporal aerial imagery and LiDAR to detect change in temperate intertidal habitats · 2020 · _no venue_ · S2 `2110f66d074119fba340691d7af10231770ee970` · verified — sections/cells.md
- Integrating a UAV-Derived DEM in Object-Based Image Analysis Increases Habitat Classification Accuracy on Coral Reefs · 2022 · Remote Sensing · S2 `50e80d4f3038e53632276c923d8cc7b04dab9087` · verified — sections/cells.md
- UAV-SfM and Geographic Object-Based Image Analysis for Measuring Multi-Temporal Planimetric and Volumetric Erosion of Arctic Coasts · 2023 · Canadian journal of remote sensing · S2 `93c8164e4f2cb0c96ea7427769ffec1abddf660f` · verified — sections/cells.md
- Deep learning versus Object-based Image Analysis (OBIA) in weed mapping of UAV imagery · 2020 · International Journal of Remote Sensing · S2 `f701bd2b83d4070c9dfeb76b7773692a47ad611a` · verified — sections/cells.md
- Multi-Temporal UAV Data and Object-Based Image Analysis (OBIA) for Estimation of Substrate Changes in a Post-Bleaching Scenario on a Maldivian Reef · 2020 · Remote Sensing · S2 `0633931bbaf5b7ab31797fff186da7881a5dfdd3` · verified — sections/cells.md
- Object-based analysis of unmanned aerial vehicle imagery to map and characterise surface features on a debris-covered glacier · 2016 · _no venue_ · S2 `5abb6bfb6267ea782d7737f47490907de066d23e` · verified — sections/cells.md

### object-based change analysis × SAR and multisensor
- Towards Monitoring of Mountain Mass Wasting Using Object-Based Image Analysis Using SAR Intensity Images · 2021 · 2021 IEEE International Geoscience and Remote Sensing Symposium IGARSS · S2 `6ba7132a1574a18d5937024d3b5e2769a14fa9ce` · verified — sections/cells.md
- Semantic Unsupervised Change Detection of Natural Land Cover With Multitemporal Object-Based Analysis on SAR Images · 2021 · IEEE Transactions on Geoscience and Remote Sensing · S2 `612a87718933d73c1bf9dc95e2d1b399a2e09ffe` · verified — sections/cells.md
- Object-Based Analysis and Fusion of Optical and SAR Satellite Data for Dwelling Detection in Refugee Camps · 2017 · IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing · S2 `d59df05fabb4dee8cb0bd4296bc43bc07881ee83` · verified — sections/cells.md
- Object-based multiscale method for SAR image change detection · 2018 · _no venue_ · S2 `91dacd1bd868cccdca77b4ff44b2d1622ae18736` · verified — sections/cells.md

### object-based change analysis × weak or cross-event supervision
- Hybrid Object-Based Augmentation and Histogram Matching for Cross-Domain Building Segmentation in Remote Sensing · 2026 · Applied Sciences · S2 `54e8d215b59c3a791196f7631674a042033fcf10` · verified — sections/cells.md

## Contradictions

- UAV-Based Structural Damage Mapping: A Review — id S2 4546399ebcef2da1294b07c1ce05ca7f23e6ed99 in sections/1-formulations.md, OpenAlex W2998460252 in sections/6-adjacent.md
- Transformers in Remote Sensing: A Survey — year 2022 in sections/1-formulations.md, 2023 in sections/3-methods.md, 2022 in sections/5-abandoned.md, 2023 in sections/5-abandoned.md
- Transformers in Remote Sensing: A Survey — id S2 744ee04b08e04ad216bd586ac74bbc1fed0dea8f in sections/1-formulations.md, OpenAlex W4362519158 in sections/3-methods.md, S2 744ee04b08e04ad216bd586ac74bbc1fed0dea8f in sections/5-abandoned.md, OpenAlex W4362519158 in sections/5-abandoned.md
- Advances in Rapid Damage Identification Methods for Post-Disaster Regional Buildings Based on Remote Sensing Images: A Survey — id S2 4fd4b271a6e24c189b23602a5dcde8fffe907569 in sections/1-formulations.md, S2 4fd4b271a6e24c189b23602a5dcde8fffe907569 in sections/2-data-regimes.md, OpenAlex W4393187295 in sections/4-reproduction.md, S2 4fd4b271a6e24c189b23602a5dcde8fffe907569 in sections/5-abandoned.md
- RS-Mamba for Large Remote Sensing Image Dense Prediction — id S2 2833716cabbd7c709f4b266832b8b3fa3e37d2c6 in sections/3-methods.md, OpenAlex W4400448280 in sections/5-abandoned.md
- xBD: A Dataset for Assessing Building Damage from Satellite Imagery — id OpenAlex W2991131216 in sections/4-reproduction.md, S2 8fbf011af21921a553bd8b20cd6eb16897f07801 in sections/4-reproduction.md
- Deep artificial intelligence applications for natural disaster management systems: A methodological review — id OpenAlex W4396667610 in sections/4-reproduction.md, S2 c61f178d9eb386cb7deeeeb3f544b1deb1de502f in sections/7-time-slice.md
- Remote Sensing Object Detection in the Deep Learning Era—A Review — id S2 ad55e35d8d2b2250fab4099b0d622aa42ddcde04 in sections/5-abandoned.md, OpenAlex W4390826350 in sections/7-time-slice.md
- Deep Learning Methods for Flood Mapping: A Review of Existing Applications and Future Research Directions — year 2021 in sections/6-adjacent.md, 2022 in sections/6-adjacent.md
- Deep Learning Methods for Flood Mapping: A Review of Existing Applications and Future Research Directions — id S2 af3b8920be370b3fadb6d06b72d23f6c19b544eb in sections/6-adjacent.md, OpenAlex W4293226370 in sections/6-adjacent.md

## Sources

- sections/1-formulations.md — 60 papers
- sections/2-data-regimes.md — 57 papers
- sections/3-methods.md — 60 papers
- sections/4-reproduction.md — 60 papers
- sections/5-abandoned.md — 60 papers
- sections/6-adjacent.md — 60 papers
- sections/7-time-slice.md — 60 papers
- sections/surveys.md — 20 papers
- sections/cells.md — 302 rows over 16 probes

## Status

2026-09-16. Cells 15 filled / 1 empty / 16 total. Contradictions 10. Sections reporting a degraded index: none.
