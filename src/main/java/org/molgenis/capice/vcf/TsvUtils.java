package org.molgenis.capice.vcf;

import org.apache.commons.csv.CSVFormat;

public class TsvUtils {
  public static final CSVFormat TSV_FORMAT =
      CSVFormat.DEFAULT.withDelimiter('\t').withRecordSeparator('\n');

  private TsvUtils() {}
}
