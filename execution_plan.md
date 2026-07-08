# 🌊 Fisherman OS — Execution Plan & MVP Roadmap
## From Idea to National Platform: A Phased Blueprint

---

## 1. Product Vision

**One-liner:** The intelligence layer between the ocean and the fisherman — delivered on WhatsApp.

**Full Vision:** Fisherman OS transforms every artisanal fisherman's smartphone into a marine operations center by delivering hyperlocal weather forecasts, fish zone recommendations, real-time market prices, and safety features through a WhatsApp bot in their native language.

---

## 2. MVP Definition (Ship in 8 Weeks)

### What the MVP IS:
A WhatsApp bot (number: +91-XXX-FISHHELP) that serves fishermen in **South Goa** (41 marine villages, ~2,758 active fishermen) with:

#### Feature 1: Morning Forecast (Auto-push at 3:30 AM daily)
```
🌊 Fisherman OS — Betul
📅 8 July 2026 | 3:30 AM

☀️ Today's Sea: 🟢 SAFE TO GO

🌬️ Wind: 12 km/h SW
🌊 Waves: 0.8m (calm)
🌧️ Rain: 20% chance after 2PM
🌡️ Sea temp: 28.5°C

⚠️ Return before 2PM — afternoon squall risk

Next 6 hours: 🟢🟢🟢🟡🟡🟡

Type "1" for detailed forecast
Type "2" for market prices
Type "SOS" for emergency
```

#### Feature 2: Market Prices (On-demand or auto-push at 5 AM)
```
🐟 Today's Fish Prices (7 July closing)

📍 Betul Landing: 
   Mackerel ₹85/kg | Pomfret ₹320/kg | Prawns ₹280/kg

📍 Cutbona Harbor:
   Mackerel ₹95/kg | Pomfret ₹350/kg | Prawns ₹310/kg

📍 Margao Fish Market:
   Mackerel ₹110/kg | Pomfret ₹380/kg | Prawns ₹340/kg

💡 TIP: Margao paying 29% more for mackerel today

Type "PRICES" anytime for latest
```

#### Feature 3: SOS Distress (Always active)
```
User sends: SOS

Bot responds:
🚨 EMERGENCY ACTIVATED
📍 Your location: [GPS coordinates]
📞 Coast Guard: 1554 (calling...)
👥 Your emergency contacts notified
🔄 Location sharing: ON (every 5 min)

Stay calm. Help is being coordinated.
Reply CANCEL to deactivate.
```

### What the MVP is NOT:
- ❌ No fish zone predictions (Phase 2)
- ❌ No catch logging or data flywheel (Phase 2)
- ❌ No AI/ML predictions (Phase 3)
- ❌ No hardware (DAT integration — Phase 4)
- ❌ No Android app (WhatsApp-only for now)

### MVP Success Criteria:
| Metric | Target |
|:---|:---|
| Registered fishermen | 500 in 8 weeks |
| Daily active users (open morning forecast) | 60% of registered |
| SOS activations | Track all (even 1 life saved = validation) |
| Price-driven market switching | 20% of users change selling destination based on bot data |
| Willingness to pay (₹99/month) | 15% conversion from free trial |
| NPS Score | >50 |

---

## 3. Technical Architecture (MVP)

### System Diagram
```
┌─────────────────────────────────────────────────────────┐
│                    DATA SOURCES                          │
├──────────┬──────────┬───────────┬───────────────────────┤
│ INCOIS   │ IMD      │ FMPIS/    │ Manual Price          │
│ PFZ/OSF  │ Weather  │ CMFRI     │ Collection            │
│ API/RSS  │ API      │ Fish Watch│ (field agents)        │
└─────┬────┴─────┬────┴─────┬─────┴──────────┬────────────┘
      │          │          │                │
      ▼          ▼          ▼                ▼
┌─────────────────────────────────────────────────────────┐
│              FISHERMAN OS BACKEND                        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────────┐ │
│  │ Weather  │ │ Price    │ │ SOS      │ │ User       │ │
│  │ Service  │ │ Service  │ │ Service  │ │ Management │ │
│  └──────────┘ └──────────┘ └──────────┘ └────────────┘ │
│  ┌──────────┐ ┌──────────┐ ┌──────────────────────────┐ │
│  │ Message  │ │ Scheduler│ │ Translation / Localization│ │
│  │ Composer │ │ (CRON)   │ │ (Konkani/Marathi/Hindi)  │ │
│  └──────────┘ └──────────┘ └──────────────────────────┘ │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│           WhatsApp Business API (via Gupshup/Wati)      │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              FISHERMEN (WhatsApp Users)                   │
│  📱 Rajesh (Betul)  📱 Suresh (Cutbona)  📱 Ravi (...)  │
└─────────────────────────────────────────────────────────┘
```

