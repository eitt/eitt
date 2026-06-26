---
name: brewery-conflict-corpus-builder
description: Search, collect, classify, and package news, scholarly literature, reports, and legal/policy documents about environmental conflicts and injustices involving craft or artisanal beer, breweries, and beer supply chains. Produces a ZIP corpus with PDF evidence files, metadata-only records for restricted sources, evidence tables, search logs, and a synthesis memo.
---

# Brewery Conflict Corpus Builder Skill

## Purpose

Use this skill to build a documented body of knowledge about environmental conflicts, racism, environmental injustice, water use, contamination, land-use disputes, gentrification, labor disputes, and other socio-environmental conflicts involving craft beer, artisanal breweries, microbreweries, industrial breweries, beer tourism, hops/barley supply chains, and brewery wastewater.

The skill must produce a reproducible research corpus, not a consumer guide to beer. It must not recommend breweries, beer products, alcohol consumption, or purchasing channels.

## Core outputs

Create one ZIP file containing:

1. `sources/` with saved PDFs or legally permissible page captures for news, scholarly papers, reports, legal documents, and policy documents. Restricted or non-open-access articles must be represented as metadata-only Markdown records rather than unauthorized full-text files.
2. `tables/conflict_evidence_table.csv` and, when spreadsheet tools are available, `tables/conflict_evidence_table.xlsx`.
3. `tables/source_inventory.csv` with every file captured and its metadata.
4. `search/search_log.md` with databases, query strings, filters, dates, and hit counts.
5. `bibliography/references.bib` and/or `bibliography/references.ris` when DOI or citation metadata is available.
6. `synthesis/knowledge_synthesis.md` summarizing patterns, gaps, cases, and recommended next searches.
7. `README.md` explaining methods, access limitations, file naming, and ethical/legal constraints.
8. `manifest.json` listing files, checksums, dates, source URLs, access status, and full-text access limitations.

## Required user inputs

Ask for missing items only when they affect retrieval or classification:

- Research question or topic focus.
- Geographic scope: global, country, region, city, watershed, or community.
- Time period.
- Languages to include.
- Source types: news, Scopus-indexed articles, open-access articles, NGO reports, legal cases, government documents, community statements.
- Whether the user has Scopus API access, institutional credentials, or exported Scopus CSV/RIS/BibTeX files.
- Whether to include only legally downloadable open-access full texts or also metadata-only records for paywalled papers.

Default assumptions when the user does not specify:

- Scope: global.
- Years: 2000 to present.
- Languages: English plus the user's working language when known.
- Output format: ZIP with CSV, Markdown, BibTeX/RIS, and PDFs/page captures.
- Evidence rule: download only open-access or otherwise legally accessible documents; for restricted sources, save metadata, abstract where allowed, DOI, citation, and landing-page capture.

## Access and copyright rules

Follow these rules strictly:

- Do not bypass paywalls, login walls, access controls, robots.txt, or database terms.
- Do not download full-text papers unless they are open access, licensed for download, provided by the user, or accessible through the user's legitimate institutional access and allowed by the license.
- For paywalled articles, collect citation metadata, DOI, abstract where legally available, keywords, and source link.
- For news pages, save a PDF/page capture only when permitted. If capture is blocked, save citation metadata and a short note explaining the limitation.
- Keep verbatim excerpts short. Use paraphrase for summaries. Store short quotations only when needed for evidence coding.
- Preserve source URLs and access dates for every item.

## Restricted and non-open-access article procedure

When a scholarly article is not open access, not legally downloadable, or available only behind a paywall or institutional login, do not download or store the full text. Instead:

