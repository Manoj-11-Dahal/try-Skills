"""Second-level mind-map taxonomy and deterministic skill-path assignment.

Assignments use the local skill slug and its existing INDEX task description;
no upstream skill bodies are needed for categorization.
"""
from __future__ import annotations

import re

from skill_categories import CATEGORIES

SUBCATEGORY_LABELS = {
    "ai-agent-systems": {
        "agent-architecture-orchestration": "Agent architecture & orchestration",
        "prompts-context-memory": "Prompts, context & memory",
        "tools-integrations": "Tools & integrations",
        "evaluation-observability": "Evaluation & observability",
        "safety-governance": "Safety & governance",
        "reasoning-planning-and-loops": "Reasoning, planning & loops",
        "agent-self-improvement-and-governance": "Agent self-improvement & governance",
        "mcp-protocol-and-server-development": "MCP protocol & server development",
    },
    "software-development": {
        "languages-frameworks": "Languages & frameworks",
        "frontend": "Frontend",
        "backend-apis": "Backend & APIs",
        "architecture-devtools": "Architecture & developer tools",
        "testing-quality-release": "Testing, quality & release",
        "implementation-and-code-architecture": "Implementation & code architecture",
    },
    "cloud-infrastructure-security": {
        "cloud-platforms": "Cloud platforms",
        "containers-kubernetes": "Containers & Kubernetes",
        "networking-edge": "Networking & edge",
        "devops-reliability": "DevOps & reliability",
        "security-privacy": "Security & privacy",
        "authorized-security-testing": "Authorized security testing",
    },
    "data-analytics": {
        "data-engineering": "Data engineering",
        "databases-storage": "Databases & storage",
        "analytics-visualization": "Analytics & visualization",
        "spreadsheets-geospatial": "Spreadsheets & geospatial",
        "data-quality-governance": "Data quality & governance",
        "pattern-recognition-and-machine-learning": "Pattern recognition & machine learning",
    },
    "business-operations": {
        "finance-accounting": "Finance & accounting",
        "product-growth": "Product & growth",
        "marketing-sales": "Marketing & sales",
        "people-operations": "People operations",
        "legal-compliance": "Legal & compliance",
        "retail-hospitality": "Retail & hospitality",
        "supply-chain": "Supply chain",
        "insurance": "Insurance",
        "management-planning-and-tasking": "Management, planning & tasking",
    },
    "science-health-research": {
        "clinical-healthcare": "Clinical & healthcare",
        "trials-research-methods": "Trials & research methods",
        "life-sciences": "Life sciences",
        "physical-earth-sciences": "Physical & earth sciences",
        "statistics-evidence": "Statistics & evidence",
        "medical-imaging": "Medical imaging",
        "deep-research-and-evidence-synthesis": "Deep research & evidence synthesis",
    },
    "engineering-industry": {
        "agriculture": "Agriculture",
        "construction-built-environment": "Construction & built environment",
        "energy-climate": "Energy & climate",
        "manufacturing-quality": "Manufacturing & quality",
        "electronics-hardware": "Electronics & hardware",
        "robotics-controls": "Robotics & controls",
        "pcb-electronics-design": "PCB & electronics design",
        "residential-home-design": "Residential & home design",
    },
    "creative-media-design": {
        "visual-graphic-design": "Visual & graphic design",
        "ux-interaction-design": "UX & interaction design",
        "games-interactive": "Games & interactive",
        "image-3d": "Image & 3D",
        "audio-video": "Audio & video",
        "writing-publishing": "Writing & publishing",
        "blender-3d-production": "Blender & 3D production",
        "music-and-audio-production": "Music & audio production",
        "sound-design-and-effects": "Sound design & effects",
        "video-production-and-post": "Video production & post",
    },
    "education-public-service": {
        "curriculum-instruction": "Curriculum & instruction",
        "assessment-learning": "Assessment & learning",
        "civic-government": "Civic & government",
        "public-service-operations": "Public-service operations",
        "nonprofit-community": "Nonprofit & community",
    },
}

