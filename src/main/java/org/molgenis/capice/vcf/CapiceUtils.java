package org.molgenis.capice.vcf;

import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.apache.commons.csv.CSVRecord;

public class CapiceUtils {
  private static final Pattern POS_PATTERN = Pattern.compile("(.+?)_(.+?)_(.+?)_(.+?)");

  private CapiceUtils(){}

  public static VcfPosition getVcfPosition(CSVRecord thatRecord) {
    String positionString = thatRecord.get(0) != null ? thatRecord.get(0) : "";
    Matcher thatMatcher = POS_PATTERN.matcher(positionString);
    if (!thatMatcher.matches()) {
      throw new PositionParseException(positionString);
    }
    String chrom = thatMatcher.group(1);
    int pos = Integer.parseInt(thatMatcher.group(2));
    String ref = thatMatcher.group(3);
    String alt = thatMatcher.group(4);
    return new VcfPosition(chrom, pos, ref, alt);
  }
}