### Tech Stack (MVP)
| Component | Technology | Cost |
|:---|:---|:---|
| **Backend** | Node.js / Python (FastAPI) on Railway/Render | Free tier → $5/mo |
| **Database** | PostgreSQL (Supabase free tier) | Free |
| **WhatsApp API** | Gupshup or Wati BSP | ₹0.50-1.00 per message |
| **Weather Data** | INCOIS RSS/API + IMD API (free/govt) | Free |
| **Price Data** | FMPIS API + manual collection (initially) | ₹5,000/mo (field agent) |
| **Hosting** | Vercel/Railway | Free → $20/mo |
| **Scheduler** | Cron jobs (built-in) | Free |
| **Monitoring** | Sentry free tier | Free |

**Total MVP cost: ~₹15,000-20,000/month** (excluding team salaries)

### Data Sources — Detailed

#### Weather & Sea State
| Source | Data | Resolution | Access |
|:---|:---|:---|:---|
| INCOIS Ocean State Forecast | Wave height, swell, wind, SST | 12km grid | Free API/RSS |
| IMD | Rainfall, cyclone warnings | District-level | Free API |
| ISRO Oceansat-3 | SST, chlorophyll | 1km | Free (NRSC portal) |
| OpenWeatherMap | Backup weather data | Point-level | Free tier (1000 calls/day) |

#### Market Prices
| Source | Data | Update Frequency | Access |
|:---|:---|:---|:---|
| FMPIS (NFDB) | Wholesale/retail prices at landing centers | Daily | Web scraping / API |
| CMFRI Fish Watch | Auction prices at major harbors | Daily | Web scraping |
| Field agents | Manual price collection from 3 Goa landing centers | Daily by 5 AM | ₹5,000/mo stipend |

---

## 4. Phased Implementation Roadmap

### Phase 1: Goa MVP (Months 1-4)

#### Month 1-2: Foundation
| Week | Task | Deliverable |
|:---|:---|:---|
| 1 | Register WhatsApp Business Account + setup BSP (Gupshup) | Verified WhatsApp number |
| 1 | Set up backend (FastAPI + PostgreSQL + Supabase) | Working API server |
| 2 | Build INCOIS/IMD data pipeline | Weather data ingestion running |
| 2 | Build message composer (Konkani + English templates) | Message templates approved by WhatsApp |
| 3 | Build scheduled push system (3:30 AM daily forecast) | Auto-push working |
| 3 | Recruit field agent in Betul for manual price collection | Price data pipeline |
| 4 | Build SOS system (location sharing + ICG 1554 call trigger) | SOS flow working |
| 4 | Build onboarding flow (new user registration via WhatsApp) | User can register by sending "Hi" |
| 5-6 | Internal testing + bug fixing | Stable system |
| 7-8 | Field pilot with 50 fishermen in Betul village | Real user feedback |

#### Month 3-4: Goa Rollout
| Task | Details |
|:---|:---|
| Visit 15 of 41 Goa fishing villages | On-ground onboarding camps |
| Partner with 3-5 fishing cooperatives | Cooperative-led distribution |
| Target: 500 registered users | Track DAU, retention, SOS usage |
| Collect user feedback | Iterate on message format, timing, language |
| Begin manual catch data collection | Paper forms → digitize (prep for Phase 2) |
| Apply for PMMSY grant | Government funding application |

**Key Milestones:**
- [ ] 500 registered fishermen
- [ ] 60% daily forecast open rate
- [ ] First SOS activation and successful response
- [ ] 15% willingness to pay (₹99/month)
- [ ] Partnership with Goa Fisheries Department

---

### Phase 2: Kerala Expansion + Fish Zones (Months 5-10)

