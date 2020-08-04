package org.molgenis.capice.vcf;

import static java.util.Collections.singletonList;
import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.doReturn;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.molgenis.capice.vcf.utils.GzippedVcfUtil.getVcfGzAsString;

import htsjdk.variant.variantcontext.VariantContext;
import htsjdk.variant.variantcontext.VariantContextBuilder;
import htsjdk.variant.variantcontext.writer.VariantContextWriter;
import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.stream.Collectors;
import java.util.zip.GZIPInputStream;
import org.apache.commons.csv.CSVRecord;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;
import org.mockito.ArgumentCaptor;

class TsvToVcfMapperImplTest {

  TsvToVcfMapperImpl tsvToVcfMapper;

  @TempDir static Path sharedTempDir;

  @BeforeEach
  void setUpBeforeEach() {
    tsvToVcfMapper = new TsvToVcfMapperImpl();
  }

  @Test
  void map() throws IOException {
    Path inputPath = Paths.get("src", "test", "resources", "sorted.tsv");
    Path outputVcfPath = sharedTempDir.resolve("output.vcf.gz");

    Settings settings = new Settings(inputPath, outputVcfPath, true, "capice2vcf", "test", null);

    tsvToVcfMapper.map(inputPath, outputVcfPath, settings);

    String actual = getVcfGzAsString(outputVcfPath);

    Path expectedPath = Paths.get("src", "test", "resources", "capice.vcf");
    String expected =
        Files.readString(expectedPath, StandardCharsets.UTF_8)
            .replaceAll("\\n|\\r\\n", System.getProperty("line.separator"));

    assertEquals(expected, actual);
  }



  @Test
  void mapLine() {
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
