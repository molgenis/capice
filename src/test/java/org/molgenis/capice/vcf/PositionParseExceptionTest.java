package org.molgenis.capice.vcf;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

class PositionParseExceptionTest {
  @Test
  void getMessage() {
    assertEquals(
        "Position 'Hanzeplein1' could not be parsed, expection a position in the format 'CHROM_POS_REF_ALT' e.g. 'X_123456789_C_G'",
        new PositionParseException("Hanzeplein1").getMessage());
  }
}