#### New Features
| Feature | Description |
|:---|:---|
| **PFZ Integration** | Overlay INCOIS PFZ advisories on simple WhatsApp map images. "Best fishing zone today: 12km SW of Betul" |
| **Catch Logging** | Fishermen reply "CATCH mackerel 50kg" and bot logs species, quantity, location, time |
| **Crowd-Sourced Zones** | "3 fishermen reported good catches near [zone]. Try heading there today" |
| **Voice Messages** | Accept voice input in Malayalam/Konkani. Process with Whisper/Bhashini ASR |
| **Vernacular Expansion** | Add Malayalam for Kerala, Kannada for Karnataka coast |

#### Kerala-Specific Data
- Kerala: 222 marine fishing villages, ~1.2 lakh active fishermen
- 775 fishing worker deaths (2011-2024) — strongest safety case
- Highest smartphone penetration among fishing communities
- Strong cooperative system (Matsyafed)

#### Technical Additions
| Component | Technology | Purpose |
|:---|:---|:---|
| **ISRO SST/Chlorophyll data** | NRSC Bhuvan portal API | Fish zone prediction |
| **Map generation** | Mapbox/Leaflet static map API | Generate fishing zone images for WhatsApp |
| **Speech-to-text** | Bhashini API (govt, free) or Whisper | Voice message processing |
| **ML Model v1** | Simple correlation: SST + Chlorophyll → likely species | Basic prediction |

**Key Milestones:**
- [ ] 10,000 registered fishermen (Goa + Kerala)
- [ ] Catch logging: 500+ entries/week
- [ ] First ML-assisted fish zone recommendation
- [ ] Matsyafed (Kerala) cooperative partnership
- [ ] PMMSY grant awarded
- [ ] Revenue: ₹1L/month (B2C subscriptions)

---

### Phase 3: Multi-State Scale + AI (Months 11-18)

#### Geographic Expansion
| State | Villages | Active Fishermen | Language |
|:---|:---|:---|:---|
| Tamil Nadu | 573 | ~2.5 lakh | Tamil |
| Andhra Pradesh | 555 | ~1.6 lakh | Telugu |
| Karnataka | 144 | ~30,000 | Kannada |
| Maharashtra | 456 | ~1.2 lakh | Marathi |

#### New Features
| Feature | Description |
|:---|:---|
| **AI Fish Zone Predictions** | ML model trained on 6+ months of crowd-sourced catch data + satellite data |
| **Route Optimization** | "Optimal route to fishing zone. Est. fuel: 18L. Est. time: 45 min" |
| **Fuel Cost Calculator** | Daily fuel price × recommended route = trip cost estimate |
| **Insurance Integration** | Partner with PMSBY/fisherman insurance schemes for one-click claims |
| **Community Rankings** | Gamification — "Top contributor this week: Rajesh (Betul)" |

#### Technical Additions
| Component | Technology |
|:---|:---|
| **ML Pipeline** | Python (scikit-learn → TensorFlow Lite) for fish zone prediction |
| **Data Lake** | AWS S3 or Google Cloud Storage for satellite + catch data |
| **Analytics Dashboard** | Metabase/Grafana for internal KPI tracking |
| **API Platform** | Serve fish zone predictions as API for third-party integrations |

**Key Milestones:**
- [ ] 100,000 registered fishermen
- [ ] AI model accuracy: 70%+ on fish zone prediction
- [ ] Revenue: ₹15L/month (B2C + B2B + B2G)
- [ ] 3 state fisheries department contracts
- [ ] Carbon credit pilot (quantified fuel savings)

---

### Phase 4: National Platform + Hardware (Months 19-30)

#### Features
| Feature | Description |
|:---|:---|
| **ISRO DAT-SG Integration** | Receive distress signals from DAT devices, relay to Coast Guard |
| **Family Tracker** | Families can track boat location via WhatsApp |
| **B2B Supply Chain** | Connect fishermen directly to restaurants/retailers (disintermediate the middleman) |
| **Credit Scoring** | Catch history → creditworthiness → microfinance access |
| **Companion Android App** | Lightweight app for fishermen who want offline maps and GPS |
| **Climate Dashboard** | Government dashboard showing fleet-wide fuel savings, catch patterns, safety metrics |

