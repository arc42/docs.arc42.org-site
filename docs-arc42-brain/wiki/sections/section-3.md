---
id: section-3
type: section
title: 3 - Context and scope
status: draft
created: '2026-09-17'
updated: '2026-09-17'
sources:
- '[[SRC-003-section-3-page]]'
related: []
number: 3
name: Context and Scope
category: context
posts-dir: 03-context
permalink: /section-3/
order: 7
faq-topic: context, scope and external interfaces
---

# 3. Context and Scope

> [!arc42-help]
>
> ## Content
> System scope and context - as the name suggests - delimits your system (i.e. your scope) from all its communication partners (neighboring systems and users, i.e. the context of your system). It thereby specifies the external interfaces.
>
> If necessary, differentiate the business context (domain specific inputs and outputs) from the technical context (channels, protocols, hardware).
>
> ## Motivation
> The domain interfaces and technical interfaces to communication partners are among
> your system's most critical aspects. Make sure that you completely understand them.
>
> ## Form
> * Various context diagrams
> * Lists of communication partners and their interfaces.
>
> ## Examples
>
> See below, separated into business- and technical context.
>
  
## 3.1 Business context

> [!arc42-help]
>
> ### Content
> Specification of *all* communication partners (users, IT-systems, ...) with explanations of domain specific inputs and outputs or interfaces. 
> Optionally you can add domain specific formats or communication protocols.
>
> ### Motivation
> All stakeholders should understand which data are exchanged with the environment of the system.
>
> ### Form
> All kinds of diagrams that show the system as a black box and specify the domain interfaces to communiations partners.
>
> Alternatively (or additionally) you can use a table. The title of the table is the name of your system, the three columns contain the name of the communication partner, the inputs, and the outputs.
> <br>
>
> <!-- collect all examples that are related to this section of arc42 -->
> %% examples: business-context %%
>

<!-- the same section, inside complete documentation of real systems -->
%% examples-link %%

### _&lt;insert diagram or table>_

### _&lt;(optionally:) insert explanation of external domain interfaces>_


## 3.2 Technical context

> [!arc42-help]
>
> ### Contents
> Technical interfaces (channels and transmission media) linking your system to its environment. 
> In addition a mapping of domain specific input/output to the channels, i.e. an explanation with I/O uses which channel.
>
> ### Motivation
> Many stakeholders make architectural decision based on the technical interfaces between the system and its context. Especially infrastructure or hardware designers decide these technical interfaces.
>
> ### Form
> E.g. UML deployment diagram describing channels to neighboring systems, together with a mapping table showing the relationships between channels and input/output.
>
> <!-- collect all examples that are related to this section of arc42 -->
> %% examples: technical-context %%
>
>



### _&lt;insert diagram or table>_

### _&lt;(optionally:) insert explanation of technical interfaces>_

### _&lt;insert mapping of input/output to channels>_