1. Create a metadata-only record in `sources/metadata_only/` using the source ID and `.md` extension.
2. Save all legally available bibliographic metadata: title, authors, year, journal, volume, issue, pages, DOI, Scopus EID when available, publisher landing page, database source, keywords, abstract, and access date.
3. Fill `conflict_evidence_table.csv` using the title, abstract, keywords, and other visible metadata only. Do not infer detailed claims that are not supported by the abstract or metadata.
4. Set `full_text_access_status` to `restricted`, `paywalled`, `institutional_access_required`, or `unknown`, as appropriate.
5. Set `download_status` to `metadata_only_full_text_needed`.
6. Set `abstract_used_for_coding` to `yes` when the evidence row is coded from the abstract.
7. Set `full_text_needed` to `yes` when the abstract is insufficient for detailed evidence extraction, confirmation of methods, affected groups, legal outcomes, severity, or direct quotations.
8. In `notes`, state clearly: `Full text not downloaded; table coding is based on metadata and abstract only. Full text access is needed for confirmation.`
9. Do not create a PDF placeholder that could be mistaken for the full article. The file path should point to the metadata-only Markdown record.

Use confidence level `low` or `medium` for abstract-only coding unless the abstract gives direct and specific evidence about the conflict, affected group, mechanism, and outcome. Never mark abstract-only records as `high` confidence unless the abstract itself contains sufficient evidence and the limitation is stated.

## Search strategy

### Concept blocks

Build searches from four blocks: industry, conflict, injustice, and environmental mechanism.

Industry terms:

- brewery OR breweries
- craft beer OR craft brewery OR microbrewery OR brewpub
- artisanal beer OR independent brewery
- beer industry OR brewing industry
- hops OR barley OR malt OR brewing wastewater

Conflict terms:

- conflict OR dispute OR opposition OR protest OR lawsuit OR complaint
- community resistance OR public hearing OR zoning dispute
- environmental conflict OR socio-environmental conflict
- environmental justice OR environmental injustice

Injustice terms:

- racism OR environmental racism
- Indigenous rights OR tribal rights OR First Nations
- procedural injustice OR distributive injustice OR recognitional injustice
- displacement OR gentrification OR exclusion
- labor exploitation OR worker safety

Environmental mechanism terms:

- water use OR water consumption OR groundwater OR aquifer
- wastewater OR effluent OR sewage OR treatment plant
- pollution OR contamination OR odor OR noise OR traffic
- drought OR scarcity OR watershed
- land use OR zoning OR industrial expansion
- energy use OR emissions OR solid waste OR packaging

### Example Boolean searches

Use these as starting points, then adapt by geography and language:

```text
("craft brewery" OR microbrewery OR brewpub OR "artisanal beer") AND ("environmental justice" OR "environmental racism" OR conflict OR dispute OR protest) AND (water OR wastewater OR contamination OR zoning)
```

```text
(brewery OR breweries OR "beer industry") AND ("water use" OR groundwater OR aquifer OR drought OR wastewater) AND (community OR residents OR Indigenous OR racism OR injustice)
```

```text
("brewing wastewater" OR "brewery effluent") AND (pollution OR contamination OR regulation OR complaint OR treatment)
```

```text
("craft beer" OR brewery) AND (gentrification OR displacement OR zoning OR "land use") AND (neighborhood OR residents OR community)
```

### Scopus route, when available

When the user provides Scopus API credentials, institutional access, or a Scopus export:

1. Use Scopus Search API or the user-provided export to retrieve records.
2. Prefer metadata fields: title, authors, year, source title, abstract, author keywords, index keywords, DOI, EID, affiliation country, citation count, document type, and source link.
3. Retrieve abstracts and citation metadata when allowed.
4. Use DOI or publisher links to locate legal open-access full text through open-access routes.
5. Do not assume Scopus gives legal access to full text. Treat Scopus primarily as metadata and abstract discovery unless full-text access is explicitly available and permitted.

When Scopus is not available, use open scholarly sources and metadata services available in the environment, such as Crossref, OpenAlex, PubMed when relevant, DOAJ, institutional repositories, government repositories, and publisher open-access pages.

### News and public-source route

Search:

- local and regional newspapers;
- national news;
- trade press only when useful for factual chronology, not promotional claims;
- government regulatory pages;
- court or administrative hearing records;
- environmental agencies;
- community organizations and NGOs;
- planning, zoning, and watershed authority records.

