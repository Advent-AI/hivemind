# Fresh versus update: all stored outputs

Diagnostic observations only; not an accuracy score.

## sample-1 / capex-fresh-379-result

```json
{
  "status": "rejected",
  "error": "ValueError: Unknown, stale, future or duplicate view/evidence pair"
}
```

## sample-1 / capex-fresh-552-result

```json
{
  "status": "rejected",
  "error": "ValueError: Unknown, stale, future or duplicate view/evidence pair"
}
```

## sample-1 / capex-fresh-584-result

```json
{
  "status": "rejected",
  "error": "ValueError: Unknown, stale, future or duplicate view/evidence pair"
}
```

## sample-1 / rubin-fresh-379-result

```json
{
  "status": "valid",
  "value": {
    "status": "supported",
    "conclusion": "Current research supports a qualified commercialization picture for Vera Rubin: NVIDIA has repeatedly guided to production shipments beginning in the second half of 2026, and customer and infrastructure deployment plans point to prospective demand. It does not establish that Rubin shipments or customer deployments have already occurred, or that forecast revenue has been realized. The strongest revenue evidence is guidance, not reported sales.",
    "arguments": [
      {
        "statement": "NVIDIA’s expected start of Vera Rubin production shipments is supported by repeated company guidance, but not confirmed as an already completed shipment event.",
        "role": "supports",
        "reason": "Management said shipments were on track to begin in the second half of 2026, starting in Q3. That is a forecast. A statement that Vera is already in production and third-party reporting that volume production has started add readiness or production claims, but do not establish that customer shipments have begun. The platform announcement and preparations at a manufacturing facility likewise are not shipment confirmation.",
        "references": [
          {
            "view_id": "v7",
            "evidence_ids": [
              "e7",
              "e19",
              "e43",
              "e128",
              "e199",
              "e511"
            ],
            "judgement_id": 350
          }
        ]
      },
      {
        "statement": "Customer and infrastructure announcements support planned deployments and commercial interest, not deployments already operating.",
        "role": "supports",
        "reason": "SK Telecom’s plan for its first Vera Rubin-powered AI factory to come online in 2027 provides a concrete prospective deployment signal. Separately, reporting that cloud providers have signed up to deploy Vera CPUs and SpaceX’s announced satellite payload partnership indicate customer commitments or plans. These are not evidence that the systems are already installed and operating; the factory announcement itself is a plan, not an operational result.",
        "references": [
          {
            "view_id": "v15",
            "evidence_ids": [
              "e55",
              "e54"
            ],
            "judgement_id": 355
          },
          {
            "view_id": "v16",
            "evidence_ids": [
              "e449"
            ],
            "judgement_id": 351
          },
          {
            "view_id": "v48",
            "evidence_ids": [
              "e523"
            ],
            "judgement_id": 357
          }
        ]
      },
      {
        "statement": "Revenue realization remains prospective: research gives a company forecast for Vera sales, but does not establish actual Vera revenue at that level.",
        "role": "context",
        "reason": "NVIDIA is reported to be guiding to around $20 billion in Vera sales for the fiscal year. That is the clearest Vera-product revenue anchor, but it is guidance rather than a reported result. A separate estimate of nearly $20 billion in total CPU revenue was clarified as standalone CPU revenue; it is not interchangeable with the Vera-product sales forecast and does not establish either amount as realized revenue.",
        "references": [
          {
            "view_id": "v48",
            "evidence_ids": [
              "e471"
            ],
            "judgement_id": 357
          },
          {
            "view_id": "v16",
            "evidence_ids": [
              "e75",
              "e76"
            ],
            "judgement_id": 351
          }
        ]
      }
    ],
    "limitations": [
      "The research does not provide a direct occurrence confirming that Vera Rubin production shipments to customers have begun.",
      "The cited deployment evidence concerns plans, sign-ups, or a partnership announcement; it does not confirm operational customer deployments.",
      "The revenue evidence is forecast or guidance, not reported realized Vera sales. The standalone CPU revenue expectation is a different measure from Vera-product sales.",
      "The evidence supports commercialization prospects but does not establish eventual shipment volumes, deployment timing, or realized revenue."
    ],
    "watch_questions": [
      "Has NVIDIA or a customer directly confirmed completed Vera Rubin production shipments?",
      "Have announced customer deployments, including the planned SK Telecom AI factory, become operational?",
      "What reported revenue will distinguish actual Vera sales from company guidance and from standalone CPU revenue?"
    ],
    "unused_ids": [
      "v14",
      "v60"
    ],
    "scope_id": "rubin",
    "as_of_seq": 379,
    "as_of": "2026-08-05",
    "input_fingerprint": "c2ba922490913aedae5b845af2bcac78214ec3b7fd9a03a6006c586822e04a6d"
  }
}
```

## sample-1 / rubin-fresh-532-result

