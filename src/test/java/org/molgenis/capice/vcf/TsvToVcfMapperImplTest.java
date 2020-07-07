package org.molgenis.capice.vcf;

import static java.util.Collections.singletonList;
import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.doReturn;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;

import htsjdk.variant.variantcontext.VariantContext;
import htsjdk.variant.variantcontext.VariantContextBuilder;
import htsjdk.variant.variantcontext.writer.VariantContextWriter;
import org.apache.commons.csv.CSVRecord;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;

class TsvToVcfMapperImplTest {

  @Test
  void mapLine() {
    TsvToVcfMapperImpl tsvToVcfMapper = new TsvToVcfMapperImpl();

    VariantContextWriter variantContextWriter = mock(VariantContextWriter.class);
    CSVRecord record = mock(CSVRecord.class);
    doReturn("MT_12345_ATG_A").when(record).get(0);
    doReturn("0.123456").when(record).get(4);

    tsvToVcfMapper.mapLine(variantContextWriter, record);

    VariantContextBuilder expectedBuilder = new VariantContextBuilder();
    expectedBuilder.chr("MT");
    expectedBuilder.start(12345);
    expectedBuilder.stop(12347);
    expectedBuilder.alleles("ATG", "A");
    expectedBuilder.attribute("CAP", singletonList(0.123456f));
    VariantContext expected = expectedBuilder.make();

    ArgumentCaptor<VariantContext> captor = ArgumentCaptor.forClass(VariantContext.class);
    verify(variantContextWriter).add(captor.capture());
    VariantContext actual = captor.getValue();
    assertAll(
        () -> {
          assertEquals(expected.getContig(), actual.getContig());
          assertEquals(expected.getStart(), actual.getStart());
          assertEquals(expected.getEnd(), actual.getEnd());
          assertEquals(expected.getReference(), actual.getReference());
          assertEquals(expected.getAlternateAllele(0), actual.getAlternateAllele(0));
        });
  }
}