# Long, specific topic roots are checked before keyword scoring. These are
# intentionally scoped to known subject prefixes; generic operation suffixes
# do not decide the topic folder.
PREFIX_RULES = {
    "ai-agent-systems": [
        ("evaluation-observability", ("agent-telemetry", "aas-agent-quality", "evaluation-harness", "agent-runtime-debugging", "agent-observability", "agent-evaluation", "agent-quality", "agent-commit-message", "evidence-certainty", "evidence-coverage", "success-signal", "attempt-diff", "verification-and-stopping", "agent-loop-budgeting", "trace-analysis", "run-trace", "run-observability", "observability", "telemetry", "tokenwise", "edge-inference", "gpu-model-serving", "per-iteration-tool-budget", "progress-ledger", "scheduled-agent", "skill-change-to-evaluation", "skill-trigger", "skill-workflow-exit", "same-error-fingerprint")),
        ("prompts-context-memory", ("agent-memory", "agent-graph-memory", "codebase-memory", "context-engineering", "prompt", "retrieval", "rag-", "memory-index", "shared-agent-memory", "session-memory", "source-grounded", "contradictory-web-claim", "web-claim", "web-query", "web-quotation", "redirected-source", "continuous-learning", "multi-chunk-fetch", "azure-ai-search-grounding")),
        ("safety-governance", ("untrusted-input", "prompt-injection", "human-approval", "human-escalation", "read-only-to-write", "side-effect", "permission-boundary", "agent-safety", "safety-gate", "privacy-governance", "trust-boundary", "external-write", "data-minimization", "issue-body-untrusted", "resume-session-permission", "safe-output", "agent-pr-changed-path", "readme-command-instruction")),
        ("tools-integrations", ("agent-tools", "mcp-", "mcp-server", "agent-browser", "browser-agent", "tool-execution", "tool-call", "tool-argument", "tool-response", "tool-timeout", "tool-unavailable", "skill-discovery", "skill-stack", "bot-development", "parallel-findall", "infsh-cli", "create-llms",  "tavily-web", "gemini-api-dev", "hugging-face", "hf-cli", "transformers-js", "vllm-server", "fal-platform", "fal-workflow", "copilot-cli", "copilot-sdk", "github-copilot", "gh-aw", "awf-skill", "agentspace", "azure-ai-agents", "azure-ai-projects", "api-tool", "web-search", "parallel-web", "documentation-automation", "elevenlabs", "planetscale-schema", "skill-frontmatter", "skill-tool-capability")),
        ("agent-architecture-orchestration", ("partial-completion-state", "agent-architecture", "agent-coordination", "agentic-loop", "agentic-workflow", "agentic-workflows", "agent-workflow", "task-decomposition", "multi-agent", "subagent", "parallel-worker", "long-running-agent", "state-and-handoff", "loop-finalization", "agentic-code-change", "custom-agents", "failure-recovery", "multi-session-project", "skill-authoring", "crewai", "neural-network-development", "hf-mem")),
        ("evaluation-observability", ("observability", "telemetry", "trace", "attempt-diff", "agent-loop-budgeting", "agent-quality", "runtime-debugging")),

    ],
    "software-development": [
        ("testing-quality-release", ("javascript-testing", "test-driven", "testing-", "test-", "qa-", "regression", "release-readiness", "release-", "ci-", "cd-", "lint-", "flaky-test", "benchmarking", "coverage-", "validation", "verification", "test-fixture", "test-case", "test-plan", "acceptance-test", "performance-benchmark", "notarization", "app-store", "apple-release", "apple-testflight", "browser-qa", "browser-test", "browser-cross-browser", "browser-regression", "pull-request-test", "build-verification", "bench-read", "instruments-", "checkpoint-artifact", "dependabot", "release-note", "xctrace-", "environment-parity", "domain-diversity", "synthetic-upload", "ios-memory-pressure", "repo-native-test")),
        ("backend-apis", ("backend-ops", "api-", "api/", "fastapi", "graphql", "grpc", "rest-api", "webhook", "server-side", "service-api", "rate-limit-handler", "database-migration", "database-connection", "auth-api", "request-routing", "event-delivery", "idempotent-jobs", "pagination-semantics", "pool-saturation", "cache-consistency", "api-onboarding", "bittorrent", "blockchain-cryptocurrency", "search-engine-development", "web-server-development", "write-read-consistency")),
        ("frontend", ("react-", "react/", "react-native", "svelte", "tailwind", "threejs", "spline-", "frontend", "browser-ui", "browser-visual", "browser-accessibility", "web-accessibility", "web-design", "ui-", "ux-", "swiftui", "avalonia-layout", "makepad-", "responsive-", "keyboard-focus", "dialog-focus", "screen-reader", "visual-regression", "layout-shift", "css-", "html-", "component-", "design-system", "interactive-ui", "angular", "sveltekit", "accessibility", "augmented-reality", "browser-", "create-web-form", "create-web-", "error-empty-state", "pagination-filter", "web-3d", "zustand", "large-text", "docs-version-selector")),
        ("languages-frameworks", ("kotlin-", "swift-", "swiftui-", "rust-", "golang-", "java-", "python-", "typescript-", "javascript-", "csharp-", "dotnet-", "php-", "ruby-", "laravel-", "framework-", "language-", "compiler-", "runtime-", "ios-app", "android-app", "macos-app", "xcodebuild-", "makepad-2-0", "bevy-ecs", "batch-files", "cuda-", "emulator-and-virtual-machine", "pydantic-", "qemu-", "regex-engine", "shell-development", "template-engine", "versioned-library", "memory-safety", "soc-memory-map", "voxel-engine")),
        ("architecture-devtools", ("uncategorized-system-building", "web-snippet-to-fetched-source-verifier", "architecture-", "codebase-", "repository-", "repo-", "git-", "github-", "gitlab-", "cli-", "command-line", "developer-tool", "devtools", "agents-generator", "gh-image", "tokenwise", "build-system", "dependency-", "package-", "monorepo", "configuration-", "toolchain", "editor-", "vscode", "code-review", "code-generation", "project-scaffold", "developer-onboarding", "api-onboarding", "checkpoint-artifact", "create-specification", "requirements-interview", "effective-config-defaults",  "documentation-", "docs-", "markdown-", "readme-", "codeql", "preview-deployment-source", "generated-artifact-source", "cross-reference", "anchor-heading")),
    ],
    "cloud-infrastructure-security": [
        ("security-privacy", ("security", "privacy", "iam", "secrets", "keyvault", "cloudtrail", "zero-trust", "policy-as-code", "mtls", "pci-compliance", "audit-logging", "vulnerability", "pentest", "incident-response", "forensic", "firewall-policy", "identity", "credential", "certificate", "encryption", "access-control", "authorization", "csp-report", "dependency-reachability", "extension-permissions", "request-signing", "macos-security", "ci-log-secret", "kali-linux", "seccomp", "remote-mac-build-agent")),
        ("containers-kubernetes", ("kubernetes", "k8s", "container", "docker", "helm-", "pod-", "cluster-", "ecs-", "aws-ecs-fargate", "fargate", "aks", "oci-", "containerd", "image-digest", "container-assurance", "nvidia-container")),
        ("networking-edge", ("cloudflare", "network", "dns-", "cdn", "edge-", "gateway", "load-balancer", "routing", "route-", "proxy", "firewall-network", "web-pubsub", "service-mesh", "ingress", "egress", "nat-", "vpc-", "subnet", "connectivity", "traffic-policy", "http-")),
        ("devops-reliability", ("terraform", "devops", "sre-", "reliability", "incident-", "backup", "disaster-recovery", "deployment", "deploy-", "infrastructure-as-code", "iac-", "release-", "monitoring", "observability", "runbook", "recovery", "cost-optimization", "capacity-planning", "site-reliability", "uptime", "ci-cd", "pipeline-", "fleet-operations", "linux-", "operating-system", "runtime-log", "azure-devops")),
        ("cloud-platforms", ("aws-", "azure-", "gcp-", "cloud-platform", "cloud-service", "vercel-", "cloud-", "storage-account", "resource-manager", "managed-database", "serverless-", "platform-as-a-service")),
    ],
    "data-analytics": [
        ("data-quality-governance", ("data-quality", "data-governance", "data-catalog", "data-lineage", "data-privacy", "data-contract", "schema-quality", "quality-rule", "record-quality", "duplicate-record", "data-validation", "metadata-governance", "data-dictionary", "data-retention", "data-access", "data-audit", "schema-change", "timestamp-timezone", "row-count-total-reconciliation")),
        ("spreadsheets-geospatial", ("geospatial", "geo-", "gis-", "spreadsheet", "excel-", "google-sheets", "sheets-", "csv-", "shapefile", "stac-", "remote-sensing", "earth-observation", "mapping-", "map-", "spatial-", "raster-", "vector-tile")),
        ("analytics-visualization", ("analytics", "visualization", "visualisation", "plotly", "dashboard", "chart-", "reporting", "business-intelligence", "bi-", "metric-analysis", "cohort-analysis", "experiment-analysis", "arize-", "insight", "statistics", "statistical", "forecasting", "trend-analysis", "adobe-cja", "adobe-analytics", "market-data", "ml-data-ops")),
        ("databases-storage", ("database", "postgres", "postgre", "sql-", "snowflake", "nosql", "redis", "mongo", "drizzle", "neon-", "vector-index", "vector-database", "storage", "lakehouse-table", "warehouse-serving", "data-warehouse", "object-store", "parquet", "data-lake", "query-engine", "dataverse", "knowledge-graph", "graph-rag")),
        ("data-engineering", ("data-eng", "data-engineering", "data-pipeline", "pipeline", "ingestion", "etl", "elt", "streaming", "stream-process", "orchestration", "lakehouse", "warehouse", "transformation", "batch-processing", "dataflow", "data-flow", "spark-", "airflow", "dbt-", "data-product", "data-platform", "polars")),
    ],
    "business-operations": [
        ("insurance", ("insure-ops", "insurance", "underwriting", "insurance-claim", "insurance-claims", "policyholder", "premium-audit", "reinsurance", "loss-ratio", "actuarial", "broker-")),
        ("finance-accounting", ("finance-ops", "finance", "accounting", "account-payable", "accounts-payable", "receivables", "revenue-recognition", "treasury", "tax-", "expense", "invoice", "billing", "cash-position", "close-reconciliation", "budget-variance", "financial", "investment-", "trading-", "backtest", "liquidity", "payment-ops")),
        ("legal-compliance", ("legal-ops", "legal", "contract", "compliance", "regulatory", "privacy-request", "legal-hold", "matter-intake", "clause-", "due-diligence", "policy-administration", "audit-evidence", "governance-", "records-retention", "gdpr", "terms-of-service", "google-admin-audit")),
        ("people-operations", ("people-ops", "human-resources", "hr-", "workforce", "recruiting", "recruitment", "employee", "payroll", "benefits", "leave-access", "onboarding", "performance-review", "candidate", "talent", "staffing", "volunteer-management")),
        ("retail-hospitality", ("retail-ops", "hospitality-ops", "retail", "hospitality", "restaurant", "food-service", "reservation", "guest-", "travel-operations", "event-operations", "hotel-", "ecommerce-fulfillment", "store-operations", "menu-", "guest-experience")),
        ("supply-chain", ("supply-ops", "supply-chain", "procurement", "sourcing", "inventory", "warehouse-operations", "logistics", "shipping", "freight", "purchase-order", "supplier", "vendor-management", "demand-planning", "transport-planning", "production-scheduling", "returns-logistics")),
        ("marketing-sales", ("gtm-ops", "marketing", "sales", "campaign", "seo-", "social-media", "linkedin-automation", "instagram-automation", "mailchimp", "klaviyo", "crm-", "customer-success", "lead-", "prospect", "account-research", "deal-room", "sales-enablement", "brand-", "ad-", "content-marketing", "newsletter", "email-campaign", "community-marketing", "devrel", "customer-support", "zendesk", "freshservice", "loops", "telegram-bot")),
        ("product-growth", ("calendar-", "google-calendar", "google-chat", "google-docs", "google-forms", "product-ops", "growth-evidence", "aas-saas", "product", "growth", "roadmap", "feature-", "product-discovery", "product-analytics", "experiments", "pricing", "saas", "retention", "activation", "onboarding", "user-research", "customer-feedback", "usage-based", "obsidian", "one-drive", "asana", "basecamp", "confluence", "meeting-distiller", "notion", "project-management", "work-management", "knowledge-management", "microsoft-365", "google-workspace", "google-drive", "gmail", "calendar-automation", "portfolio-", "strategy-", "service-desk", "knowledge-base", "freshservice", "zendesk")),
    ],
    "science-health-research": [
        ("medical-imaging", ("medical-imaging", "radiology", "radiograph", "dicom", "mri-", "ct-scan", "ultrasound", "segmentation", "imaging-model", "image-acquisition", "scanner-", "medical-image")),
        ("clinical-healthcare", ("health-admin", "clinical-care", "clinical-workflow", "patient", "healthcare", "hospital", "pharmacy-admin", "provider-credential", "prior-auth", "care-coordination", "clinical-record", "diagnostic-workflow", "medical-device-clinical", "clinical-decision")),
        ("trials-research-methods", ("trial-ops", "clinical-trial", "study-design", "research-method", "research-protocol", "protocol-design", "scientific-writing", "research-operations", "research-ethics", "systematic-review", "literature-review", "cohort-protocol", "observational-study", "experiment-design", "randomized", "study-planning", "trial-design", "publication-bias", "evidence-synthesis", "study-reporting", "sample-custody", "autoresearch", "bibliographic", "citation-fragment", "clinical-study", "clinical-cohort", "clinical-dataset", "confounder-bias", "research-gap", "literature-search", "pico-question", "scientific-dataset", "science-ml", "scientific-environment", "scientific-result", "scientific-time-series", "preprint-surveillance", "laboratory-automation", "medical-manuscript", "reference-integrity")),
        ("life-sciences", ("omics-data", "bioinformatics", "biomedical", "bioacoustic", "genomic", "genome", "genomics", "molecular", "rna-seq", "single-cell", "proteomics", "metabolic-model", "drug-discovery", "molecular-docking", "species-occurrence", "wildlife", "conservation", "ecology", "biology", "life-science", "sequence-analysis", "admet", "pharma", "biomarker", "camera-trap", "drug-target", "mass-spectrometry", "metabolic-modeling", "species-distribution", "sequence-analysis")),
        ("statistics-evidence", ("statistics", "statistical", "causal-inference", "effect-size", "confidence-interval", "power-analysis", "sample-size", "diagnostic-test-accuracy", "sensitivity-analysis", "survival-analysis", "heterogeneity", "forest-plot", "bayesian", "uncertainty-quantification", "measurement-error", "evidence-grade", "evidence-certainty", "meta-analysis", "qmd-", "regression-analysis", "statistics-and-evidence", "confounder", "bias-analysis", "effect-estimate", "risk-of-bias", "evidence-landscape", "evidence-appraisal", "scientific-visualization", "clinical-prediction", "epidemiological", "medical-claim-strength", "calibration", "diagnostic-test", "surveillance-analysis")),
        ("physical-earth-sciences", ("quantum", "physics", "astronomy", "astrophysics", "geology", "earth-science", "geophysics", "oceanography", "meteorology", "climate-science", "chemistry", "chemical", "computational-chemistry", "pde-", "ode-", "dynamical-systems", "space-weather", "earth-observation", "materials-science", "physical-science", "solar-physics", "grover", "qaoa", "vqe", "inverse-problem", "nonlinear-dynamical", "physical-law", "pinn-collocation")),
    ],
    "engineering-industry": [
        ("agriculture", ("agri-ops", "agriculture", "agricultural", "agronomy", "crop-", "soil-", "farm-", "livestock", "aquaculture", "irrigation", "forestry", "land-stewardship", "plant-health", "harvest-", "precision-ag")),
        ("construction-built-environment", ("built-env", "construction", "built-environment", "building", "facility", "facilities", "real-estate", "site-due-diligence", "permit-submittal", "design-coordination", "field-quality", "commissioning", "civil-engineering", "structural-load", "construction-schedule", "property-operations")),
        ("energy-climate", ("energy-ops", "climate-ops", "energy", "climate", "carbon", "emissions", "renewable", "solar-", "wind-", "electric-grid", "utility", "utilities", "ghg-", "sustainability", "decarbonization", "adaptation", "power-generation", "electricity", "energy-reporting", "grid-")),
        ("manufacturing-quality", ("mfg-ops", "manufacturing", "manufacture", "factory", "production-line", "production-quality", "spc-", "six-sigma", "process-control", "quality-control", "quality-assurance", "inspection", "assembly-test", "supplier-quality", "industrial-process", "production-scheduling", "yield-analysis", "process-modification", "digital-twin", "cfd-")),
        ("robotics-controls", ("robotics", "robot-", "robot-automation", "robotic", "controls", "control-system", "control-loop", "plc-", "motion-control", "actuator", "mechatronics", "ros-", "autonomous-system", "industrial-automation", "robotics-controls", "sim-to-real", "nvidia-physical-ai", "jetson-deployment")),
        ("electronics-hardware", ("pcb", "pcb-design", "printed-circuit-board", "electronics", "hardware", "embedded", "firmware", "arm-cortex", "cortex-m", "semiconductor", "silicon", "fpga", "circuit", "analog-", "spice-", "sensor", "microcontroller", "microprocessor", "chip-design", "rtl-", "static-timing", "clock-domain", "clock-tree", "signal-integrity", "power-electronics", "instrumentation", "spacecraft", "cubesat", "constellation", "edge-fleet", "edge-site", "edge-model", "iot-", "adc-", "mixed-signal", "low-power", "dft-", "post-layout", "transistor", "wafer", "fpga-", "qemu-kernel", "emc-", "finite-element", "finite-volume", "lithography", "logic-synthesis", "materials-science", "measurement-instrument", "multi-camera", "orbital-element", "formal-property", "cuda-", "macos-nested-code-signature", "mqtt-session")),
    ],
    "creative-media-design": [
        ("games-interactive", ("game-development", "game-", "games", "godot", "unity-", "unreal-", "interactive-fiction", "interactive-media", "web-games", "bevy-", "threejs", "spline-3d", "animation-", "gameplay", "engine-selection")),
        ("audio-video", ("audio", "video", "podcast", "music", "sound", "premiere", "film-", "cinema", "voiceover", "subtitle", "captioning", "broadcast", "streaming-media", "davinci-resolve", "motion-graphics", "gb28181", "rtsp-stream", "camera-interoperability")),
        ("image-3d", ("blender", "3d-", "three-dimensional", "rendering", "render-", "modeling", "sculpting", "texture-", "image-generation", "image-editing", "image-", "photography", "product-photography", "spline", "visualization-3d", "mesh-", "voxel-", "cad-", "omniverse-scene")),
        ("ux-interaction-design", ("design-it", "ux-", "ui-", "user-experience", "interaction-design", "interaction-pattern", "interface-design", "typography", "widget-based", "figma", "wireframe", "prototype", "design-system", "accessibility-design", "web-design", "frontend-design", "product-design", "landing-page-design", "responsive-design", "motion-design", "visual-hierarchy", "animate", "reduced-motion", "screenshot-diff", "accessibility")),
        ("visual-graphic-design", ("graphic-design", "visual-design", "visual-", "illustration", "brand-identity", "logo-", "poster-", "image-asset", "art-direction", "color-palette", "ad-creative", "photoshop", "canva", "figma-graphic", "vector-art", "print-design", "layout-design", "brand-design", "drawio", "google-slides", "place-route", "foundry-pdk", "ai-content-rights")),
        ("writing-publishing", ("writing", "publishing", "copywriting", "copy-editing", "editorial", "journalism", "manuscript", "book-", "newsletter-writing", "technical-writing", "content-authoring", "documentation-writing", "storytelling", "screenplay", "blog-writing", "article-writing", "scientific-writing", "grant-writing", "risk-of-bias")),
    ],
    "education-public-service": [
        ("nonprofit-community", ("nonprofit", "non-profit", "volunteer", "fundraising", "community", "donor", "grant-administration", "board-governance", "community-outreach", "volunteer-onboarding")),
        ("civic-government", ("civic", "government", "public-policy", "public-records", "records-request", "public-comment", "municipal", "constituent-service", "election", "legislative", "city-", "county-", "government-services")),
        ("public-service-operations", ("public-service", "public-sector", "service-administration", "benefits-administration", "case-management", "service-operations", "procurement-compliance", "public-program", "constituent-case", "program-outcome", "public-information", "social-service", "civic-ops-programs", "school-operations")),
        ("assessment-learning", ("assessment", "learning-assessment", "student-progress", "quiz", "grading", "learning-outcome", "evaluation", "rubric", "formative", "summative", "learner-performance", "assessment-item", "assessment-design", "program-evaluation", "learning-analytics")),
        ("curriculum-instruction", ("edu-ops", "education", "curriculum", "instruction", "lesson", "teaching", "teacher", "classroom", "course-design", "learning-design", "learning-objective", "pedagogy", "socratic", "stem-lab", "course-material", "lms-", "inclusive-learning", "language-scaffold", "student-support", "school-", "educator", "educational")),
    ],
}