```json
{
  "status": "valid",
  "value": {
    "status": "supported",
    "conclusion": "Current research supports a qualified picture of Vera Rubin commercialization: customer samples have been delivered and system validation and manufacturing preparation have occurred; production shipments and customer deployments are supported mainly by company timing or deployment plans, not confirmed completed events; and revenue is guided or forecast, not shown as realized. Thus commercialization is advancing, but the research does not establish broad production shipments, live customer deployments, or recognized Vera revenue.",
    "arguments": [
      {
        "statement": "NVIDIA has delivered Vera Rubin samples to customers, and CoreWeave completed bring-up and validation of an NVL72 system; these are actual commercialization milestones.",
        "role": "supports",
        "reason": "The sample delivery and validation show customer-facing progress, but neither establishes that production shipments to customers have begun.",
        "references": [
          {
            "view_id": "v7",
            "evidence_ids": [
              "e7",
              "e748"
            ],
            "judgement_id": 425
          }
        ]
      },
      {
        "statement": "Production shipments are expected to start in the second half of 2026, with management specifying a Q3 start; the research does not confirm that this event has occurred.",
        "role": "supports",
        "reason": "These are direct timing expectations, not shipment results. Factory preparation and reported production status increase readiness evidence but should not be treated as proof of customer shipments.",
        "references": [
          {
            "view_id": "v7",
            "evidence_ids": [
              "e19",
              "e128",
              "e511"
            ],
            "judgement_id": 425
          }
        ]
      },
      {
        "statement": "Customer deployment evidence includes plans for a SK Telecom AI factory using Vera Rubin, planned to come online in 2027; this supports intended adoption, not an operating deployment.",
        "role": "supports",
        "reason": "The stated configuration and target date connect Vera Rubin to a prospective customer infrastructure project, while the evidence does not show that the factory is already online or that the overall partnership has been fully formalized.",
        "references": [
          {
            "view_id": "v15",
            "evidence_ids": [
              "e55",
              "e54"
            ],
            "judgement_id": 431
          }
        ]
      },
      {
        "statement": "Revenue expectations indicate potential commercial scale, but there is no cited actual Vera revenue result.",
        "role": "context",
        "reason": "NVIDIA’s near-$20 billion FY2027 standalone CPU revenue visibility is a forecast and specifically concerns CPU revenue. Separately, the roughly $20 billion FY2027 Vera sales guidance is also a forecast; these amounts address different revenue scopes and cannot be treated as interchangeable or as realized revenue.",
        "references": [
          {
            "view_id": "v16",
            "evidence_ids": [
              "e75",
              "e76"
            ],
            "judgement_id": 429
          },
          {
            "view_id": "v48",
            "evidence_ids": [
              "e471"
            ],
            "judgement_id": 357
          }
        ]
      }
    ],
    "limitations": [
      "The record does not confirm that production shipments have started or quantify shipped units; management’s schedule and third-party reports remain distinct from verified shipment results.",
      "Deployment evidence is principally validation, manufacturing readiness, and future plans. It does not establish that planned customer facilities are operational or disclose resulting customer revenue.",
      "No actual Vera revenue is reported in the cited research. The FY2027 CPU and Vera sales figures are forecasts, not realized results, and refer to different scopes.",
      "Supply-chain delay risk remains a contrary consideration for the shipment timetable."
    ],
    "watch_questions": [
      "Has NVIDIA confirmed the start and scale of Vera Rubin production shipments to customers?",
      "Do planned customer projects, including the SK Telecom AI factory, reach operation with Vera Rubin systems?",
      "When will NVIDIA disclose recognized Vera revenue, and will it distinguish standalone CPU revenue from broader Vera product sales?",
      "Do supply-chain constraints affect the stated shipment timetable?"
    ],
    "unused_ids": [
      "v14",
      "v60"
    ],
    "scope_id": "rubin",
    "as_of_seq": 532,
    "as_of": "2026-08-12",
    "input_fingerprint": "12bcd167cda7b812a97346b05491681a40d915ab68cc94094c848ee6f33448ac"
  }
}
```

## sample-1 / rubin-fresh-66-result

```json
{
  "status": "valid",
  "value": {
    "status": "supported",
    "conclusion": "Current research supports a distinction between commercialization plans and realized commercialization: NVIDIA expects Vera Rubin production shipments to begin in the second half of 2026, and customer announcements describe future deployments, but the evidence does not establish that production shipments or customer deployments have already occurred. NVIDIA has also forecast nearly $20 billion in standalone CPU revenue for “this year,” but current research does not show that revenue has been realized or establish that “this year” means FY2027.",
    "arguments": [
      {
        "statement": "NVIDIA has stated that Vera Rubin production shipments are on track to begin in the second half of 2026, with one statement specifying a Q3 start and another describing a Q4 ramp.",
        "role": "supports",
        "reason": "These are company forecasts relevant to the expected start of commercialization, not evidence that production shipments have already begun. The platform announcement is an actual event, but it does not itself establish production shipments.",
        "references": [
          {
            "view_id": "v7",
            "evidence_ids": [
              "e7",
              "e19",
              "e43",
              "e82"
            ],
            "judgement_id": 71
          }
        ]
      },
      {
        "statement": "Customer-facing announcements identify planned Vera Rubin deployments, including a first SK Telecom AI factory planned to come online in 2027 and a planned expansion of NAVER’s GAK Sejong AI factory.",
        "role": "supports",
        "reason": "These plans are evidence of intended customer use and potential deployment pathways, but they do not establish that customers have received, installed, or deployed Vera Rubin systems. The SK Group-wide announcement also remained a plan formalized through letters of intent; a separate SK hynix memory partnership does not establish that AI factory construction is formally implemented.",
        "references": [
          {
            "view_id": "v15",
            "evidence_ids": [
              "e55"
            ],
            "judgement_id": 56
          },
          {
            "view_id": "v14",
            "evidence_ids": [
              "e54",
              "e56",
              "e57"
            ],
            "judgement_id": 50
          }
        ]
      },
      {
        "statement": "NVIDIA’s CFO forecast nearly $20 billion in total CPU revenue for “this year,” and the CEO clarified that the figure refers to standalone CPU rather than CPU already embedded in Vera Rubin systems.",
        "role": "supports",
        "reason": "This is relevant evidence of management’s revenue expectation for the standalone CPU opportunity, not reported revenue already earned. The research does not establish the mapping of “this year” to FY2027, so the forecast should not be treated as a confirmed FY2027 result.",
        "references": [
          {
            "view_id": "v16",
            "evidence_ids": [
              "e75",
              "e76"
            ],
            "judgement_id": 72
          }
        ]
      },
      {
        "statement": "The Vera CPU architecture and benchmarks have been published, while an outside commentator raised a concern that the nearly $20 billion forecast may be difficult to verify separately without future disclosure.",
        "role": "context",
        "reason": "The publication is an actual product-related milestone, but it does not demonstrate customer deployment or revenue realization. The disclosure concern is a limitation on verification, not evidence that the forecast is false.",
        "references": [
          {
            "view_id": "v16",
            "evidence_ids": [
              "e78",
              "e79"
            ],
            "judgement_id": 72
          }
        ]
      }
    ],
    "limitations": [
      "The cited shipment timing, customer deployments, and revenue figure are forecasts or plans; the supplied research does not document completed Vera Rubin production shipments, completed customer deployments, or realized CPU revenue.",
      "The “this year” CPU revenue forecast is not explicitly tied in the supplied evidence to FY2027.",
      "Announcements of planned facilities and partnerships indicate intended commercialization but do not establish that the related projects or deployments have been completed."
    ],
    "watch_questions": [
      "Has NVIDIA confirmed that Vera Rubin production shipments actually began, and when?",
      "Have the announced customer facilities received and deployed Vera Rubin systems?",
      "What standalone CPU revenue has NVIDIA reported, and what fiscal period does the nearly $20 billion forecast cover?"
    ],
    "unused_ids": [],
    "scope_id": "rubin",
    "as_of_seq": 66,
    "as_of": "2026-07-24",
    "input_fingerprint": "3889a291d69246d0e46c5b90607ce815c06f46d59b827670a104785a66be5f95"
  }
}
```

