---
id: infrastructure
type: term
title: Infrastructure
status: review
created: '2026-09-22'
updated: '2026-09-22'
sources:
- '[[SRC-021-section-7-content]]'
related:
- '[[hardware]]'
- '[[deployment-view]]'
term: Infrastructure
aliases:
- Technical infrastructure
legacy-tags:
- infrastructure
home: '[[section-7]]'
---

**Definition.** Everything the system runs on and communicates over: the machines, the channels
between them, and the environments they are grouped into.

**In arc42.** The subject of section 7. [[tip-7-1]] enumerates it — "nodes, i.e. processors,
server, cluster… and their relations (channels), i.e. bus, network or wireless connections…
additional hardware elements, i.e. firewall, router, switches, storage" — and [[tip-7-3]] adds the
dimension that is easy to forget: the same system usually runs in several environments (DEV, CI,
TEST, PROD) whose differences are themselves worth documenting. [[tip-7-9]] is about everything
the infrastructure needs before it can carry a release at all: accounts, directories, databases,
middleware, certificates, firewall rules — and its advice is to automate rather than describe.

**Distinguish from.** [[hardware]] — the physical machines are part of the infrastructure, but
environments, networks and the middleware of [[tip-7-9]] are infrastructure that is not hardware.
[[deployment-view]] — the infrastructure is the thing; the deployment view is the description of
it together with the mapping of software onto it.
