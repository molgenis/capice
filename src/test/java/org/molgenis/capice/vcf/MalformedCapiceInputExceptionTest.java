package org.molgenis.capice.vcf;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

class MalformedCapiceInputExceptionTest {
  @Test
  void getMessage() {
    assertEquals(
        "Invalid CAPICE input on line 1024, expecting a position in column 0 and a score in column 4",
        new MalformedCapiceInputException(1024).getMessage());
  }
}