## sample-1 / rubin-fresh-probe-result

```json
{
  "status": "valid",
  "value": {
    "facets": [
      {
        "facet": "shipments",
        "answer": "Customer samples have been delivered, but the research does not confirm that production shipments to customers have begun or quantify shipped units. The expected second-half 2026 start, with management specifying Q3, is a timeline rather than a completed shipment result; manufacturing preparation and reported production status indicate readiness, not confirmed customer shipments.",
        "references": [
          {
            "view_id": "v7",
            "evidence_ids": [
              "e7",
              "e748",
              "e19",
              "e128",
              "e511"
            ]
          }
        ]
      },
      {
        "facet": "deployments",
        "answer": "Customer-facing validation has occurred: CoreWeave completed bring-up and validation of an NVL72 system. The SK Telecom AI factory using Vera Rubin is a future plan targeted for 2027, not evidence of an operating customer deployment. The research therefore does not establish broad live deployments.",
        "references": [
          {
            "view_id": "v7",
            "evidence_ids": [
              "e748"
            ]
          },
          {
            "view_id": "v15",
            "evidence_ids": [
              "e55",
              "e54"
            ]
          }
        ]
      },
      {
        "facet": "revenue",
        "answer": "No actual Vera revenue is reported. The roughly $20 billion FY2027 Vera sales guidance and near-$20 billion FY2027 standalone CPU revenue visibility are forecasts, not realized revenue, and refer to different scopes.",
        "references": [
          {
            "view_id": "v16",
            "evidence_ids": [
              "e75",
              "e76"
            ]
          },
          {
            "view_id": "v48",
            "evidence_ids": [
              "e471"
            ]
          }
        ]
      }
    ]
  }
}
```

## sample-1 / rubin-update-379-result

```json
{
  "status": "rejected",
  "error": "ValueError: Unknown, stale, future or duplicate view/evidence pair"
}
```

## sample-2 / capex-fresh-379-result