Prioritize sources that document a conflict, grievance, regulatory event, lawsuit, community claim, or measured environmental impact.

## Relevance criteria

Include an item when it satisfies at least two of the following:

- It concerns beer, brewing, breweries, brewery supply chains, hops, barley, malt, brewing wastewater, brewery siting, or beer tourism.
- It documents a conflict, grievance, protest, lawsuit, regulatory violation, planning dispute, or public controversy.
- It identifies an affected community, worker group, Indigenous group, racialized community, watershed, neighborhood, or regulatory agency.
- It includes environmental or justice mechanisms: water use, pollution, land-use change, gentrification, labor conditions, wastewater, emissions, odor, noise, traffic, unequal exposure, or unequal participation.
- It provides empirical data, legal evidence, public testimony, official records, or scholarly analysis.

Exclude consumer reviews, beer ratings, brewery rankings, promotional pages, event announcements, tasting notes, and sales pages unless they directly document a conflict or policy dispute.

## Corpus folder structure

Create the output directory as:

```text
brewery_conflict_corpus_YYYYMMDD/
  README.md
  manifest.json
  search/
    search_log.md
    query_strings.txt
  sources/
    news/
    scholarly/
    reports/
    legal_policy/
    metadata_only/
  tables/
    conflict_evidence_table.csv
    source_inventory.csv
    deduplication_log.csv
    access_status_log.csv
  bibliography/
    references.bib
    references.ris
  synthesis/
    knowledge_synthesis.md
    gap_analysis.md
```

## File naming convention

Use stable, readable IDs:

```text
SOURCECATEGORY_YEAR_COUNTRY_SHORTTITLE_ID.pdf
```

Examples:

```text
NEWS_2024_US_brewery-water-dispute_N001.pdf
ARTICLE_2021_GLOBAL_brewing-wastewater-treatment_A004.pdf
LEGAL_2019_CA_zoning-complaint-brewery_L002.pdf
REPORT_2023_MX_water-scarcity-brewing_R003.pdf
ARTICLE_2022_GLOBAL_restricted-water-conflict_A005.md
```

For metadata-only records, create a Markdown file in `sources/metadata_only/` with the same ID and `.md` extension.

## Evidence table schema

Use the following columns for `conflict_evidence_table.csv`:

- record_id
- source_id
- source_type
- title
- authors_or_organization
- publication_year
- publication_date
- outlet_or_journal
- country
- region_city_watershed
- geographic_coordinates_if_available
- brewery_or_actor
- affected_group
- conflict_type
- injustice_type
- environmental_mechanism
- water_issue
- racism_or_discrimination_dimension
- supply_chain_stage
- evidence_summary
- short_supporting_excerpt
- methods_or_evidence_type
- outcome_or_status
- legal_or_policy_response
- severity_level
- confidence_level
- doi
- source_url
- pdf_or_capture_path
- full_text_access_status
- download_status
- abstract_available
- abstract_used_for_coding
- full_text_needed
- full_text_request_note
- access_date
- notes

For restricted scholarly articles, fill the row from metadata and abstract only when the abstract is legally visible. Leave detailed fields as `unclear` when the abstract does not support them. The `pdf_or_capture_path` must point to the metadata-only Markdown record, and `notes` must state that full-text access is needed for confirmation.

## Controlled vocabulary

### source_type

- scholarly_article
- news
- government_record
- legal_case
- ngo_report
- community_statement
- industry_report
- thesis_or_dissertation
- metadata_only

### full_text_access_status

- open_access
- legally_downloaded
- user_provided
- institutional_access_permitted
- restricted
- paywalled
- institutional_access_required
- abstract_only
- landing_page_only
- unknown

### download_status

- pdf_downloaded
- page_capture_saved
- html_saved
- metadata_only_full_text_needed
- metadata_only_capture_blocked
- metadata_only_no_abstract
- user_file_saved
- not_retrievable

### conflict_type

