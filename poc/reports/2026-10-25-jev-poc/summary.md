# Jev POC results (jev-1.14.0, threshold 0.5, 211 calls, 515,100 input tokens, $0.02163)

## Ledger C: 40 theses, 20 matter-tracking
### Jev decisions, group cards = clean (37/38 three-state agreement with the gold, target not checked)
| gold \ decided | dedup | grouped | new |
|---|---|---|---|
| dedup | 2 | 1 | 0 |
| grouped | 0 | 15 | 0 |
| new | 0 | 0 | 20 |

### Control: the pipeline as stored (20/38)
| gold \ decided | dedup | grouped | new |
|---|---|---|---|
| dedup | 0 | 0 | 3 |
| grouped | 0 | 0 | 15 |
| new | 0 | 0 | 20 |

### Judged, cards = clean: Jev **37/38** right on judged cases (founder 0, own matter 0, disputed 0, unlabelled 0 set aside); control **20/38** on its judged cases (disputed 0, own matter 0 set aside)

- wrong      v21 Nvidia讨论为园区提供的芯片融资金额: gold dedup → Jev grouped (openai_nvidia_financing, 0.98) (duplicate of v18)

Dangling matter-tracking theses (state new): control 20, Jev 0, gold 0.

### Relevance diagnostic (noul, matter-tracking theses, lowest first; D154: measured, not applied)
- 0.82 v19 日本为天然气发电厂承诺的投资金额
- 0.90 v13 SK Telecom AI factory deployment
- 0.91 v7 Vera Rubin量产出货事件
- 0.93 v15 Blackwell和Rubin芯片2025年至2027年自然年的合计收入，美元
- 0.94 v11 NVDA FY2027独立CPU全年收入，美元
- 0.95 v14 美国政府是否在2027-01-31或之前正式宣布对中国AI模型实施新的限制
- 0.95 v17 NVIDIA为OpenAI数据中心租赁及债务融资提供的担保金额
- 0.95 v20 俄亥俄州数据中心项目含芯片总成本
- 0.95 v21 Nvidia讨论为园区提供的芯片融资金额
- 0.95 v23 台湾是否对对华AI芯片销售实施限制
- 0.95 v24 NVIDIA向OpenAI提供的融资金额
- 0.95 v36 Nvidia相关AI基础设施融资安排的金额，美元

## Ledger E: 61 theses, 29 matter-tracking
### Jev decisions, group cards = clean (54/58 three-state agreement with the gold, target not checked)
| gold \ decided | dedup | grouped | new |
|---|---|---|---|
| dedup | 0 | 0 | 0 |
| grouped | 0 | 13 | 4 |
| new | 0 | 0 | 41 |

### Control: the pipeline as stored (41/58)
| gold \ decided | dedup | grouped | new |
|---|---|---|---|
| dedup | 0 | 0 | 0 |
| grouped | 0 | 0 | 17 |
| new | 0 | 0 | 41 |

### Judged, cards = clean: Jev **49/54** right on judged cases (founder 0, own matter 4, disputed 0, unlabelled 0 set aside); control **37/54** on its judged cases (disputed 0, own matter 4 set aside)

- wrong      v16 NAVER GAK Sejong NVIDIA DSX AI factory expansion: gold grouped → Jev grouped (hyperscaler_capex_cycle, 0.54) (required in ['rubin_rollout'])
- wrong      v28 META FY2026 capital expenditures: gold grouped → Jev new (None, None) (required in ['hyperscaler_capex_cycle'])
- wrong      v34 Calendar-year 2026 capital expenditures: gold grouped → Jev new (None, None) (required in ['hyperscaler_capex_cycle'])
- wrong      v44 Amazon cash capital expenditures: gold grouped → Jev new (None, None) (required in ['hyperscaler_capex_cycle'])
- own_matter v46 Amazon Leo initial satellite internet service: gold new → Jev new (None, None) 
- own_matter v48 Amazon acquisition of Globalstar: gold new → Jev new (None, None) 
- own_matter v56 Initial Helios shipments: gold new → Jev new (None, None) 
- own_matter v57 Anthropic first-gigawatt MI450 deployment: gold new → Jev new (None, None) 
- wrong      v61 Zankore by Indosat initial AI capacity deployment: gold grouped → Jev new (None, None) (required in ['rubin_rollout'])

Dangling matter-tracking theses (state new): control 29, Jev 15, gold 12.