# Ordered fallback labels are a deliberate best-fit only: every skill is placed
# inside one of the user-provided subcategories; no miscellaneous bucket exists.
DEFAULT_SUBCATEGORY = {
    "ai-agent-systems": "agent-architecture-orchestration",
    "software-development": "architecture-devtools",
    "cloud-infrastructure-security": "cloud-platforms",
    "data-analytics": "data-engineering",
    "business-operations": "product-growth",
    "science-health-research": "trials-research-methods",
    "engineering-industry": "electronics-hardware",
    "creative-media-design": "visual-graphic-design",
    "education-public-service": "public-service-operations",
}

OPERATION_WORDS = {
    "capability", "surface", "map", "version", "compatibility", "input", "output", "contract",
    "permission", "boundary", "review", "integration", "parity", "trace", "failure", "triage",
    "record", "performance", "envelope", "change", "impact", "assessment", "reproducibility",
    "fixture", "plan", "release", "handoff", "scope", "intake", "gate", "source", "provenance",
    "ledger", "threshold", "rule", "check", "scenario", "sensitivity", "matrix", "exception",
    "completeness", "reconciliation", "approval", "evidence", "packet", "recovery", "readiness",
    "drill", "closeout", "ownership", "verification", "validation", "audit", "report", "summary",
    "workflow", "workflows", "operation", "operations", "task", "tasks", "process", "reviewer",
}