- water_extraction_or_competition
- wastewater_or_effluent
- contamination_or_pollution
- land_use_or_zoning
- gentrification_or_displacement
- labor_or_worker_safety
- indigenous_rights_or_land_rights
- public_health
- odor_noise_or_traffic
- climate_energy_or_emissions
- supply_chain_agriculture
- regulatory_noncompliance
- other

### injustice_type

- distributive_injustice
- procedural_injustice
- recognitional_injustice
- environmental_racism
- indigenous_rights_violation
- economic_exclusion
- labor_injustice
- cumulative_burden
- unclear_or_not_applicable

### environmental_mechanism

- water_use
- groundwater_depletion
- surface_water_withdrawal
- wastewater_discharge
- effluent_treatment
- chemical_contamination
- organic_load_or_bod_cod
- odor
- noise
- traffic
- solid_waste
- agricultural_inputs
- energy_use_or_emissions
- land_conversion
- unclear

### severity_level

- low
- moderate
- high
- severe
- unknown

### confidence_level

- high: multiple reliable sources or strong official/scholarly evidence
- medium: one reliable source with sufficient detail
- low: partial evidence, unclear causality, or unverified allegation

## Processing workflow

1. Clarify scope and access.
2. Build query strings from the concept blocks.
3. Search scholarly sources first, then news/public records.
4. Log every query, date, database/source, filters, and hit counts.
5. Screen titles and snippets for relevance.
6. Deduplicate by DOI, title similarity, URL, and source date.
7. Download or capture legally permissible source files.
8. For non-open-access or restricted scholarly articles, create metadata-only records, collect available abstracts, and flag `full_text_needed=yes` when the full text is required for confirmation.
9. Extract metadata and short evidence summaries. For abstract-only records, limit evidence extraction to what is supported by the abstract and visible metadata.
10. Code each record using the controlled vocabulary.
11. Create the evidence table and source inventory.
12. Write a synthesis memo:
    - main conflict types;
    - affected communities;
    - water and environmental mechanisms;
    - racial, Indigenous, class, or procedural justice dimensions;
    - strongest evidence;
    - weak or uncertain evidence;
    - research gaps;
    - recommended next searches.
13. Generate `manifest.json` with file paths, source URLs, access dates, access status, and checksums.
14. Compress the corpus directory into a ZIP file.
15. Report limitations clearly.

## PDF/page-capture instructions

For each source:

- Prefer direct PDF downloads only when legal and available.
- For web pages, use a browser print-to-PDF or page-capture workflow when allowed.
- If PDF capture fails, save the HTML or create a metadata-only Markdown record.
- Verify that every PDF opens and corresponds to the source table entry.
- For restricted articles, do not attempt PDF capture unless the user supplies the file or legitimate access explicitly permits download. Save a metadata-only Markdown record instead.
- Do not use OCR unless the source is scanned and no machine-readable text is available.

## Quality checks before delivery

Before returning the ZIP:

- Confirm that every table row has a `source_id` and a matching file or metadata-only record.
- Confirm that every saved file appears in `manifest.json`.
- Confirm that `source_url`, `access_date`, and `pdf_or_capture_path` are filled whenever available.
- Confirm that no consumer-purchase, tasting, rating, or promotional beer content is included unless directly tied to a documented conflict.
- Confirm that paywalled full texts are not included unless supplied by the user or legally accessible.
- Confirm that every restricted or paywalled article has a metadata-only record, access status, download status, and full-text-needed note.
- Confirm that every abstract-only row has `abstract_used_for_coding=yes` and `full_text_needed=yes` when additional evidence is required.
- Confirm that the synthesis distinguishes documented facts from allegations and interpretations.
- Confirm that racism, injustice, and affected-group claims are supported by source evidence and not inferred without basis.

## Final response format

Return:

```text
Created: brewery_conflict_corpus_YYYYMMDD.zip
Contents: [brief list]
Key table: tables/conflict_evidence_table.csv
Search log: search/search_log.md
Limitations: [brief access/copyright/search limitations, including number of metadata-only records requiring full-text access]
```

Include the ZIP download link and, when useful, a short explanation of how many records were collected by source type.