```json
{
  "status": "valid",
  "value": {
    "status": "supported",
    "conclusion": "Cloud infrastructure investment supports a strong NVIDIA revenue outlook directionally: hyperscalers’ stated spending plans and current estimates imply substantial demand for AI infrastructure, while NVIDIA has already reported rapid data-center growth and guided to higher near-term total revenue. But this is not a one-to-one conversion. The evidence does not establish how much cloud capex will be spent on NVIDIA systems, when it will be recognized as NVIDIA revenue, or the full-year revenue outcome.",
    "arguments": [
      {
        "statement": "The scale and upward revisions of cloud-provider investment plans support the demand backdrop for NVIDIA, but only as planned or estimated industry spending.",
        "role": "supports",
        "reason": "Four hyperscalers had earlier indicated about $650 billion of planned 2026 spending; Alphabet later raised its capex guidance and Amazon raised its cash-capex expectation. Estimates for a broader five-company group and AI infrastructure spending reinforce the high-investment backdrop. These are plans, guidance, or third-party estimates—not confirmed full-year spending—and their scopes differ, so they support demand context rather than a precise NVIDIA sales estimate.",
        "references": [
          {
            "view_id": "v1",
            "evidence_ids": [
              "e127",
              "e192",
              "e347",
              "e324",
              "e322",
              "e107"
            ],
            "judgement_id": 347
          }
        ]
      },
      {
        "statement": "NVIDIA’s realized results and near-term guidance show that infrastructure demand is already converting into meaningful company revenue, particularly in data center.",
        "role": "supports",
        "reason": "NVIDIA reported FY2027 Q1 data-center revenue of $75.2 billion, up 92% year over year, and attributed growth to Blackwell 300 ramp and interconnect demand. It also guided to $91.0 billion total revenue for Q2, plus or minus 2%. The Q2 figure is total-company guidance, not a data-center forecast, and it excludes China data-center compute revenue; neither result confirms the full-year outlook.",
        "references": [
          {
            "view_id": "v3",
            "evidence_ids": [
              "e28",
              "e41"
            ],
            "judgement_id": 352
          },
          {
            "view_id": "v2",
            "evidence_ids": [
              "e27",
              "e41"
            ],
            "judgement_id": 356
          }
        ]
      },
      {
        "statement": "The cloud-investment backdrop and analyst forecasts lend support to a strong FY2027 revenue outlook, but forecasts vary and remain forecasts.",
        "role": "supports",
        "reason": "The FY2027 total-revenue assessment identifies third-party growth forecasts of 80% and 82% as support for its outlook range, while other estimates cited there are 42%. The divergence limits confidence. Those forecasts cannot be treated as reported NVIDIA revenue or as proof that cloud spending will translate into purchases at the implied rate.",
        "references": [
          {
            "view_id": "v2",
            "evidence_ids": [
              "e398",
              "e402",
              "e117",
              "e362"
            ],
            "judgement_id": 356
          }
        ]
      },
      {
        "statement": "Specific customer commitments and product readiness offer additional demand and supply signals, but do not establish the timing or dollar value of recognized NVIDIA sales.",
        "role": "supports",
        "reason": "SpaceX’s CEO said it would use NVIDIA systems exclusively and planned to deploy Vera Rubin systems; a report relayed his statement that SpaceX would receive a significant percentage of NVIDIA GPUs in 2027. Separately, a manufacturing facility was already producing GB300 and preparing for Vera Rubin. These statements and readiness evidence are not equivalent to completed deliveries, recognized revenue, or a quantified FY2027 contribution.",
        "references": [
          {
            "view_id": "v2",
            "evidence_ids": [
              "e511",
              "e514",
              "e515",
              "e516",
              "e517"
            ],
            "judgement_id": 356
          },
          {
            "view_id": "v3",
            "evidence_ids": [
              "e511",
              "e514",
              "e515",
              "e517",
              "e523"
            ],
            "judgement_id": 352
          }
        ]
      },
      {
        "statement": "Actual conversion remains constrained by the lack of customer-level allocation and by infrastructure, financing, and concentration risks.",
        "role": "challenges",
        "reason": "The evidence gives aggregate cloud capex, not the portion awarded to NVIDIA or the timing of deployment and revenue recognition. NVIDIA itself says shortages of data centers, energy, or capital could affect future revenue. Its FY2027 Q1 disclosures also show substantial direct-customer concentration. These factors make spending plans an imperfect proxy for NVIDIA sales and leave conversion uncertain.",
        "references": [
          {
            "view_id": "v1",
            "evidence_ids": [
              "e324",
              "e107"
            ],
            "judgement_id": 347
          },
          {
            "view_id": "v2",
            "evidence_ids": [
              "e48",
              "e14"
            ],
            "judgement_id": 356
          },
          {
            "view_id": "v9",
            "evidence_ids": [
              "e46",
              "e47",
              "e48"
            ],
            "judgement_id": 358
          }
        ]
      }
    ],
    "limitations": [
      "The cloud-capex figures cover differing company sets and definitions; some are management plans or guidance, while others are third-party estimates. They are not actual aggregate 2026 spending.",
      "No cited evidence quantifies the share of cloud-provider capex directed to NVIDIA, the timing of deployments, or the amount ultimately recognized as NVIDIA revenue.",
      "NVIDIA’s Q2 revenue guidance is for total revenue and excludes China data-center compute revenue; it is not a full-year or data-center-specific forecast.",
      "SpaceX’s stated future use, projected GPU allocation, and Vera Rubin manufacturing preparation are future intentions or readiness signals, not completed sales or confirmed revenue.",
      "Customer concentration, access to data-center capacity, energy and capital, and China-market limitations remain relevant risks to conversion."
    ],
    "watch_questions": [
      "How much of cloud providers’ actual 2026 spending is allocated to NVIDIA systems, and how much is recognized as revenue during FY2027?",
      "Do subsequent NVIDIA reports confirm sustained data-center growth and delivery volumes, including Vera Rubin, rather than only plans or readiness?",
      "Do cloud providers continue to raise or meet capex plans, and do capacity, energy, financing, concentration, or China-market constraints affect deployment and purchases?"
    ],
    "unused_ids": [
      "v17",
      "v28",
      "v34"
    ],
    "scope_id": "capex",
    "as_of_seq": 379,
    "as_of": "2026-08-05",
    "input_fingerprint": "77b914a651fb7e5c2dd2ac4ac4590d343a23f11689c83cac596fd2f062a18102"
  }
}
```

## sample-2 / capex-fresh-552-result

```json
{
  "status": "rejected",
  "error": "ValueError: Unknown, stale, future or duplicate view/evidence pair"
}
```

## sample-2 / capex-fresh-584-result

```json
{
  "status": "rejected",
  "error": "ValueError: Unknown, stale, future or duplicate view/evidence pair"
}
```

## sample-2 / capex-update-552-result

```json
{
  "status": "rejected",
  "error": "ValueError: Unknown, stale, future or duplicate view/evidence pair"
}
```

## sample-2 / rubin-fresh-379-result

