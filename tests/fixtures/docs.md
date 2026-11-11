---
title: TeX guide
url: /tex/java/guide/
---
# Guide
{{< highlight csharp >}}
TeXOptions options = TeXOptions.consoleAppOptions(TeXConfig.objectLaTeX());
new TeXJob("hello.tex", new PdfDevice(), options).run();
{{< /highlight >}}
