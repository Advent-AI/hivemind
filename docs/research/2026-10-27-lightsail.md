# Singapore development server — October 27, 2026

Alex requested creation of the USD 44/month Lightsail server in Singapore, with a final footprint check for extraction, Docker and frontend/API hosting. This slice provisions the server and verifies a private read-only application sample. It does not start paid extraction, expose the model-backed API publicly, transfer provider credentials or publish unfinished product changes.

## Resource and cost check

AWS's live `get-bundles` result in `ap-southeast-1` identifies `large_3_0`: two vCPUs, 8 GB RAM, 160 GB SSD, 5,120 GB monthly transfer and USD 44/month. Ubuntu 24.04 LTS (`ubuntu_24_04`) is available. No Lightsail instances existed in this region before this operation.

Measured locally before launch: `poc/data` 2.022 GiB, `poc/corpus` 4.225 GiB, and `poc/reports` 0.834 GiB. The default English ledger is 3.02 MiB (90 theses, 534 evidence records), its input database is 36.04 MiB (2,205 items), and its model archive is 59.71 MiB (2,061 calls). The largest archived request is 413.03 KiB. These are measurements of the present POC, not forecasts for a larger universe.

The default extractor processes items sequentially; model inference and embeddings use external services. A small Docker/API/frontend runtime shares this host. Disk capacity is ample. Eight GB is the starting memory budget; the private server check will measure the sample runtime, not claim a full paid-extraction benchmark. The plan has a 30% per-vCPU sustained baseline and burst capacity; prolonged CPU-heavy workloads need a separate measurement.

The USD 44 bundle includes the server's disk, attached static IPv4 address and transfer allowance. Docker Engine and serving the API/static frontend on this machine add no AWS service fee. Provider API usage, tax, optional snapshots and transfer overage are separate. Singapore internet egress above the allowance is USD 0.12/GB; both incoming and outgoing traffic consume the allowance. No extra managed database, load balancer or paid backup is provisioned.

Sources: [AWS plans](https://docs.aws.amazon.com/lightsail/latest/userguide/amazon-lightsail-bundles.html), [CPU baseline](https://docs.aws.amazon.com/lightsail/latest/userguide/baseline-cpu-performance.html), [transfer rules](https://docs.aws.amazon.com/lightsail/latest/userguide/amazon-lightsail-faq-data-transfer-allowance.html), [Docker installation](https://docs.docker.com/engine/install/ubuntu/).

## State and event plan

| State / event | Action and record |
|---|---|
| Before creation | Check account identity, existing instances, bundle price, image, region and unused local key path. Record this plan. |
| Ready to create | Use a dedicated local SSH key, import its public half, create one named instance with Docker bootstrap and project tags. Record AWS operation IDs. |
| Instance starting | Wait for the creation operation and SSH; do not submit a second create request while the first is in flight. |
| Network setup | Attach one static address to the new instance and restrict inbound SSH to the current client IP. Public application ports remain closed for this slice. |
| Bootstrap failure | Inspect the server's cloud-init log and repair only that installation; no replacement instance or larger plan without a new choice. |
| Ready | Verify CPU/RAM/disk, Docker/Compose, outbound HTTPS, and a private read-only API/frontend sample without model credentials. |
| Client disconnected | Server and data persist. The dedicated key and recorded endpoint allow reconnection. |
| Existing name found or uncertain creation result | Inspect that exact resource/operation before any retry. Do not replace or delete it. |
| Handoff | Record endpoint, configuration, measured check, cost and remaining work. Stop test containers; retain test artifacts. |

## Values and readers

| Value | Writer and readers |
|---|---|
| Instance name and AWS operation IDs | AWS creation response; later status, firewall, static-address and SSH checks |
| Dedicated SSH key | Local SSH key generator; private key stays in the owner's SSH directory, public key is imported to Lightsail |
| Static address | Lightsail allocation/attachment; local SSH command and future sync configuration |
| Bootstrap script | This provisioning slice; cloud-init only, with no provider credentials |
| Private sizing artifact | Explicit source/frontend files and read-only database copies; temporary validation containers only |

## Scope and checks

D337 records this user-authorized infrastructure slice. Frozen product modules, extraction defaults, model configuration, experimental concurrency and original local databases remain unchanged. Existing Dockerfiles provide the runtime boundary; the private test uses lexical reads with Idea calls disabled. Original data stays local and is never overwritten by the check.

Pending: resource creation and measured server verification.

## Provider keys in Secrets Manager (2026-10-27, Alex's request)

Alex asked for the OpenAI, Jev and DeepSeek keys this repository uses (`~/.config/hivemind/credentials.json`) to be placed in AWS Secrets Manager so the instance can use them. One secret, `hivemind/dev-sg/provider-keys` (ap-southeast-1, account 781007641082, tags Project/Owner/Environment as the instance), holds a JSON object with the same three names the code reads: `OPENAI_API_KEY`, `TYPESAFE_API_KEY` (Jev, `jev.KEY_NAME`), `DEEPSEEK_API_KEY`. Written from a temporary owner-only file that was deleted afterwards; verified by reading the value back and comparing hashes with the local file (all three match). Cost: USD 0.40 per secret per month plus USD 0.05 per 10,000 API calls.

Not done: a Lightsail instance cannot assume an IAM role, so reading the secret from the server needs an IAM user limited to `secretsmanager:GetSecretValue` on `arn:aws:secretsmanager:ap-southeast-1:781007641082:secret:hivemind/dev-sg/*`, whose access key goes on the instance. Creating that user was blocked by the agent's permission policy and is left to Alex. SSH from this Mac was also refused during banner exchange (the same happens to github.com: the VPN closes outbound port 22), so nothing was placed on the instance.
