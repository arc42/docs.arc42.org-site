---
layout: default
title: Home
order: 0
permalink: /home/
---
<div align="center">
	<a href="https://u24.gov.ua/">
		<img src="https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner2-direct.svg">
	</a>
	<br>
</div>    

{% assign nr_sec01_tips = site.posts | where: "category", "requirements" | size %}
{% assign nr_sec02_tips = site.posts | where: "category", "constraints" | size %}
{% assign nr_sec03_tips = site.posts | where: "category", "context" | size %}
{% assign nr_sec04_tips = site.posts | where: "category", "solution-strategy" | size  %}
{% assign nr_sec05_tips = site.posts | where: "category", "building-block" | size %}
{% assign nr_sec06_tips = site.posts | where: "category", "runtime" | size %}
{% assign nr_sec07_tips = site.posts | where: "category", "deployment" | size %}
{% assign nr_sec08_tips = site.posts | where: "category", "concepts" | size %}
{% assign nr_sec09_tips = site.posts | where: "category", "decisions" | size %}
{% assign nr_sec10_tips = site.posts | where: "category", "quality" | size %}
{% assign nr_sec11_tips = site.posts | where: "category", "risks" | size %}
{% assign nr_sec12_tips = site.posts | where: "category", "glossary" | size %}



Check out  **[ practical tips](/keywords)** for using arc42, organized by template sections:

1. [**Introduction and goals**](/section-1/): Requirements, stakeholder, (top) quality goals ({{ nr_sec01_tips }} tips)
2. [**Constraints**](/section-2/): Technical and organizational constraints, conventions ({{ nr_sec02_tips }} tips)
3. [**Context and scope**](/section-3/): Business and technical context, external interfaces ({{ nr_sec03_tips }} tips)
4. [**Solution strategy**](/section-4/): Fundamental solution decisions and ideas ({{ nr_sec04_tips }} tips)
5. [**Building block view**](/section-5/): Abstractions of source code, black-/whiteboxes ({{ nr_sec05_tips }} tips)
6. [**Runtime view**](/section-6/): Runtime scenarios: How do building blocks interact ({{ nr_sec06_tips }} tips)
7. [**Deployment view**](/section-7/): Hardware and technical infrastructure, deployment ({{ nr_sec07_tips }} tips)
8. [**Crosscutting concepts**](/section-8/): Recurring solution approaches and patterns ({{ nr_sec08_tips }} tips)
9. [**Architecture decisions**](/section-9/): Important decisions ({{ nr_sec09_tips }} tips)
10. [**Quality**](/section-10/): Quality tree and quality scenarios ({{ nr_sec10_tips }} tips)
11. [**Risks and technical debt**](/section-11/): Known problems, risks and technical debt ({{ nr_sec11_tips }} tips)
12. [**Glossary**](/section-12/): Definitions of important business and technical terms ({{ nr_sec12_tips }} tips)


>Our tips are tagged by [**{{ site.tags.size }} keywords**](/keywords) that will help you navigate. Three of these stand out:
>
>* **[<font color="#dd354b">lean</font>](/keywords/#lean)**: You are looking for opportunities to shorten or  streamline your documentation pragmatically. You want to reduce efforts without loosing content or value. You are working in an agile environment and want to have lightweight documentation – based on the motto: _travel light_.
>* **[<font color="#dd354b">thorough</font>](/keywords/#thorough)**: You are working in a more formal environment, e.g. developing very large or critical systems with hard quality requirements. Your stakeholders require thoroughness, accuracy and attention to detail. Maybe your systems and their documentation have to be audited.
>* **[<font color="#dd354b">essential</font>](/keywords/#essential)**: Despite lean and agile, there are some informations about your system that you should always document; i.e. quality goals of your architecture.

## <font color="#dd354b">Still have questions?</font>

<a href="https://faq.arc42.org"><img src="/images/faq-icon.png" alt="??" style="float:left;width:42px;height:42px;"></a>
<br>... then try our [**extensive FAQ**](https://faq.arc42.org), answering more than 120 frequently asked questions.

## <font color="#dd354b">Need further assistance?</font>

<a href="/contact"><img src="/images/contact-icon.png" alt="!!" style="float:left;width:42px;height:42px;"></a>
<br>... let us [**know here**](/contact/), we're listening.

## <font color="#dd354b">We're offering architecture training!</font>

The _dynamic duo_, always two trainers in parallel, practically applicable
knowledge from Peter Hruschka and Gernot Starke. See [arc42.de](https://arc42.de/termine) for details, and schedule.

We've successfully trained more than 1000 developers in software architecture,
many of them passed the [iSAQB CPSA-F](https://isaqb.org) certification.
(sorry - public training currently German-only, English for inhouse trainings.)


## <font color="#dd354b">This is open-source!</font>

This site is completely open-source, maintained on a [public Github repository](https://github.com/arc42/docs.arc42.org-site/).