def _normalized(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.casefold()).strip()


def _matches_prefix(slug: str, prefix: str) -> bool:
    return slug == prefix or slug.startswith(prefix + "-")


def _slug_words(slug: str) -> set[str]:
    return {word for word in re.findall(r"[a-z0-9]+", slug.casefold()) if word not in OPERATION_WORDS}


DESCRIPTION_NOISE = OPERATION_WORDS | {
    "claim", "claims", "ledger", "inventory", "evidence", "review", "record",
    "packet", "approval", "scope", "boundary", "task", "workflow", "check",
}


def _semantic_description(description: str) -> str:
    """Drop standard artifact labels before the topical part of INDEX rows."""
    text = re.sub(r"\s+", " ", description).strip()
    # Generated catalog rows use labels such as "Failure Triage Record for X";
    # the subject follows the first "for". This avoids routing on generic
    # artifact words like ledger, inventory, or claim.
    if re.search(r"\bfor\b", text, re.I):
        text = re.split(r"\bfor\b", text, maxsplit=1, flags=re.I)[1]
    return text.strip(" :—-.")


def _keyword_score(slug: str, description: str, keywords: tuple[str, ...]) -> tuple[int, list[str]]:
    normalized_slug = _normalized(slug)
    normalized_description = _normalized(_semantic_description(description))
    slug_words = _slug_words(slug)
    hits: list[str] = []
    score = 0
    for raw in keywords:
        phrase = _normalized(raw)
        if not phrase:
            continue
        if " " in phrase:
            if f" {phrase} " in f" {normalized_slug} ":
                score += 9
                hits.append(raw)
            elif f" {phrase} " in f" {normalized_description} ":
                score += 3
                hits.append(raw)
        elif phrase in slug_words:
            score += 5
            hits.append(raw)
        elif phrase not in DESCRIPTION_NOISE and re.search(
            rf"(?<![a-z0-9]){re.escape(phrase)}(?![a-z0-9])", normalized_description
        ):
            score += 2
            hits.append(raw)
    return score, hits