**Key Milestones:**
- [ ] 500,000 registered fishermen
- [ ] All coastal states covered (9 states + 4 UTs)
- [ ] Revenue: ₹1.5Cr/month
- [ ] Series A fundraise or self-sustaining via government contracts
- [ ] Carbon credit revenue stream active
- [ ] National Fisheries Digital Platform integration

---

## 5. Team Requirements

### Phase 1 (MVP) — 3-4 people
| Role | Responsibility | Monthly Cost |
|:---|:---|:---|
| **Full-Stack Developer** | Backend, WhatsApp API integration, data pipelines | ₹80,000 |
| **Product/Founder** | Product design, user research, cooperative partnerships | ₹0 (equity) |
| **Field Operations** | On-ground onboarding, price collection, fisherman relationships | ₹25,000 |
| **Part-time Designer** | WhatsApp message templates, branding | ₹15,000 |

### Phase 2 (Scale) — Add 3-4 more
| Role | Addition |
|:---|:---|
| **ML Engineer** | Fish zone prediction models |
| **Regional Field Ops (Kerala)** | Malayalam-speaking field agent |
| **Data Analyst** | Catch data analysis, dashboard |
| **Government Relations** | PMMSY grants, state partnerships |

---

## 6. Budget & Funding

### Phase 1 Budget (4 months)
| Item | Monthly | Total (4 mo) |
|:---|:---|:---|
| Team salaries | ₹1,20,000 | ₹4,80,000 |
| WhatsApp API (Gupshup) | ₹15,000 | ₹60,000 |
| Server/hosting | ₹2,000 | ₹8,000 |
| Field operations (travel, camps) | ₹30,000 | ₹1,20,000 |
| Miscellaneous | ₹10,000 | ₹40,000 |
| **Total** | **₹1,77,000** | **₹7,08,000** |

### Funding Strategy
| Stage | Source | Amount |
|:---|:---|:---|
| Pre-seed | Founder bootstrapping + friends/family | ₹5-10L |
| Seed | Social impact grants (Niti Aayog, BIRAC, Villgro) | ₹25-50L |
| Grant | PMMSY (Govt of India fisheries scheme) | ₹15-25L |
| Series Seed | Impact investors (Omidyar, Aavishkaar, Unitus) | ₹1-2Cr |

---

## 7. Go-to-Market Strategy

### Beachhead: South Goa (Why Goa First)

| Factor | Why Goa |
|:---|:---|
| **Small, manageable** | 41 villages, 2,758 active fishermen. Can cover on foot in 2 weeks |
| **High smartphone penetration** | Tourism economy = better digital infrastructure |
| **Cooperative system** | 21% of fishermen in cooperatives. Ready distribution channel |
| **Bilingual** | Konkani + English. Easier to start than Tamil/Malayalam |
| **Government access** | Small state bureaucracy. Easier to get Fisheries Dept meeting |
| **Media attention** | Goa is well-covered. Success story here gets national press |

### Distribution Channels

```
                    ┌─────────────────────┐
                    │   Fisherman OS Bot   │
                    │   (WhatsApp Number)  │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
    ┌─────────▼──────┐ ┌──────▼────────┐ ┌─────▼──────────┐
    │  Cooperatives  │ │  Village      │ │  Government    │
    │  (bulk onboard)│ │  Champions    │ │  Fisheries Dept│
    │                │ │  (1 per       │ │  (mandate/     │
    │  21% of Goa    │ │  village)     │ │  recommend)    │
    │  fishermen     │ │              │ │                │
    └────────────────┘ └──────────────┘ └────────────────┘
```

### Onboarding Flow
1. Cooperative president demonstrates bot at village meeting
2. Fisherman saves number → sends "Hi"
3. Bot asks: Name, Village, Boat type (3 messages)
4. Bot sends first forecast immediately
5. Fisherman shares number with crew via WhatsApp (viral)

### Growth Loops
1. **Cooperative viral loop:** President onboards → members onboard → neighboring cooperative hears about it
2. **Catch logging gamification:** Top contributors get featured → social status → more participation
3. **Life-saved PR:** Every SOS rescue = media story = thousands of organic signups
4. **Government mandate:** State Fisheries Dept makes it official tool = mandatory adoption

---

## 8. Revenue Model