```json
{
  "status": "valid",
  "value": {
    "status": "supported",
    "conclusion": "Current research supports a qualified commercialization picture: Vera Rubin production and shipments are planned or underway at the production stage, customer demand and deployment plans are visible, and NVIDIA has given a roughly $20 billion FY2027 Vera sales expectation. It does not establish that Vera Rubin customer shipments or deployments have broadly occurred, or that the forecast revenue has been realized.",
    "arguments": [
      {
        "statement": "Production readiness and the start of production shipments are supported mainly by company statements, but actual customer shipments remain unconfirmed in the cited evidence.",
        "role": "supports",
        "reason": "NVIDIA said it had shipped samples and expected production shipments to begin in the second half of 2026, starting in Q3. The CEO later said Vera Rubin was already in production. These support production progress and the shipment outlook, but production is not the same as customer shipment; the cited evidence does not confirm that production shipments had begun.",
        "references": [
          {
            "view_id": "v7",
            "evidence_ids": [
              "e7",
              "e19",
              "e128"
            ],
            "judgement_id": 350
          }
        ]
      },
      {
        "statement": "Customer interest and planned deployments provide evidence of a commercial route to use, not proof of completed deployments.",
        "role": "supports",
        "reason": "Reports say several cloud providers had signed up to deploy Vera CPUs, and SK Telecom planned a 2027 AI factory using Vera Rubin. SpaceX also announced a satellite payload partnership specifying Vera CPUs and Rubin GPUs. These are meaningful demand and deployment signals, but the cited material describes commitments, plans, or a partnership rather than completed customer installations or operational deployments.",
        "references": [
          {
            "view_id": "v16",
            "evidence_ids": [
              "e449"
            ],
            "judgement_id": 351
          },
          {
            "view_id": "v15",
            "evidence_ids": [
              "e55"
            ],
            "judgement_id": 355
          },
          {
            "view_id": "v48",
            "evidence_ids": [
              "e523"
            ],
            "judgement_id": 357
          }
        ]
      },
      {
        "statement": "Revenue realization is not established; the best direct revenue evidence is guidance, not reported sales.",
        "role": "context",
        "reason": "NVIDIA was reported as guiding to around $20 billion in FY2027 Vera sales, supporting an expectation of material revenue if delivered. Separately, management said it had visibility to nearly $20 billion in total CPU revenue and clarified that this referred to standalone CPU revenue. That CPU figure is not interchangeable with total Vera product sales, and neither is an actual revenue result.",
        "references": [
          {
            "view_id": "v48",
            "evidence_ids": [
              "e471"
            ],
            "judgement_id": 357
          },
          {
            "view_id": "v16",
            "evidence_ids": [
              "e75",
              "e76"
            ],
            "judgement_id": 351
          }
        ]
      }
    ],
    "limitations": [
      "The evidence is mostly statements, plans, third-party reporting, and forecasts; it does not establish realized customer shipments at scale, completed deployments, or reported Vera revenue.",
      "Production status, production shipments, customer deployment, and revenue recognition are distinct stages and should not be treated as interchangeable.",
      "The approximately $20 billion Vera sales expectation and the nearly $20 billion standalone CPU revenue visibility are separate measures; the research does not establish that either amount has been realized. The CPU figure is not a substitute for total Vera product revenue."
    ],
    "watch_questions": [
      "Do subsequent company disclosures confirm that Vera Rubin production shipments to customers actually began, and when?",
      "Do named customers confirm Vera Rubin installations operating in production rather than planned or signed deployments?",
      "Do financial disclosures report Vera sales or standalone CPU revenue, and clarify how those amounts are defined and recognized?"
    ],
    "unused_ids": [
      "v14",
      "v60"
    ],
    "scope_id": "rubin",
    "as_of_seq": 379,
    "as_of": "2026-08-05",
    "input_fingerprint": "c2ba922490913aedae5b845af2bcac78214ec3b7fd9a03a6006c586822e04a6d"
  }
}
```

## sample-2 / rubin-fresh-532-result

```json
{
  "status": "rejected",
  "error": "ValueError: Unknown, stale, future or duplicate view/evidence pair"
}
```

## sample-2 / rubin-fresh-66-result

```json
{
  "status": "valid",
  "value": {
    "status": "insufficient",
    "conclusion": "Current research supports a credible commercialization pathway for Vera Rubin, but not established commercial results across production shipments, customer deployments, and revenue realization. NVIDIA has forecast production shipments beginning in the second half of 2026; named customer AI-factory projects plan to use Vera Rubin, with one planned to come online in 2027; and NVIDIA has forecast nearly $20 billion in CPU revenue for the year. The evidence does not establish that production shipments have begun, those customer deployments are operational, or the forecast revenue has been realized.",
    "arguments": [
      {
        "statement": "Management forecasts support expected production-shipment readiness, not completed shipments.",
        "role": "supports",
        "reason": "NVIDIA said it had shipped initial samples to customers and remained on track to begin production shipments in the second half of 2026, with a later statement specifying a Q3 start. These are management expectations, while the cited platform announcement is not evidence that production shipments actually began.",
        "references": [
          {
            "view_id": "v7",
            "evidence_ids": [
              "e7",
              "e19",
              "e43"
            ],
            "judgement_id": 71
          }
        ]
      },
      {
        "statement": "Named customer plans provide evidence of prospective deployment demand, but not operational deployments.",
        "role": "supports",
        "reason": "SK Telecom planned its first AI factory using Vera Rubin for 2027, and NVIDIA described a planned Vera Rubin buildout at NAVER's GAK Sejong site. These plans connect the platform to prospective customer infrastructure; they do not show that either site has come online or that the planned equipment has been deployed.",
        "references": [
          {
            "view_id": "v15",
            "evidence_ids": [
              "e55"
            ],
            "judgement_id": 56
          },
          {
            "view_id": "v7",
            "evidence_ids": [
              "e59"
            ],
            "judgement_id": 71
          }
        ]
      },
      {
        "statement": "The announced SK collaboration and memory relationship add commercialization context, but do not establish completed factory deployment or production supply.",
        "role": "context",
        "reason": "The broader SK-NVIDIA arrangement was announced as plans accompanied by letters of intent, while a long-term SK hynix AI-memory partnership and joint development were separately described. These facts indicate partnership activity, but the research does not show formal completion of the broader arrangement or actual Vera Rubin deployment under it.",
        "references": [
          {
            "view_id": "v14",
            "evidence_ids": [
              "e54",
              "e56",
              "e57"
            ],
            "judgement_id": 50
          },
          {
            "view_id": "v7",
            "evidence_ids": [
              "e61"
            ],
            "judgement_id": 71
          }
        ]
      },
      {
        "statement": "The nearly $20 billion CPU figure is a management forecast, not evidence of revenue already realized.",
        "role": "supports",
        "reason": "The CFO said NVIDIA had visibility to nearly $20 billion in total CPU revenue that year, and the CEO clarified that the figure concerned standalone CPU. Vera architecture and benchmarks had been published, but neither that release nor the forecast establishes recognized revenue; the research also notes that separate CPU revenue may be difficult to verify without disclosure.",
        "references": [
          {
            "view_id": "v16",
            "evidence_ids": [
              "e75",
              "e76",
              "e78",
              "e79"
            ],
            "judgement_id": 72
          }
        ]
      }
    ],
    "limitations": [
      "The cited evidence does not confirm that Vera Rubin production shipments had begun as of the research date; shipment timing remains guidance.",
      "Customer factory announcements are plans with future milestones, not evidence of completed or operational deployments.",
      "The CPU revenue forecast is not actual reported revenue, and the evidence does not establish its correspondence to a specific fiscal-year total.",
      "Production shipments, customer deployments, and revenue realization are distinct milestones; evidence for one should not be treated as proof of the others."
    ],
    "watch_questions": [
      "Does NVIDIA subsequently confirm that Vera Rubin production shipments have started, and when?",
      "Do the announced customer AI factories reach operational status with Vera Rubin deployed?",
      "Does NVIDIA report realized CPU revenue, with enough detail to assess it against the nearly $20 billion forecast?"
    ],
    "unused_ids": [],
    "scope_id": "rubin",
    "as_of_seq": 66,
    "as_of": "2026-07-24",
    "input_fingerprint": "3889a291d69246d0e46c5b90607ce815c06f46d59b827670a104785a66be5f95"
  }
}
```

