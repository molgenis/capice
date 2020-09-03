package org.molgenis.capice.vcf;

import static java.lang.String.format;

public class PositionParseException extends RuntimeException {
  private static final String MESSAGE =
      "Position '%s' could not be parsed, expection a position in the format 'CHROM_POS_REF_ALT' e.g. 'X_123456789_C_G'";
  private final String position;

  public PositionParseException(String position) {
    this.position = position;
  }

  @Override
  public String getMessage() {
    return format(MESSAGE, position);
  }
}