| Stream | Description | Phase | Revenue Potential |
|:---|:---|:---|:---|
| **B2C Subscription** | ₹99/month per fisherman (after free trial) | Phase 1+ | ₹2.97Cr/year at 25K users |
| **B2G Contracts** | State Fisheries Dept pays per-user license | Phase 2+ | ₹50L-2Cr per state/year |
| **B2B Data Licensing** | Anonymized catch + zone data sold to research orgs, FAO | Phase 3+ | ₹25-50L/year |
| **Carbon Credits** | Quantified fuel savings → Verified Carbon Units | Phase 3+ | ₹10-30L/year |
| **Supply Chain Commission** | Connect fishermen to direct buyers (1-2% transaction fee) | Phase 4+ | High upside |

---

## 9. Key Metrics & KPIs

| Category | Metric | Target (Phase 1) |
|:---|:---|:---|
| **Adoption** | Registered users | 500 |
| **Engagement** | DAU / Registered | 60% |
| **Retention** | 30-day retention | 70% |
| **Safety** | SOS activations | Track all |
| **Economic** | % users who switch market based on price data | 20% |
| **Data** | Catch logs per week | 100+ |
| **Revenue** | Paying users (₹99/month) | 15% of registered |
| **Virality** | Referrals per user | 2+ |

---

## 10. Regulatory & Partnership Landscape

### Key Government Partners
| Entity | Role | How to Engage |
|:---|:---|:---|
| **INCOIS (Hyderabad)** | Data provider (PFZ, OSF) | MoU for data access |
| **ISRO/NRSC** | Satellite data (SST, chlorophyll) | NRSC Bhuvan API registration |
| **Dept of Fisheries (Goa)** | State endorsement + funding | Present at Fisheries Board meeting |
| **CMFRI (Kochi)** | Research partner + validation | Academic collaboration |
| **Indian Coast Guard** | SOS response integration | Pilot proposal for ICG Region 11 (Goa) |
| **NFDB (Hyderabad)** | FMPIS data + PMMSY funding | Apply through state fisheries dept |

### Regulatory Considerations
| Area | Requirement |
|:---|:---|
| **WhatsApp Business** | Green tick verification. Message template approval by Meta |
| **Data Privacy** | Location data handling. DPDP Act 2023 compliance |
| **Emergency Services** | Clear disclaimer that SOS is supplementary, not replacement for 1554 |
| **Financial** | If charging, GST registration required after ₹20L annual threshold |

---

## 11. Immediate Next Steps (This Week)

| # | Action | Owner | Timeline |
|:---|:---|:---|:---|
| 1 | Register on Gupshup/Wati for WhatsApp Business API access | Tech | Day 1-3 |
| 2 | Register on INCOIS portal for PFZ/OSF data feeds | Tech | Day 1-3 |
| 3 | Identify and contact 3 fishing cooperatives in South Goa | Field | Day 1-7 |
| 4 | Build basic backend + INCOIS data pipeline | Tech | Week 1-2 |
| 5 | Design message templates (Konkani/English) and submit to WhatsApp | Design | Week 1-2 |
| 6 | Visit Betul fishing village — talk to 10 fishermen (Mom Test) | Founder | Week 1 |
| 7 | Recruit field agent in South Goa (part-time, ₹5,000/month) | Founder | Week 1-2 |
| 8 | Set up Supabase database schema (users, messages, prices, catches) | Tech | Week 2 |
| 9 | Build and test morning forecast push system | Tech | Week 3-4 |
| 10 | Soft launch with 50 fishermen in Betul | Team | Week 7-8 |

---

## 12. What Success Looks Like

### In 3 months:
> 500 fishermen in Goa check their Fisherman OS forecast every morning before heading out. 3 fishermen have been saved by the SOS feature. Average fuel savings: ₹500/trip. 15% are paying ₹99/month.

### In 12 months:
> 25,000 fishermen across Goa and Kerala. Catch logging creates the first crowd-sourced fish migration dataset in India. Matsyafed Kerala signs a ₹50L annual contract. PMMSY grant awarded.

### In 3 years:
> 100,000+ fishermen. AI-powered fish zone predictions with 75% accuracy. Government contracts in 4 states. Carbon credits generating secondary revenue. The phrase "Check Fisherman OS" becomes as common as "Check WhatsApp" in coastal India.

---

> **The ocean doesn't care about your plan. But 4 million fishermen desperately need one.**
> **Let's build the bridge between ISRO's satellites and Rajesh's boat.**