### Relevance diagnostic (noul, matter-tracking theses, lowest first; D154: measured, not applied)
- 0.59 v17 allocation of the remaining FY2027 raw cane sugar tariff-rate quota qu
- 0.74 v61 Zankore by Indosat initial AI capacity deployment
- 0.83 v22 RTX Spark shipment
- 0.83 v46 Amazon Leo initial satellite internet service
- 0.85 v15 SK Telecom AI factory deployment
- 0.85 v48 Amazon acquisition of Globalstar
- 0.87 v39 U.S. revenue-share rate on licensed Nvidia GPU sales to China
- 0.89 v6 Vera Rubin production shipments
- 0.90 v16 NAVER GAK Sejong NVIDIA DSX AI factory expansion
- 0.91 v18 NVIDIA–SK Group AI initiative business value
- 0.91 v56 Initial Helios shipments
- 0.92 v55 2026 new design wins

## Ledger G: 45 theses, 18 matter-tracking
### Jev decisions, group cards = clean (40/44 three-state agreement with the gold, target not checked)
| gold \ decided | dedup | grouped | new |
|---|---|---|---|
| dedup | 0 | 0 | 0 |
| grouped | 0 | 9 | 4 |
| new | 0 | 0 | 31 |

### Control: the pipeline as stored (40/44)
| gold \ decided | dedup | grouped | new |
|---|---|---|---|
| dedup | 0 | 0 | 0 |
| grouped | 0 | 11 | 2 |
| new | 0 | 2 | 29 |

### Judged, cards = clean: Jev **36/41** right on judged cases (founder 0, own matter 3, disputed 0, unlabelled 0 set aside); control **39/41** on its judged cases (disputed 0, own matter 3 set aside)

- own_matter v15 NVIDIA 2026 public debt offering: gold new → Jev new (None, None) 
- own_matter v17 Completion of remaining actions under the 2025 Restructuri: gold new → Jev new (None, None) 
- wrong      v19 NAVER GAK Sejong AI factory expansion: gold grouped → Jev grouped (hyperscaler_capex_cycle, 0.73) (required in ['rubin_rollout'])
- wrong      v24 FY2026 capital expenditures: gold grouped → Jev new (None, None) (required in ['hyperscaler_capex_cycle'])
- wrong      v30 Microsoft calendar 2026 capital expenditures: gold grouped → Jev new (None, None) (required in ['hyperscaler_capex_cycle'])
- wrong      v39 Amazon FY2026 cash CapEx: gold grouped → Jev new (None, None) (required in ['hyperscaler_capex_cycle'])
- wrong      v42 Alphabet calendar-year 2026 capital expenditures: gold grouped → Jev new (None, None) (required in ['hyperscaler_capex_cycle'])
- own_matter v45 Amazon's acquisition of Globalstar: gold new → Jev new (None, None) 

### Jev decisions, group cards = stored (35/44 three-state agreement with the gold, target not checked)
| gold \ decided | dedup | grouped | new |
|---|---|---|---|
| dedup | 0 | 0 | 0 |
| grouped | 0 | 4 | 9 |
| new | 0 | 0 | 31 |

### Control: the pipeline as stored (40/44)
| gold \ decided | dedup | grouped | new |
|---|---|---|---|
| dedup | 0 | 0 | 0 |
| grouped | 0 | 11 | 2 |
| new | 0 | 2 | 29 |

### Judged, cards = stored: Jev **32/36** right on judged cases (founder 5, own matter 3, disputed 0, unlabelled 0 set aside); control **39/41** on its judged cases (disputed 0, own matter 3 set aside)

- founder    v1 2026 capex by the top five cloud providers and hyperscaler: gold grouped → Jev new (None, None) (founded its group in the same input; nothing to judge against)
- founder    v4 Blackwell and Rubin revenue opportunity: gold grouped → Jev new (None, None) (founded its group in the same input; nothing to judge against)
- founder    v5 Vera Rubin production shipments: gold grouped → Jev new (None, None) (founded its group in the same input; nothing to judge against)
- founder    v9 H200 China import authorization: gold grouped → Jev new (None, None) (founded its group in the same input; nothing to judge against)
- own_matter v15 NVIDIA 2026 public debt offering: gold new → Jev new (None, None) 
- own_matter v17 Completion of remaining actions under the 2025 Restructuri: gold new → Jev new (None, None) 
- wrong      v24 FY2026 capital expenditures: gold grouped → Jev new (None, None) (required in ['hyperscaler_capex_cycle'])
- wrong      v30 Microsoft calendar 2026 capital expenditures: gold grouped → Jev new (None, None) (required in ['hyperscaler_capex_cycle'])
- founder    v35 A potential Taiwanese criminal ban on AI chip exports to C: gold grouped → Jev new (None, None) (founded its group in the same input; nothing to judge against)
- wrong      v39 Amazon FY2026 cash CapEx: gold grouped → Jev new (None, None) (required in ['hyperscaler_capex_cycle'])
- wrong      v42 Alphabet calendar-year 2026 capital expenditures: gold grouped → Jev new (None, None) (required in ['hyperscaler_capex_cycle'])
- own_matter v45 Amazon's acquisition of Globalstar: gold new → Jev new (None, None) 

