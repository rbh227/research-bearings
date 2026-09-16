# Datasets: <the question>

<!-- Written by the dataset-scout agent, at research/landscape/datasets.md.
     One row per dataset the cards name, filled from the host record and from
     quoted passages of the papers. Four headings, fixed.

     Every fact here is either on a host record or quoted from a paper. A fact
     that is on neither is written as
     `could not determine, checked <hosts>` — never guessed, because /audit
     and /baseline read this file and act on it. -->

## Datasets

<!-- One ### per dataset, most-used first.

     ### <name>
     - Size: <images / scenes / polygons, with units> — <source>
     - Modality: <optical, SAR, multispectral, video, text…> — <source>
     - Resolution and scale: <ground sample distance, altitude, or the
       equivalent for a non-imagery dataset> — <source>
     - Geography: <where the data was collected> — <source>
     - Annotation: <what a label is, and who made it> — <source>
     - Split protocol: <how the standard split is constructed, quoted where
       the paper states it> — <source>
     - License: <spdx or the host's string, or `could not determine, checked
       huggingface, github`>
     - Host: <url> — <stars / downloads / last update>
     - Who uses it: <card slug>, <card slug>
     - Known flaws: <one line each, each with the card or passage it came from>
     - Leakage of the standard split: <what the split does about spatial,
       temporal and group overlap, quoted; or `not assessed — /audit a card
       that uses it`>

     `<source>` is `host: <url>`, or `<card slug> §<section>`, or
     `could not determine, checked <what>`. Every line carries one. -->

## Named but not found

<!-- Datasets the cards name that neither host returned, one per line, with
     the query that was run and both hosts named. A dataset can be real and
     absent from both: many remote-sensing benchmarks are distributed from a
     university page. This block says where to look next, and it is the only
     shape an absence claim takes in this file. -->

## What was searched

<!-- One line per dataset: the name as queried, the context appended to the
     GitHub query, rows returned per host, and the date. Then the key states:
     HF_TOKEN present or not, GITHUB_TOKEN present or not, and what that
     changed about the rate limit. -->

## Status

<!-- Date. Cards read, datasets named, rows written, rows with at least one
     `could not determine` line. Web search was not used and is not available
     to this agent. -->
