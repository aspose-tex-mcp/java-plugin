---
title: TeXJob
second_title: Aspose.TeX for Java API Reference
description: Implements features of a TeX job.
type: docs
weight: 39
url: /java/com.aspose.tex/texjob/
---
**Inheritance:**
java.lang.Object
```
public class TeXJob
```

Implements features of a TeX job.
## Constructors

| Constructor | Description |
| --- | --- |
| [TeXJob(InputStream stream, Device device, TeXOptions options)](#TeXJob-java.io.InputStream-com.aspose.tex.rendering.Device-com.aspose.tex.TeXOptions-) | Creates a TeX job for running the engine in production mode to typeset a TeX file. |
| [TeXJob(String path, Device device, TeXOptions options)](#TeXJob-java.lang.String-com.aspose.tex.rendering.Device-com.aspose.tex.TeXOptions-) | Creates a TeX job for running the engine in production mode to typeset a TeX file. |
| [TeXJob(Device device, TeXOptions options)](#TeXJob-com.aspose.tex.rendering.Device-com.aspose.tex.TeXOptions-) | Creates a TeX job for running the engine in production mode to typeset a TeX file. |
## Methods

| Method | Description |
| --- | --- |
| [run()](#run--) | Runs TeX job. |
| [createFormat(String path, TeXOptions options)](#createFormat-java.lang.String-com.aspose.tex.TeXOptions-) | Runs TeX engine in INITEX mode to create a format file (.fmt). |
### TeXJob(InputStream stream, Device device, TeXOptions options) {#TeXJob-java.io.InputStream-com.aspose.tex.rendering.Device-com.aspose.tex.TeXOptions-}
```
public TeXJob(InputStream stream, Device device, TeXOptions options)
```


Creates a TeX job for running the engine in production mode to typeset a TeX file.

**Parameters:**
| Parameter | Type | Description |
| --- | --- | --- |
| stream | java.io.InputStream | The stream containing the TeX file. |
| device | [Device](../../com.aspose.tex.rendering/device) | The device defining output representation. |
| options | [TeXOptions](../../com.aspose.tex/texoptions) | TeX engine run options. |

### TeXJob(String path, Device device, TeXOptions options) {#TeXJob-java.lang.String-com.aspose.tex.rendering.Device-com.aspose.tex.TeXOptions-}
```
public TeXJob(String path, Device device, TeXOptions options)
```


Creates a TeX job for running the engine in production mode to typeset a TeX file.

**Parameters:**
| Parameter | Type | Description |
| --- | --- | --- |
| path | java.lang.String | The path to the TeX file. |
| device | [Device](../../com.aspose.tex.rendering/device) | The device defining output representation. |
| options | [TeXOptions](../../com.aspose.tex/texoptions) | TeX engine run options. |

### TeXJob(Device device, TeXOptions options) {#TeXJob-com.aspose.tex.rendering.Device-com.aspose.tex.TeXOptions-}
```
public TeXJob(Device device, TeXOptions options)
```


Creates a TeX job for running the engine in production mode to typeset a TeX file. The engine will prompt the file name as soon as it starts. Thus this run is supposed to be interactive.

**Parameters:**
| Parameter | Type | Description |
| --- | --- | --- |
| device | [Device](../../com.aspose.tex.rendering/device) | The device defining output representation. |
| options | [TeXOptions](../../com.aspose.tex/texoptions) | TeX engine run options. |

### run() {#run--}
```
public TeXJobResult run()
```


Runs TeX job.

**Returns:**
[TeXJobResult](../../com.aspose.tex/texjobresult) - The result of the job execution.
### createFormat(String path, TeXOptions options) {#createFormat-java.lang.String-com.aspose.tex.TeXOptions-}
```
public static void createFormat(String path, TeXOptions options)
```


Runs TeX engine in INITEX mode to create a format file (.fmt).

**Parameters:**
| Parameter | Type | Description |
| --- | --- | --- |
| path | java.lang.String | The path to the main format source file. |
| options | [TeXOptions](../../com.aspose.tex/texoptions) | TeX engine run options. |