## sample-2 / rubin-update-379-result

```json
{
  "status": "rejected",
  "error": "ValueError: Unknown, stale, future or duplicate view/evidence pair"
}
```

## sample-3 / capex-fresh-379-result

```json
{
  "status": "rejected",
  "error": "ValueError: Unknown, stale, future or duplicate view/evidence pair"
}
```

## sample-3 / capex-fresh-552-result

```json
{
  "status": "rejected",
  "error": "ValueError: Unknown, stale, future or duplicate view/evidence pair"
}
```

## sample-3 / capex-fresh-584-result

```json
{
  "status": "rejected",
  "error": "ValueError: Unknown, stale, future or duplicate view/evidence pair"
}
```

## sample-3 / rubin-fresh-379-result

```json
{
  "status": "rejected",
  "error": "ValueError: Unknown, stale, future or duplicate view/evidence pair"
}
```

## sample-3 / rubin-fresh-532-result

```json
{
  "status": "rejected",
  "error": "ValueError: Unknown, stale, future or duplicate view/evidence pair"
}
```

## sample-3 / rubin-fresh-66-result

```json
{
  "status": "valid",
  "value": {
    "status": "supported",
    "conclusion": "Current research supports an early, forward-looking commercialization picture for Vera Rubin: NVIDIA has shipped customer samples, management expects production shipments to begin in 2026’s second half, and named customer AI-factory deployments are planned. It does not establish that production shipments have begun, customer deployments are operational, or Vera-related revenue has been realized. The nearly $20 billion CPU revenue figure is a management forecast for standalone CPU revenue, not reported results, and the evidence does not establish that it is a Vera Rubin revenue figure or that “this year” maps to FY2027.",
    "arguments": [
      {
        "statement": "Customer sampling has occurred, while production shipments remain an expectation rather than a confirmed result.",
        "role": "supports",
        "reason": "This is the strongest evidence of progress toward commercialization, but it marks readiness and a management timetable—not proof of production shipments. The latest cited expectation is production shipments starting in Q3 and ramping into Q4; the recorded assessment also cautions that no cited event confirms production shipments have started.",
        "references": [
          {
            "view_id": "v7",
            "evidence_ids": [
              "e7",
              "e19",
              "e82",
              "e43"
            ],
            "judgement_id": 71
          }
        ]
      },
      {
        "statement": "Named customer and infrastructure plans show prospective deployment demand, not completed deployments.",
        "role": "supports",
        "reason": "NVIDIA described Vera Rubin in plans for SK Telecom’s first AI factory in 2027 and for an expanded NAVER facility. Those plans connect the platform to potential customer use, but neither statement says the facilities are already online or the systems deployed. The broader SK partnership was announced as plans with letters of intent to formalize it; a separate AI-memory partnership exists, but that does not establish that AI-factory construction is formally implemented.",
        "references": [
          {
            "view_id": "v15",
            "evidence_ids": [
              "e55"
            ],
            "judgement_id": 56
          },
          {
            "view_id": "v14",
            "evidence_ids": [
              "e54",
              "e56",
              "e57"
            ],
            "judgement_id": 50
          },
          {
            "view_id": "v7",
            "evidence_ids": [
              "e59",
              "e61"
            ],
            "judgement_id": 71
          }
        ]
      },
      {
        "statement": "Revenue evidence is a forecast for standalone CPUs, not realized Vera Rubin revenue.",
        "role": "challenges",
        "reason": "The CFO’s nearly $20 billion figure is explicitly a forecast of total CPU revenue “this year,” and the CEO clarified it refers to standalone CPU. It is therefore not evidence of revenue already earned, nor can it be treated as a Vera Rubin systems revenue forecast. The research assessment also notes that the evidence does not establish that “this year” corresponds to FY2027. Vera architecture and benchmark publication are product progress, not revenue realization.",
        "references": [
          {
            "view_id": "v16",
            "evidence_ids": [
              "e75",
              "e76",
              "e78"
            ],
            "judgement_id": 72
          }
        ]
      },
      {
        "statement": "The revenue forecast’s realization and independent verification remain uncertain.",
        "role": "context",
        "reason": "A third-party author notes that absent separate CPU revenue disclosure, the nearly $20 billion forecast may be harder to verify independently. This is a limitation on observability, not evidence that the forecast is false or that revenue has not been earned.",
        "references": [
          {
            "view_id": "v16",
            "evidence_ids": [
              "e79"
            ],
            "judgement_id": 72
          }
        ]
      }
    ],
    "limitations": [
      "The cited production-shipment statements are management expectations; the research contains no confirmation that Vera Rubin production shipments have actually begun.",
      "The cited customer facilities are planned or described as future deployments, not operating installations.",
      "No cited evidence reports realized Vera Rubin revenue. The CPU forecast concerns standalone CPUs, and its time-period mapping to FY2027 is not established.",
      "The evidence does not quantify Vera Rubin orders, shipment volumes, deployment timing beyond the stated plans, or recognized revenue."
    ],
    "watch_questions": [
      "Has NVIDIA confirmed actual Vera Rubin production shipments, rather than samples or expected start dates?",
      "Do the announced customer facilities proceed to operational deployments, and when?",
      "Does NVIDIA report realized revenue attributable to Vera Rubin systems or standalone Vera CPUs, and clarify the relevant fiscal period?"
    ],
    "unused_ids": [],
    "scope_id": "rubin",
    "as_of_seq": 66,
    "as_of": "2026-07-24",
    "input_fingerprint": "3889a291d69246d0e46c5b90607ce815c06f46d59b827670a104785a66be5f95"
  }
}
```

