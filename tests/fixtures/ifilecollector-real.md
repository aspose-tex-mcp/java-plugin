---
title: IFileCollector
second_title: Aspose.TeX for Java API Reference
description: Defines methods for selecting collections of files.
type: docs
weight: 42
url: /java/com.aspose.tex/ifilecollector/
---```
public interface IFileCollector
```

Defines methods for selecting collections of files.
## Methods

| Method | Description |
| --- | --- |
| [getFileNamesByExtension(String extension)](#getFileNamesByExtension-java.lang.String-) | Returns the array of file names by an extension. |
| [getFileNamesByExtension(String extension, String path)](#getFileNamesByExtension-java.lang.String-java.lang.String-) | Returns the array of file names by an extension. |
### getFileNamesByExtension(String extension) {#getFileNamesByExtension-java.lang.String-}
```
public abstract String[] getFileNamesByExtension(String extension)
```


Returns the array of file names by an extension.

**Parameters:**
| Parameter | Type | Description |
| --- | --- | --- |
| extension | java.lang.String | The file extension. |

**Returns:**
java.lang.String[] - The array of file names.
### getFileNamesByExtension(String extension, String path) {#getFileNamesByExtension-java.lang.String-java.lang.String-}
```
public abstract String[] getFileNamesByExtension(String extension, String path)
```


Returns the array of file names by an extension.

**Parameters:**
| Parameter | Type | Description |
| --- | --- | --- |
| extension | java.lang.String | The file extension. |
| path | java.lang.String | The path inside the directory. |

**Returns:**
java.lang.String[] - The array of file names.