MATRIX_SUFFIXES = (
    "approval-evidence-packet", "change-impact-trace", "closeout-handoff-ledger",
    "completeness-reconciliation", "exception-triage-queue", "recovery-readiness-drill",
    "scenario-sensitivity-matrix", "scope-intake-gate", "source-provenance-ledger",
    "threshold-rule-check",
)


def _topic_tail(slug: str, prefix: str) -> str:
    tail = slug[len(prefix):].strip("-")
    for suffix in sorted(MATRIX_SUFFIXES, key=len, reverse=True):
        if tail.endswith("-" + suffix):
            return tail[:-(len(suffix) + 1)].rstrip("-")
    return tail


def _assigned(subcategory: str, reason: str) -> tuple[str, str, int, int]:
    return subcategory, reason, 100, 100


EXPANSION_PREFIX_RULES = {
    "ai-agent-systems": (
        ("looplab-", "reasoning-planning-and-loops"),
        ("selfupdate-", "agent-self-improvement-and-governance"),
        ("mcplab-", "mcp-protocol-and-server-development"),
    ),
    "software-development": (
        ("codelab-", "implementation-and-code-architecture"),
        ("testlab-", "testing-quality-release"),
    ),
    "cloud-infrastructure-security": (("authorizedsec-", "authorized-security-testing"),),
    "business-operations": (("managementlab-", "management-planning-and-tasking"),),
    "data-analytics": (("patternlab-", "pattern-recognition-and-machine-learning"),),
    "science-health-research": (("deepresearch-", "deep-research-and-evidence-synthesis"),),
    "engineering-industry": (
        ("pcblab-", "pcb-electronics-design"),
        ("residentiallab-", "residential-home-design"),
    ),
    "creative-media-design": (
        ("blenderlab-", "blender-3d-production"),
        ("musiclab-", "music-and-audio-production"),
        ("soundlab-", "sound-design-and-effects"),
        ("videolab-", "video-production-and-post"),
    ),
}