## sample-3 / rubin-update-379-result

```json
{
  "status": "valid",
  "value": {
    "status": "supported",
    "conclusion": "Current research supports an early, forward-looking commercialization picture for Vera Rubin: customer samples have been shipped, production shipments are expected to start in 2026’s second half, and customers have announced future deployment plans. It does not establish that production shipments have begun or customer facilities are operational. Revenue evidence includes an NVIDIA guide of around $20 billion in Vera sales for the fiscal year, but this is a forecast, not reported or realized revenue. It is distinct from the separate forecast of nearly $20 billion in total standalone CPU revenue.",
    "arguments": [
      {
        "statement": "Customer samples have shipped, while production shipments are expected rather than confirmed as an actual result.",
        "role": "supports",
        "reason": "This supports progress toward commercialization and a stated shipment timetable. NVIDIA forecast a second-half start, with a later statement specifying Q3; however, the assessment finds no direct event confirming production shipments have actually started. A third-party report says volume production has started, and a factory is preparing to produce Vera Rubin, but neither establishes customer shipments as an occurred result.",
        "references": [
          {
            "view_id": "v7",
            "evidence_ids": [
              "e7",
              "e19",
              "e128",
              "e199",
              "e511"
            ],
            "judgement_id": 350
          }
        ]
      },
      {
        "statement": "Named customer deployment plans support prospective demand, not completed deployments.",
        "role": "supports",
        "reason": "SK Telecom’s plan identifies Vera Rubin accelerated computing for a first AI factory planned to come online in 2027. This connects the product to an intended customer use, but the facility is not shown as operational. Separately, the SK Group collaboration was announced as plans with letters of intent to formalize the agreement, so that announcement should not be treated as proof that the broader partnership or factory build is fully implemented.",
        "references": [
          {
            "view_id": "v15",
            "evidence_ids": [
              "e55",
              "e54",
              "e217"
            ],
            "judgement_id": 355
          },
          {
            "view_id": "v14",
            "evidence_ids": [
              "e54",
              "e56"
            ],
            "judgement_id": 323
          }
        ]
      },
      {
        "statement": "The revenue evidence is a company forecast, not realized revenue, and the Vera-sales guide is distinct from the standalone-CPU forecast.",
        "role": "supports",
        "reason": "NVIDIA is reported as guiding to around $20 billion in Vera sales for the fiscal year; this is the most direct cited revenue outlook for Vera, but it does not show revenue already earned. Separately, management’s nearly $20 billion estimate is for total CPU revenue, and the CEO clarified that it is standalone CPU revenue. Those similar amounts answer different revenue questions and are not interchangeable.",
        "references": [
          {
            "view_id": "v48",
            "evidence_ids": [
              "e471"
            ],
            "judgement_id": 357
          },
          {
            "view_id": "v16",
            "evidence_ids": [
              "e75",
              "e76"
            ],
            "judgement_id": 351
          }
        ]
      },
      {
        "statement": "The evidence does not establish revenue realization or independently verify the forecast.",
        "role": "context",
        "reason": "The research provides forecasts, not reported Vera revenue results. It also notes that the standalone CPU revenue figure may be harder to verify if CPU revenue is not separately disclosed. That is an observability limitation, not evidence that the forecast is false.",
        "references": [
          {
            "view_id": "v16",
            "evidence_ids": [
              "e79"
            ],
            "judgement_id": 351
          },
          {
            "view_id": "v48",
            "evidence_ids": [
              "e471"
            ],
            "judgement_id": 357
          }
        ]
      }
    ],
    "limitations": [
      "No cited event directly confirms that Vera Rubin production shipments to customers have begun; expectations, claims of production, and factory preparations are not equivalent to confirmed shipments.",
      "The cited customer deployment evidence is prospective. It does not establish that the named facilities are operational or that Vera systems have been deployed there.",
      "The approximately $20 billion Vera-sales figure is guidance, not realized revenue. The nearly $20 billion standalone-CPU forecast is a separate figure and should not be substituted for Vera product revenue.",
      "The research does not establish recognized revenue attributable to Vera Rubin or provide enough evidence to determine how much of the forecast has been realized."
    ],
    "watch_questions": [
      "Has NVIDIA confirmed actual Vera Rubin production shipments to customers, beyond samples, forecasts, or production-readiness statements?",
      "Have the announced customer facilities become operational with Vera Rubin systems deployed?",
      "Has NVIDIA reported realized Vera sales, and clarified the period and revenue attribution?"
    ],
    "unused_ids": [
      "v60"
    ],
    "scope_id": "rubin",
    "as_of_seq": 379,
    "as_of": "2026-08-05",
    "input_fingerprint": "c2ba922490913aedae5b845af2bcac78214ec3b7fd9a03a6006c586822e04a6d"
  }
}
```

## sample-3 / rubin-update-532-result

