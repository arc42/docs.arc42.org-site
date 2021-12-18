---
layout: post
title: "Example Risk: HTML Sanity Checker"
tags: risks example 
category: risks
permalink: /examples/risk-htmlsc-1/
---

## 11. Risks and Technical Debts


**Remark:** In our small example we don't see any _real_ risks for architecture and implementation.
Therefore the risks shown below are a bit artificial...

### 11.1 Technical risks

|Risk                            |Description                                |
|--------------------------------|-------------------------------------------|
|Bottleneck with access rights on public repositories |Currently only one single developer has access rights to deploy new versions of HtmlSC on public servers like Bintray or Gradle plugin portal.  |
| System relies on `gradle` - which may not be available on target computers| Although the Java Runtime is installed on many computers, it might not be available for every potential HtmlSC user. |  
|--------------------------------|-------------------------------------------|


### 11.2 Business or domain risks

|Risk                            |Description                                |
|--------------------------------|-------------------------------------------|
|System might become obsolete    |In case AsciiDoc or Markdown processors implement HTML checking natively, HtmlSC might become obsolete.                             |
|--------------------------------|--------------------------------------------|

