package org.molgenis.capice.vcf.utils;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.util.stream.Collectors;
import java.util.zip.GZIPInputStream;

public class GzippedVcfUtil {

  private GzippedVcfUtil(){

  }

  public static String getVcfGzAsString(Path outputVcfPath) throws IOException {
    String actual;
    try (InputStream fileStream = new FileInputStream(outputVcfPath.toFile());
        InputStream gzipStream = new GZIPInputStream(fileStream);
        Reader decoder = new InputStreamReader(gzipStream, StandardCharsets.UTF_8);
        BufferedReader buffered = new BufferedReader(decoder))
    {
      actual = buffered.lines().collect(Collectors.joining(System.getProperty("line.separator")));
    }
    return actual;
  }
}