```json
{
  "status": "valid",
  "value": {
    "status": "supported",
    "conclusion": "Current research supports a forward-looking, early commercialization picture for Vera Rubin, not completed commercialization across all three stages. NVIDIA has shipped customer samples and guides to production shipments beginning in the second half of 2026, but the research does not establish that production shipments to customers have actually begun. Customer plans and completed system validation show progress toward deployment, but do not establish operating customer facilities. Revenue evidence is guidance of around $20 billion in Vera sales for the fiscal year, not reported or realized revenue.",
    "arguments": [
      {
        "statement": "Samples have shipped and production shipments are guided for the second half of 2026, but actual production shipments to customers are not established.",
        "role": "supports",
        "reason": "This supports shipment readiness and a stated commercialization timetable, rather than confirming commercial shipments as an occurred result. NVIDIA said it shipped samples and expected production shipments in the second half, with a later statement specifying a Q3 start. The current assessment explicitly finds no actual shipment event. A third-party report says volume production has started, and NVIDIA's CEO said the product is already in production, but production status is not proof of customer shipments.",
        "references": [
          {
            "view_id": "v7",
            "evidence_ids": [
              "e7",
              "e19",
              "e128",
              "e199",
              "e511"
            ],
            "judgement_id": 425
          }
        ]
      },
      {
        "statement": "Customer evidence supports prospective deployments and technical readiness, not completed customer deployments.",
        "role": "supports",
        "reason": "SK Telecom plans a 2027 AI factory using Vera Rubin, while CoreWeave reports completed bring-up and validation of an NVL72 system. These connect Vera Rubin to intended customer use and show technical progress, but neither establishes that a customer facility is operating with deployed Vera Rubin systems. The SK Group announcement was a plan accompanied by letters of intent to formalize the agreement, not evidence that the broader partnership or factory is fully implemented.",
        "references": [
          {
            "view_id": "v15",
            "evidence_ids": [
              "e55",
              "e217"
            ],
            "judgement_id": 431
          },
          {
            "view_id": "v7",
            "evidence_ids": [
              "e748"
            ],
            "judgement_id": 425
          },
          {
            "view_id": "v14",
            "evidence_ids": [
              "e54"
            ],
            "judgement_id": 402
          }
        ]
      },
      {
        "statement": "The Vera revenue figure is a forecast, not revenue realization; a similar-sized standalone-CPU forecast is a different measure.",
        "role": "supports",
        "reason": "NVIDIA is reported as guiding to around $20 billion in Vera sales for the fiscal year. That is the direct revenue outlook for Vera, but current research provides no reported result showing that amount, or any portion of it, has been realized. Separately, management's nearly $20 billion forecast is for total standalone CPU revenue. The similar amounts concern different scopes and cannot be substituted for one another.",
        "references": [
          {
            "view_id": "v48",
            "evidence_ids": [
              "e471"
            ],
            "judgement_id": 357
          },
          {
            "view_id": "v16",
            "evidence_ids": [
              "e75",
              "e76"
            ],
            "judgement_id": 429
          }
        ]
      },
      {
        "statement": "Revenue attribution and verification remain limited.",
        "role": "context",
        "reason": "The cited research offers forward guidance rather than reported Vera revenue. It also notes that the standalone CPU estimate may be harder to verify without separate disclosure; this is an observability concern, not evidence that the forecast is wrong. The materials do not quantify recognized revenue attributable to Vera Rubin.",
        "references": [
          {
            "view_id": "v16",
            "evidence_ids": [
              "e79"
            ],
            "judgement_id": 429
          },
          {
            "view_id": "v48",
            "evidence_ids": [
              "e471"
            ],
            "judgement_id": 357
          }
        ]
      }
    ],
    "limitations": [
      "No cited event directly confirms that Vera Rubin production shipments to customers have begun. Samples, shipment guidance, production statements, and factory preparation are distinct from confirmed commercial shipments.",
      "Customer plans and CoreWeave's reported bring-up and validation do not establish completed deployment at an operating customer facility.",
      "The around-$20-billion Vera sales figure is guidance, not realized revenue; the nearly-$20-billion standalone CPU forecast is a separate measure.",
      "Current research does not establish reported or recognized Vera Rubin revenue or how much of the forecast, if any, has been realized."
    ],
    "watch_questions": [
      "Has NVIDIA confirmed actual Vera Rubin production shipments to customers, rather than samples or expected shipments?",
      "Have announced customer facilities become operational with Vera Rubin systems deployed?",
      "Has NVIDIA reported Vera sales or other realized revenue with a clear period and attribution?"
    ],
    "unused_ids": [
      "v60"
    ],
    "scope_id": "rubin",
    "as_of_seq": 532,
    "as_of": "2026-08-12",
    "input_fingerprint": "12bcd167cda7b812a97346b05491681a40d915ab68cc94094c848ee6f33448ac"
  }
}
```

## sample-3 / rubin-update-probe-result

```json
{
  "status": "valid",
  "value": {
    "facets": [
      {
        "facet": "shipments",
        "answer": "Research supports that customer samples have shipped and production shipments are guided to begin in the second half of 2026, with a later statement specifying a Q3 start. It does not establish that production shipments to customers have actually begun. Statements that the product is in production or that volume production has started are not confirmation of customer shipments.",
        "references": [
          {
            "view_id": "v7",
            "evidence_ids": [
              "e7",
              "e19",
              "e128",
              "e199",
              "e511"
            ]
          }
        ]
      },
      {
        "facet": "deployments",
        "answer": "Research shows prospective customer use and technical progress, not completed deployments at operating customer facilities. SK Telecom has a plan for a 2027 AI factory, and CoreWeave has reported bring-up and validation of an NVL72 system; neither establishes an operating facility with deployed Vera Rubin systems.",
        "references": [
          {
            "view_id": "v15",
            "evidence_ids": [
              "e55",
              "e217"
            ]
          },
          {
            "view_id": "v7",
            "evidence_ids": [
              "e748"
            ]
          },
          {
            "view_id": "v14",
            "evidence_ids": [
              "e54"
            ]
          }
        ]
      },
      {
        "facet": "revenue",
        "answer": "The around-$20-billion Vera sales figure is guidance, not reported or realized revenue; the research does not establish how much, if any, Vera revenue has been recognized. A nearly-$20-billion standalone CPU forecast is a separate measure and should not be treated as Vera revenue.",
        "references": [
          {
            "view_id": "v48",
            "evidence_ids": [
              "e471"
            ]
          },
          {
            "view_id": "v16",
            "evidence_ids": [
              "e75",
              "e76",
              "e79"
            ]
          }
        ]
      }
    ]
  }
}
```