def classify_subcategory(category: str, slug: str, description: str = "") -> tuple[str, str, int, int]:
    """Return (subcategory, reason, score, margin) using only local metadata."""
    if category not in SUBCATEGORY_LABELS:
        raise ValueError(f"unknown top-level category: {category}")
    rules = PREFIX_RULES[category]
    for prefix, subcategory in EXPANSION_PREFIX_RULES.get(category, ()):
        if slug.startswith(prefix):
            return _assigned(subcategory, f"internet topic-pack namespace: {prefix.rstrip('-')}")

    # Family-level packs encode a domain in their prefix and a finer topic in
    # the middle of the slug. Remove the controlled workflow suffix first.
    if category == "ai-agent-systems" and slug.startswith("aas-agent-quality-"):
        tail = _topic_tail(slug, "aas-agent-quality")
        if any(token in tail for token in ("refusal", "trust-boundary", "tool-argument-boundary", "privacy", "minimization", "activation-boundary", "sensitive")):
            return _assigned("safety-governance", "AAS agent-quality safety topic")
        if any(token in tail for token in ("retrieval", "source-provenance", "citation")):
            return _assigned("prompts-context-memory", "AAS agent-quality retrieval/context topic")
        return _assigned("evaluation-observability", "AAS agent-quality evaluation topic")
    if category == "ai-agent-systems" and slug.startswith("aas-agent-coordination-"):
        tail = _topic_tail(slug, "aas-agent-coordination")
        if any(token in tail for token in ("permission", "approval", "trust", "untrusted", "authorization", "sensitive")):
            return _assigned("safety-governance", "AAS agent-coordination authorization topic")
        if "tool" in tail or "quota" in tail:
            return _assigned("tools-integrations", "AAS agent-coordination tool/quota topic")
        return _assigned("agent-architecture-orchestration", "AAS agent-coordination topic")
    if category == "education-public-service" and slug.startswith("edu-ops-"):
        tail = _topic_tail(slug, "edu-ops")
        if any(token in tail for token in ("assessment", "learner-support", "program-evaluation")):
            return _assigned("assessment-learning", "education operations assessment/support topic")
        if "school-operations" in tail:
            return _assigned("public-service-operations", "school administration topic")
        return _assigned("curriculum-instruction", "education operations instructional topic")
    if category == "education-public-service" and slug.startswith("civic-ops-"):
        tail = _topic_tail(slug, "civic-ops")
        if any(token in tail for token in ("grant", "volunteer", "board", "nonprofit")):
            return _assigned("nonprofit-community", "civic operations nonprofit/community topic")
        if any(token in tail for token in ("records", "public-comment", "policy", "governance")):
            return _assigned("civic-government", "civic operations government topic")
        return _assigned("public-service-operations", "civic operations service topic")
    if category == "data-analytics" and slug.startswith("aas-data-"):
        tail = _topic_tail(slug, "aas-data")
        if any(token in tail for token in ("quality", "governance", "lineage", "schema", "privacy", "catalog", "retention")):
            return _assigned("data-quality-governance", "AAS data quality/governance topic")
        if any(token in tail for token in ("csv", "spreadsheet", "formula", "geospatial", "mapping", "sheet")):
            return _assigned("spreadsheets-geospatial", "AAS data spreadsheet/geospatial topic")
        if any(token in tail for token in ("query", "index", "database", "postgres", "storage", "sql")):
            return _assigned("databases-storage", "AAS data database/query topic")
        if any(token in tail for token in ("dashboard", "visualization", "metric", "chart", "analytics", "report")):
            return _assigned("analytics-visualization", "AAS data analytics topic")
        return _assigned("data-engineering", "AAS data engineering topic")
    if category == "data-analytics" and slug.startswith("ml-data-ops-"):
        tail = _topic_tail(slug, "ml-data-ops")
        if any(token in tail for token in ("snapshot-lineage", "split-leakage", "feature-parity", "target-quality")):
            return _assigned("data-quality-governance", "tabular ML data quality/lineage topic")
        if any(token in tail for token in ("baseline", "calibration", "drift", "metric", "subgroup", "experiment")):
            return _assigned("analytics-visualization", "tabular ML analytics/evaluation topic")
        return _assigned("data-engineering", "tabular ML data pipeline topic")
    if category == "software-development" and slug.startswith("aas-mobile-"):
        tail = _topic_tail(slug, "aas-mobile")
        if "push-token" in tail or "notification" in tail:
            return _assigned("backend-apis", "mobile push service integration topic")
        if any(token in tail for token in ("deep-link", "locale-layout", "accessibility", "navigation", "layout")):
            return _assigned("frontend", "mobile interface/navigation topic")
        if any(token in tail for token in ("app-size", "crash-symbol", "store-privacy", "permission-declaration")):
            return _assigned("testing-quality-release", "mobile release/privacy verification topic")
        return _assigned("languages-frameworks", "mobile application framework topic")
    if category == "software-development" and slug.startswith("aas-devtools-"):
        tail = _topic_tail(slug, "aas-devtools")
        if "api-version" in tail or "sdk-error" in tail or "api-" in tail:
            return _assigned("backend-apis", "developer API/SDK contract topic")
        if any(token in tail for token in ("test", "regression", "compat-exception", "quickstart-parity")):
            return _assigned("testing-quality-release", "developer-toolchain verification topic")
        return _assigned("architecture-devtools", "developer tooling topic")
    if category == "business-operations":
        for prefix, subcategory in (
            ("aas-docs", "product-growth"),
            ("aas-saas", "product-growth"),
            ("growth-evidence", "product-growth"),
            ("aas-devrel", "marketing-sales"),
        ):
            if _matches_prefix(slug, prefix):
                return _assigned(subcategory, f"business domain prefix: {prefix}")
    if category == "software-development":
        if slug.startswith(("apple-", "app-store-", "macos-", "xcode-", "xcodebuild-")):
            quality_markers = ("test", "release", "notariz", "sign", "privacy", "crash", "symbol", "storage-footprint", "energy-impact", "background-task", "installer", "entitlement", "sandbox", "tcc", "update-feed", "build-train")
            if any(marker in slug for marker in quality_markers):
                return _assigned("testing-quality-release", "Apple platform verification/release topic")
            return _assigned("languages-frameworks", "Apple platform development topic")
        if slug.startswith("browser-") and any(marker in slug for marker in ("qa", "test", "regression", "cross-browser", "pagination-validation", "print-to-pdf")):
            return _assigned("testing-quality-release", "browser verification/testing topic")
    if category == "cloud-infrastructure-security":
        for prefix, subcategory in (
            ("aws-ecs-fargate", "containers-kubernetes"),
            ("aas-secure-delivery", "security-privacy"),
            ("azure-sre", "devops-reliability"),
            ("vercel-deployment", "devops-reliability"),
            ("vercel-optimize", "devops-reliability"),
        ):
            if _matches_prefix(slug, prefix):
                return _assigned(subcategory, f"cloud domain prefix: {prefix}")
    if category == "creative-media-design" and slug.startswith("aas-game-"):
        tail = _topic_tail(slug, "aas-game")
        if any(token in tail for token in ("audio", "subtitle", "voice", "caption", "sound")):
            return _assigned("audio-video", "AAS game audio/caption topic")
        return _assigned("games-interactive", "AAS game-development topic")
    if category == "creative-media-design" and slug.startswith("game-"):
        if any(token in slug for token in ("audio", "subtitle", "voice", "caption", "sound")):
            return _assigned("audio-video", "game audio/caption topic")
        if any(token in slug for token in ("ui-", "layout", "accessibility", "reduced-motion")):
            return _assigned("ux-interaction-design", "game interface/accessibility topic")
        return _assigned("games-interactive", "game systems/topic")
    if category == "creative-media-design" and slug.startswith("aas-visual-"):
        tail = _topic_tail(slug, "aas-visual")
        if any(token in tail for token in ("interface", "interaction", "ux", "accessibility", "layout")):
            return _assigned("ux-interaction-design", "AAS visual interaction-design topic")
        return _assigned("visual-graphic-design", "AAS visual-design topic")

    # Exact topic roots with known scope: generic workflow suffixes do not
    # decide the subject folder.
    for subcategory, prefixes in rules:
        for prefix in sorted(prefixes, key=len, reverse=True):
            if _matches_prefix(slug, prefix):
                return subcategory, f"topic prefix: {prefix}", 100, 100

    scored: list[tuple[int, int, str, list[str]]] = []
    for order, (subcategory, prefixes) in enumerate(rules):
        score, hits = _keyword_score(slug, description, tuple(prefixes))
        scored.append((score, -order, subcategory, hits))
    scored.sort(reverse=True)
    best_score, _, best, hits = scored[0]
    second_score = scored[1][0] if len(scored) > 1 else 0
    margin = best_score - second_score
    if best_score == 0:
        return DEFAULT_SUBCATEGORY[category], "best-fit category default (no distinct metadata token)", 0, 0
    return best, "metadata keywords: " + ", ".join(hits[:5]), best_score, margin


def skill_path(root, category: str, slug: str, description: str = ""):
    """Return the canonical category/subcategory/skill directory path."""
    subcategory, _, _, _ = classify_subcategory(category, slug, description)
    return root / category / subcategory / slug


def relative_skill_path(category: str, slug: str, description: str = "") -> str:
    """Return the INDEX-style relative path from repository root."""
    subcategory, _, _, _ = classify_subcategory(category, slug, description)
    return f"skills/{category}/{subcategory}/{slug}/SKILL.md"


def subcategory_for_slug(category: str, slug: str, description: str = "") -> str:
    return classify_subcategory(category, slug, description)[0]