### Repeatability: 89/90 three-state decisions identical across two fresh replicates

Dangling matter-tracking theses (state new): control 6, Jev 13, gold 7.

### Relevance diagnostic (noul, matter-tracking theses, lowest first; D154: measured, not applied)
- 0.59 v21 NVIDIA NemoClaw for LangChain Deep Agents enterprise adoption and cust
- 0.67 v17 Completion of remaining actions under the 2025 Restructuring Plan
- 0.72 v15 NVIDIA 2026 public debt offering
- 0.82 v22 RTX Spark systems shipping
- 0.84 v45 Amazon's acquisition of Globalstar
- 0.89 v18 SK Telecom AI factory deployment
- 0.89 v19 NAVER GAK Sejong AI factory expansion
- 0.90 v5 Vera Rubin production shipments
- 0.93 v13 FY2027 standalone Vera CPU revenue
- 0.93 v35 A potential Taiwanese criminal ban on AI chip exports to China
- 0.94 v31 Xbox FY2027 revenue growth
- 0.95 v9 H200 China import authorization

## F1 diagnostic: the fused g1 members against the clean Rubin and capex cards (p)
| thesis | rubin_rollout | hyperscaler_capex_cycle |
|---|---:|---:|
| v1 | 0.03 | 0.98 |
| v4 | 0.76 | 0.24 |
| v5 | 0.98 | 0.11 |
| v12 | 0.2 | 0.97 |
| v18 | 0.96 | 0.58 |
| v19 | 0.03 | 0.73 |
| v20 | 0.02 | 0.97 |
| v39 | — | — |
| v42 | — | — |

## Identity on the gold pairs (five-way)
| gold \ Jev | same_quantity_or_event | part_of | same_matter_different_quantity | different | cannot_tell |
|---|---|---|---|---|---|
| same | 3 | 2 | 0 | 0 | 0 |
| part_of | 0 | 2 | 0 | 0 | 0 |
| related_not_same | 0 | 4 | 7 | 1 | 0 |
| different | 0 | 0 | 0 | 0 | 0 |

Exact label 12/19; binary same/not-same 17/19.

- S v16/v48: gold same → Jev part_of {'same_quantity_or_event': 0.07, 'part_of': 0.69, 'same_matter_different_quantity': 0.15, 'different': 0.03, 'cannot_tell': 0.06}
- C v17/v24: gold same → Jev part_of {'same_quantity_or_event': 0.29, 'part_of': 0.5, 'same_matter_different_quantity': 0.15, 'different': 0.01, 'cannot_tell': 0.05}
- G v1/v20: gold related_not_same → Jev part_of {'same_quantity_or_event': 0.04, 'part_of': 0.74, 'same_matter_different_quantity': 0.08, 'different': 0.04, 'cannot_tell': 0.1}
- E v11/v19: gold related_not_same → Jev part_of {'same_quantity_or_event': 0.14, 'part_of': 0.46, 'same_matter_different_quantity': 0.24, 'different': 0.03, 'cannot_tell': 0.13}
- E v19/v20: gold related_not_same → Jev part_of {'same_quantity_or_event': 0.0, 'part_of': 0.44, 'same_matter_different_quantity': 0.3, 'different': 0.22, 'cannot_tell': 0.04}
- S v86/v89: gold related_not_same → Jev part_of {'same_quantity_or_event': 0.0, 'part_of': 0.38, 'same_matter_different_quantity': 0.34, 'different': 0.27, 'cannot_tell': 0.01}
- C v19/v17: gold related_not_same → Jev different {'same_quantity_or_event': 0.01, 'part_of': 0.01, 'same_matter_different_quantity': 0.26, 'different': 0.71, 'cannot_tell': 0.01}
