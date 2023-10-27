---
layout: post
title: "Example Concept: HTML Sanity Checker (Domain + URIs)"
tags: concept example 
category: concepts
permalink: /examples/concept-htmlsc-1/
---

Showing two crosscutting concepts useful for HTML Sanity Checking.

## 8. Crosscutting Concepts

### 8.1 Domain Terminology 


![HTML Checking Domain Model]({{ site.imageurl }}/examples/htmlsc/8-1-checking-domain.png)

Properties of the implementation classes are private, as we manipulate these via getter/setter methods.


| Term          | Description |
|:-------|:--------|
|Anchor         | Html element to create ->Links. Contains link-target in the form `<a href="link-target">`|
|-------|--------|
|Cross Reference|Link from one part of the document to another part within the same document. Special form of ->Internal Link, with a ->Link Target in the same document.|
|-------|--------|
|External Link  |Link to another page or resource at another domain. |
|-------|--------|
|Finding        |Description of a problem found by one ->Checker within the ->Html Page.|
|-------|--------|
|Html Element   |HTML pages (documents) are made up by HTML elements .e.g., `<a href="link target">`, `<img src="image.png">` and others. See the definition from the <a target="_blank" rel="noopener noreferrer nofollow" href="https://www.w3schools.com/html/html_elements.asp">W3-Consortium</a>|
|-------|--------|
|Html Page      |A single chunk of HTML, mostly regarded as a single file. Shall comply to standard HTML syntax. Minimal requirement: Our HTML parser can successfully parse this page. Contains ->Html Elements. Synonym: _Html Document_.|
|-------|--------|
|id             |Identifier for a specific part of a document, e.g. `<h2 id="#someHeader">`.Often used to describe ->Link Targets.|
|-------|--------|
|Internal Link  |Link to another section of the same page or to another page of the same domain. Also called ->Cross Reference or _Local Link_.|
|-------|--------|
|Link           |Any a reference in the ->Html Page that lets you display or activate another part of this document (->Internal Link) or another document, image or  resource (can be either ->Internal (local) or ->External Link). Every link leads from the _Link Source_ to the _Link Target_.           |
|-------|--------|
|Link Target    |Target of any ->Link, e.g. heading or any other a part of ->Html Documents, any internal or external resource (identified by URI). Expressed by ->id.|  
|-------|--------|
|Local Resource    | Local file, either other Html files or other types (e.g. pdf, docx) |
|-------|--------|
|Run Result        | The overall results of checking a number of pages (at least one page).|
|-------|--------|
|Single Page Result| A collection of all checks of a single ->Html Page.|
|-------|--------|
|URI               | Universal Resource Identifier. Defined in <a target="_blank" rel="noopener noreferrer nofollow" href="https://www.ietf.org/rfc/rfc2396.txt">RFC-2396</a>, the ultimate source of truth concerning link syntax and semantic. |
|-------|--------|


### 8.2 Structure of HTML Links

**Remark:** For many web developers or HTML experts the following information
on URI syntax might be completely evident. As we wrote this book also for
different kind of people, we included this information anyhow.

HtmlSC performs various checks on HTML links (hyperlinks), which usually
follow the URI syntax specified by <a target="_blank" rel="noopener noreferrer nofollow" href="https://www.ietf.org/rfc/rfc2396.txt">RFC-2396</a>. URIs are generally used to link to arbitrary resources (documents, files or parts within documents).

Their general structure is depicted in the following figure - you also find
a unit test below.


![Figure: Generic URI structure]({{ site.imageurl}}/examples/htmlsc/8-uri-generic-example.png)

~~~~
@Test
public void testGenericURISyntax() {
    // based upon an example from the Oracle(tm) Java tutorial:
    // https://docs.oracle.com/javase/tutorial/networking/urls/urlInfo.html
    def aURL = new URL(
        "https://example.com:42/docs/tutorial/index.html?name=aim42#INTRO");
    aURL.with {
        assert getProtocol() == "http"
        assert getAuthority() == "example.com:42"
        assert getHost() == "example.com"
        assert getPort() == 42
        assert getPath() == "/docs/tutorial/index.html"
        assert getQuery() == "name=aim42"
        assert getRef() == "INTRO"
    }
}
~~~~
**Test showing generic URI syntax"**
