package org.molgenis.capice.vcf;

import static java.lang.String.format;
import static org.molgenis.capice.vcf.TsvToVcfMapperImpl.POSITION_INDEX;
import static org.molgenis.capice.vcf.TsvToVcfMapperImpl.SCORE_INDEX;

public class MalformedCapiceInputException extends RuntimeException {
  private static final String MESSAGE =
      "Invalid CAPICE input on line %d, expecting a position in column %d and a score in column %d";
  private final long line;

  public MalformedCapiceInputException( long line) {
    this.line = line;
  }

  @Override
  public String getMessage() {
    return format(MESSAGE, line, POSITION_INDEX, SCORE_INDEX);
  }
}
