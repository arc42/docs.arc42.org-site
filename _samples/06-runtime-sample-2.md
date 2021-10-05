---
layout: post
title: "Runtine View Example: MaMa CRM"
tags: runtime sample 
category: runtime
permalink: /samples/runtime-2/
---

## 6. (Sample) Runtime View 

<div class="arc42-help" markdown="1">
The runtime view describes concrete behavior and interactions of the system’s building blocks in form of scenarios.
</div>

### 6.1 Import File

One of the major use cases is _Import File_, which can be from both mandator and partner. 
Such files contain always contain `Client` related data in configurable formats (CSV, fix-formats or XML).

We split the explanation of _import file_ into two phases:

1. Import Raw File Generic (from an external source)
2. Validate the imported data and update the internal `Client` database

#### 6.1.1 Import Raw Generic

At first we explain the _generic_ import, where no campaign-specific activities are executed. 
This concerns `configureReceiveChannel` and especially the `instantiateFilterChain()` activities.

![(First part of data import:) Import Raw File](images/mama/9-getRawFile.png)

1. tryImport: `ProcessControl` starts the import. The `activity` is a uniqe ID identifying the mandator, the campaign and the activity.
2. `importConfiguration` gets all required configuration information 
3. `configureReceiveChannel` prepares everything needed to get data from an external source. 
For example, URL, filenames and authentication credentials for an external ftp server need to be configured here.
4. `archive` sends the file to the (configured) archive system, usually an optical write-once non-erasable backup archive.
5. `setup` initializes the required filters, e.g. unzip or decrypt.
6. `filter` executes all the filters

The steps 5+6 are a dynamically configured pipes-and-filter dataflow subsystem. You find some more info in
the filter concept in section 8.


#### 6.1.2 Validate File

**Prerequisite:** Data has been imported from external source, has been successfully filtered (i.e. decrypted and decompressed). 
See previous section (_Import Raw Generic_).

The diagram below contains error handling. 
In _good cases_ there will be no errors.
Calls to `ImportErrorHandler` are only executed if errors occur!

![(Second part of data import:) Validate imported data](images/mama/9-validateRawData.png)

